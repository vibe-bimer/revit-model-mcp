using System.Runtime.Serialization;
using RevitModelMcp.Core.Models;

namespace RevitModelMcp.Core.Control;

public static class ActionJobParser
{
    public static bool IsAction(string command) => command is
        "select" or "show" or "isolate" or "move" or "place-family" or "create-wall" or "create-floor" or "set-phase" or "merge-phases" or "set-parameter" or "delete" or "reset-element-ids" or "rebuild-model-ids" or "batch";

    public static ControlJobParseResult Parse(string command, ControlJobContract job)
    {
        try
        {
            var action = new ActionJobContract
            {
                DryRun = job.DryRun ?? false,
                ElementIds = (job.ElementIds ?? []).Distinct().ToList(),
                Select = job.Select ?? true,
                Reset = job.Reset ?? false,
                DxMm = job.DxMm ?? 0,
                DyMm = job.DyMm ?? 0,
                DzMm = job.DzMm ?? 0,
                Family = job.Family,
                TypeName = job.TypeName,
                Level = job.Level,
                XMm = job.XMm ?? 0,
                YMm = job.YMm ?? 0,
                RotationDeg = job.RotationDeg ?? 0,
                StartMm = job.StartMm ?? [],
                EndMm = job.EndMm ?? [],
                WallType = job.WallType,
                HeightMm = job.HeightMm ?? 3000,
                PointsMm = job.PointsMm ?? [],
                FloorType = job.FloorType,
                CreatedPhase = job.CreatedPhase,
                DemolishedPhase = job.DemolishedPhase,
                SourcePhase = job.SourcePhase,
                TargetPhase = job.TargetPhase,
                ElementId = job.ActionElementId ?? 0,
                Parameter = job.Parameter,
                Value = job.Value,
                View = job.View,
                DestinationPath = job.DestinationPath,
                Overwrite = job.Overwrite ?? false,
                TemplatePath = job.TemplatePath,
                RemoveTemplateLevels = job.RemoveTemplateLevels ?? true,
                Seed = job.Seed ?? 0,
                Copies = job.Copies ?? 1,
                DuplicateNames = job.DuplicateNames ?? "override"
            };
            if (command == "batch")
            {
                Require(job.Steps is { Count: > 0 and <= 50 }, "batch requires 1 to 50 steps.");
                foreach (var step in job.Steps!)
                {
                    var stepCommand = step?.Command ?? string.Empty;
                    Require(IsAction(stepCommand) && stepCommand is not ("show" or "batch" or "merge-phases" or "rebuild-model-ids"),
                        "Batch steps must be move, place-family, create-wall, create-floor, set-phase, set-parameter, delete, select or isolate.");
                    var parsed = Parse(stepCommand, step!);
                    Require(parsed.Error is null, $"Step {action.Steps.Count}: {parsed.Error}");
                    action.Steps.Add(parsed);
                }
            }
            if (command is "select" or "show" or "isolate" or "move" or "delete" or "set-phase" or "reset-element-ids")
            {
                Require(job.ElementIds is not null, "elementIds is required.");
                Require(action.ElementIds.All(elementId => elementId > 0), "Element IDs must be positive.");
                Require(action.ElementIds.Count > 0 || command == "select" || command == "isolate" && action.Reset,
                    "elementIds must not be empty.");
            }
            if (command == "move")
            {
                Require(job.DxMm.HasValue && job.DyMm.HasValue, "dxMm and dyMm are required.");
                Require(Finite(action.DxMm, action.DyMm, action.DzMm), "Move offsets must be finite millimetres.");
            }
            if (command == "place-family")
            {
                Require(!string.IsNullOrWhiteSpace(action.Family), "family is required.");
                var familyParts = action.Family!.Split([':'], 2);
                action.Family = familyParts[0].Trim();
                Require(action.Family.Length > 0, "family is required.");
                if (familyParts.Length == 2)
                {
                    var embeddedType = familyParts[1].Trim();
                    Require(embeddedType.Length > 0, "The type in Family: Type must not be blank.");
                    Require(action.TypeName is null || string.Equals(action.TypeName.Trim(), embeddedType, StringComparison.OrdinalIgnoreCase),
                        "typeName conflicts with the type in Family: Type.");
                    action.TypeName = embeddedType;
                }
                else action.TypeName = action.TypeName?.Trim();
                Require(job.XMm.HasValue && job.YMm.HasValue, "xMm and yMm are required.");
                Require(Finite(action.XMm, action.YMm, action.RotationDeg), "Placement coordinates and rotation must be finite.");
                Require(action.TypeName is null || !string.IsNullOrWhiteSpace(action.TypeName), "typeName must not be blank.");
            }
            if (command is "place-family" or "create-wall" or "create-floor")
                Require(!string.IsNullOrWhiteSpace(action.Level), "level is required.");
            if (command == "create-wall")
            {
                Require(action.StartMm.Count == 2 && action.EndMm.Count == 2, "startMm and endMm must each contain two coordinates.");
                Require(Finite(action.StartMm.Concat(action.EndMm).ToArray()), "Wall coordinates must be finite millimetres.");
                Require(!action.StartMm.SequenceEqual(action.EndMm), "Wall endpoints must differ.");
                Require(Finite(action.HeightMm) && action.HeightMm > 0, "heightMm must be finite and positive.");
                Require(action.WallType is null || !string.IsNullOrWhiteSpace(action.WallType), "wallType must not be blank.");
            }
            if (command == "create-floor")
            {
                Require(action.PointsMm.Count >= 3, "pointsMm must contain at least three boundary points.");
                Require(action.PointsMm.All(point => point.Count == 2), "Each floor boundary point must contain two coordinates.");
                Require(Finite(action.PointsMm.SelectMany(point => point).ToArray()), "Floor boundary coordinates must be finite millimetres.");
                for (var index = 0; index < action.PointsMm.Count; index++)
                    Require(!action.PointsMm[index].SequenceEqual(action.PointsMm[(index + 1) % action.PointsMm.Count]),
                        "Floor boundary points must not repeat consecutively.");
                Require(action.FloorType is null || !string.IsNullOrWhiteSpace(action.FloorType), "floorType must not be blank.");
            }
            if (command == "set-phase")
            {
                Require(action.CreatedPhase is not null || action.DemolishedPhase is not null,
                    "createdPhase or demolishedPhase is required.");
                foreach (var (label, value) in new[] { ("createdPhase", action.CreatedPhase), ("demolishedPhase", action.DemolishedPhase) })
                    Require(value is null || value.Length == 0 || value.Trim().Length > 0,
                        $"{label} must be a phase name, an empty string to clear, or null.");
            }
            if (command == "merge-phases")
            {
                Require(!string.IsNullOrWhiteSpace(action.SourcePhase), "sourcePhase is required.");
                Require(!string.IsNullOrWhiteSpace(action.TargetPhase), "targetPhase is required.");
                Require(!string.Equals(action.SourcePhase!.Trim(), action.TargetPhase!.Trim(), StringComparison.OrdinalIgnoreCase),
                    "sourcePhase and targetPhase must differ.");
            }
            if (command == "set-parameter")
            {
                Require(action.ElementId > 0, "elementId must be positive.");
                Require(!string.IsNullOrWhiteSpace(action.Parameter), "parameter is required.");
                Require(action.Value is not null, "value is required (an empty string is allowed).");
            }
            if (command == "rebuild-model-ids")
            {
                Require(!string.IsNullOrWhiteSpace(action.DestinationPath), "destinationPath is required.");
                action.DestinationPath = action.DestinationPath!.Trim();
                Require(action.DestinationPath.EndsWith(".rvt", StringComparison.OrdinalIgnoreCase),
                    "destinationPath must name a .rvt file.");
                Require(action.DestinationPath.Length > 4, "destinationPath must not be a bare .rvt file name.");
                if (action.TemplatePath is not null)
                {
                    Require(!string.IsNullOrWhiteSpace(action.TemplatePath), "templatePath must not be blank.");
                    action.TemplatePath = action.TemplatePath.Trim();
                    Require(action.TemplatePath.EndsWith(".rte", StringComparison.OrdinalIgnoreCase)
                        || action.TemplatePath.EndsWith(".rvt", StringComparison.OrdinalIgnoreCase),
                        "templatePath must name a .rte or .rvt file.");
                }
                Require(action.Seed is >= 0 and <= 20000, "seed must be between 0 and 20000.");
                action.DuplicateNames = action.DuplicateNames.Trim().ToLowerInvariant();
                Require(action.DuplicateNames is "override" or "rename",
                    "duplicateNames must be 'override' or 'rename'.");
                Require(action.Copies is >= 1 and <= 50, "copies must be between 1 and 50.");
                Require(!(action.DryRun && action.Copies > 1), "copies is only available without dryRun.");
            }
            var result = ControlJobParseResult.Create(ControlJobKind.Action, command);
            result.Action = action;
            return result;
        }
        catch (ArgumentException exception)
        {
            return ControlJobParseResult.Invalid(command, exception.Message);
        }
    }

