using System;

namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The identifier text the 2021 unit surface reports, derived from the Revit 2020 enumeration names.
/// </summary>
/// <remarks>
/// The 2020 build has no ForgeTypeId, so the add-in names units and specs from the enumeration that
/// 2020 does carry. The derivations live here, away from the API, because the capture surface
/// classifies a parameter by markers in this text: a wrong marker turns a length into an element id
/// without any error. The inputs are the 2020 enumeration names, so the rules are testable without Revit.
/// </remarks>
public static class UnitSpecNames
{
    private const string SpecUnitPrefix = "autodesk.spec.unit:";
    private const string UnitPrefix = "autodesk.unit.unit:";
    private const string GroupPrefix = "autodesk.parameter.group:";
    private const string UndefinedUnitType = "UT_Undefined";

    /// <summary>The spec identifier for a 2020 unit type name, such as UT_Length.</summary>
    public static string SpecForUnit(string unitTypeName) => unitTypeName switch
    {
        "UT_Length" => "autodesk.spec.aec:length-2.0.0",
        "UT_Area" => "autodesk.spec.aec:area-2.0.0",
        "UT_Volume" => "autodesk.spec.aec:volume-2.0.0",
        "UT_Angle" => "autodesk.spec:angle-1.0.0",
        "UT_Number" => "autodesk.spec:number-1.0.0",
        _ => SpecUnitPrefix + Camel(unitTypeName, "UT_") + "-1.0.0"
    };

    /// <summary>The spec identifier for a 2020 parameter type name that carries no unit of its own.</summary>
    public static string SpecForParameterType(string parameterTypeName) => parameterTypeName switch
    {
        "Text" => "autodesk.spec:string:text-1.0.0",
        "MultilineText" => "autodesk.spec:string:multiline-1.0.0",
        "URL" => "autodesk.spec:string:url-1.0.0",
        "Integer" => "autodesk.spec:int:integer-1.0.0",
        "YesNo" => "autodesk.spec:yesno-1.0.0",
        "Material" => "autodesk.spec:material-1.0.0",
        "Image" => "autodesk.spec:image-1.0.0",
        "FamilyType" => "autodesk.spec:familyType-1.0.0",
        "LoadClassification" => "autodesk.spec:loadClassification-1.0.0",
        _ => SpecUnitPrefix + Camel(parameterTypeName, string.Empty) + "-1.0.0"
    };

    /// <summary>The unit identifier for a 2020 display unit name, such as DUT_MILLIMETERS.</summary>
    public static string UnitFor(string displayUnitName) =>
        UnitPrefix + Camel(displayUnitName, "DUT_") + "-1.0.0";

    /// <summary>The group identifier for a 2020 parameter group name, such as PG_IDENTITY_DATA.</summary>
    public static string GroupFor(string groupName) => GroupPrefix + Camel(groupName, "PG_") + "-1.0.0";

    /// <summary>True when a 2020 unit type name names a unit that can be measured.</summary>
    public static bool IsMeasurableUnit(string? unitTypeName) =>
        !string.IsNullOrEmpty(unitTypeName) && unitTypeName != UndefinedUnitType;

    /// <summary>lowerCamelCase of an enumeration name without its prefix: PG_IDENTITY_DATA becomes identityData.</summary>
    public static string Camel(string name, string prefix)
    {
        if (prefix.Length > 0 && name.StartsWith(prefix, StringComparison.Ordinal)) name = name.Substring(prefix.Length);
        var parts = name.Split(new[] { '_' }, StringSplitOptions.RemoveEmptyEntries);
        if (parts.Length == 0) return string.Empty;
        var text = parts[0].ToLowerInvariant();
        for (var index = 1; index < parts.Length; index++)
            text += char.ToUpperInvariant(parts[index][0]) + parts[index].Substring(1).ToLowerInvariant();
        return text;
    }
}
