using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Creates a level at a given elevation, optionally with its floor plan. A level whose name already exists is
/// refused, because every later lookup in this codebase resolves a level by its exact name. Runs inside the
/// caller's transaction, so a dry run is rolled back by the executor.
/// </summary>
internal static class ForkLevels
{
    /// <summary>Checks the level inputs before anything is created.</summary>
    internal static void Validate(ActionJobContract action)
    {
        ForkLookup.Require(!string.IsNullOrWhiteSpace(action.Name), "name is required.");
        ForkLookup.Require(action.Options.ElevationMm.HasValue, "elevationMm is required.");
        ForkLookup.Require(double.IsFinite(action.Options.ElevationMm!.Value), "elevationMm must be a finite number.");
    }

    /// <summary>Creates the level and reports its id, category and the readings of the new level.</summary>
    internal static ActionResultData Apply(Document document, ActionJobContract action)
    {
        Validate(action);
        var name = action.Name!.Trim();
        var elevationMm = action.Options.ElevationMm!.Value;
        var existing = ForkLookup.LevelOrNull(document, name);
        if (existing is not null)
        {
            throw new ArgumentException(
                $"Level '{name}' already exists at {ForkLookup.Number(ForkLookup.MillimetersFromInternal(existing.Elevation))} mm.");
        }

        var level = Level.Create(document, ForkLookup.Millimeters(elevationMm));
        level.Name = name;
        if (action.Options.CreateView == true)
        {
            using var viewTypes = document.CollectElements().OfClass<ViewFamilyType>();
            // Resolve the plan type by view family: the stock templates' view type names are not stable.
            var planType = viewTypes.Cast<ViewFamilyType>()
                               .FirstOrDefault(type => type.ViewFamily == ViewFamily.FloorPlan)
                           ?? throw new ArgumentException(
                               "No floor plan view family type is available in this document.");
            ViewPlan.Create(document, planType.Id, level.Id);
        }

        return new ActionResultData { Id = RevitValueReader.GetId(level.Id), Category = level.Category?.Name };
    }

    /// <summary>Reads the addressed level, or reports nothing when the action creates it.</summary>
    internal static ForkFacts Read(Document document, ElementId id)
    {
        if (id.ToElement<Level>(document) is not { } level) return new ForkFacts();
        return new ForkFacts
        {
            Name = level.Name,
            ElevationMm = ForkLookup.MillimetersFromInternal(level.Elevation)
        };
    }
}
