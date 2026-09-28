using System.IO;
using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Models;

namespace RevitModelMcp.Control;

/// <summary>
/// Copies the selectable components of a 3D view into a new project so Revit assigns every element a
/// fresh id, while the source model stays exactly as it was. The copy is cross-document: nothing is
/// deleted and no dependency chain is broken, but only model content travels, so views, sheets,
/// schedules, annotations, phases, worksets and systems are not part of the result.
/// </summary>
internal static class ModelRebuild
{
    private const int MaxMappingEntries = 5_000;
    private const int MaxIsolationTransactions = 400;
    private const string RebuildTransactionName = "revit_rebuild_model_ids";
    private const string TemplateLevelPrefix = "__rebuild_";

    internal static ActionResultData Rebuild(Document source, ActionJobContract action)
    {
        var destinationPath = Path.GetFullPath(action.DestinationPath!);
        var templatePath = string.IsNullOrWhiteSpace(action.TemplatePath) ? null : Path.GetFullPath(action.TemplatePath);
        if (templatePath is not null && !File.Exists(templatePath))
            throw new FileNotFoundException($"The template file was not found: {templatePath}.", templatePath);
        if (File.Exists(destinationPath) && !action.Overwrite)
            throw new IOException($"The destination file already exists: {destinationPath}. Pass overwrite=true to replace it.");
        var directory = Path.GetDirectoryName(destinationPath);
        if (!string.IsNullOrEmpty(directory)) Directory.CreateDirectory(directory);

        var view = ResolveView(source, action.View);
        var selected = SelectSource(source, view, out var excluded);
        if (selected.Count == 0)
            throw new InvalidOperationException($"The 3D view '{view.Name}' contains no selectable components.");

        var result = new ActionResultData
        {
            DestinationPath = destinationPath,
            SourceView = view.Name,
            Excluded = excluded.Count == 0 ? null : excluded,
            DryRun = action.DryRun,
            Count = 0
        };

        var ordered = OrderForCopy(source, selected, result);
        result.SourceElementCount = ordered.Count;
        result.DatumCount = ordered.Count(id => IsDatum(source.GetElement(id)));
        result.SourceCategoryCounts = CountCategories(source, ordered);

        Document? destination = null;
        try
        {
            destination = templatePath is null
                ? source.Application.NewProjectDocument(UnitSystem.Metric)
                : source.Application.NewProjectDocument(templatePath);
            result.TemplatePath = templatePath ?? "the default metric template";

            var newIds = Copy(source, destination, ordered, action.RemoveTemplateLevels, result);
            if (newIds.Count == 0)
                throw new InvalidOperationException("Revit copied no element into the new model; nothing was written.");
            result.Count = newIds.Count;
            result.CopiedCategoryCounts = CountCategories(destination, newIds);
            result.NewIdMin = newIds.Min(RevitValueReader.GetId);
            result.NewIdMax = newIds.Max(RevitValueReader.GetId);
            BuildMapping(source, destination, ordered, newIds, result);
            EnsureOpenableView(destination, result);

            if (action.DryRun)
            {
                result.RolledBack = true;
                return result;
            }

            destination.SaveAs(destinationPath, new SaveAsOptions { OverwriteExistingFile = action.Overwrite });
            result.Saved = true;
            result.SizeBytes = new FileInfo(destinationPath).Length;
            return result;
        }
        finally
        {
            Close(destination);
        }
    }

    private static View3D ResolveView(Document document, string? requested)
    {
        if (!string.IsNullOrWhiteSpace(requested))
        {
            var view = ReadCommandReader.FindView(document, requested.Trim());
            if (view is null) throw new ArgumentException($"View '{requested}' was not found.");
            if (view is not View3D threeDimensional || threeDimensional.IsTemplate)
                throw new ArgumentException($"A rebuild copies the selectable components of a 3D view, and '{view.Name}' is a {view.ViewType} view.");
            return threeDimensional;
        }

        var candidates = new FilteredElementCollector(document).OfClass(typeof(View3D)).Cast<View3D>()
            .Where(view => !view.IsTemplate && !view.IsPerspective)
            .OrderBy(view => RevitValueReader.GetId(view.Id)).ToList();
        if (candidates.Count == 0)
            throw new InvalidOperationException("The document has no non-perspective 3D view to rebuild from.");
        return candidates[0];
    }

