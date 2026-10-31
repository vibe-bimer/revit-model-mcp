using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Creates a floor from a closed boundary on a named level. The boundary is the caller's polygon in
/// millimetres at the level's elevation, closed automatically. Runs inside the caller's transaction, so a dry
/// run is rolled back by the executor.
/// </summary>
internal static class ForkFloors
{
    /// <summary>Checks the floor inputs before anything is created.</summary>
    internal static void Validate(ActionJobContract action)
    {
        ForkLookup.Require(!string.IsNullOrWhiteSpace(action.Level), "level is required.");
        var points = action.PointsMm;
        ForkLookup.Require(points is { Count: >= 3 }, "pointsMm must hold at least 3 vertices.");
        for (var index = 0; index < points!.Count; index++)
        {
            var point = points[index];
            ForkLookup.Require(point is { Count: >= 2 }, "Each pointsMm vertex needs an x and a y in millimetres.");
            var next = points[(index + 1) % points.Count];
            ForkLookup.Require(
                point[0] != next[0] || point[1] != next[1],
                "Floor boundary points must not repeat consecutively.");
        }
    }

    /// <summary>Creates the floor and reports its id, category and level.</summary>
    internal static ActionResultData Apply(Document document, ActionJobContract action)
    {
        Validate(action);
        var level = ForkLookup.Level(document, action.Level!);
        using var types = document.CollectElements().OfClass<FloorType>();
        if (action.Options.FloorType is not null)
        {
            types.WhereParameter(BuiltInParameter.SYMBOL_NAME_PARAM).Equals(action.Options.FloorType);
        }

        var floorType = types.Cast<FloorType>().FirstOrDefault()
                        ?? throw new ArgumentException(
                            $"Floor type '{action.Options.FloorType ?? "floor"}' was not found.");
        var elevation = level.ProjectElevation;
        var points = action.PointsMm!
            .Select(point => new XYZ(
                ForkLookup.Millimeters(point[0]),
                ForkLookup.Millimeters(point[1]),
                elevation))
            .ToList();
        IList<Curve> boundary = points
            .Select((point, index) => (Curve)Line.CreateBound(point, points[(index + 1) % points.Count]))
            .ToList();
        var loop = CurveLoop.Create(boundary);
        var floor = Floor.Create(document, [loop], floorType.Id, level.Id);
        return new ActionResultData
        {
            Id = RevitValueReader.GetId(floor.Id),
            Category = floor.Category?.Name,
            Level = level.Name
        };
    }

    /// <summary>Reads the created floor as an element fact block.</summary>
    internal static ActionFacts Read(Document document, ElementId id)
    {
        if (id.ToElement(document) is not { } element) return new ActionFacts();
        var type = element.GetTypeId().ToElement(document) as FloorType;
        var box = element.get_BoundingBox(null);
        var facts = new ActionFacts
        {
            Id = RevitValueReader.GetId(element.Id),
            Category = element.Category?.Name,
            Family = type?.FamilyName,
            Type = type?.Name,
            Level = element.LevelId.ToElement<Level>(document)?.Name
        };
        if (box is not null)
        {
            facts.BoundingBoxMinMm = ForkBounds.Minimum(box);
            facts.BoundingBoxMaxMm = ForkBounds.Maximum(box);
        }

        return facts;
    }
}
