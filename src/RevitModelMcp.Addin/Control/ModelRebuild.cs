using System.Diagnostics;
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
    private const int MaxCopies = 50;
    private const int MaxMappingEntries = 5_000;
    private const int MaxIsolationTransactions = 400;
    private const string RebuildTransactionName = "revit_rebuild_model_ids";
    private const string TemplateLevelPrefix = "__rebuild_";
    private const string TemplateTypeSuffix = " (模板)";
    private const string SeedLevelPrefix = "__rebuild_seed_";

    internal static ActionResultData Rebuild(Document source, ActionJobContract action)
    {
        var destinationPath = Path.GetFullPath(action.DestinationPath!);
        var templatePath = string.IsNullOrWhiteSpace(action.TemplatePath) ? null : Path.GetFullPath(action.TemplatePath);
        if (templatePath is not null && !File.Exists(templatePath))
            throw new FileNotFoundException($"The template file was not found: {templatePath}.", templatePath);
        var copies = action.DryRun ? 1 : Math.Clamp(action.Copies, 1, MaxCopies);
        var paths = DestinationPaths(destinationPath, copies);
        foreach (var path in paths)
        {
            if (File.Exists(path) && !action.Overwrite)
                throw new IOException($"The destination file already exists: {path}. Pass overwrite=true to replace it.");
            var pathDirectory = Path.GetDirectoryName(path);
            if (!string.IsNullOrEmpty(pathDirectory)) Directory.CreateDirectory(pathDirectory);
        }

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
            Count = 0,
            Copies = copies > 1 ? copies : null
        };

        var ordered = OrderForCopy(source, selected, result);
        result.SourceElementCount = ordered.Count;
        result.DatumCount = ordered.Count(id => IsDatum(source.GetElement(id)));
        result.SourceCategoryCounts = CountCategories(source, ordered);

        Document? destination = null;
        var phases = new PhaseLog();
        try
        {
            destination = templatePath is null
                ? source.Application.NewProjectDocument(UnitSystem.Metric)
                : source.Application.NewProjectDocument(templatePath);
            result.TemplatePath = templatePath ?? "the default metric template";
            phases.Mark("new-project");

            var answerDuplicates = !string.Equals(action.DuplicateNames, "rename", StringComparison.OrdinalIgnoreCase);
            result.DuplicateNames = answerDuplicates ? "override" : "rename";

            var copyResults = new List<RebuildCopyResult>(copies);
            for (var index = 0; index < copies; index++)
            {
                var first = index == 0;
                var copyPhases = new PhaseLog();
                var scratch = new ActionResultData { DestinationPath = paths[index] };

                var seed = first ? CreateSeed(destination, action.Seed) : [];
                copyPhases.Mark("seed");
                if (first && seed.Count > 0)
                {
                    result.Seed = seed.Count;
                    (result.Notes ??= []).Add($"{seed.Count} temporary level(s) were added to the new model before the copy so this copy's ids start after them, and were removed again afterwards.");
                }

                var newIds = Copy(source, destination, ordered, action.RemoveTemplateLevels && first, seed,
                    answerDuplicates && first, scratch, copyPhases, first, out var renamedTypes);
                copyPhases.Mark("copy");
                if (newIds.Count == 0)
                    throw new InvalidOperationException("Revit copied no element into the new model; nothing was written.");

                BuildMapping(source, destination, ordered, newIds, scratch);
                EnsureOpenableView(destination, scratch);
                copyPhases.Mark("view");

                if (first)
                {
                    result.CopiedCategoryCounts = CountCategories(destination, newIds);
                    result.IdMapping = scratch.IdMapping;
                    result.IdMappingVerified = scratch.IdMappingVerified;
                    result.IdMappingTruncated = scratch.IdMappingTruncated;
                    result.MappingMismatches = scratch.MappingMismatches;
                    result.AutoAnsweredDialogs = scratch.AutoAnsweredDialogs;
                    result.IsolatedCopy = scratch.IsolatedCopy;
                    result.TemplateLevelsRemoved = scratch.TemplateLevelsRemoved;
                    result.TemplateLevelsKept = scratch.TemplateLevelsKept;
                    result.Excluded = scratch.Excluded ?? result.Excluded;
                    foreach (var note in scratch.Notes ?? []) (result.Notes ??= []).Add(note);
                }
                else
                {
                    foreach (var note in scratch.Notes ?? [])
                        (result.Notes ??= []).Add($"{Path.GetFileName(paths[index])}: {note}");
                }

                if (action.DryRun)
                {
                    result.RolledBack = true;
                    (result.Notes ??= []).Add($"phase timings: {phases.Summary()}.");
                    return result;
                }

                if (first && renamedTypes.Count > 0)
                {
                    var leftovers = RemoveRenamedTemplateElements(destination, renamedTypes);
                    if (leftovers.Removed > 0 || leftovers.Kept > 0)
                        (result.Notes ??= []).Add($"{leftovers.Removed} of the renamed template element(s) were removed again, and {leftovers.Kept} stayed because Revit still uses them.");
                }
                copyPhases.Mark("cleanup");

                destination.SaveAs(paths[index], new SaveAsOptions { OverwriteExistingFile = action.Overwrite });
                copyPhases.Mark("save");

                copyResults.Add(new RebuildCopyResult
                {
                    DestinationPath = paths[index],
                    Count = newIds.Count,
                    NewIdMin = newIds.Min(RevitValueReader.GetId),
                    NewIdMax = newIds.Max(RevitValueReader.GetId),
                    SizeBytes = new FileInfo(paths[index]).Length,
                    IdMappingVerified = scratch.IdMappingVerified ?? false,
                    MappingMismatches = scratch.MappingMismatches,
                    IdMapping = scratch.IdMapping
                });
                PluginLog.Info($"Rebuild copy {index + 1}/{copies} '{Path.GetFileName(paths[index])}': {copyPhases.Summary()}.");

                if (index < copies - 1)
                {
                    // The next copy needs the template's own content again, and Revit does not hand the ids of
                    // deleted elements out twice, so the copy that follows lands in a block of its own.
                    var freed = DeleteCopied(destination, newIds);
                    copyPhases.Mark("delete-copy");
                    PluginLog.Info($"Rebuild copy {index + 1} removed again: {freed.Deleted} element(s) deleted, {freed.Left} stayed.");
                    if (freed.Left > 0)
                        (result.Notes ??= []).Add($"{freed.Left} element(s) of copy {index + 1} could not be removed before the next copy, so they stay in the copies that follow.");
                }
            }

            result.Count = copyResults[0].Count;
            result.SizeBytes = copyResults[0].SizeBytes;
            result.NewIdMin = copyResults.Min(copy => copy.NewIdMin);
            result.NewIdMax = copyResults.Max(copy => copy.NewIdMax);
            result.Saved = true;
            result.IdMappingVerified = copyResults.All(copy => copy.IdMappingVerified);
            if (copies > 1)
            {
                result.CopyResults = copyResults;
                (result.Notes ??= []).Add($"{copies} copies were written from one new model; each copy's ids start after the copy before it, and its own mapping sits in copyResults.");
            }

            (result.Notes ??= []).Add($"phase timings: {phases.Summary()}.");
            return result;
        }
        finally
        {
            Close(destination);
            phases.Mark("close");
            PluginLog.Info($"Rebuild phases: {phases.Summary()}.");
        }
    }

    /// <summary>
    /// The file each copy is written to: the requested path with "{n}" replaced by the copy number, or the copy
    /// number appended before the extension when the path carries no placeholder.
    /// </summary>
    private static List<string> DestinationPaths(string destinationPath, int copies)
    {
        if (copies == 1) return [destinationPath];
        var directory = Path.GetDirectoryName(destinationPath) ?? string.Empty;
        var name = Path.GetFileNameWithoutExtension(destinationPath);
        var extension = Path.GetExtension(destinationPath);
        var paths = new List<string>(copies);
        for (var index = 1; index <= copies; index++)
            paths.Add(destinationPath.Contains("{n}")
                ? destinationPath.Replace("{n}", index.ToString())
                : Path.Combine(directory, $"{name}-{index}{extension}"));
        return paths;
    }

    /// <summary>
    /// Removes the elements of one copy so the next copy starts from the template's own content again. Revit
    /// keeps handing out higher ids in a document, so the copy that follows lands in a block of its own.
    /// </summary>
    private static (int Deleted, int Left) DeleteCopied(Document destination, IReadOnlyList<ElementId> ids)
    {
        if (ids.Count == 0) return (0, 0);
        var deleted = 0;
        try
        {
            deleted = InTransaction(destination, () => destination.Delete(ids.ToList()).Count);
        }
        catch (Exception exception)
        {
            // Revit refuses the whole call when one element cannot go, so the rest is removed one by one.
            PluginLog.Warn($"A copy could not be removed in one call ({FirstLine(exception.Message)}); removing it element by element.");
            foreach (var id in ids)
            {
                try
                {
                    deleted += InTransaction(destination, () => destination.Delete(id).Count);
                }
                catch (Exception inner)
                {
                    PluginLog.Warn($"A copied element could not be removed: {FirstLine(inner.Message)}");
                }
            }
        }

        var left = ids.Count(id => destination.GetElement(id) is not null);
        return (deleted, left);
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
        bool removeTemplateLevels, IReadOnlyList<ElementId> seed, bool answerDuplicates, ActionResultData result,
        PhaseLog phases, bool first, out List<ElementId> renamedTypes)
    {
        renamedTypes = [];
        var reserved = (Renamed: new List<ElementId>(), Removed: 0);
        if (first)
        {
            // Only the first copy meets the template's own content; every later copy finds the model the copy
            // before it left behind, where the names are already the source's own.
            InTransaction(destination, () =>
            {
                ReserveDestinationLevelNames(source, destination, ordered);
                if (!answerDuplicates) reserved = ReserveDestinationNames(source, destination);
            });
        }
        phases.Mark("reserve");
        renamedTypes = reserved.Renamed;
        if (renamedTypes.Count > 0 || reserved.Removed > 0)
            (result.Notes ??= []).Add($"{renamedTypes.Count} element(s) the new project's template contributed were renamed and {reserved.Removed} were removed before the copy, so Revit would not ask how to resolve a duplicate name.");

        var duplicates = new ReportDuplicateTypeNames(source, destination);
        var isolation = new Isolation { Duplicates = duplicates };
        var answeredBefore = DialogOverride.Answered;
        List<ElementId>? copied;
        // Answering the duplicate-name question keeps the source model's own types, which is why the fast path
        // needs neither the rename above nor the cleanup that removes the renamed elements again.
        using (IDisposable? guard = answerDuplicates ? DialogOverride.Scope() : null)
        {
            copied = TryCopyGroup(source, destination, ordered, isolation, answerDuplicates);
            phases.Mark("copy-call");
            if (copied is null)
            {
                // One copy call is the only way to keep every reference between the copied elements (stairs,
                // railings, curtain panels), so it is tried first. When Revit refuses it, the elements Revit
                // rejects are isolated instead of discarding the whole rebuild.
                result.IsolatedCopy = true;
                (result.Notes ??= []).Add("Revit refused the single copy call, so the rebuild isolated the elements Revit rejects and copied the rest; references between the isolated groups are lost.");
                copied = [];
                IsolateCopy(source, destination, ordered, copied, isolation, result, answerDuplicates);
                phases.Mark("isolate");
            }
        }

        var answered = DialogOverride.Answered - answeredBefore;
        if (answered > 0)
        {
            result.AutoAnsweredDialogs = answered;
            (result.Notes ??= []).Add($"{answered} question(s) Revit would have waited on were answered with OK, so the copy kept the source model's own types.");
        }

        if (duplicates.Count > 0)
            (result.Notes ??= []).Add($"Revit reported {duplicates.Count} duplicate type name(s) the rename did not cover; the copy used the types the new project already had for them.");

        if (isolation.Truncated)
            (result.Notes ??= []).Add($"Revit rejected so many elements that the rebuild stopped isolating them after {MaxIsolationTransactions} attempts; the rejected elements are not in the new model.");

        RemoveSeed(destination, seed);
        phases.Mark("remove-seed");

        if (removeTemplateLevels && copied.Count > 0)
        {
            var levels = InTransaction(destination, () => RemoveTemplateLevels(destination, copied));
            result.TemplateLevelsRemoved = levels.Removed;
            result.TemplateLevelsKept = levels.Kept;
        }
        phases.Mark("remove-template-levels");

        return copied.OrderBy(RevitValueReader.GetId).ToList();
    }

    /// <summary>
    /// Adds the requested number of temporary levels to the new model before the copy. Revit hands the copied
    /// elements the ids that follow the ids the new model already holds, so two rebuilds of the same source
    /// otherwise produce the same ids; the seed moves each copy into a block of its own.
    /// </summary>
    private static List<ElementId> CreateSeed(Document destination, int seed)
    {
        if (seed <= 0) return [];
        var ids = new List<ElementId>(seed);
        InTransaction(destination, () =>
        {
            for (var index = 0; index < seed; index++)
            {
                var level = Level.Create(destination, SeedElevation(index));
                try
                {
                    level.Name = $"{SeedLevelPrefix}{index}";
                }
                catch (Exception exception)
                {
                    PluginLog.Warn($"A seed level could not be named: {exception.Message}");
                }
                ids.Add(level.Id);
            }
        });
        return ids;
    }

    /// <summary>Far below the model, so a seed level never collides with a real one; the seed is removed again anyway.</summary>
    private static double SeedElevation(int index) => -1_000_000d - index;

    private static void RemoveSeed(Document destination, IReadOnlyList<ElementId> seed)
    {
        if (seed.Count == 0) return;
        InTransaction(destination, () =>
        {
            foreach (var id in seed)
            {
                try
                {
                    destination.Delete(id);
                }
                catch (Exception exception)
                {
                    PluginLog.Warn($"A seed level could not be removed: {exception.Message}");
                }
            }
        });
    }

    /// <summary>
    /// Copies one group in a transaction of its own, so Revit processes the failures of that group before
    /// the next one is attempted. A null result means Revit rolled the group back and recorded why.
    /// </summary>
    private static List<ElementId>? TryCopyGroup(Document source, Document destination, IReadOnlyList<ElementId> ids,
        Isolation isolation, bool answerDuplicates)
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
            var copied = CopyElements(source, destination, ids, isolation, answerDuplicates);
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
        List<ElementId> copied, Isolation isolation, ActionResultData result, bool answerDuplicates)
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
            var group = TryCopyGroup(source, destination, half, isolation, answerDuplicates);
            if (group is not null) copied.AddRange(group);
            else IsolateCopy(source, destination, half, copied, isolation, result, answerDuplicates);
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

    private static ICollection<ElementId> CopyElements(Document source, Document destination, IReadOnlyList<ElementId> ids,
        Isolation isolation, bool answerDuplicates)
    {
        var options = new CopyPasteOptions();
        if (!answerDuplicates)
        {
            // Without an answer the handler is what keeps the copy moving; with the override the handler must
            // stay off, because Revit only asks the question when no handler is set, and the answer is what
            // keeps the source model's own types.
            options.SetDuplicateTypeNamesHandler(isolation.Duplicates);
        }

        return ElementTransformUtils.CopyElements(source, ids.ToList(), destination, Transform.Identity, options);
    }

    /// <summary>
    /// Revit asks the user how to resolve a duplicate type name while it pastes, and that question blocks an
    /// unattended run. The rebuild renames every type the destination already has before it copies, so this
    /// handler only reports what slipped through a rule the rename did not anticipate, and it continues with
    /// the destination types rather than waiting for an answer.
    /// </summary>
    private sealed class ReportDuplicateTypeNames : IDuplicateTypeNamesHandler
    {
        private readonly Document _source;
        private readonly Document _destination;

        internal ReportDuplicateTypeNames(Document source, Document destination)
        {
            _source = source;
            _destination = destination;
        }

        public int Count { get; private set; }

        public DuplicateTypeAction OnDuplicateTypeNamesFound(DuplicateTypeNamesHandlerArgs args)
        {
            try
            {
                var names = new List<string>();
                foreach (var id in args.GetTypeIds())
                {
                    Count++;
                    names.Add($"{Describe(_source, id)} -> {Describe(_destination, id)}");
                }

                PluginLog.Warn($"Duplicate type names in the rebuild copy: {string.Join("; ", names)}");
            }
            catch (Exception exception)
            {
                PluginLog.Warn($"Duplicate type names could not be reported: {exception.Message}");
            }

            return DuplicateTypeAction.UseDestinationTypes;
        }

        private static string Describe(Document document, ElementId id)
        {
            if (document.GetElement(id) is ElementType type)
                return $"{type.Category?.Name}/{type.Name}({RevitValueReader.GetId(id)})";
            var element = document.GetElement(id);
            return element is null
                ? $"{RevitValueReader.GetId(id)} (missing)"
                : $"{element.GetType().Name}/{element.Name}({RevitValueReader.GetId(id)})";
        }
    }

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

    /// <summary>
    /// Renames the destination elements whose name the source can bring in, so Revit never asks the user how
    /// to resolve a duplicate name while it pastes — that question blocks an unattended run. The question
    /// covers more than element types: Revit reported source materials and a source line pattern by name, so
    /// every named kind the paste can carry is reserved the same way.
    /// </summary>
    private static (List<ElementId> Renamed, int Removed) ReserveDestinationNames(Document source, Document destination)
    {
        var renamed = new List<ElementId>();
        var removed = 0;
        var names = SourceNames(source);
        var failures = new List<string>();

        foreach (var type in new FilteredElementCollector(destination).WhereElementIsElementType()
                     .Cast<ElementType>().ToList())
            if (type.Name is { Length: > 0 } name && names.Contains(name))
                Reserve(type, destination, renamed, ref removed, failures);

        foreach (var material in new FilteredElementCollector(destination).OfClass(typeof(Material))
                     .Cast<Material>().ToList())
            if (material.Name is { Length: > 0 } name && names.Contains(name))
                Reserve(material, destination, renamed, ref removed, failures);

        foreach (var pattern in new FilteredElementCollector(destination)
                     .WherePasses(new ElementMulticlassFilter([typeof(LinePatternElement), typeof(FillPatternElement)]))
                     .Cast<Element>().ToList())
            if (pattern.Name is { Length: > 0 } name && names.Contains(name))
                Reserve(pattern, destination, renamed, ref removed, failures);

        // One line per run: every element that kept its name is expected on some templates, and logging each
        // one used to fill the log with thousands of lines a day.
        if (failures.Count > 0)
            PluginLog.Warn($"{failures.Count} template element(s) kept a name the source also uses: {failures[0]}");

        return (renamed, removed);
    }

    /// <summary>Every name the source document can hand to the paste.</summary>
    private static HashSet<string> SourceNames(Document source)
    {
        var names = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var element in new FilteredElementCollector(source).WhereElementIsElementType().Cast<Element>())
            if (element.Name is { Length: > 0 } name) names.Add(name);

        foreach (var element in new FilteredElementCollector(source)
                     .WherePasses(new ElementMulticlassFilter([typeof(Material), typeof(LinePatternElement), typeof(FillPatternElement)]))
                     .Cast<Element>())
            if (element.Name is { Length: > 0 } name) names.Add(name);

        return names;
    }

    private static void Reserve(Element element, Document destination, List<ElementId> renamed, ref int removed,
        List<string> failures)
    {
        if (TryRename(element, element.Name, failures)) renamed.Add(element.Id);
        else
        {
            // An element Revit refuses to rename keeps a name the source can collide with, and removing it
            // takes that name away just as well: the copy brings the source's own element back in.
            try
            {
                if (destination.Delete(element.Id).Count > 0) removed++;
            }
            catch (Exception exception)
            {
                failures.Add($"neither renamed nor removed ({exception.GetType().Name}: {FirstLine(exception.Message)})");
            }
        }
    }

    private static bool TryRename(Element element, string original, List<string> failures)
    {
        try
        {
            element.Name = $"{original}{TemplateTypeSuffix}";
            return true;
        }
        catch (Exception first)
        {
            try
            {
                element.Name = $"{original}{TemplateTypeSuffix} {RevitValueReader.GetId(element.Id)}";
                return true;
            }
            catch (Exception second)
            {
                failures.Add($"could not be renamed ({first.GetType().Name}: {FirstLine(first.Message)}; {second.GetType().Name}: {FirstLine(second.Message)})");
                return false;
            }
        }
    }

    /// <summary>
    /// Removes the renamed template elements once the copy has brought the source names in, so the new model does
    /// not carry unused leftovers. An element Revit still needs refuses the delete and stays. The transaction is
    /// best effort: when Revit rolls it back the model simply keeps every renamed element.
    /// </summary>
    private static (int Removed, int Kept) RemoveRenamedTemplateElements(Document destination, IReadOnlyList<ElementId> renamed)
    {
        if (renamed.Count == 0) return (0, 0);
        using var transaction = new Transaction(destination, RebuildTransactionName);
        if (transaction.Start() != TransactionStatus.Started) return (0, renamed.Count);
        var failures = new RebuildFailures();
        transaction.SetFailureHandlingOptions(transaction.GetFailureHandlingOptions()
            .SetFailuresPreprocessor(failures).SetClearAfterRollback(true));
        var removed = 0;
        var deleteFailures = new List<string>();
        foreach (var id in renamed)
        {
            try
            {
                if (destination.Delete(id).Count > 0) removed++;
            }
            catch (Exception exception)
            {
                deleteFailures.Add($"{exception.GetType().Name}: {FirstLine(exception.Message)}");
            }
        }

        if (deleteFailures.Count > 0)
            PluginLog.Warn($"{deleteFailures.Count} of {renamed.Count} renamed template element(s) could not be removed: {deleteFailures[0]}");
        if (transaction.Commit() != TransactionStatus.Committed) return (0, renamed.Count);
        return (removed, renamed.Count - removed);
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
        public ReportDuplicateTypeNames Duplicates { get; set; } = null!;
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

    /// <summary>
    /// Records how long each step of a rebuild took, so a slow copy can be attributed to the step that
    /// caused it. The marks are reported in the result and in the plugin log.
    /// </summary>
    private sealed class PhaseLog
    {
        private readonly Stopwatch _watch = Stopwatch.StartNew();
        private readonly List<string> _phases = [];
        private long _last;

        public void Mark(string name)
        {
            var elapsed = _watch.ElapsedMilliseconds;
            _phases.Add($"{name}={elapsed - _last}");
            _last = elapsed;
        }

        public string Summary() => $"{string.Join(" ", _phases)} total={_watch.ElapsedMilliseconds}";
    }
}