    public static List<string> ClosestFamilyNames(string requested, IEnumerable<string> candidates) =>
        candidates.Distinct(StringComparer.OrdinalIgnoreCase)
            .Select(candidate => new
            {
                Name = candidate,
                Contains = candidate.IndexOf(requested, StringComparison.OrdinalIgnoreCase) >= 0,
                Similarity = 1.0 - (double)NameDistance(requested, candidate) / Math.Max(1, Math.Max(requested.Length, candidate.Length))
            })
            .Where(candidate => candidate.Contains || candidate.Similarity >= 0.5)
            .OrderByDescending(candidate => candidate.Contains)
            .ThenByDescending(candidate => candidate.Similarity)
            .ThenBy(candidate => candidate.Name, StringComparer.OrdinalIgnoreCase)
            .Take(5).Select(candidate => candidate.Name).ToList();

    private static int NameDistance(string requested, string candidate)
    {
        var previous = Enumerable.Range(0, candidate.Length + 1).ToArray();
        for (var requestedIndex = 1; requestedIndex <= requested.Length; requestedIndex++)
        {
            var current = new int[candidate.Length + 1];
            current[0] = requestedIndex;
            for (var candidateIndex = 1; candidateIndex <= candidate.Length; candidateIndex++)
            {
                var cost = char.ToUpperInvariant(requested[requestedIndex - 1]) == char.ToUpperInvariant(candidate[candidateIndex - 1]) ? 0 : 1;
                current[candidateIndex] = Math.Min(Math.Min(current[candidateIndex - 1] + 1, previous[candidateIndex] + 1), previous[candidateIndex - 1] + cost);
            }
            previous = current;
        }
        return previous[candidate.Length];
    }

