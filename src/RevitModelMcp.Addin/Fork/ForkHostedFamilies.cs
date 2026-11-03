using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Places one door, window or other one-level hosted family on a wall. Revit does not check the host
/// it is handed: a symbol that wants a face or two levels, or a wall that cannot carry the family,
/// fails later or silently misplaces the instance. So the host and the symbol are both resolved and
/// checked here, before anything is created, and the resolution is reported back through
/// <c>fork.hostResolution</c> so a dry run also shows which wall the family would hang on.
/// The nearest-wall search only looks at walls of the placement's own storey, because a wall drawn
/// once per level is otherwise tied with its own neighbours above and below; the rules that decide
/// among those walls live in <see cref="HostSearch"/>, where they are tested without Revit.
/// Nothing is attached: "attach to host" means a slab, roof, ceiling, beam or brace target, which has
/// no bearing on a door or a window. Runs inside the caller's transaction, so a dry run is rolled
/// back by the executor.
/// </summary>
internal static class ForkHostedFamilies
{
    /// <summary>Checks the placement inputs that need no document.</summary>
    internal static void Validate(ActionJobContract action)
    {
        ForkLookup.Require(!string.IsNullOrWhiteSpace(action.Family), "family is required.");
        ForkLookup.Require(Finite(action.XMm) && Finite(action.YMm),
            "xMm and yMm must be finite numbers.");
        ForkLookup.Require(action.Options.HostSearchRadiusMm is null
                           || Finite(action.Options.HostSearchRadiusMm.Value)
                           && action.Options.HostSearchRadiusMm.Value > 0,
            "hostSearchRadiusMm must be a positive number.");
        ForkLookup.Require(action.Options.SillHeightMm is null || Finite(action.Options.SillHeightMm.Value),
            "sillHeightMm must be a finite number.");
        ForkLookup.Require(Finite(action.RotationDeg), "rotationDeg must be a finite number.");
        // A hosted instance takes its orientation from the host wall: rotating one in the API moves
        // it along the wall or does nothing, so a non-zero angle would be a silent no-op.
        ForkLookup.Require(action.RotationDeg == 0,
            "A one-level hosted family takes its orientation from its host wall, so rotationDeg must be 0; "
            + "use flipFacing to turn the family around and revit_place_family for a family that rotates freely.");
    }

    /// <summary>Checks everything a placement needs, including the host, without creating anything.</summary>
    internal static void Check(Document document, ActionJobContract action) =>
        Resolve(document, action);

    /// <summary>Places the family and reports its id, category and the wall it resolved to.</summary>
    internal static ActionResultData Apply(Document document, ActionJobContract action)
    {
        var placement = Resolve(document, action);
        var symbol = placement.Symbol;
        if (!symbol.IsActive)
        {
            symbol.Activate();
            document.Regenerate();
        }

        var point = new XYZ(
            ForkLookup.Millimeters(action.XMm),
            ForkLookup.Millimeters(action.YMm),
            placement.Level.ProjectElevation);
        var instance = document.Create.NewFamilyInstance(
            point, symbol, placement.Host, placement.Level, StructuralType.NonStructural);
        document.Regenerate();

        SetSillHeight(instance, action.Options.SillHeightMm);
        if (action.Options.FlipFacing == true) instance.flipFacing();
        document.Regenerate();

        return new ActionResultData
        {
            Id = RevitValueReader.GetId(instance.Id),
            Category = instance.Category?.Name,
            Level = placement.Level.Name,
            ForkOutcome = new ForkOutcome
            {
                HostResolution = new ForkHostResolution
                {
                    Mode = placement.Mode,
                    HostId = RevitValueReader.GetId(placement.Host.Id),
                    DistanceMm = placement.DistanceMm
                }
            }
        };
    }

    /// <summary>Reads the placed family as an element fact block.</summary>
    internal static ActionFacts Read(Document document, ElementId id)
    {
        if (id.ToElement(document) is not { } element) return new ActionFacts();
        var facts = new ActionFacts
        {
            Id = RevitValueReader.GetId(element.Id),
            Category = element.Category?.Name,
            Family = element.get_Parameter(BuiltInParameter.ALL_MODEL_FAMILY_NAME)?.AsString(),
            Type = element.Name
        };
        if (element.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_PARAM)?.AsElementId() is { } baseId
            && baseId.ToElement(document) is Level baseLevel)
            facts.Level = baseLevel.Name;
        else if (element is FamilyInstance instance
                 && instance.LevelId.ToElement(document) is Level hostedLevel)
            facts.Level = hostedLevel.Name;
        var box = element.get_BoundingBox(null);
        if (box is not null)
        {
            facts.BoundingBoxMinMm = ForkBounds.Minimum(box);
            facts.BoundingBoxMaxMm = ForkBounds.Maximum(box);
        }

