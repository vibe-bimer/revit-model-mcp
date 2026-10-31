using System.Globalization;
using Autodesk.Revit.DB;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Replaces each element with a copy so Revit assigns a new <see cref="ElementId"/>: the API has no way to
/// assign one. A dry run rehearses the whole replacement and reports what would be lost. Elements whose
/// deletion takes other elements with them, or whose copy Revit cannot rehost, are refused rather than
/// silently skipped.
/// </summary>
internal static class ForkReset
{
    /// <summary>Whether the request names at least one element, which every reset needs.</summary>
    internal static void Validate(ActionJobContract action) =>
        ForkLookup.Require(action.ElementIds is { Count: > 0 }, "elementIds must hold at least one element id.");

    /// <summary>Replaces the addressed elements and reports the old to new pairing.</summary>
    internal static ActionResultData Reset(Document document, ActionJobContract action, List<ElementId> ids)
    {
        Validate(action);
        var ineligible = new List<ForkIneligibleElement>();
        var eligible = new List<ElementId>();
        var systemMembers = SystemMemberIds(document);
        var dependentCategories = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var id in ids)
        {
            var (kind, reason) = IneligibilityReason(document, id, systemMembers, dependentCategories);
            if (reason is null)
            {
                eligible.Add(id);
            }
            else
            {
                ineligible.Add(new ForkIneligibleElement { Id = RevitValueReader.GetId(id), Kind = kind, Reason = reason });
            }
        }

        // A whole-model rehearsal has to stay readable: group the refusals by reason and keep samples.
        var summary = Summarize(ineligible);
        var samples = Sample(ineligible);

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

        // One element at a time keeps the old to new pairing exact, and each exchange runs in its own
        // sub-transaction so a copy Revit refuses names the element instead of aborting the whole call.
        var mapping = new List<ForkIdPair>();
        var failures = new List<ForkIneligibleElement>();
        var joinsFound = 0;
        var joinsRestored = 0;
        foreach (var id in eligible)
        {
            var oldId = RevitValueReader.GetId(id);
            using var exchange = new SubTransaction(document);
            exchange.Start();
            try
            {
                var expectedCategory = document.GetElement(id)?.Category?.Name ?? string.Empty;

                // Joins are not carried by a copy, so remember them and restore them after the exchange.
                var joined = new List<ElementId>();
                if (document.GetElement(id) is { } original)
                {
                    joined.AddRange(JoinGeometryUtils.GetJoinedElements(document, original)
                        .Where(neighbour => RevitValueReader.GetId(neighbour) != oldId));
                }

                // The document to document overload rehosts hosted elements, which the XYZ overload does not.
                var created = ElementTransformUtils
                    .CopyElements(document, new List<ElementId> { id }, document, Transform.Identity, new CopyPasteOptions())
                    .ToList();
                if (created.Count != 1)
                {
                    throw new InvalidOperationException(
                        $"Revit created {created.Count} copies for element {oldId}; expected exactly one.");
                }

                var newId = RevitValueReader.GetId(created[0]);
                var copiedCategory = document.GetElement(created[0])?.Category?.Name ?? string.Empty;
                if (!string.Equals(copiedCategory, expectedCategory, StringComparison.Ordinal))
                {
                    throw new InvalidOperationException(
                        $"The copy of element {oldId} landed in category '{copiedCategory}' instead of '{expectedCategory}'.");
                }

                document.Delete(new List<ElementId> { id });
                if (document.GetElement(created[0]) is null)
                {
                    throw new InvalidOperationException(
                        $"Copy {newId} did not survive deleting element {oldId}; the element was not replaced.");
                }

                joinsFound += joined.Count;
                var copy = document.GetElement(created[0]);
                foreach (var neighbour in joined)
                {
                    var neighbourElement = document.GetElement(neighbour);
                    if (copy is null || neighbourElement is null ||
                        JoinGeometryUtils.AreElementsJoined(document, copy, neighbourElement))
                    {
                        continue;
                    }

                    JoinGeometryUtils.JoinGeometry(document, copy, neighbourElement);
                    joinsRestored++;
                }

                exchange.Commit();
                mapping.Add(new ForkIdPair { Old = oldId, New = newId });
            }
            catch (Exception exception)
            {
                exchange.RollBack();
                failures.Add(new ForkIneligibleElement
                {
                    Id = oldId,
                    Kind = "copy-failed",
                    Reason = $"Revit could not replace this element: {exception.Message.Trim()}"
                });
            }
        }

        // A real run stays all or nothing: the executor rolls the whole action back when this throws,
        // because a selection that is half replaced is harder to reason about than a refusal.
        if (action.DryRun != true && failures.Count > 0)
        {
            throw new InvalidOperationException(
                $"Refusing to keep a partial reset: {failures.Count} of {eligible.Count} elements could not be replaced. {Describe(failures)}");
        }

        ineligible.AddRange(failures);
        summary = Summarize(ineligible);
        samples = Sample(ineligible);