    private static List<ElementId> SelectSource(Document document, View3D view, out List<IneligibleElement> excluded)
    {
        var ids = new FilteredElementCollector(document, view.Id).WhereElementIsNotElementType()
            .ToElementIds().OrderBy(RevitValueReader.GetId).ToList();
        var kept = new List<ElementId>(ids.Count);
        excluded = [];
        foreach (var id in ids)
        {
            var element = document.GetElement(id);
            if (element is null) continue;
            var reason = ExclusionReason(element);
            if (reason is null)
            {
                kept.Add(id);
                continue;
            }

            excluded.Add(new IneligibleElement
            {
                Id = RevitValueReader.GetId(id),
                Kind = reason.Value.Kind,
                Reason = reason.Value.Reason
            });
        }

        return kept;
    }

    /// <summary>View helpers that a 3D view returns but that are not model content.</summary>
    private static (string Kind, string Reason)? ExclusionReason(Element element)
    {
        if (element.Category is null)
            return ("no-category", "The element has no category, so it is view infrastructure rather than a component.");
        if (element is View)
            return ("view", "Views are view infrastructure, not components.");
        var category = (BuiltInCategory)RevitValueReader.GetId(element.Category.Id);
        if (category == BuiltInCategory.OST_Cameras) return ("camera", "A camera is a view helper, not a component.");
        if (category == BuiltInCategory.OST_SunStudy) return ("sun-path", "The sun path is a view helper, not a component.");
        if (category == BuiltInCategory.OST_SectionBox) return ("section-box", "A section box is a view helper, not a component.");
        return null;
    }

    private static List<ElementId> OrderForCopy(Document source, List<ElementId> selected, ActionResultData result)
    {
        var ids = new List<ElementId>(selected);
        var known = new HashSet<long>(ids.Select(RevitValueReader.GetId));
        var added = 0;
        foreach (var id in ids.ToList())
        {
            var levelId = source.GetElement(id)?.LevelId;
            if (levelId is null || levelId == ElementId.InvalidElementId) continue;
            if (!known.Add(RevitValueReader.GetId(levelId))) continue;
            ids.Add(levelId);
            added++;
        }

        if (added > 0)
            (result.Notes ??= []).Add($"{added} level(s) were added to the selection because selected elements are hosted on them.");

        // Levels, grids and reference planes are copied first: a hosted element resolves its host while it is copied.
        var datumKeys = new HashSet<long>(ids.Where(id => IsDatum(source.GetElement(id))).Select(RevitValueReader.GetId));
        return ids.Where(id => datumKeys.Contains(RevitValueReader.GetId(id)))
            .Concat(ids.Where(id => !datumKeys.Contains(RevitValueReader.GetId(id))).OrderBy(RevitValueReader.GetId))
            .ToList();
    }

    private static bool IsDatum(Element? element) => element is Level or Grid or ReferencePlane;

    private static List<ElementId> Copy(Document source, Document destination, IReadOnlyList<ElementId> ordered,
        bool removeTemplateLevels, ActionResultData result)
    {
        InTransaction(destination, () => ReserveDestinationLevelNames(source, destination, ordered));

        var isolation = new Isolation();
        var copied = TryCopyGroup(source, destination, ordered, isolation);
        if (copied is null)
        {
            // One copy call is the only way to keep every reference between the copied elements (stairs,
            // railings, curtain panels), so it is tried first. When Revit refuses it, the elements Revit
            // rejects are isolated instead of discarding the whole rebuild.
            result.IsolatedCopy = true;
            (result.Notes ??= []).Add("Revit refused the single copy call, so the rebuild isolated the elements Revit rejects and copied the rest; references between the isolated groups are lost.");
            copied = [];
            IsolateCopy(source, destination, ordered, copied, isolation, result);
        }

        if (isolation.Truncated)
            (result.Notes ??= []).Add($"Revit rejected so many elements that the rebuild stopped isolating them after {MaxIsolationTransactions} attempts; the rejected elements are not in the new model.");

        if (removeTemplateLevels && copied.Count > 0)
        {
            var levels = InTransaction(destination, () => RemoveTemplateLevels(destination, copied));
            result.TemplateLevelsRemoved = levels.Removed;
            result.TemplateLevelsKept = levels.Kept;
        }

        return copied.OrderBy(RevitValueReader.GetId).ToList();
    }

