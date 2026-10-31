using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Assigns the created or demolished phase of existing elements, and merges one phase into another. Revit
/// offers no API to create a phase, so both actions only reassign elements between phases the document
/// already holds. Runs inside the caller's transaction, so a dry run is rolled back by the executor.
/// </summary>
internal static class ForkPhases
{
    /// <summary>Checks a phase assignment before any element is touched.</summary>
    internal static void Validate(ActionJobContract action)
    {
        var created = action.Options.CreatedPhase;
        var demolished = action.Options.DemolishedPhase;
        ForkLookup.Require(
            created is not null || demolished is not null,
            "At least one of createdPhase or demolishedPhase is required.");
        foreach (var (label, value) in new[] { ("createdPhase", created), ("demolishedPhase", demolished) })
        {
            ForkLookup.Require(
                value is null || value.Length == 0 || value.Trim().Length > 0,
                $"{label} must be a phase name, an empty string to clear, or null.");
        }
    }

    /// <summary>Assigns the requested phases and reports how many elements changed.</summary>
    internal static ActionResultData Set(Document document, ActionJobContract action, List<ElementId> ids)
    {
        Validate(action);
        ForkLookup.Require(ids.Count > 0, "elementIds must hold at least one element id.");
        var created = action.Options.CreatedPhase is null
            ? null
            : ResolveAssignment(document, action.Options.CreatedPhase);
        var demolished = action.Options.DemolishedPhase is null
            ? null
            : ResolveAssignment(document, action.Options.DemolishedPhase);
        var changed = 0;
        foreach (var id in ids)
        {
            var element = id.ToElement(document)
                          ?? throw new ArgumentException($"Element {RevitValueReader.GetId(id)} was not found.");
            ApplyAssignment(document, element, created, true);
            ApplyAssignment(document, element, demolished, false);
            changed++;
        }

        return new ActionResultData { Count = changed };
    }

    /// <summary>Reads each addressed element's phase assignment.</summary>
    internal static ActionFacts ReadAssignment(Document document, IReadOnlyList<long> ids)
    {
        var elements = new List<ActionFacts>();
        foreach (var id in ids)
        {
            if (ForkLookup.CreateId(id).ToElement(document) is not { } element) continue;
            elements.Add(new ActionFacts
            {
                Id = RevitValueReader.GetId(element.Id),
                Category = element.Category?.Name,
                Fork = new ForkFacts
                {
                    CreatedPhase = ForkLookup.PhaseName(document, element.CreatedPhaseId),
                    DemolishedPhase = ForkLookup.PhaseName(document, element.DemolishedPhaseId)
                }
            });
        }

        return new ActionFacts { Elements = elements };
    }

    /// <summary>Ids whose phase assignment differs between two readings.</summary>
    internal static List<long>? ChangedBetween(ActionFacts? before, ActionFacts? after)
    {
        if (before?.Elements is null || after?.Elements is null) return null;
        var previous = before.Elements.ToDictionary(facts => facts.Id!.Value);
        var changed = new List<long>();
        foreach (var facts in after.Elements)
        {
            if (!previous.TryGetValue(facts.Id!.Value, out var old)) continue;
            if (old.Fork?.CreatedPhase != facts.Fork?.CreatedPhase
                || old.Fork?.DemolishedPhase != facts.Fork?.DemolishedPhase)
            {
                changed.Add(facts.Id!.Value);
            }
        }

        return changed;
    }

    /// <summary>Reads the phase pair a merge names, refusing a missing phase before anything moves.</summary>
    internal static ActionFacts ReadSource(Document document, ActionJobContract action)
    {
        var source = ForkLookup.Phase(document, action.Options.SourcePhase!);
        var target = ForkLookup.Phase(document, action.Options.TargetPhase!);
        ForkLookup.Require(source.Id != target.Id, "sourcePhase and targetPhase must differ.");
        return new ActionFacts
        {
            Fork = new ForkFacts
            {
                SourcePhase = source.Name,
                TargetPhase = target.Name,
                SourceRemaining = CountReferences(document, source.Id)
            }
        };
    }