        return new ActionResultData
        {
            Count = mapping.Count,
            ForkOutcome = new ForkOutcome
            {
                IdMapping = mapping,
                Ineligible = samples.Count > 0 ? samples : null,
                IneligibleCount = ineligible.Count > 0 ? ineligible.Count : null,
                IneligibleKinds = summary.Count > 0 ? summary : null,
                JoinsFound = joinsFound,
                JoinsRestored = joinsRestored,
                DependentCategories = dependentCategories.Count > 0
                    ? dependentCategories
                        .Select(entry => new ForkCount { Category = entry.Key, Count = entry.Value })
                        .OrderByDescending(entry => entry.Count)
                        .ThenBy(entry => entry.Category, StringComparer.Ordinal)
                        .Take(20)
                        .ToList()
                    : null
            },
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
            if (element is not MEPSystem system) continue;

            // MEPSystem.Elements is an ElementSet of terminal elements; it excludes base equipment.
            foreach (Element member in system.Elements) members.Add(RevitValueReader.GetId(member.Id));
        }

        return members;
    }

    /// <summary>Whether any MEP connector of the element is joined to something else.</summary>
    private static bool IsConnectedToNetwork(Element element)
    {
        var manager = (element as FamilyInstance)?.MEPModel?.ConnectorManager
                      ?? (element as MEPCurve)?.ConnectorManager;
        if (manager is null) return false;

        // ConnectorSet is non-generic as well; its items are connectors.
        foreach (Connector connector in manager.Connectors)
            if (connector.IsConnected)
                return true;

        return false;
    }

    private static (string Kind, string? Reason) IneligibilityReason(
        Document document,
        ElementId id,
        ISet<long> systemMembers,
        IDictionary<string, int> dependentCategories)
    {
        var element = document.GetElement(id);
        if (element is null) return ("missing", "The element does not exist in this document.");
        if (element is ElementType) return ("type", "Element types are not reset; select instances.");
        if (element.GroupId != ElementId.InvalidElementId)
            return ("group", "The element belongs to a group; ungroup it before resetting.");
        if (element is DatumPlane)
            return ("datum", "Datum elements such as grids, levels and reference planes are excluded.");

        // Hosted elements are not refused: the document to document copy overload rehosts them, and a
        // copy that Revit still refuses shows up as copy-failed with the element id.
        if (element is MEPCurve)
            return ("mep-curve", "MEP curves belong to a system, and copying them breaks the system membership.");
        if (systemMembers.Contains(RevitValueReader.GetId(id)))
        {
            return ("mep-system",
                "The element is an MEP system member; the copy would not rejoin the network, and Revit re-heals the run around the deleted original.");
        }

        if (IsConnectedToNetwork(element))
            return ("mep-connected", "The element has connected MEP connectors, so a copy would start detached from the network.");

        // GetDependentElements reports the element itself among the parent/child relationships, so
        // only the other entries matter: those are the elements Revit deletes along with this one.
        var idValue = RevitValueReader.GetId(id);
        var dependents = element.GetDependentElements(null)?
            .Where(dependent => RevitValueReader.GetId(dependent) != idValue)
            .ToList();
        if (dependents is { Count: > 0 })
        {
            var described = new List<string>();
            foreach (var dependent in dependents)
            {
                var name = document.GetElement(dependent)?.Category?.Name ?? "unknown";
                dependentCategories[name] = dependentCategories.TryGetValue(name, out var seen) ? seen + 1 : 1;
                described.Add($"{RevitValueReader.GetId(dependent)} ({name})");
            }

            return ("dependents",
                $"{dependents.Count} dependent element(s) would be deleted with it: {string.Join(", ", described.Take(3))}.");
        }

        if (!ElementTransformUtils.CanMirrorElement(document, id))
            return ("cannot-copy", "Revit reports that this element cannot be copied by this route.");

        return (string.Empty, null);
    }

    private static List<ForkCount> Summarize(IReadOnlyList<ForkIneligibleElement> ineligible) =>
        ineligible
            .GroupBy(entry => entry.Kind ?? "other", StringComparer.Ordinal)
            .Select(group => new ForkCount { Kind = group.Key, Count = group.Count() })
            .OrderByDescending(entry => entry.Count)
            .ThenBy(entry => entry.Kind, StringComparer.Ordinal)
            .ToList();

    private static List<ForkIneligibleElement> Sample(IReadOnlyList<ForkIneligibleElement> ineligible) =>
        ineligible
            .GroupBy(entry => entry.Kind ?? "other", StringComparer.Ordinal)
            .SelectMany(group => group.Take(3))
            .OrderBy(entry => entry.Id)
            .ToList();

    private static string Describe(IReadOnlyList<ForkIneligibleElement> ineligible) =>
        string.Join("; ", ineligible.Take(5).Select(entry => $"{entry.Id}: {entry.Reason}"));
}
