using System.Globalization;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Control;

internal static class ActionMutations
{
    internal static ActionResultData PlaceFamily(Document document, ActionJobContract action)
    {
        using var symbols = document.CollectElements().OfClass<FamilySymbol>()
            .WhereParameter(BuiltInParameter.ALL_MODEL_FAMILY_NAME).Equals(action.Family!);
        if (!symbols.Any())
        {
            using var familyCollector = document.CollectElements().OfClass<Family>();
            var families = familyCollector.Cast<Family>().ToList();
            var categories = families.GroupBy(loaded => loaded.Name, StringComparer.OrdinalIgnoreCase)
                .ToDictionary(group => group.Key,
                    group => string.Join(", ", group.Select(loaded => loaded.FamilyCategory?.Name ?? "Uncategorized").Distinct()),
                    StringComparer.OrdinalIgnoreCase);
            var suggestions = ActionJobParser.ClosestFamilyNames(action.Family!, categories.Keys)
                .Select(name => $"{name} ({categories[name]})").ToList();
            throw new FamilyNotLoadedException(action.Family!, suggestions);
        }
        if (action.TypeName is not null)
            symbols.WhereParameter(BuiltInParameter.SYMBOL_NAME_PARAM).Equals(action.TypeName);
        var symbol = symbols.FirstOrDefault() as FamilySymbol
                     ?? throw new ArgumentException($"Type '{action.TypeName}' was not found in family '{action.Family}'.");
        var level = FindLevel(document, action.Level!);
        if (!symbol.IsActive)
        {
            symbol.Activate();
            document.Regenerate();
        }
        var point = new XYZ(Millimeters(action.XMm), Millimeters(action.YMm), level.ProjectElevation);
        var instance = document.Create.NewFamilyInstance(point, symbol, level, StructuralType.NonStructural);
        if (action.RotationDeg != 0)
            instance.Rotate(Line.CreateBound(point, point + XYZ.BasisZ), action.RotationDeg * Math.PI / 180);
        return new ActionResultData { Id = RevitValueReader.GetId(instance.Id), Category = instance.Category?.Name, Level = level.Name };
    }

    internal static ActionResultData CreateWall(Document document, ActionJobContract action)
    {
        var level = FindLevel(document, action.Level!);
        using var types = document.CollectElements().OfClass<WallType>();
        if (action.WallType is not null)
            types.WhereParameter(BuiltInParameter.SYMBOL_NAME_PARAM).Equals(action.WallType);
        var wallType = types.Cast<WallType>().FirstOrDefault(candidate => action.WallType is not null || candidate.Kind == WallKind.Basic)
                       ?? throw new ArgumentException($"Wall type '{action.WallType ?? "basic wall"}' was not found.");
        var start = new XYZ(Millimeters(action.StartMm[0]), Millimeters(action.StartMm[1]), level.ProjectElevation);
        var end = new XYZ(Millimeters(action.EndMm[0]), Millimeters(action.EndMm[1]), level.ProjectElevation);
        var line = Line.CreateBound(start, end);
        var wall = Wall.Create(document, line, wallType.Id, level.Id, Millimeters(action.HeightMm), 0, false, false);
        return new ActionResultData { Id = RevitValueReader.GetId(wall.Id), LengthMm = line.Length.ToMillimeters() };
    }

    internal static ActionResultData CreateFloor(Document document, ActionJobContract action)
    {
        var level = FindLevel(document, action.Level!);
        using var types = document.CollectElements().OfClass<FloorType>();
        if (action.FloorType is not null)
            types.WhereParameter(BuiltInParameter.SYMBOL_NAME_PARAM).Equals(action.FloorType);
        var floorType = types.Cast<FloorType>().FirstOrDefault()
                        ?? throw new ArgumentException($"Floor type '{action.FloorType ?? "floor"}' was not found.");
        var elevation = level.ProjectElevation;
        var points = action.PointsMm
            .Select(point => new XYZ(Millimeters(point[0]), Millimeters(point[1]), elevation))
            .ToList();
        IList<Curve> boundary = points
            .Select((point, index) => (Curve)Line.CreateBound(point, points[(index + 1) % points.Count]))
            .ToList();
        var loop = CurveLoop.Create(boundary);
        var floor = Floor.Create(document, [loop], floorType.Id, level.Id);
        return new ActionResultData { Id = RevitValueReader.GetId(floor.Id), Category = floor.Category?.Name, Level = level.Name };
    }