    /// <summary>Moves every reference from the source phase to the target and deletes the source phase.</summary>
    internal static ActionResultData Merge(Document document, ActionJobContract action)
    {
        ForkLookup.Require(
            !string.IsNullOrWhiteSpace(action.Options.SourcePhase),
            "sourcePhase is required.");
        ForkLookup.Require(
            !string.IsNullOrWhiteSpace(action.Options.TargetPhase),
            "targetPhase is required.");
        var source = ForkLookup.Phase(document, action.Options.SourcePhase!);
        var target = ForkLookup.Phase(document, action.Options.TargetPhase!);
        ForkLookup.Require(source.Id != target.Id, "sourcePhase and targetPhase must differ.");
        var sourceId = source.Id;
        var reassignedCreated = ReassignReferences(document, sourceId, target.Id, ElementOnPhaseStatus.New, true);
        var reassignedDemolished = ReassignReferences(
            document,
            sourceId,
            target.Id,
            ElementOnPhaseStatus.Demolished,
            false);
        var data = new ActionResultData
        {
            Count = reassignedCreated.Count + reassignedDemolished.Count,
            Verification = new ActionVerification
            {
                Before = new ActionFacts
                {
                    Fork = new ForkFacts { SourcePhase = source.Name, TargetPhase = target.Name }
                }
            }
        };
        string? deleteError = null;
        var deleted = false;
        try
        {
            document.Delete(sourceId);
            deleted = true;
        }
        catch (Exception exception)
        {
            deleteError = exception.Message;
        }

        data.Verification.After = new ActionFacts
        {
            Fork = new ForkFacts
            {
                SourcePhase = source.Name,
                TargetPhase = target.Name,
                ReassignedCreated = reassignedCreated.Count,
                ReassignedDemolished = reassignedDemolished.Count,
                SourceRemaining = CountReferences(document, sourceId)
            }
        };
        data.Verification.Changed = reassignedCreated.Concat(reassignedDemolished)
            .Select(RevitValueReader.GetId).Distinct().ToList();
        data.Notes = [deleted ? $"Deleted phase '{source.Name}'." : $"Phase '{source.Name}' was kept: {deleteError}"];
        return data;
    }

    /// <summary>Reads each addressed element's phase assignment.</summary>
    internal static ActionFacts ReadAssignment(Document document, IEnumerable<ElementId> ids) =>
        ReadAssignment(document, ids.Select(RevitValueReader.GetId).ToList());

    private static ElementId ResolveAssignment(Document document, string name) =>
        name.Length == 0 ? ElementId.InvalidElementId : ForkLookup.Phase(document, name).Id;

    private static void ApplyAssignment(Document document, Element element, ElementId? phaseId, bool created)
    {
        if (phaseId is null) return;
        if (!element.ArePhasesModifiable())
        {
            throw new InvalidOperationException(
                $"Phases cannot be modified on element {RevitValueReader.GetId(element.Id)} ('{element.Category?.Name ?? element.Name}').");
        }

        var id = RevitValueReader.GetId(element.Id);
        if (created)
        {
            if (phaseId != ElementId.InvalidElementId && !element.IsPhaseCreatedValid(phaseId))
            {
                throw new ArgumentException($"The phase is not a valid creation phase for element {id}.");
            }

            element.CreatedPhaseId = phaseId;
            return;
        }

        if (phaseId != ElementId.InvalidElementId && !element.IsDemolishedPhaseOrderValid(phaseId))
        {
            throw new ArgumentException(
                $"The demolition phase is out of order for element {id}; demolition must follow the creation phase.");
        }

        element.DemolishedPhaseId = phaseId;
    }

    private static List<ElementId> ReassignReferences(
        Document document,
        ElementId sourceId,
        ElementId targetId,
        ElementOnPhaseStatus status,
        bool created)
    {
        using var filter = new ElementPhaseStatusFilter(sourceId, status);
        using var collector = document.CollectElements().WherePasses(filter);
        var moved = new List<ElementId>();
        foreach (var element in collector.ToElements())
        {
            if (element is Phase || element.Id == sourceId) continue;
            ApplyAssignment(document, element, targetId, created);
            moved.Add(element.Id);
        }

        return moved;
    }

    private static int CountReferences(Document document, ElementId sourceId)
    {
        if (sourceId.ToElement(document) is null) return 0;
        using var createdCollector = document.CollectElements()
            .WherePasses(new ElementPhaseStatusFilter(sourceId, ElementOnPhaseStatus.New));
        using var demolishedCollector = document.CollectElements()
            .WherePasses(new ElementPhaseStatusFilter(sourceId, ElementOnPhaseStatus.Demolished));
        return createdCollector.ToElementIds().Concat(demolishedCollector.ToElementIds())
            .Distinct().Count(id => id != sourceId);
    }
}