        return facts;
    }

    /// <summary>The symbol, the wall and the level a placement will use; every failure happens here.</summary>
    private static Placement Resolve(Document document, ActionJobContract action)
    {
        Validate(action);
        var symbol = HostedSymbol(document, action.Family!, action.TypeName);
        var point = new XYZ(
            ForkLookup.Millimeters(action.XMm),
            ForkLookup.Millimeters(action.YMm),
            0);
        // The level comes first: a wall only hosts what sits in its own storey, so the level decides
        // which walls are candidates at all.
        var level = ResolveLevel(document, action.Level, point);
        var host = ResolveHost(document, action, point, level, out var mode, out var distanceMm);
        return new Placement(symbol, host, level, mode, distanceMm);
    }

    /// <summary>Resolves the wall, either the one the caller named or the nearest one in range.</summary>
    private static Wall ResolveHost(
        Document document,
        ActionJobContract action,
        XYZ point,
        Level level,
        out string mode,
        out double? distanceMm)
    {
        if (action.Options.HostElementId is { } hostId)
        {
            mode = "explicit";
            var host = WallById(document, hostId);
            distanceMm = WallDistance(host, point) is { } distance
                ? Math.Round(distance, 1)
                : null;
            return host;
        }

        mode = "nearest";
        var radiusMm = action.Options.HostSearchRadiusMm ?? HostSearch.DefaultRadiusMm;
        var wall = NearestWall(document, point, level, radiusMm, out distanceMm);
        return wall;
    }

    /// <summary>The wall the caller named, refused with the reason when it cannot host a family.</summary>
    private static Wall WallById(Document document, long hostId)
    {
        if (ForkLookup.CreateId(hostId).ToElement(document) is not { } element)
            throw new ArgumentException($"Host element {hostId} was not found.");
        if (element is not Wall wall)
            throw new ArgumentException(
                $"Host element {hostId} is a {element.Category?.Name ?? element.GetType().Name}, not a wall. "
                + "A hosted family needs a wall.");
        if (wall.WallType?.Kind == WallKind.Curtain)
            throw new ArgumentException(
                $"Host element {hostId} is a curtain wall; a door or window cannot hang on it.");
        return wall;
    }

    /// <summary>
    /// The wall of the placement's own storey whose location line runs closest to the point. Walls of
    /// other storeys are not candidates: a door on the first floor cannot hang on the wall above it, and
    /// a building whose walls are drawn once per storey would otherwise report every one of them as
    /// equally far. Which of those walls wins - range, tie, order - is <see cref="HostSearch"/>'s call.
    /// </summary>
    private static Wall NearestWall(
        Document document,
        XYZ point,
        Level level,
        double radiusMm,
        out double? distanceMm)
    {
        var levelMm = RevitValueReader.ToMillimeters(level.ProjectElevation);
        var wallsById = new Dictionary<long, Wall>();
        var candidates = new List<HostSearch.Candidate>();
        using var walls = document.CollectElements().OfClass<Wall>();
        foreach (var wall in walls.Cast<Wall>())
        {
            if (wall.WallType?.Kind == WallKind.Curtain) continue;
            if (WallSpan(document, wall) is not { } span) continue;
            if (!HostSearch.SpansStorey(span.BaseMm, span.TopMm, levelMm)) continue;
            if (WallDistance(wall, point) is not { } distanceFromLine) continue;
            var id = RevitValueReader.GetId(wall.Id);
            wallsById[id] = wall;
            candidates.Add(new HostSearch.Candidate(id, distanceFromLine));
        }

        distanceMm = null;
        if (candidates.Count == 0)
            throw new ArgumentException(
                $"The document has no wall on level '{level.Name}' to host the family.");

        var chosen = HostSearch.Nearest(candidates, radiusMm);
        distanceMm = Math.Round(chosen.DistanceMm, 1);
        return wallsById[chosen.Id];
    }

    /// <summary>
    /// Distance in millimetres from the point to the wall's location line, measured on the level plane
    /// and only when the foot of the perpendicular lands on the wall itself (the projection sits inside
    /// the curve). The projection uses the real curve, so a wall drawn as an arc is measured against the
    /// arc and not against the chords the curve is tessellated into.
    /// </summary>
    /// <remarks>
    /// The offsets stay in Revit's feet and unrounded: the right-angle test is a product of the offsets,
    /// and a display rounding on the way in would turn a true perpendicular beside a diagonal wall into
    /// a rejection. The millimetres this returns are unrounded for the same reason - the search compares
    /// them against its radius and its tie tolerance - so rounding happens only where the answer is
    /// shown, never where it is decided.
    /// </remarks>
    private static double? WallDistance(Wall wall, XYZ point)
    {
        if (wall.Location is not LocationCurve location || location.Curve is not { } curve) return null;
        if (!curve.IsBound) return null;
        if (curve.Project(point) is not { } projection) return null;
        if (!curve.IsInside(projection.Parameter)) return null;
        if (projection.XYZPoint is not { } foot) return null;

        var dx = point.X - foot.X;
        var dy = point.Y - foot.Y;

        var tangent = curve.ComputeDerivatives(projection.Parameter, false).BasisX;
        if (!HostSearch.MeetsAtRightAngles(tangent.X, tangent.Y, dx, dy)) return null;

        return FeetToMillimeters(Math.Sqrt((dx * dx) + (dy * dy)));
    }

    /// <summary>Revit's feet per millimetre, so the search works in unrounded millimetres.</summary>
    /// <remarks>
    /// <see cref="RevitValueReader.ToMillimeters"/> rounds to three decimals for display; the host
    /// search needs the full value. The factor mirrors <c>UnitConverter</c>'s private one, which the
    /// fork layer cannot reach.
    /// </remarks>
    private const double MillimetersPerFoot = 304.8;

    private static double FeetToMillimeters(double feet) => feet * MillimetersPerFoot;

    /// <summary>The named level, or the level whose elevation sits closest to the placement point.</summary>
    private static Level ResolveLevel(Document document, string? name, XYZ point)
    {
        if (!string.IsNullOrWhiteSpace(name)) return ForkLookup.Level(document, name);

        using var levels = document.CollectElements().OfClass<Level>();
        var all = levels.Cast<Level>().ToList();
        ForkLookup.Require(all.Count > 0, "The document has no level to place the family on.");

        return all
            .OrderBy(level => Math.Abs(level.ProjectElevation - point.Z))
            .ThenBy(level => level.ProjectElevation)
            .ThenBy(level => RevitValueReader.GetId(level.Id))
            .First();
    }

    /// <summary>
    /// The elevations in millimetres a wall spans. A height-constrained wall runs from its base level to
    /// the level it is drawn up to; an unconnected wall runs from its base level through its own height.
    /// </summary>
    private static (double BaseMm, double TopMm)? WallSpan(Document document, Wall wall)
    {
        var baseLevel = wall.get_Parameter(BuiltInParameter.WALL_BASE_CONSTRAINT)?.AsElementId() is { } baseId
            ? baseId.ToElement(document) as Level
            : null;
        if (baseLevel is null) return null;
        var baseMm = RevitValueReader.ToMillimeters(baseLevel.ProjectElevation);

        var topLevel = wall.get_Parameter(BuiltInParameter.WALL_HEIGHT_TYPE)?.AsElementId() is { } topId
            ? topId.ToElement(document) as Level
            : null;
        if (topLevel is not null) return (baseMm, RevitValueReader.ToMillimeters(topLevel.ProjectElevation));

        var height = wall.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM)?.AsDouble() ?? 0;
        return (baseMm, baseMm + RevitValueReader.ToMillimeters(height));
    }

    /// <summary>The family symbol, refused unless the family is a one-level hosted family.</summary>
    private static FamilySymbol HostedSymbol(Document document, string family, string? typeName)
    {
        using var symbols = document.CollectElements().OfClass<FamilySymbol>()
            .WhereParameter(BuiltInParameter.ALL_MODEL_FAMILY_NAME).Equals(family);
        if (typeName is not null)
            symbols.WhereParameter(BuiltInParameter.SYMBOL_NAME_PARAM).Equals(typeName);
        var symbol = symbols.FirstOrDefault() as FamilySymbol;
        if (symbol is null) throw UnresolvedSymbol(document, family, typeName);

        var placement = symbol.Family?.FamilyPlacementType;
        ForkLookup.Require(placement == FamilyPlacementType.OneLevelBasedHosted,
            $"Family '{family}' is {placement?.ToString() ?? "unknown"} based, not one-level hosted. "
            + "This tool places doors, windows and similar families that need a host wall; "
            + "use revit_place_family for a level-based family.");
        return symbol;
    }

    /// <summary>The "not found" refusal, with the type names the family does offer.</summary>
    private static ArgumentException UnresolvedSymbol(Document document, string family, string? typeName)
    {
        // The caller deserves the names that exist, not just "not found".
        using var loaded = document.CollectElements().OfClass<FamilySymbol>()
            .WhereParameter(BuiltInParameter.ALL_MODEL_FAMILY_NAME).Equals(family);
        var available = loaded.Cast<FamilySymbol>()
            .Select(candidate => candidate.Name)
            .OrderBy(name => name, StringComparer.OrdinalIgnoreCase)
            .ToList();
        if (available.Count == 0)
            return new ArgumentException(
                $"Family '{family}' was not found. Use revit_load_family_file to load it first.");
        return new ArgumentException(
            $"Type '{typeName}' was not found in family '{family}'. Available types: {string.Join(", ", available)}.");
    }

    /// <summary>The sill height, written through the family's own parameter and refused when it has none.</summary>
    private static void SetSillHeight(FamilyInstance instance, double? sillHeightMm)
    {
        if (sillHeightMm is null) return;
        var parameter = instance.get_Parameter(BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM);
        if (parameter is null || parameter.IsReadOnly || !parameter.Set(ForkLookup.Millimeters(sillHeightMm.Value)))
            throw new InvalidOperationException(
                $"The placed '{instance.Name}' exposes no writable sill height; drop sillHeightMm or use a window family.");
    }

    private static bool Finite(double value) => !double.IsNaN(value) && !double.IsInfinity(value);

    /// <summary>Everything a placement resolved before it touched the document.</summary>
    private sealed record Placement(
        FamilySymbol Symbol,
        Wall Host,
        Level Level,
        string Mode,
        double? DistanceMm);
}