    /// <summary>
    /// Copies one group in a transaction of its own, so Revit processes the failures of that group before
    /// the next one is attempted. A null result means Revit rolled the group back and recorded why.
    /// </summary>
    private static List<ElementId>? TryCopyGroup(Document source, Document destination, IReadOnlyList<ElementId> ids,
        Isolation isolation)
    {
        isolation.Transactions++;
        using var transaction = new Transaction(destination, RebuildTransactionName);
        if (transaction.Start() != TransactionStatus.Started)
            throw new InvalidOperationException("Could not start the rebuild transaction in the new document.");
        var failures = new RebuildFailures();
        transaction.SetFailureHandlingOptions(transaction.GetFailureHandlingOptions()
            .SetFailuresPreprocessor(failures).SetClearAfterRollback(true));
        try
        {
            var copied = CopyElements(source, destination, ids);
            if (transaction.Commit() != TransactionStatus.Committed)
            {
                isolation.Record(failures, null);
                return null;
            }

            isolation.WarningsDismissed += failures.WarningsDismissed;
            return copied.OrderBy(RevitValueReader.GetId).ToList();
        }
        catch (Exception exception)
        {
            if (transaction.GetStatus() == TransactionStatus.Started) transaction.RollBack();
            isolation.Record(failures, exception);
            return null;
        }
    }

    /// <summary>
    /// Halves a group Revit refused until the elements Revit rejects stand alone, so one bad element no
    /// longer costs the whole model. Each accepted half keeps the internal references of that half.
    /// </summary>
    private static void IsolateCopy(Document source, Document destination, IReadOnlyList<ElementId> ids,
        List<ElementId> copied, Isolation isolation, ActionResultData result)
    {
        if (isolation.Transactions >= MaxIsolationTransactions)
        {
            isolation.Truncated = true;
            return;
        }

        if (ids.Count == 1)
        {
            (result.Excluded ??= []).Add(new IneligibleElement
            {
                Id = RevitValueReader.GetId(ids[0]),
                Kind = "copy-failed",
                Reason = isolation.LastReason ?? "Revit refused to copy the element."
            });
            return;
        }

        var middle = ids.Count / 2;
        foreach (var half in new[] { ids.Take(middle).ToList(), ids.Skip(middle).ToList() })
        {
            if (half.Count == 0) continue;
            var group = TryCopyGroup(source, destination, half, isolation);
            if (group is not null) copied.AddRange(group);
            else IsolateCopy(source, destination, half, copied, isolation, result);
        }
    }

    private static void InTransaction(Document document, Action body) =>
        InTransaction(document, () =>
        {
            body();
            return true;
        });

    private static T InTransaction<T>(Document document, Func<T> body)
    {
        using var transaction = new Transaction(document, RebuildTransactionName);
        if (transaction.Start() != TransactionStatus.Started)
            throw new InvalidOperationException("Could not start the rebuild transaction in the new document.");
        var failures = new RebuildFailures();
        transaction.SetFailureHandlingOptions(transaction.GetFailureHandlingOptions()
            .SetFailuresPreprocessor(failures).SetClearAfterRollback(true));
        try
        {
            var value = body();
            if (transaction.Commit() != TransactionStatus.Committed)
                throw new InvalidOperationException(failures.Message ?? "Revit rolled back the rebuild.");
            return value;
        }
        catch
        {
            if (transaction.GetStatus() == TransactionStatus.Started) transaction.RollBack();
            throw;
        }
    }

