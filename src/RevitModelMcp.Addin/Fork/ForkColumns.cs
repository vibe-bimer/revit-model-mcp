using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Creates one structural column at a point on a named level. The instance is placed through the
/// level-based overload with <see cref="StructuralType.Column"/>, and the top is either the named
/// <c>top_level</c> or a height above the base. Both levels and both offsets are written here,
/// because they are ElementId-valued parameters the generic set-parameter tool refuses on purpose.
/// No attachment is attempted: an attachment target must be a slab, roof, ceiling, beam or brace,
/// so "attach to the top level" has no API meaning. Runs inside the caller's transaction, so a dry
/// run is rolled back by the executor.
/// </summary>
internal static class ForkColumns
{
    /// <summary>Checks the column inputs before anything is created.</summary>
    internal static void Validate(ActionJobContract action)
    {
        ForkLookup.Require(!string.IsNullOrWhiteSpace(action.Family), "family is required.");
        ForkLookup.Require(!string.IsNullOrWhiteSpace(action.Level), "level is required.");
        ForkLookup.Require(Finite(action.XMm) && Finite(action.YMm),
            "xMm and yMm must be finite numbers.");
        var hasTop = !string.IsNullOrWhiteSpace(action.Options.TopLevel);
        var height = action.Options.HeightMm;
        ForkLookup.Require(hasTop || height is not null,
            "Either topLevel or heightMm is required.");
        ForkLookup.Require(height is null || Finite(height.Value) && height.Value > 0,
            "heightMm must be a positive number.");
        ForkLookup.Require(action.Options.BaseOffsetMm is null || Finite(action.Options.BaseOffsetMm.Value),
            "baseOffsetMm must be a finite number.");
        ForkLookup.Require(action.Options.TopOffsetMm is null || Finite(action.Options.TopOffsetMm.Value),
            "topOffsetMm must be a finite number.");
        ForkLookup.Require(Finite(action.RotationDeg), "rotationDeg must be a finite number.");
    }

    /// <summary>Creates the column and reports its id, category and level.</summary>
    internal static ActionResultData Apply(Document document, ActionJobContract action)
    {
        Validate(action);
        var symbol = ColumnSymbol(document, action.Family!, action.TypeName);
        var level = ForkLookup.Level(document, action.Level!);
        var topLevel = action.Options.TopLevel is { } topName
            ? ForkLookup.Level(document, topName)
            : null;

        if (!symbol.IsActive)
        {
            symbol.Activate();
            document.Regenerate();
        }

        var point = new XYZ(
            ForkLookup.Millimeters(action.XMm),
            ForkLookup.Millimeters(action.YMm),
            level.ProjectElevation);
        var instance = document.Create.NewFamilyInstance(point, symbol, level, StructuralType.Column);
        if (action.RotationDeg != 0 && instance.Location is LocationPoint location)
        {
            // LocationPoint.Rotate takes the rotation axis as a line, not as a vector.
            var axis = Line.CreateBound(point, point + XYZ.BasisZ);
            location.Rotate(axis, Math.PI * action.RotationDeg / 180.0);
        }

        // The base level the placement overload recorded is the caller's level; the offsets and the
        // top are written here, because they are ElementId-valued parameters that the generic
        // set-parameter tool refuses on purpose.
        SetLevelParameter(instance, BuiltInParameter.FAMILY_BASE_LEVEL_PARAM, level.Id);
        SetOffsetParameter(instance, BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM, action.Options.BaseOffsetMm);
        if (topLevel is not null)
        {
            SetLevelParameter(instance, BuiltInParameter.FAMILY_TOP_LEVEL_PARAM, topLevel.Id);
            var topElevation = topLevel.ProjectElevation
                               + ForkLookup.Millimeters(action.Options.TopOffsetMm ?? 0);
            var height = topElevation - (level.ProjectElevation + ForkLookup.Millimeters(action.Options.BaseOffsetMm ?? 0));
            ForkLookup.Require(height > 0,
                $"Column '{action.Family}' would be {ForkLookup.Number(ForkLookup.MillimetersFromInternal(height))} mm tall; the top must sit above the base.");
            SetOffsetParameter(instance, BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM, action.Options.TopOffsetMm);
        }
        else
        {
            SetColumnHeight(instance, level, action.Options.HeightMm!.Value, action.Options.BaseOffsetMm ?? 0);
        }

        document.Regenerate();
        return new ActionResultData
        {
            Id = RevitValueReader.GetId(instance.Id),
            Category = instance.Category?.Name,
            Level = level.Name
        };
    }