    private static bool Finite(params double[] values) => values.All(value => !double.IsNaN(value) && !double.IsInfinity(value));

    private static void Require(bool condition, string message)
    {
        if (!condition) throw new ArgumentException(message);
    }
}

public sealed class ActionJobContract
{
    public bool DryRun { get; set; }
    public List<ControlJobParseResult> Steps { get; set; } = [];
    public List<long> ElementIds { get; set; } = [];
    public bool Select { get; set; }
    public bool Reset { get; set; }
    public double DxMm { get; set; }
    public double DyMm { get; set; }
    public double DzMm { get; set; }
    public string? Family { get; set; }
    public string? TypeName { get; set; }
    public double XMm { get; set; }
    public double YMm { get; set; }
    public string? Level { get; set; }
    public double RotationDeg { get; set; }
    public List<double> StartMm { get; set; } = [];
    public List<double> EndMm { get; set; } = [];
    public string? WallType { get; set; }
    public double HeightMm { get; set; }
    public List<List<double>> PointsMm { get; set; } = [];
    public string? FloorType { get; set; }
    public string? CreatedPhase { get; set; }
    public string? DemolishedPhase { get; set; }
    public string? SourcePhase { get; set; }
    public string? TargetPhase { get; set; }
    public long ElementId { get; set; }
    public string? Parameter { get; set; }
    public string? Value { get; set; }

    /// <summary>The 3D view whose selectable components a rebuild copies; the default is the first non-template 3D view.</summary>
    public string? View { get; set; }

    /// <summary>Where a rebuild writes the new model. The source document is never saved.</summary>
    public string? DestinationPath { get; set; }

    public bool Overwrite { get; set; }
    public string? TemplatePath { get; set; }

    /// <summary>Remove the destination template's own levels once the copied levels exist, so the result has one level list.</summary>
    public bool RemoveTemplateLevels { get; set; }

    /// <summary>
    /// Elements the rebuild adds to the new model before the copy and removes again afterwards. Revit hands the
    /// copied elements the ids that follow the ids the new model already holds, so a seed shifts this copy's ids
    /// away from every other copy made from the same source.
    /// </summary>
    public int Seed { get; set; }

