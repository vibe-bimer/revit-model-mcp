using System.Runtime.Serialization;

namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The element identifier register: where it was written, what it holds and which categories were left out.
/// The identifier itself stays read-only, because the Revit API cannot assign an <see cref="ElementId"/>.
/// </summary>
[DataContract]
public sealed class ForkElementIdExport
{
    /// <summary>Absolute path of the workbook on the workstation.</summary>
    [DataMember(Name = "path")]
    public string Path { get; set; } = string.Empty;

    [DataMember(Name = "fileName")]
    public string FileName { get; set; } = string.Empty;

    [DataMember(Name = "sheetName")]
    public string SheetName { get; set; } = string.Empty;

    /// <summary>Column headers in the order the sheet writes them.</summary>
    [DataMember(Name = "columns")]
    public List<string> Columns { get; set; } = [];

    [DataMember(Name = "rowCount")]
    public int RowCount { get; set; }

    /// <summary>Drawn components found before the row cap, so a truncated list stays visible.</summary>
    [DataMember(Name = "totalCandidates")]
    public int TotalCandidates { get; set; }

    [DataMember(Name = "truncated")]
    public bool Truncated { get; set; }

    [DataMember(Name = "sizeBytes")]
    public long SizeBytes { get; set; }

    /// <summary>Rows per category, largest first.</summary>
    [DataMember(Name = "categoryCounts", EmitDefaultValue = false)]
    public List<ForkCount>? CategoryCounts { get; set; }

    /// <summary>Categories held back as infrastructure rather than components, largest first.</summary>
    [DataMember(Name = "skippedCategories", EmitDefaultValue = false)]
    public List<ForkCount>? SkippedCategories { get; set; }
}
