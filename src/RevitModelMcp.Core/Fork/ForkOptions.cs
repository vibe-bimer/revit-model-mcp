namespace RevitModelMcp.Core.Fork;

/// <summary>
/// Every input the fork's actions accept, in one fork-owned type. The shared action contract carries a
/// single property of this type, so a fork action adds an input here without touching an upstream field
/// list, and the wire reaches these values through the job's one <c>fork</c> bag (see <see cref="ForkInputs"/>).
/// Upstream fields keep their meaning: a fork action reuses <c>level</c>, <c>name</c>, <c>pointsMm</c> and
/// <c>view</c> rather than restating them here. See adr/0002 and adr/0005.
/// </summary>
public sealed class ForkOptions
{
    // set-view-lighting
    public bool? Shadows { get; set; }
    public int? ShadowIntensity { get; set; }
    public int? SunlightIntensity { get; set; }
    public string? SunDate { get; set; }
    public string? SunTime { get; set; }
    public double? SunAzimuthDeg { get; set; }
    public double? SunAltitudeDeg { get; set; }
    public bool? GroundPlane { get; set; }
    public string? GroundPlaneLevel { get; set; }
    public string? Background { get; set; }
    public List<string>? BackgroundColors { get; set; }
    public string? LightingScheme { get; set; }

    // create-level
    public double? ElevationMm { get; set; }
    public bool? CreateView { get; set; }

    // create-floor
    public string? FloorType { get; set; }

    // create-grid
    public List<double>? StartMm { get; set; }
    public List<double>? EndMm { get; set; }
    public List<double>? MidMm { get; set; }

    // create-column
    public string? TopLevel { get; set; }
    public double? HeightMm { get; set; }
    public double? BaseOffsetMm { get; set; }
    public double? TopOffsetMm { get; set; }

    // create-beam (the axis reuses startMm/endMm above, as create-grid does)
    public string? StructuralUsage { get; set; }
    public double? ZOffsetMm { get; set; }

    // place-hosted-family
    public long? HostElementId { get; set; }
    public double? HostSearchRadiusMm { get; set; }
    public double? SillHeightMm { get; set; }
    public bool? FlipFacing { get; set; }

    // load-family-file
    public string? FamilyPath { get; set; }
    public string? FamilyTypeName { get; set; }
    public bool? OverwriteParameters { get; set; }

    // set-phase
    public string? CreatedPhase { get; set; }
    public string? DemolishedPhase { get; set; }

    // merge-phases
    public string? SourcePhase { get; set; }
    public string? TargetPhase { get; set; }

    // rebuild-model-ids
    public string? DestinationPath { get; set; }
    public string? TemplatePath { get; set; }
    public bool? Overwrite { get; set; }
    public bool? RemoveTemplateLevels { get; set; }
    public int? Seed { get; set; }
    public string? DuplicateNames { get; set; }
    public int? Copies { get; set; }

    /// <summary>Copies every input, so a cloned contract never shares one options object.</summary>
    public ForkOptions Copy() => new()
    {
        Shadows = Shadows,
        ShadowIntensity = ShadowIntensity,
        SunlightIntensity = SunlightIntensity,
        SunDate = SunDate,
        SunTime = SunTime,
        SunAzimuthDeg = SunAzimuthDeg,
        SunAltitudeDeg = SunAltitudeDeg,
        GroundPlane = GroundPlane,
        GroundPlaneLevel = GroundPlaneLevel,
        Background = Background,
        BackgroundColors = BackgroundColors is null ? null : [.. BackgroundColors],
        LightingScheme = LightingScheme,
        ElevationMm = ElevationMm,
        CreateView = CreateView,
        FloorType = FloorType,
        StartMm = StartMm is null ? null : [.. StartMm],
        EndMm = EndMm is null ? null : [.. EndMm],
        MidMm = MidMm is null ? null : [.. MidMm],
        TopLevel = TopLevel,
        HeightMm = HeightMm,
        BaseOffsetMm = BaseOffsetMm,
        TopOffsetMm = TopOffsetMm,
        StructuralUsage = StructuralUsage,
        ZOffsetMm = ZOffsetMm,
        HostElementId = HostElementId,
        HostSearchRadiusMm = HostSearchRadiusMm,
        SillHeightMm = SillHeightMm,
        FlipFacing = FlipFacing,
        FamilyPath = FamilyPath,
        FamilyTypeName = FamilyTypeName,
        OverwriteParameters = OverwriteParameters,
        CreatedPhase = CreatedPhase,
        DemolishedPhase = DemolishedPhase,
        SourcePhase = SourcePhase,
        TargetPhase = TargetPhase,
        DestinationPath = DestinationPath,
        TemplatePath = TemplatePath,
        Overwrite = Overwrite,
        RemoveTemplateLevels = RemoveTemplateLevels,
        Seed = Seed,
        DuplicateNames = DuplicateNames,
        Copies = Copies
    };
}