    internal static ActionResultData SetPhase(Document document, ActionJobContract action, List<ElementId> ids)
    {
        var created = action.CreatedPhase is null ? null : ResolvePhaseAssignment(document, action.CreatedPhase);
        var demolished = action.DemolishedPhase is null ? null : ResolvePhaseAssignment(document, action.DemolishedPhase);
        var changed = 0;
        foreach (var id in ids)
        {
            var element = id.ToElement(document)
                       ?? throw new ArgumentException($"Element {RevitValueReader.GetId(id)} was not found.");
            ApplyPhaseAssignment(document, element, created, true);
            ApplyPhaseAssignment(document, element, demolished, false);
            changed++;
        }
        return new ActionResultData { Count = changed };
    }

    internal static ActionResultData MergePhases(Document document, ActionJobContract action)
    {
        var source = FindPhase(document, action.SourcePhase!);
        var target = FindPhase(document, action.TargetPhase!);
        var sourceId = source.Id;
        var reassignedCreated = ReassignPhaseReferences(
            document, sourceId, target.Id, ElementOnPhaseStatus.New, true);
        var reassignedDemolished = ReassignPhaseReferences(
            document, sourceId, target.Id, ElementOnPhaseStatus.Demolished, false);
        var data = new ActionResultData
        {
            Count = reassignedCreated.Count + reassignedDemolished.Count,
            Verification = new ActionVerification
            {
                Before = new ActionFacts { SourcePhase = source.Name, TargetPhase = target.Name },
            },
        };
        try
        {
            document.Delete(sourceId);
            data.SourceDeleted = true;
        }
        catch (Exception exception)
        {
            data.SourceDeleted = false;
            data.PhaseDeleteError = exception.Message;
        }
        data.Verification.After = new ActionFacts
        {
            ReassignedCreated = reassignedCreated.Count,
            ReassignedDemolished = reassignedDemolished.Count,
            SourceRemaining = CountPhaseReferences(document, sourceId),
        };
        data.Verification.Changed = reassignedCreated.Concat(reassignedDemolished)
            .Select(RevitValueReader.GetId).Distinct().ToList();
        return data;
    }

    private static ElementId? ResolvePhaseAssignment(Document document, string name) =>
        name.Length == 0 ? ElementId.InvalidElementId : FindPhase(document, name).Id;

    private static void ApplyPhaseAssignment(Document document, Element element, ElementId? phaseId, bool created)
    {
        if (phaseId is null) return;
        if (!element.ArePhasesModifiable())
            throw new InvalidOperationException(
                $"Phases cannot be modified on element {RevitValueReader.GetId(element.Id)} ('{element.Category?.Name ?? element.Name}').");
        if (created)
        {
            if (phaseId != ElementId.InvalidElementId && !element.IsPhaseCreatedValid(phaseId))
                throw new ArgumentException($"The phase is not a valid creation phase for element {RevitValueReader.GetId(element.Id)}.");
            element.CreatedPhaseId = phaseId;
        }
        else
        {
            if (phaseId != ElementId.InvalidElementId && !element.IsDemolishedPhaseOrderValid(phaseId))
                throw new ArgumentException(
                    $"The demolition phase is out of order for element {RevitValueReader.GetId(element.Id)}; demolition must follow the creation phase.");
            element.DemolishedPhaseId = phaseId;
        }
    }

    private static List<ElementId> ReassignPhaseReferences(
        Document document, ElementId sourceId, ElementId targetId, ElementOnPhaseStatus status, bool created)
    {
        using var filter = new ElementPhaseStatusFilter(sourceId, status);
        using var collector = document.CollectElements().WherePasses(filter);
        var moved = new List<ElementId>();
        foreach (var element in collector.ToElements())
        {
            if (element is Phase || element.Id == sourceId) continue;
            ApplyPhaseAssignment(document, element, targetId, created);
            moved.Add(element.Id);
        }
        return moved;
    }

    private static int CountPhaseReferences(Document document, ElementId sourceId)
    {
        if (sourceId.ToElement(document) is null) return 0;
        using var createdCollector = document.CollectElements()
            .WherePasses(new ElementPhaseStatusFilter(sourceId, ElementOnPhaseStatus.New));
        using var demolishedCollector = document.CollectElements()
            .WherePasses(new ElementPhaseStatusFilter(sourceId, ElementOnPhaseStatus.Demolished));
        return createdCollector.ToElementIds().Concat(demolishedCollector.ToElementIds())
            .Distinct().Count(id => id != sourceId);
    }

