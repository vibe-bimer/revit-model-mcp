using Autodesk.Revit.DB;

namespace RevitModelMcp.Compatibility;

/// <summary>
/// Version-neutral identity of a Revit parameter data type.
/// Revit 2022 describes data types with <c>ForgeTypeId</c>; Revit 2020 and 2021 use
/// <c>ParameterType</c> and <c>UnitType</c>. The default value is empty and leaves values unchanged.
/// </summary>
internal readonly struct ParameterDataType
{
#if REVIT2022_OR_GREATER
    private readonly ForgeTypeId? spec;

    private ParameterDataType(ForgeTypeId? spec)
    {
        this.spec = spec;
    }

    internal static ParameterDataType From(Definition? definition)
    {
        return new ParameterDataType(definition?.GetDataType());
    }

    internal bool IsEmpty => spec is null;

    internal string? Id => spec?.TypeId;

    internal bool IsLength => spec == SpecTypeId.Length;

    internal bool IsArea => spec == SpecTypeId.Area;

    internal bool IsVolume => spec == SpecTypeId.Volume;

    internal bool IsMeasurable => spec is not null && UnitUtils.IsMeasurableSpec(spec);

    internal bool IsText => Id?.Contains("spec:string", StringComparison.OrdinalIgnoreCase) == true;

    internal bool IsInteger =>
        Id?.Contains("yesno", StringComparison.OrdinalIgnoreCase) == true ||
        Id?.Contains("int", StringComparison.OrdinalIgnoreCase) == true;

    internal double ToInternalUnits(Document document, double value)
    {
        if (spec is null || !UnitUtils.IsMeasurableSpec(spec))
        {
            return value;
        }

        if (spec == SpecTypeId.Length)
        {
            return RevitUnits.MillimetersToInternalUnits(value);
        }

        if (spec == SpecTypeId.Area)
        {
            return RevitUnits.SquareMetersToInternalUnits(value);
        }

        return spec == SpecTypeId.Volume
            ? UnitUtils.ConvertToInternalUnits(value, UnitTypeId.CubicMeters)
            : UnitUtils.ConvertToInternalUnits(value, document.GetUnits().GetFormatOptions(spec).GetUnitTypeId());
    }

    internal double FromInternalUnits(double value)
    {
        if (spec == SpecTypeId.Length)
        {
            return RevitUnits.InternalUnitsToMillimeters(value);
        }

        return spec == SpecTypeId.Area ? RevitUnits.InternalUnitsToSquareMeters(value) : value;
    }
#else
    private readonly ParameterType parameterType;
    private readonly UnitType unitType;

    private ParameterDataType(ParameterType parameterType, UnitType unitType)
    {
        this.parameterType = parameterType;
        this.unitType = unitType;
    }

    internal static ParameterDataType From(Definition? definition)
    {
        return definition is null
            ? default
            : new ParameterDataType(definition.ParameterType, definition.UnitType);
    }

    internal bool IsEmpty => parameterType == ParameterType.Invalid;

    internal string? Id => IsEmpty ? null : parameterType.ToString();

    internal bool IsLength => parameterType == ParameterType.Length;

    internal bool IsArea => parameterType == ParameterType.Area;

    internal bool IsVolume => parameterType == ParameterType.Volume;

    /// <summary>
    /// Mirrors <c>UnitUtils.IsMeasurableSpec</c>, which Revit 2020 does not expose.
    /// Unitless and non-numeric data types stay non-measurable.
    /// </summary>
    internal bool IsMeasurable =>
        unitType != UnitType.UT_Undefined &&
        unitType != UnitType.UT_Number &&
        parameterType is not (ParameterType.Invalid or ParameterType.Text or ParameterType.Integer
            or ParameterType.YesNo or ParameterType.Material or ParameterType.Image or ParameterType.URL
            or ParameterType.FamilyType or ParameterType.LoadClassification);

    internal bool IsText => parameterType == ParameterType.Text;

    internal bool IsInteger => parameterType is ParameterType.YesNo or ParameterType.Integer;

    internal double ToInternalUnits(Document document, double value)
    {
        if (IsEmpty)
        {
            return value;
        }

        if (IsLength)
        {
            return RevitUnits.MillimetersToInternalUnits(value);
        }

        if (IsArea)
        {
            return RevitUnits.SquareMetersToInternalUnits(value);
        }

        if (IsVolume)
        {
            return UnitUtils.ConvertToInternalUnits(value, DisplayUnitType.DUT_CUBIC_METERS);
        }

        var displayUnits = ProjectDisplayUnits(document);
        return displayUnits is null ? value : UnitUtils.ConvertToInternalUnits(value, displayUnits.Value);
    }

    internal double FromInternalUnits(double value)
    {
        if (IsLength)
        {
            return RevitUnits.InternalUnitsToMillimeters(value);
        }

        return IsArea ? RevitUnits.InternalUnitsToSquareMeters(value) : value;
    }

    /// <summary>
    /// Returns the project display unit for this data type, or <c>null</c> when the type is
    /// not measurable or Revit rejects the unit, in which case the value stays unconverted.
    /// </summary>
    private DisplayUnitType? ProjectDisplayUnits(Document document)
    {
        if (!IsMeasurable || !UnitUtils.IsValidUnitType(unitType))
        {
            return null;
        }

        var displayUnits = document.GetUnits().GetFormatOptions(unitType).DisplayUnits;
        if (displayUnits is DisplayUnitType.DUT_UNDEFINED or DisplayUnitType.DUT_CUSTOM)
        {
            return null;
        }

        return UnitUtils.IsValidDisplayUnit(unitType, displayUnits) ? displayUnits : null;
    }
#endif
}