    private static ICollection<ElementId> CopyElements(Document source, Document destination, IReadOnlyList<ElementId> ids) =>
        ElementTransformUtils.CopyElements(source, ids.ToList(), destination, Transform.Identity, new CopyPasteOptions());

    /// <summary>
    /// Renames the levels a fresh project already has when they carry a name the source also uses, so the
    /// copied elements keep the source elevations instead of landing on the template level.
    /// </summary>
    private static void ReserveDestinationLevelNames(Document source, Document destination, IReadOnlyList<ElementId> ordered)
    {
        var names = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var id in ordered)
            if (source.GetElement(id) is Level level) names.Add(level.Name);
        if (names.Count == 0) return;

        var index = 0;
        foreach (var level in new FilteredElementCollector(destination).OfClass(typeof(Level)).Cast<Level>().ToList())
        {
            if (!names.Contains(level.Name)) continue;
            level.Name = $"{TemplateLevelPrefix}{index++}";
        }
    }

    private static (int Removed, int Kept) RemoveTemplateLevels(Document destination, IEnumerable<ElementId> copied)
    {
        var copiedKeys = new HashSet<long>(copied.Select(RevitValueReader.GetId));
        var removed = 0;
        var kept = 0;
        foreach (var level in new FilteredElementCollector(destination).OfClass(typeof(Level)).Cast<Level>().ToList())
        {
            if (copiedKeys.Contains(RevitValueReader.GetId(level.Id))) continue;
            // A model without a level is not usable, so the last remaining one stays.
            if (new FilteredElementCollector(destination).OfClass(typeof(Level)).GetElementCount() <= 1)
            {
                kept++;
                continue;
            }

            try
            {
                destination.Delete(level.Id);
                removed++;
            }
            catch (Exception exception)
            {
                PluginLog.Warn($"A level the template contributed could not be removed: {exception.Message}");
                kept++;
            }
        }

        return (removed, kept);
    }

    private static void BuildMapping(Document source, Document destination, IReadOnlyList<ElementId> ordered,
        IReadOnlyList<ElementId> newIds, ActionResultData result)
    {
        // A copy call returns the new ids but documents no order, so the pairing is checked against the
        // category and type of both elements instead of being trusted.
        if (newIds.Count != ordered.Count)
        {
            result.IdMappingVerified = false;
            return;
        }

        var mapping = new List<ElementIdPair>();
        var mismatches = 0;
        for (var index = 0; index < ordered.Count; index++)
        {
            if (mapping.Count < MaxMappingEntries)
                mapping.Add(new ElementIdPair
                {
                    Old = RevitValueReader.GetId(ordered[index]),
                    New = RevitValueReader.GetId(newIds[index])
                });
            else result.IdMappingTruncated = true;

            if (!SameShape(source.GetElement(ordered[index]), destination.GetElement(newIds[index]))) mismatches++;
        }

        result.IdMapping = mapping.Count == 0 ? null : mapping;
        result.IdMappingVerified = mismatches == 0;
        if (mismatches > 0) result.MappingMismatches = mismatches;
    }

    private static bool SameShape(Element? left, Element? right)
    {
        if (left is null || right is null) return left is null && right is null;
        return string.Equals(CategoryName(left), CategoryName(right), StringComparison.Ordinal)
            && string.Equals(TypeName(left), TypeName(right), StringComparison.Ordinal);
    }

    private static string CategoryName(Element element) => element.Category?.Name ?? string.Empty;

    private static string TypeName(Element element) =>
        element.GetTypeId().ToElement<ElementType>(element.Document)?.Name ?? string.Empty;

    private static List<ElementCategoryCount> CountCategories(Document document, IReadOnlyCollection<ElementId> ids)
    {
        var counts = new Dictionary<(string Name, string BuiltIn), int>();
        foreach (var id in ids)
        {
            if (document.GetElement(id)?.Category is not { } category) continue;
            var key = (category.Name, ((BuiltInCategory)RevitValueReader.GetId(category.Id)).ToString());
            counts[key] = counts.TryGetValue(key, out var count) ? count + 1 : 1;
        }

        return counts
            .Select(entry => new ElementCategoryCount
            {
                Category = entry.Key.Name,
                BuiltInCategory = entry.Key.BuiltIn,
                Count = entry.Value
            })
            .OrderByDescending(entry => entry.Count)
            .ThenBy(entry => entry.Category, StringComparer.Ordinal)
            .ToList();
    }

    private static string FirstLine(string value)
    {
        var index = value.IndexOfAny(['\r', '\n']);
        return index < 0 ? value : value[..index];
    }

    private static void EnsureOpenableView(Document destination, ActionResultData result)
    {
        // Revit refuses to open a model that has no view it can activate, so the rebuild has to leave one behind.
        var views = new FilteredElementCollector(destination).OfClass(typeof(View)).Cast<View>()
            .Where(view => !view.IsTemplate)
            .ToList();
        var summary = string.Join(", ", views.Take(12).Select(view => $"{view.ViewType} '{view.Name}'"));
        (result.Notes ??= []).Add($"the new model carries {views.Count} view(s) before it is saved: {summary}");

        if (views.Any(view => view is View3D)) return;

        var family = new FilteredElementCollector(destination).OfClass(typeof(ViewFamilyType)).Cast<ViewFamilyType>()
            .FirstOrDefault(type => type.ViewFamily == ViewFamily.ThreeDimensional);
        if (family is null)
        {
            (result.Notes ??= []).Add("the new model has no three-dimensional view family, so no view could be added.");
            return;
        }

        InTransaction(destination, () =>
        {
            var created = View3D.CreateIsometric(destination, family.Id);
            (result.Notes ??= []).Add($"the new model had no three-dimensional view, so '{created.Name}' was added so that the model opens with a view.");
            return true;
        });
    }

    private static void Close(Document? document)
    {
        if (document is null) return;
        try
        {
            if (document.IsValidObject) document.Close(false);
        }
        catch (Exception exception)
        {
            PluginLog.Warn($"The rebuilt document could not be closed: {exception.Message}");
        }
    }

    /// <summary>What the isolated copy learned about the elements Revit refuses.</summary>
    private sealed class Isolation
    {
        public int Transactions { get; set; }
        public int WarningsDismissed { get; set; }
        public bool Truncated { get; set; }
        public string? LastReason { get; private set; }

        public void Record(RebuildFailures failures, Exception? exception)
        {
            var message = failures.Message ?? exception?.Message;
            if (!string.IsNullOrWhiteSpace(message)) LastReason = FirstLine(message);
        }
    }

    /// <summary>
    /// A rebuild copies the whole model, so a warning about the copy itself must not stop it. An error
    /// rolls the group back, which lets the caller isolate the elements Revit rejects.
    /// </summary>
    private sealed class RebuildFailures : IFailuresPreprocessor
    {
        private readonly List<string> _errors = [];

        public int WarningsDismissed { get; private set; }
        public string? Message => _errors.Count == 0 ? null : string.Join("; ", _errors);

        public FailureProcessingResult PreprocessFailures(FailuresAccessor failuresAccessor)
        {
            var rollBack = false;
            foreach (var failure in failuresAccessor.GetFailureMessages())
            {
                var severity = failure.GetSeverity();
                if (severity == FailureSeverity.None) continue;
                if (severity == FailureSeverity.Warning)
                {
                    failuresAccessor.DeleteWarning(failure);
                    WarningsDismissed++;
                    continue;
                }

                _errors.Add(failure.GetDescriptionText());
                rollBack = true;
            }

            return rollBack ? FailureProcessingResult.ProceedWithRollBack : FailureProcessingResult.Continue;
        }
    }
}