    private static Phase FindPhase(Document document, string name)
    {
        using var phases = document.CollectElements().OfClass<Phase>();
        return phases.Cast<Phase>().FirstOrDefault(phase => string.Equals(phase.Name, name, StringComparison.OrdinalIgnoreCase))
               ?? throw new ArgumentException($"Phase '{name}' was not found. Use revit_list_catalog(section=\"phases\") for exact names.");
    }

    internal static string PhaseName(Document document, ElementId phaseId)
    {
        if (phaseId is null || phaseId == ElementId.InvalidElementId) return string.Empty;
        return phaseId.ToElement<Phase>(document)?.Name ?? string.Empty;
    }

    internal static ActionResultData SetParameter(Document document, ActionJobContract action)
    {
        var element = CreateId(action.ElementId).ToElement(document)
                      ?? throw new ArgumentException($"Element {action.ElementId} was not found.");
        var parameter = element.FindParameter(action.Parameter!)
                        ?? throw new ArgumentException($"Parameter '{action.Parameter}' was not found on the instance or type.");
        if (parameter.IsReadOnly) throw new InvalidOperationException($"Parameter '{action.Parameter}' is read-only.");
        var oldValue = ParameterValue(parameter);
        var value = action.Value!;
        var changed = parameter.StorageType switch
        {
            StorageType.String => parameter.Set(value),
            StorageType.Integer => parameter.Set(int.Parse(value, NumberStyles.Integer, CultureInfo.InvariantCulture)),
            StorageType.Double => parameter.Set(ParameterDouble(parameter, value)),
            _ => throw new ArgumentException("Only String, Integer and Double parameters are supported; ElementId parameters cannot be set.")
        };
        if (!changed)
            throw new InvalidOperationException($"Revit could not set parameter '{action.Parameter}'.");
        return new ActionResultData
        {
            OldValue = oldValue,
            NewValue = ParameterValue(parameter),
            ParameterScope = parameter.Element.Id == element.Id ? "instance" : "type"
        };
    }

    private static double ParameterDouble(Parameter parameter, string text)
    {
        var value = double.Parse(text, NumberStyles.Float, CultureInfo.InvariantCulture);
        if (double.IsNaN(value) || double.IsInfinity(value)) throw new ArgumentException("Parameter value must be finite.");
        var spec = parameter.Definition.GetDataType();
        if (spec == SpecTypeId.Length) return Millimeters(value);
        if (spec == SpecTypeId.Area) return UnitUtils.ConvertToInternalUnits(value, UnitTypeId.SquareMeters);
        return value;
    }

    internal static string ParameterValue(Parameter parameter)
    {
        if (!parameter.HasValue) return string.Empty;
        if (parameter.StorageType == StorageType.String) return parameter.AsString() ?? string.Empty;
        if (parameter.StorageType == StorageType.Integer) return parameter.AsInteger().ToString(CultureInfo.InvariantCulture);
        if (parameter.StorageType != StorageType.Double) throw new ArgumentException("Unsupported parameter storage type.");
        var spec = parameter.Definition.GetDataType();
        var value = parameter.AsDouble();
        if (spec == SpecTypeId.Length) value = value.ToMillimeters();
        else if (spec == SpecTypeId.Area) value = UnitUtils.ConvertFromInternalUnits(value, UnitTypeId.SquareMeters);
        return value.ToString("R", CultureInfo.InvariantCulture);
    }

    private static Level FindLevel(Document document, string name)
    {
        using var levels = document.CollectElements().OfClass<Level>()
            .WhereParameter(BuiltInParameter.DATUM_TEXT).Equals(name);
        return levels.FirstOrDefault() as Level
               ?? throw new ArgumentException($"Level '{name}' was not found.");
    }

    private static ElementId CreateId(long value) => ActionCommandExecutor.CreateId(value);
    private static double Millimeters(double value) => UnitUtils.ConvertToInternalUnits(value, UnitTypeId.Millimeters);

    internal sealed class FamilyNotLoadedException(string name, List<string> closestFamilies)
        : ArgumentException($"Family '{name}' is not loaded. Closest loaded families: {string.Join(", ", closestFamilies)}")
    {
        public List<string> ClosestFamilies { get; } = closestFamilies;
    }
}
