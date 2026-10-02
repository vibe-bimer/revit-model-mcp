using System.Runtime.Serialization;

namespace RevitModelMcp.Core.Control;

[DataContract]
public sealed class ActionVerification
{
    [DataMember(Name = "before", EmitDefaultValue = false)] public ActionFacts? Before { get; set; }
    [DataMember(Name = "after", EmitDefaultValue = false)] public ActionFacts? After { get; set; }
    [DataMember(Name = "error", EmitDefaultValue = false)] public string? Error { get; set; }
    [DataMember(Name = "changed", EmitDefaultValue = false)] public List<long>? Changed { get; set; }
    [DataMember(Name = "wouldCreate", EmitDefaultValue = false)] public bool? WouldCreate { get; set; }
}

[DataContract]
public sealed class ActionFacts
{
    [DataMember(Name = "elements", EmitDefaultValue = false)] public List<ActionFacts>? Elements { get; set; }
    [DataMember(Name = "id", EmitDefaultValue = false)] public long? Id { get; set; }
    [DataMember(Name = "category", EmitDefaultValue = false)] public string? Category { get; set; }
    [DataMember(Name = "boundingBoxMinMm", EmitDefaultValue = false)] public List<double>? BoundingBoxMinMm { get; set; }
    [DataMember(Name = "boundingBoxMaxMm", EmitDefaultValue = false)] public List<double>? BoundingBoxMaxMm { get; set; }
    [DataMember(Name = "family", EmitDefaultValue = false)] public string? Family { get; set; }
    [DataMember(Name = "type", EmitDefaultValue = false)] public string? Type { get; set; }
    [DataMember(Name = "level", EmitDefaultValue = false)] public string? Level { get; set; }

    /// <summary>A datum element has no geometry, so its name and elevation carry the facts a level reports.</summary>
    [DataMember(Name = "name", EmitDefaultValue = false)] public string? Name { get; set; }

    [DataMember(Name = "elevationMm", EmitDefaultValue = false)] public double? ElevationMm { get; set; }
    [DataMember(Name = "parameter", EmitDefaultValue = false)] public string? Parameter { get; set; }
    [DataMember(Name = "value", EmitDefaultValue = false)] public string? Value { get; set; }
    [DataMember(Name = "storageType", EmitDefaultValue = false)] public string? StorageType { get; set; }
    [DataMember(Name = "owner", EmitDefaultValue = false)] public string? Owner { get; set; }
    [DataMember(Name = "requested", EmitDefaultValue = false)] public List<long>? Requested { get; set; }
    [DataMember(Name = "dependents", EmitDefaultValue = false)] public List<long>? Dependents { get; set; }
    [DataMember(Name = "stillPresent", EmitDefaultValue = false)] public List<long>? StillPresent { get; set; }
    [DataMember(Name = "createdPhase", EmitDefaultValue = false)] public string? CreatedPhase { get; set; }
    [DataMember(Name = "demolishedPhase", EmitDefaultValue = false)] public string? DemolishedPhase { get; set; }
    [DataMember(Name = "sourcePhase", EmitDefaultValue = false)] public string? SourcePhase { get; set; }
    [DataMember(Name = "targetPhase", EmitDefaultValue = false)] public string? TargetPhase { get; set; }
    [DataMember(Name = "reassignedCreated", EmitDefaultValue = false)] public int? ReassignedCreated { get; set; }
    [DataMember(Name = "reassignedDemolished", EmitDefaultValue = false)] public int? ReassignedDemolished { get; set; }
    [DataMember(Name = "sourceRemaining", EmitDefaultValue = false)] public int? SourceRemaining { get; set; }

    /// <summary>Lighting readings of the addressed view, before and after a lighting change.</summary>
    [DataMember(Name = "lighting", EmitDefaultValue = false)] public ViewLightingFacts? Lighting { get; set; }
}

/// <summary>
/// One view's lighting state: shadows, sun position, ground plane, display background and the rendering
/// lighting scheme. Every reading is optional so a view that does not expose a setting reports null for it.
/// </summary>
[DataContract]
public sealed class ViewLightingFacts
{
    [DataMember(Name = "viewId")] public long ViewId { get; set; }
    [DataMember(Name = "view")] public string View { get; set; } = string.Empty;
    [DataMember(Name = "viewType")] public string ViewType { get; set; } = string.Empty;
    [DataMember(Name = "shadows", EmitDefaultValue = false)] public bool? Shadows { get; set; }
    [DataMember(Name = "shadowIntensity", EmitDefaultValue = false)] public int? ShadowIntensity { get; set; }
    [DataMember(Name = "sunlightIntensity", EmitDefaultValue = false)] public int? SunlightIntensity { get; set; }