    /// <summary>Reads the created column as an element fact block.</summary>
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
        var box = element.get_BoundingBox(null);
        if (box is not null)
        {
            facts.BoundingBoxMinMm = ForkBounds.Minimum(box);
            facts.BoundingBoxMaxMm = ForkBounds.Maximum(box);
        }

        return facts;
    }

    private static FamilySymbol ColumnSymbol(Document document, string family, string? typeName)
    {
        using var symbols = document.CollectElements().OfClass<FamilySymbol>()
            .WhereParameter(BuiltInParameter.ALL_MODEL_FAMILY_NAME).Equals(family);
        if (typeName is not null)
            symbols.WhereParameter(BuiltInParameter.SYMBOL_NAME_PARAM).Equals(typeName);
        var symbol = symbols.FirstOrDefault() as FamilySymbol;
        if (symbol is not null) return symbol;

        // The caller deserves the names that exist, not just "not found".
        using var loaded = document.CollectElements().OfClass<FamilySymbol>()
            .WhereParameter(BuiltInParameter.ALL_MODEL_FAMILY_NAME).Equals(family);
        var available = loaded.Cast<FamilySymbol>()
            .Select(candidate => candidate.Name)
            .OrderBy(name => name, StringComparer.OrdinalIgnoreCase)
            .ToList();
        if (available.Count == 0)
            throw new ArgumentException($"Family '{family}' was not found. Use revit_load_family_file to load it first.");
        var list = available.Count == 0 ? "none" : string.Join(", ", available);
        throw new ArgumentException($"Type '{typeName}' was not found in family '{family}'. Available types: {list}.");
    }

    /// <summary>Without a top level the top is set by moving the column's own height above the base:
    /// the family's column-length parameter does not exist on every family, but the level-driven top
    /// offset does, so the top elevation is written through the top-level and top-offset pair.</summary>
    private static void SetColumnHeight(FamilyInstance instance, Level level, double heightMm, double baseOffsetMm)
    {
        // The top stays on the base level and rides its offset; that is what the UI does for a
        // column whose top is not bound to another level.
        SetLevelParameter(instance, BuiltInParameter.FAMILY_TOP_LEVEL_PARAM, level.Id);
        var topOffset = baseOffsetMm + heightMm;
        var parameter = instance.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM);
        if (parameter is null || parameter.IsReadOnly || !parameter.Set(ForkLookup.Millimeters(topOffset)))
            throw new InvalidOperationException(
                $"Column '{instance.Name}' exposes no writable top offset; give topLevel instead of heightMm.");
    }

    private static void SetLevelParameter(FamilyInstance instance, BuiltInParameter id, ElementId value)
    {
        var parameter = instance.get_Parameter(id);
        if (parameter is null || parameter.IsReadOnly || !parameter.Set(value))
            throw new InvalidOperationException($"The column's level parameter {id} could not be set.");
    }

    private static void SetOffsetParameter(FamilyInstance instance, BuiltInParameter id, double? offsetMm)
    {
        if (offsetMm is null) return;
        var parameter = instance.get_Parameter(id);
        if (parameter is null || parameter.IsReadOnly || !parameter.Set(ForkLookup.Millimeters(offsetMm.Value)))
            throw new InvalidOperationException($"The column's offset parameter {id} could not be set.");
    }

    private static bool Finite(double value) => !double.IsNaN(value) && !double.IsInfinity(value);
}