    /// <summary>
    /// How a rebuild handles a name the paste would duplicate: "override" answers Revit's question with OK so
    /// the copy keeps the source model's own types, "rename" renames the destination template's elements first
    /// and removes them again afterwards, which is slower and can fail on elements Revit refuses to delete.
    /// </summary>
    public string DuplicateNames { get; set; } = "override";

    /// <summary>
    /// How many copies one run writes. The copies come out of one new model, one after another, so Revit hands
    /// each copy the ids that follow the copy before it: the files hold the same geometry with different ids and
    /// the run does not need to burn ids for every copy. The destination path may carry "{n}" for the number.
    /// </summary>
    public int Copies { get; set; } = 1;
}

public sealed partial class ControlJobContract
{
    [DataMember(Name = "dryRun")] public bool? DryRun { get; set; }
    [DataMember(Name = "steps")] public List<ControlJobContract>? Steps { get; set; }
    [DataMember(Name = "elementIds")] public List<long>? ElementIds { get; set; }
    [DataMember(Name = "select")] public bool? Select { get; set; }
    [DataMember(Name = "reset")] public bool? Reset { get; set; }
    [DataMember(Name = "dxMm")] public double? DxMm { get; set; }
    [DataMember(Name = "dyMm")] public double? DyMm { get; set; }
    [DataMember(Name = "dzMm")] public double? DzMm { get; set; }
    [DataMember(Name = "typeName")] public string? TypeName { get; set; }
    [DataMember(Name = "xMm")] public double? XMm { get; set; }
    [DataMember(Name = "yMm")] public double? YMm { get; set; }
    [DataMember(Name = "rotationDeg")] public double? RotationDeg { get; set; }
    [DataMember(Name = "startMm")] public List<double>? StartMm { get; set; }
    [DataMember(Name = "endMm")] public List<double>? EndMm { get; set; }
    [DataMember(Name = "wallType")] public string? WallType { get; set; }
    [DataMember(Name = "heightMm")] public double? HeightMm { get; set; }
    [DataMember(Name = "pointsMm")] public List<List<double>>? PointsMm { get; set; }
    [DataMember(Name = "floorType")] public string? FloorType { get; set; }
    [DataMember(Name = "createdPhase")] public string? CreatedPhase { get; set; }
    [DataMember(Name = "demolishedPhase")] public string? DemolishedPhase { get; set; }
    [DataMember(Name = "sourcePhase")] public string? SourcePhase { get; set; }
    [DataMember(Name = "targetPhase")] public string? TargetPhase { get; set; }
    [DataMember(Name = "elementId")] public long? ActionElementId { get; set; }
    [DataMember(Name = "parameter")] public string? Parameter { get; set; }
    [DataMember(Name = "value")] public string? Value { get; set; }
    [DataMember(Name = "destinationPath")] public string? DestinationPath { get; set; }
    [DataMember(Name = "overwrite")] public bool? Overwrite { get; set; }
    [DataMember(Name = "templatePath")] public string? TemplatePath { get; set; }
    [DataMember(Name = "removeTemplateLevels")] public bool? RemoveTemplateLevels { get; set; }
    [DataMember(Name = "seed")] public int? Seed { get; set; }
    [DataMember(Name = "duplicateNames")] public string? DuplicateNames { get; set; }
    [DataMember(Name = "copies")] public int? Copies { get; set; }
}

[DataContract]
public sealed class RebuildCopyResult
{
    [DataMember(Name = "destinationPath")] public string? DestinationPath { get; set; }
    [DataMember(Name = "count")] public int Count { get; set; }
    [DataMember(Name = "newIdMin")] public long NewIdMin { get; set; }
    [DataMember(Name = "newIdMax")] public long NewIdMax { get; set; }
    [DataMember(Name = "sizeBytes")] public long SizeBytes { get; set; }
    [DataMember(Name = "idMappingVerified")] public bool IdMappingVerified { get; set; }
    [DataMember(Name = "mappingMismatches", EmitDefaultValue = false)] public int? MappingMismatches { get; set; }
    [DataMember(Name = "idMapping", EmitDefaultValue = false)] public List<ElementIdPair>? IdMapping { get; set; }
}