    /// <summary>StillImage, OneDayStudy, MultiDayStudy or Lighting.</summary>
    [DataMember(Name = "sunType", EmitDefaultValue = false)] public string? SunType { get; set; }

    /// <summary>Sun date and time as ISO 8601 UTC, which is the form Revit reports.</summary>
    [DataMember(Name = "sunDateAndTimeUtc", EmitDefaultValue = false)] public string? SunDateAndTimeUtc { get; set; }

    /// <summary>Project time-zone offset in hours, which is how the date and time above is read locally.</summary>
    [DataMember(Name = "sunTimeZoneHours", EmitDefaultValue = false)] public double? SunTimeZoneHours { get; set; }

    [DataMember(Name = "sunUsesDst", EmitDefaultValue = false)] public bool? SunUsesDst { get; set; }

    /// <summary>Lighting-study azimuth in degrees clockwise from north; only read in lighting mode.</summary>
    [DataMember(Name = "sunAzimuthDeg", EmitDefaultValue = false)] public double? SunAzimuthDeg { get; set; }

    /// <summary>Lighting-study altitude in degrees above the horizon; only read in lighting mode.</summary>
    [DataMember(Name = "sunAltitudeDeg", EmitDefaultValue = false)] public double? SunAltitudeDeg { get; set; }

    /// <summary>True when this view shares its sun and shadow settings with other views.</summary>
    [DataMember(Name = "sunSettingsShared", EmitDefaultValue = false)] public bool? SunSettingsShared { get; set; }

    [DataMember(Name = "groundPlane", EmitDefaultValue = false)] public bool? GroundPlane { get; set; }
    [DataMember(Name = "groundPlaneLevel", EmitDefaultValue = false)] public string? GroundPlaneLevel { get; set; }

    /// <summary>None, Gradient, Image or SunAndClouds.</summary>
    [DataMember(Name = "background", EmitDefaultValue = false)] public string? Background { get; set; }

    /// <summary>Sky, horizon and ground colors of a gradient background as "#RRGGBB".</summary>
    [DataMember(Name = "backgroundColors", EmitDefaultValue = false)] public List<string>? BackgroundColors { get; set; }

    /// <summary>Rendering lighting scheme, with the same names the tool accepts.</summary>
    [DataMember(Name = "lightingScheme", EmitDefaultValue = false)] public string? LightingScheme { get; set; }
}

/// <summary>
/// Names the lighting settings that differ between two readings. The tool reports them as
/// <c>changedSettings</c>, because a view change has no element id to report.
/// </summary>
public static class ViewLightingComparison
{
    public static List<string> Differences(ViewLightingFacts? before, ViewLightingFacts? after)
    {
        var changed = new List<string>();
        if (before is null || after is null)
        {
            return changed;
        }

        Compare(changed, "shadows", before.Shadows, after.Shadows);
        Compare(changed, "shadow_intensity", before.ShadowIntensity, after.ShadowIntensity);
        Compare(changed, "sunlight_intensity", before.SunlightIntensity, after.SunlightIntensity);
        Compare(changed, "sun_type", before.SunType, after.SunType);
        Compare(changed, "sun_date_time", before.SunDateAndTimeUtc, after.SunDateAndTimeUtc);
        Compare(changed, "sun_azimuth_deg", before.SunAzimuthDeg, after.SunAzimuthDeg);
        Compare(changed, "sun_altitude_deg", before.SunAltitudeDeg, after.SunAltitudeDeg);
        Compare(changed, "ground_plane", before.GroundPlane, after.GroundPlane);
        Compare(changed, "ground_plane_level", before.GroundPlaneLevel, after.GroundPlaneLevel);
        Compare(changed, "background", before.Background, after.Background);
        Compare(
            changed,
            "background_colors",
            before.BackgroundColors is null ? null : string.Join(",", before.BackgroundColors),
            after.BackgroundColors is null ? null : string.Join(",", after.BackgroundColors));
        Compare(changed, "lighting_scheme", before.LightingScheme, after.LightingScheme);
        return changed;
    }

    private static void Compare<T>(List<string> changed, string name, T before, T after)
    {
        if (!EqualityComparer<T>.Default.Equals(before, after))
        {
            changed.Add(name);
        }
    }
}

[DataContract]
public sealed class BatchStepResult
{
    [DataMember(Name = "index")] public int Index { get; set; }
    [DataMember(Name = "command")] public string Command { get; set; } = string.Empty;
    [DataMember(Name = "success")] public bool Success { get; set; }
    [DataMember(Name = "data", EmitDefaultValue = false)] public ActionResultData? Data { get; set; }
    [DataMember(Name = "error", EmitDefaultValue = false)] public string? Error { get; set; }
    [DataMember(Name = "rolledBack", EmitDefaultValue = false)] public bool? RolledBack { get; set; }
}
