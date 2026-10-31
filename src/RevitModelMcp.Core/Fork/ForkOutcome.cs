using System.Runtime.Serialization;

namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The fork's result block. A fork action reports what it did here, so it never needs a new field on
/// upstream's <c>ActionResultData</c>; the wire name is <c>fork</c>. See adr/0005.
/// </summary>
[DataContract]
public sealed class ForkOutcome
{
    /// <summary>Every element id the action replaced, in the order the copy was made.</summary>
    [DataMember(Name = "idMapping", EmitDefaultValue = false)]
    public List<ForkIdPair>? IdMapping { get; set; }

    /// <summary>Whether the copied ids pair one to one with the source ids.</summary>
    [DataMember(Name = "idMappingVerified", EmitDefaultValue = false)]
    public bool? IdMappingVerified { get; set; }

    /// <summary>Whether the mapping list was cut at its entry limit.</summary>
    [DataMember(Name = "idMappingTruncated", EmitDefaultValue = false)]
    public bool? IdMappingTruncated { get; set; }

    /// <summary>How many pairs did not share a category and type.</summary>
    [DataMember(Name = "mappingMismatches", EmitDefaultValue = false)]
    public int? MappingMismatches { get; set; }

    /// <summary>Elements the action could not handle, with the reason for each.</summary>
    [DataMember(Name = "ineligible", EmitDefaultValue = false)]
    public List<ForkIneligibleElement>? Ineligible { get; set; }

    /// <summary>How many elements the action could not handle.</summary>
    [DataMember(Name = "ineligibleCount", EmitDefaultValue = false)]
    public int? IneligibleCount { get; set; }

    /// <summary>How many elements fell into each ineligible kind.</summary>
    [DataMember(Name = "ineligibleKinds", EmitDefaultValue = false)]
    public List<ForkCount>? IneligibleKinds { get; set; }

    /// <summary>Categories of the elements that depend on a reset element, most frequent first.</summary>
    [DataMember(Name = "dependentCategories", EmitDefaultValue = false)]
    public List<ForkCount>? DependentCategories { get; set; }

    /// <summary>How many joins a reset found on its elements before it copied them.</summary>
    [DataMember(Name = "joinsFound", EmitDefaultValue = false)]
    public int? JoinsFound { get; set; }

    /// <summary>How many of those joins were put back on the replacement elements.</summary>
    [DataMember(Name = "joinsRestored", EmitDefaultValue = false)]
    public int? JoinsRestored { get; set; }

    /// <summary>The file a rebuild wrote.</summary>
    [DataMember(Name = "destinationPath", EmitDefaultValue = false)]
    public string? DestinationPath { get; set; }

    /// <summary>The template the rebuild started from, or a note that it used the default metric template.</summary>
    [DataMember(Name = "templatePath", EmitDefaultValue = false)]
    public string? TemplatePath { get; set; }

    /// <summary>The 3D view the rebuild copied its components from.</summary>
    [DataMember(Name = "sourceView", EmitDefaultValue = false)]
    public string? SourceView { get; set; }

    /// <summary>How the rebuild answered duplicate names.</summary>
    [DataMember(Name = "duplicateNames", EmitDefaultValue = false)]
    public string? DuplicateNames { get; set; }

    /// <summary>How many copies the rebuild wrote.</summary>
    [DataMember(Name = "copiesWritten", EmitDefaultValue = false)]
    public int? CopiesWritten { get; set; }

    /// <summary>How many temporary levels moved the copy's ids into a block of their own.</summary>
    [DataMember(Name = "seed", EmitDefaultValue = false)]
    public int? Seed { get; set; }

    /// <summary>How many source elements the rebuild selected.</summary>
    [DataMember(Name = "sourceElementCount", EmitDefaultValue = false)]
    public int? SourceElementCount { get; set; }

    /// <summary>How many of the selected elements were levels, grids or reference planes.</summary>
    [DataMember(Name = "datumCount", EmitDefaultValue = false)]
    public int? DatumCount { get; set; }

