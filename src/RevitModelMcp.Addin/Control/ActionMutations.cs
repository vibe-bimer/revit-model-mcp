using System.Globalization;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Compatibility;
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
#if REVIT2022_OR_GREATER
        var floor = Floor.Create(document, [loop], floorType.Id, level.Id);
#else
        // Revit 2020 has no Floor.Create; document.Create.NewFloor takes a CurveArray and elements.
        var profile = new CurveArray();
        foreach (var curve in boundary)
        {
            profile.Append(curve);
        }

        var floor = document.Create.NewFloor(profile, floorType, level, false);
#endif
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
            if (phaseId != ElementId.InvalidElementId && !IsDemolishedPhaseOrderValid(document, element, phaseId))
                throw new ArgumentException(
                    $"The demolition phase is out of order for element {RevitValueReader.GetId(element.Id)}; demolition must follow the creation phase.");
            element.DemolishedPhaseId = phaseId;
        }
    }

    /// <summary>
    /// Revit 2020 has no <c>Element.IsDemolishedPhaseOrderValid</c>;
    /// the demolition phase must not precede the creation phase.
    /// </summary>
    private static bool IsDemolishedPhaseOrderValid(Document document, Element element, ElementId demolishedPhaseId)
    {
#if REVIT2022_OR_GREATER
        return element.IsDemolishedPhaseOrderValid(demolishedPhaseId);
#else
        return PhaseIndex(document, element.CreatedPhaseId) <= PhaseIndex(document, demolishedPhaseId);
#endif
    }

#if !REVIT2022_OR_GREATER
    private static int PhaseIndex(Document document, ElementId phaseId)
    {
        var index = 0;
        foreach (Phase phase in document.Phases)
        {
            if (phase.Id == phaseId) return index;
            index++;
        }

        return -1;
    }
