using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Creates one structural beam along an axis on a named level. The instance goes through the
/// curve-and-level overload with <see cref="StructuralType.Beam"/>, because the work-plane overload
/// needs a face reference the caller cannot supply. The axis is taken exactly as given: Revit has no
/// programmatic snapping API, and <c>StructuralFramingUtils.SetEndReference</c> only acts on an end the
/// model already joined. The vertical offset is written through the elevation parameters that carry it —
/// the two beam end elevations first, then the instance elevation — and a write counts only when the
/// bounding box actually rises, because a family can accept a value and keep the geometry on its level.
/// The parameter that carried the offset is read back rather than assumed, so the response names the
/// column that actually holds it.
/// Runs inside the caller's transaction, so a dry run is rolled back by the executor.
/// </summary>
internal static class ForkBeams
{
    /// <summary>Parameters that can carry the vertical offset, in the order they are tried.</summary>
    private static readonly BuiltInParameter[] OffsetParameters =
    [
        BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION,
        BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION,
        BuiltInParameter.INSTANCE_ELEVATION_PARAM
    ];

    /// <summary>Parameter groups the offset is written through, in the order they are tried.</summary>
    private static readonly BuiltInParameter[][] OffsetCarriers =
    [
        [BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION, BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION],
        [BuiltInParameter.INSTANCE_ELEVATION_PARAM]
    ];

    /// <summary>Checks the beam inputs before anything is created.</summary>
    internal static void Validate(ActionJobContract action)
    {
        ForkLookup.Require(!string.IsNullOrWhiteSpace(action.Family), "family is required.");
        ForkLookup.Require(!string.IsNullOrWhiteSpace(action.Level), "level is required.");
        var start = action.Options.StartMm;
        var end = action.Options.EndMm;
        ForkLookup.Require(start is { Count: 2 }, "startMm must contain an x and a y in millimetres.");
        ForkLookup.Require(end is { Count: 2 }, "endMm must contain an x and a y in millimetres.");
        var from = start!;
        var to = end!;
        ForkLookup.Require(from.All(Finite) && to.All(Finite),
            "startMm and endMm must be finite numbers.");
        ForkLookup.Require(from[0] != to[0] || from[1] != to[1],
            "startMm and endMm must not be the same point.");
        ForkLookup.Require(action.Options.ZOffsetMm is null || Finite(action.Options.ZOffsetMm.Value),
            "zOffsetMm must be a finite number.");
    }

    /// <summary>Creates the beam and reports its id, category and level.</summary>
    internal static ActionResultData Apply(Document document, ActionJobContract action)
    {
        Validate(action);
        var symbol = BeamSymbol(document, action.Family!, action.TypeName);
        var level = ForkLookup.Level(document, action.Level!);

        if (!symbol.IsActive)
        {
            symbol.Activate();
            document.Regenerate();
        }

        var instance = document.Create.NewFamilyInstance(
            Axis(action.Options.StartMm!, action.Options.EndMm!, level), symbol, level, StructuralType.Beam);

        if (action.Options.StructuralUsage is { } usage)
            SetStructuralUsage(instance, usage);

        if (action.Options.ZOffsetMm is { } offsetMm && offsetMm != 0)
            ApplyOffset(document, instance, offsetMm);

        document.Regenerate();
        return new ActionResultData
        {
            Id = RevitValueReader.GetId(instance.Id),
            Category = instance.Category?.Name,
            Level = level.Name
        };
    }

    /// <summary>Reads the created beam as an element fact block.</summary>
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
        // A structural framing instance names its reference level through its own parameter; the
        // family base level is the fallback for the families that carry only that one.
        foreach (var candidate in new[] { BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM, BuiltInParameter.FAMILY_BASE_LEVEL_PARAM })
        {
            if (element.get_Parameter(candidate)?.AsElementId() is { } levelId
                && levelId.ToElement(document) is Level level)
            {
                facts.Level = level.Name;
                break;
            }
        }

        var box = element.get_BoundingBox(null);
        if (box is not null)
        {
            facts.BoundingBoxMinMm = ForkBounds.Minimum(box);
            facts.BoundingBoxMaxMm = ForkBounds.Maximum(box);
        }

