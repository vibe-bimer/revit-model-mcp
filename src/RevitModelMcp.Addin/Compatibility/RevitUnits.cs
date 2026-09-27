using Autodesk.Revit.DB;

namespace RevitModelMcp.Compatibility;

/// <summary>
/// Bridges the unit APIs that changed in Revit 2022.
/// Revit 2022 introduced <c>ForgeTypeId</c>, <c>UnitTypeId</c> and <c>SpecTypeId</c>.
/// Revit 2020 and 2021 identify the same units with <c>DisplayUnitType</c> and <c>UnitType</c>.
/// Conversions delegate to <see cref="UnitUtils"/> on every version so rounding matches Revit.
/// </summary>
internal static class RevitUnits
{
    internal static double MillimetersToInternalUnits(double value)
    {
#if REVIT2022_OR_GREATER
        return UnitUtils.ConvertToInternalUnits(value, UnitTypeId.Millimeters);
#else
        return UnitUtils.ConvertToInternalUnits(value, DisplayUnitType.DUT_MILLIMETERS);
#endif
    }

    internal static double SquareMetersToInternalUnits(double value)
    {
#if REVIT2022_OR_GREATER
        return UnitUtils.ConvertToInternalUnits(value, UnitTypeId.SquareMeters);
#else
        return UnitUtils.ConvertToInternalUnits(value, DisplayUnitType.DUT_SQUARE_METERS);
#endif
    }

    internal static double InternalUnitsToMillimeters(double value)
    {
#if REVIT2022_OR_GREATER
        return UnitUtils.ConvertFromInternalUnits(value, UnitTypeId.Millimeters);
#else
        return UnitUtils.ConvertFromInternalUnits(value, DisplayUnitType.DUT_MILLIMETERS);
#endif
    }

    internal static double InternalUnitsToSquareMeters(double value)
    {
#if REVIT2022_OR_GREATER
        return UnitUtils.ConvertFromInternalUnits(value, UnitTypeId.SquareMeters);
#else
        return UnitUtils.ConvertFromInternalUnits(value, DisplayUnitType.DUT_SQUARE_METERS);
#endif
    }

    internal static string LengthUnitId(Document document)
    {
        return ProjectUnitId(document, "length");
    }

    internal static string AreaUnitId(Document document)
    {
        return ProjectUnitId(document, "area");
    }

    internal static string VolumeUnitId(Document document)
    {
        return ProjectUnitId(document, "volume");
    }

    /// <summary>
    /// Reports the project unit for a measurable quantity as a stable identifier,
    /// for example <c>millimeters</c> or <c>squareMeters</c>.
    /// </summary>
    private static string ProjectUnitId(Document document, string quantity)
    {
#if REVIT2022_OR_GREATER
        var spec = quantity switch
        {
            "length" => SpecTypeId.Length,
            "area" => SpecTypeId.Area,
            _ => SpecTypeId.Volume
        };
        return document.GetUnits().GetFormatOptions(spec).GetUnitTypeId().TypeId;
#else
        var unitType = quantity switch
        {
            "length" => UnitType.UT_Length,
            "area" => UnitType.UT_Area,
            _ => UnitType.UT_Volume
        };
        if (!UnitUtils.IsValidUnitType(unitType))
        {
            return string.Empty;
        }

        return UnitUtils.GetTypeCatalogString(document.GetUnits().GetFormatOptions(unitType).DisplayUnits);
#endif
    }
}