#endif

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
            StorageType.Double => parameter.Set(ParameterDouble(document, parameter, value)),
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

    private static double ParameterDouble(Document document, Parameter parameter, string text)
    {
        var value = double.Parse(text, NumberStyles.Float, CultureInfo.InvariantCulture);
        if (double.IsNaN(value) || double.IsInfinity(value)) throw new ArgumentException("Parameter value must be finite.");
        return ParameterDataType.From(parameter.Definition).ToInternalUnits(document, value);
    }

    internal static string ParameterValue(Parameter parameter)
    {
        if (!parameter.HasValue) return string.Empty;
        if (parameter.StorageType == StorageType.String) return parameter.AsString() ?? string.Empty;
        if (parameter.StorageType == StorageType.Integer) return parameter.AsInteger().ToString(CultureInfo.InvariantCulture);
        if (parameter.StorageType != StorageType.Double) throw new ArgumentException("Unsupported parameter storage type.");
        var value = ParameterDataType.From(parameter.Definition).FromInternalUnits(parameter.AsDouble());
        return value.ToString("R", CultureInfo.InvariantCulture);
    }

    /// <summary>
    /// Replaces each element with a copy so Revit assigns a new <see cref="ElementId"/>: the API has no
    /// way to assign one. A dry run rehearses the whole replacement and reports what would be lost.
    /// Elements whose deletion takes other elements with them, or whose copy Revit cannot rehost, are
    /// refused rather than silently skipped.
    /// </summary>
    internal static ActionResultData ResetElementIds(Document document, ActionJobContract action, List<ElementId> ids)
    {
        var ineligible = new List<IneligibleElement>();
        var eligible = new List<ElementId>();
        var systemMembers = SystemMemberIds(document);
        foreach (var id in ids)
        {
            var (kind, reason) = IneligibilityReason(document, id, systemMembers);
            if (reason is null)
            {
                eligible.Add(id);
            }
            else
            {
                ineligible.Add(new IneligibleElement { Id = RevitValueReader.GetId(id), Kind = kind, Reason = reason });
            }
        }

        // A whole-model rehearsal has to stay readable: group the refusals by reason and keep samples.
        var summary = ineligible
            .GroupBy(entry => entry.Kind ?? "other", StringComparer.Ordinal)
            .Select(group => new IneligibleKindCount { Kind = group.Key, Count = group.Count() })
            .OrderByDescending(entry => entry.Count)
            .ThenBy(entry => entry.Kind, StringComparer.Ordinal)
            .ToList();
        var samples = ineligible
            .GroupBy(entry => entry.Kind ?? "other", StringComparer.Ordinal)
            .SelectMany(group => group.Take(3))
            .OrderBy(entry => entry.Id)
            .ToList();

        if (eligible.Count == 0)
        {
            throw new InvalidOperationException($"No selected element can be reset. {Describe(ineligible)}");
        }

        // A real run is all or nothing: a half replaced selection is harder to reason about than a refusal.
        if (action.DryRun != true && ineligible.Count > 0)
        {
            throw new InvalidOperationException(
                $"Refusing to reset {eligible.Count} of {ids.Count} elements while others are ineligible. {Describe(ineligible)}");
        }

        // One element at a time keeps the old to new pairing exact, and lets each exchange be checked
        // before the next one starts; Revit does not document the order of a bulk copy result.
        var mapping = new List<ElementIdPair>();
        foreach (var id in eligible)
        {
            var oldId = RevitValueReader.GetId(id);
            var expectedCategory = document.GetElement(id)?.Category?.Name ?? string.Empty;
            var created = ElementTransformUtils.CopyElements(document, new List<ElementId> { id }, XYZ.Zero).ToList();
            if (created.Count != 1)
            {
                throw new InvalidOperationException($"Revit created {created.Count} copies for element {oldId}; expected exactly one.");
            }

            var newId = RevitValueReader.GetId(created[0]);
            var copiedCategory = document.GetElement(created[0])?.Category?.Name ?? string.Empty;
            if (!string.Equals(copiedCategory, expectedCategory, StringComparison.Ordinal))
            {
                throw new InvalidOperationException($"The copy of element {oldId} landed in category '{copiedCategory}' instead of '{expectedCategory}'.");
            }

            document.Delete(new List<ElementId> { id });
            if (document.GetElement(created[0]) is null)
            {
                throw new InvalidOperationException($"Copy {newId} did not survive deleting element {oldId}; the element was not replaced.");
            }

            mapping.Add(new ElementIdPair { Old = oldId, New = newId });
        }

        return new ActionResultData
        {
            Count = mapping.Count,
            IdMapping = mapping,
            Ineligible = samples.Count > 0 ? samples : null,
            IneligibleCount = ineligible.Count > 0 ? ineligible.Count : null,
            IneligibleKinds = summary.Count > 0 ? summary : null,
            Verification = new ActionVerification
            {
                Changed = mapping.Select(pair => pair.New).ToList()
            }
        };
    }

    /// <summary>
    /// Every element that belongs to an MEP system. Copying one leaves the copy outside the network and
    /// makes Revit re-heal the run around the deleted original, which changes the pipe and duct count.
    /// </summary>
    private static HashSet<long> SystemMemberIds(Document document)
    {
        var members = new HashSet<long>();
        foreach (var element in new FilteredElementCollector(document).OfClass(typeof(MEPSystem)))
        {
            if (element is not MEPSystem system)
            {
                continue;
            }

            // MEPSystem.Elements is an ElementSet of terminal elements; it excludes base equipment.
            foreach (Element member in system.Elements)
            {
                members.Add(RevitValueReader.GetId(member.Id));
            }
        }

        return members;
    }

    /// <summary>Whether any MEP connector of the element is joined to something else.</summary>
    private static bool IsConnectedToNetwork(Element element)
    {
        var manager = (element as FamilyInstance)?.MEPModel?.ConnectorManager
            ?? (element as MEPCurve)?.ConnectorManager;
        if (manager is null)
        {
            return false;
        }

        // ConnectorSet is non-generic as well; its items are connectors.
        foreach (Connector connector in manager.Connectors)
        {
            if (connector.IsConnected)
            {
                return true;
            }
        }

        return false;
    }

    private static (string Kind, string? Reason) IneligibilityReason(
        Document document,
        ElementId id,
        ISet<long> systemMembers)
    {
        var element = document.GetElement(id);
        if (element is null)
        {
            return ("missing", "The element does not exist in this document.");
        }

        if (element is ElementType)
        {
            return ("type", "Element types are not reset; select instances.");
        }

        if (element.GroupId != ElementId.InvalidElementId)
        {
            return ("group", "The element belongs to a group; ungroup it before resetting.");
        }

        if (element is DatumPlane)
        {
            return ("datum", "Datum elements such as grids, levels and reference planes are excluded.");
        }

        var host = (element as FamilyInstance)?.Host ?? (element as Opening)?.Host;
        if (host is not null)
        {
            return ("hosted", $"The element is hosted by '{host.Category?.Name ?? "another element"}'; copies are not rehosted.");
        }

        if (element is MEPCurve)
        {
            return ("mep-curve", "MEP curves belong to a system, and copying them breaks the system membership.");
        }

        if (systemMembers.Contains(RevitValueReader.GetId(id)))
        {
            return ("mep-system", "The element is an MEP system member; the copy would not rejoin the network, and Revit re-heals the run around the deleted original.");
        }

        if (IsConnectedToNetwork(element))
        {
            return ("mep-connected", "The element has connected MEP connectors, so a copy would start detached from the network.");
        }

        // GetDependentElements reports the element itself among the parent/child relationships, so
        // only the other entries matter: those are the elements Revit deletes along with this one.
        var idValue = RevitValueReader.GetId(id);
        var dependents = element.GetDependentElements(null)?
            .Where(dependent => RevitValueReader.GetId(dependent) != idValue)
            .ToList();
        if (dependents is { Count: > 0 })
        {
            var sample = string.Join(", ", dependents.Take(3).Select(dependent =>
                $"{RevitValueReader.GetId(dependent)} ({document.GetElement(dependent)?.Category?.Name ?? "unknown"})"));
            return ("dependents", $"{dependents.Count} dependent element(s) would be deleted with it: {sample}.");
        }

        if (!ElementTransformUtils.CanMirrorElement(document, id))
        {
            return ("cannot-copy", "Revit reports that this element cannot be copied by this route.");
        }

        return (string.Empty, null);
    }

    private static string Describe(IReadOnlyList<IneligibleElement> ineligible) =>
        string.Join("; ", ineligible.Take(5).Select(entry => $"{entry.Id}: {entry.Reason}"));

    private static Level FindLevel(Document document, string name)
    {
        using var levels = document.CollectElements().OfClass<Level>()
            .WhereParameter(BuiltInParameter.DATUM_TEXT).Equals(name);
        return levels.FirstOrDefault() as Level
               ?? throw new ArgumentException($"Level '{name}' was not found.");
    }

    private static ElementId CreateId(long value) => ActionCommandExecutor.CreateId(value);
    private static double Millimeters(double value) => RevitUnits.MillimetersToInternalUnits(value);

    internal sealed class FamilyNotLoadedException(string name, List<string> closestFamilies)
        : ArgumentException($"Family '{name}' is not loaded. Closest loaded families: {string.Join(", ", closestFamilies)}")
    {
        public List<string> ClosestFamilies { get; } = closestFamilies;
    }
}