    /// <summary>The source elements per category.</summary>
    [DataMember(Name = "sourceCategoryCounts", EmitDefaultValue = false)]
    public List<ForkCount>? SourceCategoryCounts { get; set; }

    /// <summary>The copied elements per category.</summary>
    [DataMember(Name = "copiedCategoryCounts", EmitDefaultValue = false)]
    public List<ForkCount>? CopiedCategoryCounts { get; set; }

    /// <summary>Whether the rebuild had to isolate elements Revit rejected.</summary>
    [DataMember(Name = "isolatedCopy", EmitDefaultValue = false)]
    public bool? IsolatedCopy { get; set; }

    /// <summary>How many template levels the rebuild removed from the new model.</summary>
    [DataMember(Name = "templateLevelsRemoved", EmitDefaultValue = false)]
    public int? TemplateLevelsRemoved { get; set; }

    /// <summary>How many template levels the rebuild kept.</summary>
    [DataMember(Name = "templateLevelsKept", EmitDefaultValue = false)]
    public int? TemplateLevelsKept { get; set; }

    /// <summary>The lowest id the rebuild assigned.</summary>
    [DataMember(Name = "newIdMin", EmitDefaultValue = false)]
    public long? NewIdMin { get; set; }

    /// <summary>The highest id the rebuild assigned.</summary>
    [DataMember(Name = "newIdMax", EmitDefaultValue = false)]
    public long? NewIdMax { get; set; }

    /// <summary>The size of the first written copy.</summary>
    [DataMember(Name = "sizeBytes", EmitDefaultValue = false)]
    public long? SizeBytes { get; set; }

    /// <summary>The result of each copy when the rebuild wrote more than one.</summary>
    [DataMember(Name = "copyResults", EmitDefaultValue = false)]
    public List<ForkCopyResult>? CopyResults { get; set; }
}

/// <summary>One replacement: the id an element had and the id it now has.</summary>
[DataContract]
public sealed class ForkIdPair
{
    [DataMember(Name = "old")] public long Old { get; set; }
    [DataMember(Name = "new")] public long New { get; set; }
}

/// <summary>An element a fork action could not handle, and why.</summary>
[DataContract]
public sealed class ForkIneligibleElement
{
    [DataMember(Name = "id")] public long Id { get; set; }
    [DataMember(Name = "kind")] public string Kind { get; set; } = string.Empty;
    [DataMember(Name = "reason")] public string Reason { get; set; } = string.Empty;
}

/// <summary>A name and how many elements carry it.</summary>
[DataContract]
public sealed class ForkCount
{
    [DataMember(Name = "category", EmitDefaultValue = false)] public string? Category { get; set; }
    [DataMember(Name = "builtInCategory", EmitDefaultValue = false)] public string? BuiltInCategory { get; set; }
    [DataMember(Name = "kind", EmitDefaultValue = false)] public string? Kind { get; set; }
    [DataMember(Name = "count")] public int Count { get; set; }
}

/// <summary>One written copy of a rebuild, with its own mapping.</summary>
[DataContract]
public sealed class ForkCopyResult
{
    [DataMember(Name = "destinationPath")] public string DestinationPath { get; set; } = string.Empty;
    [DataMember(Name = "count")] public int Count { get; set; }
    [DataMember(Name = "newIdMin")] public long NewIdMin { get; set; }
    [DataMember(Name = "newIdMax")] public long NewIdMax { get; set; }
    [DataMember(Name = "sizeBytes")] public long SizeBytes { get; set; }
    [DataMember(Name = "idMappingVerified")] public bool IdMappingVerified { get; set; }
    [DataMember(Name = "mappingMismatches", EmitDefaultValue = false)] public int? MappingMismatches { get; set; }
    [DataMember(Name = "idMapping", EmitDefaultValue = false)] public List<ForkIdPair>? IdMapping { get; set; }
}