[DataContract]
public sealed class ElementIdPair
{
    [DataMember(Name = "old")] public long Old { get; set; }
    [DataMember(Name = "new")] public long New { get; set; }
}

[DataContract]
public sealed class IneligibleElement
{
    [DataMember(Name = "id")] public long Id { get; set; }

    /// <summary>Stable reason key, so a large selection can be summarised without reading every entry.</summary>
    [DataMember(Name = "kind", EmitDefaultValue = false)] public string? Kind { get; set; }

    [DataMember(Name = "reason")] public string Reason { get; set; } = string.Empty;
}

[DataContract]
public sealed class IneligibleKindCount
{
    [DataMember(Name = "kind")] public string Kind { get; set; } = string.Empty;
    [DataMember(Name = "count")] public int Count { get; set; }
}

[DataContract]
public sealed class ActionResultData
{
    [DataMember(Name = "dryRun", EmitDefaultValue = false)] public bool? DryRun { get; set; }
    [DataMember(Name = "rolledBack", EmitDefaultValue = false)] public bool? RolledBack { get; set; }
    [DataMember(Name = "verification", EmitDefaultValue = false)] public ActionVerification? Verification { get; set; }
    [DataMember(Name = "steps", EmitDefaultValue = false)] public List<BatchStepResult>? Steps { get; set; }
    [DataMember(Name = "undoName", EmitDefaultValue = false)] public string? UndoName { get; set; }
    [DataMember(Name = "committed", EmitDefaultValue = false)] public bool? Committed { get; set; }
    [DataMember(Name = "failedStep")] public int? FailedStep { get; set; }

    /// <summary>Old to new element id for a reset, so a caller can audit the replacement without storing it in the model.</summary>
    [DataMember(Name = "idMapping", EmitDefaultValue = false)] public List<ElementIdPair>? IdMapping { get; set; }

    /// <summary>Elements the reset refused, with the reason, so nothing fails silently.</summary>
    [DataMember(Name = "ineligible", EmitDefaultValue = false)] public List<IneligibleElement>? Ineligible { get; set; }

    /// <summary>Total refused, which the sampled list above does not have to carry.</summary>
    [DataMember(Name = "ineligibleCount", EmitDefaultValue = false)] public int? IneligibleCount { get; set; }

    /// <summary>Refusals grouped by reason key, so a whole model can be judged from one response.</summary>
    [DataMember(Name = "ineligibleKinds", EmitDefaultValue = false)] public List<IneligibleKindCount>? IneligibleKinds { get; set; }

    /// <summary>Geometry joins seen before the reset, and how many of them were put back.</summary>
    [DataMember(Name = "joinsFound", EmitDefaultValue = false)] public int? JoinsFound { get; set; }

    [DataMember(Name = "joinsRestored", EmitDefaultValue = false)] public int? JoinsRestored { get; set; }

    /// <summary>Categories of the dependent elements a reset would delete, aggregated over the selection.</summary>
    [DataMember(Name = "dependentCategories", EmitDefaultValue = false)] public List<ElementCategoryCount>? DependentCategories { get; set; }

    [DataMember(Name = "count", EmitDefaultValue = false)] public int? Count { get; set; }
    [DataMember(Name = "notes", EmitDefaultValue = false)] public List<string>? Notes { get; set; }
    [DataMember(Name = "sourceDeleted", EmitDefaultValue = false)] public bool? SourceDeleted { get; set; }
    [DataMember(Name = "phaseDeleteError", EmitDefaultValue = false)] public string? PhaseDeleteError { get; set; }
    [DataMember(Name = "id", EmitDefaultValue = false)] public long? Id { get; set; }
    [DataMember(Name = "category", EmitDefaultValue = false)] public string? Category { get; set; }
    [DataMember(Name = "level", EmitDefaultValue = false)] public string? Level { get; set; }
    [DataMember(Name = "lengthMm", EmitDefaultValue = false)] public double? LengthMm { get; set; }
    [DataMember(Name = "oldValue", EmitDefaultValue = false)] public string? OldValue { get; set; }
    [DataMember(Name = "newValue", EmitDefaultValue = false)] public string? NewValue { get; set; }
    [DataMember(Name = "parameterScope", EmitDefaultValue = false)] public string? ParameterScope { get; set; }
    [DataMember(Name = "closestFamilies", EmitDefaultValue = false)] public List<string>? ClosestFamilies { get; set; }

