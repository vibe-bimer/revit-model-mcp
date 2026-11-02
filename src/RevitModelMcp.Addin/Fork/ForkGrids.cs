using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Creates one grid: a straight line from <c>start_mm</c> to <c>end_mm</c>, or a three-point arc when
/// <c>mid_mm</c> is supplied. The curve always lies on the horizontal plane at z=0, as
/// <c>Grid.Create</c> requires. A grid whose name already exists is refused, because later lookups
/// resolve a grid by its exact name. Runs inside the caller's transaction, so a dry run is rolled
/// back by the executor.
/// </summary>
internal static class ForkGrids
{
    /// <summary>Checks the grid inputs before anything is created.</summary>
    internal static void Validate(ActionJobContract action)
    {
        ForkLookup.Require(!string.IsNullOrWhiteSpace(action.Name), "name is required.");
        var start = action.Options.StartMm;
        var end = action.Options.EndMm;
        var mid = action.Options.MidMm;
        ForkLookup.Require(start is { Count: 2 }, "startMm must contain an x and a y in millimetres.");
        ForkLookup.Require(end is { Count: 2 }, "endMm must contain an x and a y in millimetres.");
        ForkLookup.Require(mid is null or { Count: 2 }, "midMm must contain an x and a y in millimetres.");
        ForkLookup.Require(start!.All(Finite) && end!.All(Finite) && (mid is null || mid.All(Finite)),
            "startMm, endMm and midMm must be finite numbers.");
        ForkLookup.Require(start![0] != end![0] || start[1] != end[1],
            "startMm and endMm must not be the same point.");
        if (mid is not null)
        {
            // A three-point arc degenerates when the mid point sits on the start-end line.
            ForkLookup.Require(
                mid[0] != start[0] || mid[1] != start[1],
                "midMm must not be the same point as startMm.");
            ForkLookup.Require(
                mid[0] != end[0] || mid[1] != end[1],
                "midMm must not be the same point as endMm.");
            var cross = (mid[0] - start[0]) * (end[1] - start[1]) - (mid[1] - start[1]) * (end[0] - start[0]);
            ForkLookup.Require(Math.Abs(cross) > 1e-9,
                "startMm, midMm and endMm must not be collinear: an arc needs a mid point off the start-end line.");
        }
    }

    /// <summary>Creates the grid and reports its id and category.</summary>
    internal static ActionResultData Apply(Document document, ActionJobContract action)
    {
        Validate(action);
        var name = action.Name!.Trim();
        var existing = GridOrNull(document, name);
        if (existing is not null)
        {
            throw new ArgumentException($"Grid '{name}' already exists.");
        }

        var start = Point(action.Options.StartMm!);
        var end = Point(action.Options.EndMm!);
        var grid = action.Options.MidMm is { } mid
            ? Grid.Create(document, Arc.Create(start, end, Point(mid)))
            : Grid.Create(document, Line.CreateBound(start, end));
        grid.Name = name;
        return new ActionResultData { Id = RevitValueReader.GetId(grid.Id), Category = grid.Category?.Name };
    }

    /// <summary>Reads the created grid as an element fact block.</summary>
    internal static ActionFacts Read(Document document, ElementId id)
    {
        if (id.ToElement(document) is not { } element) return new ActionFacts();
        var box = element.get_BoundingBox(null);
        var facts = new ActionFacts
        {
            Id = RevitValueReader.GetId(element.Id),
            Category = element.Category?.Name,
            // A grid is a datum: it has no geometry in the model, so its bounding box is null outside a
            // view and the label is the fact that identifies it.
            Fork = new Core.Fork.ForkFacts { Name = element.Name }
        };
        if (box is not null)
        {
            facts.BoundingBoxMinMm = ForkBounds.Minimum(box);
            facts.BoundingBoxMaxMm = ForkBounds.Maximum(box);
        }

        return facts;
    }

    private static bool Finite(double value) => !double.IsNaN(value) && !double.IsInfinity(value);

    private static XYZ Point(IReadOnlyList<double> point) => new(
        ForkLookup.Millimeters(point[0]),
        ForkLookup.Millimeters(point[1]),
        0);

    private static Grid? GridOrNull(Document document, string name)
    {
        using var grids = document.CollectElements().OfClass<Grid>()
            .WhereParameter(BuiltInParameter.DATUM_TEXT).Equals(name);
        return grids.FirstOrDefault() as Grid;
    }
}