        facts.Fork = ReadForkFacts(element);
        return facts;
    }

    /// <summary>Reads the offset and the structural usage back off the instance.</summary>
    private static ForkFacts ReadForkFacts(Element element)
    {
        var facts = new ForkFacts();
        if (element is FamilyInstance instance) facts.StructuralUsage = instance.StructuralUsage.ToString();
        foreach (var candidate in OffsetParameters)
        {
            if (element.get_Parameter(candidate) is not { StorageType: StorageType.Double } parameter) continue;
            var offsetMm = ForkLookup.MillimetersFromInternal(parameter.AsDouble());
            if (Math.Abs(offsetMm) < 0.05) continue;
            facts.ZOffsetMm = offsetMm;
            facts.ZOffsetParam = parameter.Definition?.Name;
            break;
        }

        return facts;
    }

    /// <summary>Lifts the instance off its reference level through the parameter group that carries the offset.</summary>
    private static void ApplyOffset(Document document, FamilyInstance instance, double offsetMm)
    {
        var target = ForkLookup.Millimeters(offsetMm);
        // The instance has no box until the model regenerates once after creation, and a missing box
        // would read as "no parameter lifted it"; measure the baseline after that first regenerate.
        document.Regenerate();
        var before = BoxBottom(instance);
        foreach (var carrier in OffsetCarriers)
        {
            var parameters = carrier.Select(instance.get_Parameter).ToList();
            if (parameters.Any(parameter => parameter is not { IsReadOnly: false, StorageType: StorageType.Double }))
                continue;
            var originals = parameters.Select(parameter => parameter!.AsDouble()).ToList();
            if (parameters.Any(parameter => !parameter!.Set(target)))
            {
                Restore(document, parameters!, originals);
                continue;
            }

            // A family can take the value and keep the geometry on its level: the read-back agrees while
            // the beam does not move, so the box decides which parameter actually carries the offset.
            document.Regenerate();
            if (Lifted(instance, before, target)) return;
            Restore(document, parameters!, originals);
        }

        // No parameter group lifts the geometry, so the instance moves instead and the read-back carries
        // no parameter name. A beam that refuses both keeps the caller's offset unmet, which is an error
        // rather than a silent create on the level.
        ElementTransformUtils.MoveElement(document, instance.Id, new XYZ(0, 0, target));
        document.Regenerate();
        if (!Lifted(instance, before, target))
            throw new InvalidOperationException(
                $"Family '{instance.Symbol?.Family?.Name}' cannot take a vertical offset of {ForkLookup.Number(offsetMm)} mm: no elevation parameter lifts it and the instance does not move off its level.");
    }

    /// <summary>Puts the written values back before the next carrier is tried.</summary>
    private static void Restore(Document document, IEnumerable<Parameter> parameters, IEnumerable<double> originals)
    {
        foreach (var (parameter, original) in parameters.Zip(originals))
            parameter.Set(original);
        document.Regenerate();
    }

    /// <summary>Whether the box rose by the offset, within rounding.</summary>
    private static bool Lifted(FamilyInstance instance, double? before, double target) =>
        before is { } start && BoxBottom(instance) is { } end && Math.Abs(end - start - target) <= Tolerance;

    /// <summary>Bottom of the instance, or null when the model gives no box.</summary>
    private static double? BoxBottom(FamilyInstance instance) => instance.get_BoundingBox(null)?.Min.Z;

    /// <summary>Box movement below this is rounding, not an offset.</summary>
    private const double Tolerance = 1e-6;

    private static void SetStructuralUsage(FamilyInstance instance, string usage)
    {
        if (!Enum.TryParse<StructuralInstanceUsage>(usage, ignoreCase: true, out var parsed))
            throw new ArgumentException(
                $"structuralUsage '{usage}' is not a structural usage. Use one of: {string.Join(", ", Enum.GetNames<StructuralInstanceUsage>())}.");
        instance.StructuralUsage = parsed;
    }

    private static FamilySymbol BeamSymbol(Document document, string family, string? typeName)
    {
        using var symbols = document.CollectElements().OfClass<FamilySymbol>()
            .WhereParameter(BuiltInParameter.ALL_MODEL_FAMILY_NAME).Equals(family);
        if (typeName is not null)
            symbols.WhereParameter(BuiltInParameter.SYMBOL_NAME_PARAM).Equals(typeName);
        var symbol = symbols.FirstOrDefault() as FamilySymbol;
        if (symbol is not null) return symbol;

        using var loaded = document.CollectElements().OfClass<FamilySymbol>()
            .WhereParameter(BuiltInParameter.ALL_MODEL_FAMILY_NAME).Equals(family);
        var available = loaded.Cast<FamilySymbol>()
            .Select(candidate => candidate.Name)
            .OrderBy(name => name, StringComparer.OrdinalIgnoreCase)
            .ToList();
        if (available.Count == 0)
            throw new ArgumentException($"Family '{family}' was not found. Use revit_load_family_file to load it first.");
        throw new ArgumentException($"Type '{typeName}' was not found in family '{family}'. Available types: {string.Join(", ", available)}.");
    }

    private static Line Axis(IReadOnlyList<double> start, IReadOnlyList<double> end, Level level) =>
        Line.CreateBound(
            new XYZ(ForkLookup.Millimeters(start[0]), ForkLookup.Millimeters(start[1]), level.ProjectElevation),
            new XYZ(ForkLookup.Millimeters(end[0]), ForkLookup.Millimeters(end[1]), level.ProjectElevation));

    private static bool Finite(double value) => !double.IsNaN(value) && !double.IsInfinity(value);
}