    /// <summary>Where a rebuild wrote the new model.</summary>
    [DataMember(Name = "destinationPath", EmitDefaultValue = false)] public string? DestinationPath { get; set; }

    /// <summary>The 3D view a rebuild read.</summary>
    [DataMember(Name = "sourceView", EmitDefaultValue = false)] public string? SourceView { get; set; }

    [DataMember(Name = "sourceElementCount", EmitDefaultValue = false)] public int? SourceElementCount { get; set; }

    /// <summary>Levels, grids and reference planes in the selection: they are copied first so hosted elements resolve.</summary>
    [DataMember(Name = "datumCount", EmitDefaultValue = false)] public int? DatumCount { get; set; }

    /// <summary>Elements the rebuild left behind, with the reason, so nothing is dropped silently.</summary>
    [DataMember(Name = "excluded", EmitDefaultValue = false)] public List<IneligibleElement>? Excluded { get; set; }

    [DataMember(Name = "sourceCategoryCounts", EmitDefaultValue = false)] public List<ElementCategoryCount>? SourceCategoryCounts { get; set; }
    [DataMember(Name = "copiedCategoryCounts", EmitDefaultValue = false)] public List<ElementCategoryCount>? CopiedCategoryCounts { get; set; }

    /// <summary>The lowest and highest new element id, which shows that the ids really are fresh.</summary>
    [DataMember(Name = "newIdMin", EmitDefaultValue = false)] public long? NewIdMin { get; set; }

    [DataMember(Name = "newIdMax", EmitDefaultValue = false)] public long? NewIdMax { get; set; }

    [DataMember(Name = "saved", EmitDefaultValue = false)] public bool? Saved { get; set; }
    [DataMember(Name = "sizeBytes", EmitDefaultValue = false)] public long? SizeBytes { get; set; }
    [DataMember(Name = "templatePath", EmitDefaultValue = false)] public string? TemplatePath { get; set; }
    [DataMember(Name = "templateLevelsRemoved", EmitDefaultValue = false)] public int? TemplateLevelsRemoved { get; set; }
    [DataMember(Name = "templateLevelsKept", EmitDefaultValue = false)] public int? TemplateLevelsKept { get; set; }

    /// <summary>Elements a rebuild added to the new model before the copy so this copy's ids sit in their own block.</summary>
    [DataMember(Name = "seed", EmitDefaultValue = false)] public int? Seed { get; set; }

    /// <summary>Questions Revit asked while the rebuild pasted, which the rebuild answered itself instead of waiting.</summary>
    [DataMember(Name = "autoAnsweredDialogs", EmitDefaultValue = false)] public int? AutoAnsweredDialogs { get; set; }

    /// <summary>How the rebuild handled a duplicated name: "override" or "rename".</summary>
    [DataMember(Name = "duplicateNames", EmitDefaultValue = false)] public string? DuplicateNames { get; set; }

    /// <summary>How many copies one run wrote; absent when the run wrote one.</summary>
    [DataMember(Name = "copies", EmitDefaultValue = false)] public int? Copies { get; set; }

    /// <summary>One entry per copy: where it was written, how many elements it holds and its own id mapping.</summary>
    [DataMember(Name = "copyResults", EmitDefaultValue = false)] public List<RebuildCopyResult>? CopyResults { get; set; }

    /// <summary>True when one copy call was refused and the rebuild fell back to copying element by element.</summary>
    [DataMember(Name = "isolatedCopy", EmitDefaultValue = false)] public bool? IsolatedCopy { get; set; }

    /// <summary>
    /// True when every id pair was checked against the copied element's category and type, so a caller can
    /// trust the mapping. A copy call does not promise the order of its return value, so this is verified
    /// rather than assumed.
    /// </summary>
    [DataMember(Name = "idMappingVerified", EmitDefaultValue = false)] public bool? IdMappingVerified { get; set; }

    [DataMember(Name = "idMappingTruncated", EmitDefaultValue = false)] public bool? IdMappingTruncated { get; set; }

    /// <summary>How many id pairs failed the category and type check, when the mapping could not be verified.</summary>
    [DataMember(Name = "mappingMismatches", EmitDefaultValue = false)] public int? MappingMismatches { get; set; }
}
