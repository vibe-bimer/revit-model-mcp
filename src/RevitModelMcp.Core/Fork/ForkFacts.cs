using System.Runtime.Serialization;

namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The fork's own element facts. Upstream's <c>ActionFacts</c> describes what an upstream action changed; a
/// fork action reports what it changed here, so no upstream fact has to be widened for the fork's sake. Every
/// member is optional and omitted when it does not apply, which keeps one block usable by several actions.
/// See adr/0005.
/// </summary>
[DataContract]
public sealed class ForkFacts
{
    /// <summary>Name the action gave an element, such as a new level's name.</summary>
    [DataMember(Name = "name", EmitDefaultValue = false)]
    public string? Name { get; set; }

    /// <summary>Element elevation in millimetres, rounded to one decimal.</summary>
    [DataMember(Name = "elevationMm", EmitDefaultValue = false)]
    public double? ElevationMm { get; set; }

    /// <summary>Phase the element is created in, empty when it has none.</summary>
    [DataMember(Name = "createdPhase", EmitDefaultValue = false)]
    public string? CreatedPhase { get; set; }

    /// <summary>Phase the element is demolished in, empty when it has none.</summary>
    [DataMember(Name = "demolishedPhase", EmitDefaultValue = false)]
    public string? DemolishedPhase { get; set; }

    /// <summary>Phase a merge reads from.</summary>
    [DataMember(Name = "sourcePhase", EmitDefaultValue = false)]
    public string? SourcePhase { get; set; }

    /// <summary>Phase a merge moves references into.</summary>
    [DataMember(Name = "targetPhase", EmitDefaultValue = false)]
    public string? TargetPhase { get; set; }

    /// <summary>Structural usage the action wrote on the instance, such as "Girder".</summary>
    [DataMember(Name = "structuralUsage", EmitDefaultValue = false)]
    public string? StructuralUsage { get; set; }

    /// <summary>Vertical offset above the reference level, in millimetres, as read back from the instance.</summary>
    [DataMember(Name = "zOffsetMm", EmitDefaultValue = false)]
    public double? ZOffsetMm { get; set; }

    /// <summary>Name of the parameter that holds the vertical offset, as read back from the instance.</summary>
    [DataMember(Name = "zOffsetParam", EmitDefaultValue = false)]
    public string? ZOffsetParam { get; set; }

    /// <summary>Elements whose creation phase a merge reassigned.</summary>
    [DataMember(Name = "reassignedCreated", EmitDefaultValue = false)]
    public int? ReassignedCreated { get; set; }

    /// <summary>Elements whose demolition phase a merge reassigned.</summary>
    [DataMember(Name = "reassignedDemolished", EmitDefaultValue = false)]
    public int? ReassignedDemolished { get; set; }

    /// <summary>Elements still referencing the source phase after a merge.</summary>
    [DataMember(Name = "sourceRemaining", EmitDefaultValue = false)]
    public int? SourceRemaining { get; set; }
}
