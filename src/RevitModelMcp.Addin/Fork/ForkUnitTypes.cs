// Revit 2020 keeps only the DisplayUnitType and UnitType unit surface; 2021 moved every unit answer
// behind ForgeTypeId. This file restores the 2021 surface for the 2020 build so the rest of the add-in
// compiles and behaves unchanged, and it disappears at compile time for 2021 and later.
#if REVIT2020_BUILD
using System;
using RevitModelMcp.Core.Fork;

namespace Autodesk.Revit.DB
{
    /// <summary>The 2021 unit identity type, standing in for the 2020 display-unit and unit-type pair.</summary>
    /// <remarks>
    /// Equality is the identifier text, exactly as the 2021 type behaves. The payload carries the 2020
    /// enumeration the identifier was built from so the implicit conversions and the units lookups can
    /// hand the real 2020 API the value it expects.
    /// </remarks>
    public sealed class ForgeTypeId : IEquatable<ForgeTypeId>
    {
        internal ForgeTypeId(string typeId, UnitType unitType = UnitType.UT_Undefined,
            DisplayUnitType displayUnit = DisplayUnitType.DUT_UNDEFINED,
            BuiltInParameterGroup group = BuiltInParameterGroup.INVALID)
        {
            TypeId = typeId ?? string.Empty;
            UnitType = unitType;
            DisplayUnit = displayUnit;
            Group = group;
        }

        /// <summary>The stable identifier text, compared ordinally.</summary>
        public string TypeId { get; }

        internal UnitType UnitType { get; }

        internal DisplayUnitType DisplayUnit { get; }

        internal BuiltInParameterGroup Group { get; }

        public bool Equals(ForgeTypeId? other) => other is not null && string.Equals(TypeId, other.TypeId, StringComparison.Ordinal);

        public override bool Equals(object? obj) => obj is ForgeTypeId other && Equals(other);

        public override int GetHashCode() => StringComparer.Ordinal.GetHashCode(TypeId);

        public static bool operator ==(ForgeTypeId? left, ForgeTypeId? right) =>
            ReferenceEquals(left, right) || (left is not null && left.Equals(right));

        public static bool operator !=(ForgeTypeId? left, ForgeTypeId? right) => !(left == right);

        public override string ToString() => TypeId;

        /// <summary>The 2020 display unit behind this unit identifier.</summary>
        public static implicit operator DisplayUnitType(ForgeTypeId id) => id.DisplayUnit != DisplayUnitType.DUT_UNDEFINED
            ? id.DisplayUnit
            : throw new InvalidOperationException($"ForgeTypeId '{id.TypeId}' is not a display unit.");

        /// <summary>The 2020 parameter group behind this group identifier.</summary>
        public static implicit operator BuiltInParameterGroup(ForgeTypeId id) => id.Group != BuiltInParameterGroup.INVALID
            ? id.Group
            : throw new InvalidOperationException($"ForgeTypeId '{id.TypeId}' is not a parameter group.");
    }

    /// <summary>The unit identifiers the add-in names directly.</summary>
    public static class UnitTypeId
    {
        public static ForgeTypeId Millimeters { get; } =
            new ForgeTypeId("autodesk.unit.unit:millimeters-1.0.0", UnitType.UT_Length, DisplayUnitType.DUT_MILLIMETERS);

        public static ForgeTypeId SquareMeters { get; } =
            new ForgeTypeId("autodesk.unit.unit:squareMeters-1.0.0", UnitType.UT_Area, DisplayUnitType.DUT_SQUARE_METERS);

        public static ForgeTypeId CubicMeters { get; } =
            new ForgeTypeId("autodesk.unit.unit:cubicMeters-1.0.0", UnitType.UT_Volume, DisplayUnitType.DUT_CUBIC_METERS);
    }

    /// <summary>The measurable spec identifiers the add-in compares against.</summary>
    public static class SpecTypeId
    {
        public static ForgeTypeId Length { get; } = ForkUnitTypes.SpecFor(UnitType.UT_Length);

        public static ForgeTypeId Area { get; } = ForkUnitTypes.SpecFor(UnitType.UT_Area);

        public static ForgeTypeId Volume { get; } = ForkUnitTypes.SpecFor(UnitType.UT_Volume);
    }

    /// <summary>The parameter group identifiers the add-in resolves by name.</summary>
    public static class GroupTypeId
    {
    public static ForgeTypeId IdentityData => Group(BuiltInParameterGroup.PG_IDENTITY_DATA);
    public static ForgeTypeId Geometry => Group(BuiltInParameterGroup.PG_GEOMETRY);
    public static ForgeTypeId Construction => Group(BuiltInParameterGroup.PG_CONSTRUCTION);
    public static ForgeTypeId Graphics => Group(BuiltInParameterGroup.PG_GRAPHICS);
    public static ForgeTypeId Materials => Group(BuiltInParameterGroup.PG_MATERIALS);
    public static ForgeTypeId Underlay => Group(BuiltInParameterGroup.PG_UNDERLAY);
    public static ForgeTypeId StairTreads => Group(BuiltInParameterGroup.PG_STAIR_TREADS);
    public static ForgeTypeId StairRisers => Group(BuiltInParameterGroup.PG_STAIR_RISERS);
    public static ForgeTypeId StairStringers => Group(BuiltInParameterGroup.PG_STAIR_STRINGERS);
    public static ForgeTypeId Electrical => Group(BuiltInParameterGroup.PG_ELECTRICAL);
    public static ForgeTypeId Plumbing => Group(BuiltInParameterGroup.PG_PLUMBING);
    public static ForgeTypeId Structural => Group(BuiltInParameterGroup.PG_STRUCTURAL);
    public static ForgeTypeId Mechanical => Group(BuiltInParameterGroup.PG_MECHANICAL);
    public static ForgeTypeId Phasing => Group(BuiltInParameterGroup.PG_PHASING);
    public static ForgeTypeId Constraints => Group(BuiltInParameterGroup.PG_CONSTRAINTS);
    public static ForgeTypeId Pattern => Group(BuiltInParameterGroup.PG_PATTERN);
    public static ForgeTypeId ViewExtents => Group(BuiltInParameterGroup.PG_VIEW_EXTENTS);
    public static ForgeTypeId ViewCamera => Group(BuiltInParameterGroup.PG_VIEW_CAMERA);
    public static ForgeTypeId Text => Group(BuiltInParameterGroup.PG_TEXT);
    public static ForgeTypeId ElectricalLighting => Group(BuiltInParameterGroup.PG_ELECTRICAL_LIGHTING);
    public static ForgeTypeId ElectricalLoads => Group(BuiltInParameterGroup.PG_ELECTRICAL_LOADS);
    public static ForgeTypeId MechanicalLoads => Group(BuiltInParameterGroup.PG_MECHANICAL_LOADS);
    public static ForgeTypeId MechanicalAirflow => Group(BuiltInParameterGroup.PG_MECHANICAL_AIRFLOW);
    public static ForgeTypeId StructuralAnalysis => Group(BuiltInParameterGroup.PG_STRUCTURAL_ANALYSIS);
    public static ForgeTypeId EnergyAnalysis => Group(BuiltInParameterGroup.PG_ENERGY_ANALYSIS);
    public static ForgeTypeId Aelectrical => Group(BuiltInParameterGroup.PG_AELECTRICAL);
    public static ForgeTypeId Ifc => Group(BuiltInParameterGroup.PG_IFC);
    public static ForgeTypeId CurtainGridVert => Group(BuiltInParameterGroup.PG_CURTAIN_GRID_VERT);
    public static ForgeTypeId CurtainGrid1 => Group(BuiltInParameterGroup.PG_CURTAIN_GRID_1);
    public static ForgeTypeId CurtainGridHoriz => Group(BuiltInParameterGroup.PG_CURTAIN_GRID_HORIZ);
    public static ForgeTypeId CurtainGrid2 => Group(BuiltInParameterGroup.PG_CURTAIN_GRID_2);
    public static ForgeTypeId CurtainMullionVert => Group(BuiltInParameterGroup.PG_CURTAIN_MULLION_VERT);
    public static ForgeTypeId CurtainMullion1 => Group(BuiltInParameterGroup.PG_CURTAIN_MULLION_1);
    public static ForgeTypeId CurtainMullionHoriz => Group(BuiltInParameterGroup.PG_CURTAIN_MULLION_HORIZ);
    public static ForgeTypeId CurtainMullion2 => Group(BuiltInParameterGroup.PG_CURTAIN_MULLION_2);
    public static ForgeTypeId CurtainGrid => Group(BuiltInParameterGroup.PG_CURTAIN_GRID);
    public static ForgeTypeId RebarSystemLayers => Group(BuiltInParameterGroup.PG_REBAR_SYSTEM_LAYERS);
    public static ForgeTypeId RebarArray => Group(BuiltInParameterGroup.PG_REBAR_ARRAY);
    public static ForgeTypeId AnalyticalModel => Group(BuiltInParameterGroup.PG_ANALYTICAL_MODEL);
    public static ForgeTypeId TranslationIn => Group(BuiltInParameterGroup.PG_TRANSLATION_IN);
    public static ForgeTypeId RotationAbout => Group(BuiltInParameterGroup.PG_ROTATION_ABOUT);
    public static ForgeTypeId FireProtection => Group(BuiltInParameterGroup.PG_FIRE_PROTECTION);
    public static ForgeTypeId Title => Group(BuiltInParameterGroup.PG_TITLE);
    public static ForgeTypeId TrussFamilyVertWeb => Group(BuiltInParameterGroup.PG_TRUSS_FAMILY_VERT_WEB);
    public static ForgeTypeId TrussFamilyDiagWeb => Group(BuiltInParameterGroup.PG_TRUSS_FAMILY_DIAG_WEB);
    public static ForgeTypeId TrussFamilyTopChord => Group(BuiltInParameterGroup.PG_TRUSS_FAMILY_TOP_CHORD);
    public static ForgeTypeId TrussFamilyBottomChord => Group(BuiltInParameterGroup.PG_TRUSS_FAMILY_BOTTOM_CHORD);
    public static ForgeTypeId Profile => Group(BuiltInParameterGroup.PG_PROFILE);
    public static ForgeTypeId Profile1 => Group(BuiltInParameterGroup.PG_PROFILE_1);
    public static ForgeTypeId Profile2 => Group(BuiltInParameterGroup.PG_PROFILE_2);
    public static ForgeTypeId GreenBuilding => Group(BuiltInParameterGroup.PG_GREEN_BUILDING);
    public static ForgeTypeId PatternApplication => Group(BuiltInParameterGroup.PG_PATTERN_APPLICATION);
    public static ForgeTypeId LightPhotometrics => Group(BuiltInParameterGroup.PG_LIGHT_PHOTOMETRICS);
    public static ForgeTypeId SlabShapeEdit => Group(BuiltInParameterGroup.PG_SLAB_SHAPE_EDIT);
    public static ForgeTypeId AnalysisResults => Group(BuiltInParameterGroup.PG_ANALYSIS_RESULTS);
    public static ForgeTypeId Display => Group(BuiltInParameterGroup.PG_DISPLAY);
    public static ForgeTypeId CurtainGridU => Group(BuiltInParameterGroup.PG_CURTAIN_GRID_U);
    public static ForgeTypeId CurtainGridV => Group(BuiltInParameterGroup.PG_CURTAIN_GRID_V);
    public static ForgeTypeId AdskModelProperties => Group(BuiltInParameterGroup.PG_ADSK_MODEL_PROPERTIES);
    public static ForgeTypeId Area => Group(BuiltInParameterGroup.PG_AREA);
    public static ForgeTypeId ConceptualEnergyData => Group(BuiltInParameterGroup.PG_CONCEPTUAL_ENERGY_DATA);
    public static ForgeTypeId Fitting => Group(BuiltInParameterGroup.PG_FITTING);
    public static ForgeTypeId EnergyAnalysisDetailedAndConceptualModels => Group(BuiltInParameterGroup.PG_ENERGY_ANALYSIS_DETAILED_AND_CONCEPTUAL_MODELS);
    public static ForgeTypeId EnergyAnalysisDetailedModel => Group(BuiltInParameterGroup.PG_ENERGY_ANALYSIS_DETAILED_MODEL);
    public static ForgeTypeId EnergyAnalysisConceptualModel => Group(BuiltInParameterGroup.PG_ENERGY_ANALYSIS_CONCEPTUAL_MODEL);
    public static ForgeTypeId Flexible => Group(BuiltInParameterGroup.PG_FLEXIBLE);
    public static ForgeTypeId General => Group(BuiltInParameterGroup.PG_GENERAL);
    public static ForgeTypeId ElectricalCircuiting => Group(BuiltInParameterGroup.PG_ELECTRICAL_CIRCUITING);
    public static ForgeTypeId ConceptualEnergyDataBuildingServices => Group(BuiltInParameterGroup.PG_CONCEPTUAL_ENERGY_DATA_BUILDING_SERVICES);
    public static ForgeTypeId RailingSystemFamilyTopRail => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_FAMILY_TOP_RAIL);
    public static ForgeTypeId RailingSystemFamilyHandrails => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_FAMILY_HANDRAILS);
    public static ForgeTypeId RailingSystemFamilySegmentPattern => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_FAMILY_SEGMENT_PATTERN);
    public static ForgeTypeId RailingSystemSegmentPatternRepeat => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_SEGMENT_PATTERN_REPEAT);
    public static ForgeTypeId RailingSystemSegmentPatternRemainder => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_SEGMENT_PATTERN_REMAINDER);
    public static ForgeTypeId RailingSystemSegmentPosts => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_SEGMENT_POSTS);
    public static ForgeTypeId RailingSystemSegmentUGrid => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_SEGMENT_U_GRID);
    public static ForgeTypeId RailingSystemSegmentVGrid => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_SEGMENT_V_GRID);
    public static ForgeTypeId Support => Group(BuiltInParameterGroup.PG_SUPPORT);
    public static ForgeTypeId Visibility => Group(BuiltInParameterGroup.PG_VISIBILITY);
    public static ForgeTypeId OverallLegend => Group(BuiltInParameterGroup.PG_OVERALL_LEGEND);
    public static ForgeTypeId Insulation => Group(BuiltInParameterGroup.PG_INSULATION);
    public static ForgeTypeId Lining => Group(BuiltInParameterGroup.PG_LINING);
    public static ForgeTypeId SystemtypeRisedrop => Group(BuiltInParameterGroup.PG_SYSTEMTYPE_RISEDROP);
    public static ForgeTypeId AnalyticalAlignment => Group(BuiltInParameterGroup.PG_ANALYTICAL_ALIGNMENT);
    public static ForgeTypeId AnalyticalProperties => Group(BuiltInParameterGroup.PG_ANALYTICAL_PROPERTIES);
    public static ForgeTypeId Nodes => Group(BuiltInParameterGroup.PG_NODES);
    public static ForgeTypeId Length => Group(BuiltInParameterGroup.PG_LENGTH);
    public static ForgeTypeId SplitProfileDimensions => Group(BuiltInParameterGroup.PG_SPLIT_PROFILE_DIMENSIONS);
    public static ForgeTypeId StairsCalculatorRules => Group(BuiltInParameterGroup.PG_STAIRS_CALCULATOR_RULES);
    public static ForgeTypeId StairsTreadsRisers => Group(BuiltInParameterGroup.PG_STAIRS_TREADS_RISERS);
    public static ForgeTypeId Termintation => Group(BuiltInParameterGroup.PG_TERMINTATION);
    public static ForgeTypeId RailingSystemSecondaryFamilyHandrails => Group(BuiltInParameterGroup.PG_RAILING_SYSTEM_SECONDARY_FAMILY_HANDRAILS);
    public static ForgeTypeId StairsOpenEndConnection => Group(BuiltInParameterGroup.PG_STAIRS_OPEN_END_CONNECTION);
    public static ForgeTypeId StairsSupports => Group(BuiltInParameterGroup.PG_STAIRS_SUPPORTS);
    public static ForgeTypeId StairsWinders => Group(BuiltInParameterGroup.PG_STAIRS_WINDERS);
    public static ForgeTypeId ContinuousrailBeginBottomExtension => Group(BuiltInParameterGroup.PG_CONTINUOUSRAIL_BEGIN_BOTTOM_EXTENSION);
    public static ForgeTypeId ContinuousrailEndTopExtension => Group(BuiltInParameterGroup.PG_CONTINUOUSRAIL_END_TOP_EXTENSION);
    public static ForgeTypeId SegmentsFittings => Group(BuiltInParameterGroup.PG_SEGMENTS_FITTINGS);
    public static ForgeTypeId DivisionGeometry => Group(BuiltInParameterGroup.PG_DIVISION_GEOMETRY);
    public static ForgeTypeId GeometryPositioning => Group(BuiltInParameterGroup.PG_GEOMETRY_POSITIONING);
    public static ForgeTypeId Reference => Group(BuiltInParameterGroup.PG_REFERENCE);
    public static ForgeTypeId FabricationProductData => Group(BuiltInParameterGroup.PG_FABRICATION_PRODUCT_DATA);
    public static ForgeTypeId Forces => Group(BuiltInParameterGroup.PG_FORCES);
    public static ForgeTypeId Moments => Group(BuiltInParameterGroup.PG_MOMENTS);
    public static ForgeTypeId PrimaryEnd => Group(BuiltInParameterGroup.PG_PRIMARY_END);
    public static ForgeTypeId SecondaryEnd => Group(BuiltInParameterGroup.PG_SECONDARY_END);
    public static ForgeTypeId ReleasesMemberForces => Group(BuiltInParameterGroup.PG_RELEASES_MEMBER_FORCES);
    public static ForgeTypeId EnergyAnalysisAdvanced => Group(BuiltInParameterGroup.PG_ENERGY_ANALYSIS_ADVANCED);
    public static ForgeTypeId CouplerArray => Group(BuiltInParameterGroup.PG_COUPLER_ARRAY);
    public static ForgeTypeId EnergyAnalysisBuildingData => Group(BuiltInParameterGroup.PG_ENERGY_ANALYSIS_BUILDING_DATA);
    public static ForgeTypeId EnergyAnalysisRoomSpaceData => Group(BuiltInParameterGroup.PG_ENERGY_ANALYSIS_ROOM_SPACE_DATA);
    public static ForgeTypeId EnergyAnalysisBldgConsMtlThermalProps => Group(BuiltInParameterGroup.PG_ENERGY_ANALYSIS_BLDG_CONS_MTL_THERMAL_PROPS);
    public static ForgeTypeId StructuralSectionGeometry => Group(BuiltInParameterGroup.PG_STRUCTURAL_SECTION_GEOMETRY);
    public static ForgeTypeId GeoLocation => Group(BuiltInParameterGroup.PG_GEO_LOCATION);
    public static ForgeTypeId RouteAnalysis => Group(BuiltInParameterGroup.PG_ROUTE_ANALYSIS);
    public static ForgeTypeId Data => Group(BuiltInParameterGroup.PG_DATA);
        private static ForgeTypeId Group(BuiltInParameterGroup group) => ForkUnitTypes.GroupFor(group);
    }

    /// <summary>The unit helpers the 2020 API does not carry, plus the extension methods the 2021 call sites expect.</summary>
    public static class ForkUnitTypes
    {
        /// <summary>True when the identifier names a spec that carries a unit, mirroring UnitUtils.IsMeasurableSpec.</summary>
        public static bool IsMeasurableSpec(ForgeTypeId spec) => spec.UnitType != UnitType.UT_Undefined;

        /// <summary>The spec identifier for a 2020 unit type, whose text the Core seam derives and tests.</summary>
        internal static ForgeTypeId SpecFor(UnitType unitType) => new(UnitSpecNames.SpecForUnit(unitType.ToString()), unitType);

        /// <summary>The group identifier for a 2020 parameter group.</summary>
        internal static ForgeTypeId GroupFor(BuiltInParameterGroup group) =>
            new(UnitSpecNames.GroupFor(group.ToString()), group: group);

        /// <summary>The unit identifier for a display unit, as the project reports it.</summary>
        internal static ForgeTypeId UnitFor(DisplayUnitType displayUnit) => new(
            UnitSpecNames.UnitFor(displayUnit.ToString()),
            UnitTypeFor(displayUnit),
            displayUnit);

        /// <summary>The spec identifier behind a 2020 parameter type, keeping the markers the query surface classifies on.</summary>
        internal static ForgeTypeId SpecForDefinition(Definition definition)
        {
            var unitType = definition.UnitType;
            if (unitType != UnitType.UT_Undefined) return SpecFor(unitType);
            return new ForgeTypeId(UnitSpecNames.SpecForParameterType(definition.ParameterType.ToString()));
        }

        /// <summary>The unit type a display unit belongs to, or undefined when the project cannot measure it.</summary>
        private static UnitType UnitTypeFor(DisplayUnitType displayUnit) => displayUnit switch
        {
            DisplayUnitType.DUT_MILLIMETERS or DisplayUnitType.DUT_CENTIMETERS or DisplayUnitType.DUT_METERS
                or DisplayUnitType.DUT_FEET_FRACTIONAL_INCHES or DisplayUnitType.DUT_FRACTIONAL_INCHES
                or DisplayUnitType.DUT_DECIMAL_INCHES or DisplayUnitType.DUT_DECIMAL_FEET => UnitType.UT_Length,
            DisplayUnitType.DUT_SQUARE_MILLIMETERS or DisplayUnitType.DUT_SQUARE_METERS
                or DisplayUnitType.DUT_SQUARE_FEET or DisplayUnitType.DUT_SQUARE_INCHES => UnitType.UT_Area,
            DisplayUnitType.DUT_CUBIC_MILLIMETERS or DisplayUnitType.DUT_CUBIC_METERS
                or DisplayUnitType.DUT_CUBIC_FEET or DisplayUnitType.DUT_CUBIC_INCHES => UnitType.UT_Volume,
            DisplayUnitType.DUT_DECIMAL_DEGREES or DisplayUnitType.DUT_DEGREES_AND_MINUTES
                or DisplayUnitType.DUT_RADIANS or DisplayUnitType.DUT_GRADS => UnitType.UT_Angle,
            _ => UnitType.UT_Undefined
        };
    }

    /// <summary>The 2021 members the add-in calls, re-expressed over the 2020 surface.</summary>
    public static class ForkUnitExtensions
    {
        /// <summary>The spec a parameter definition stores, as the 2021 GetDataType reports it.</summary>
        public static ForgeTypeId GetDataType(this Definition definition) => ForkUnitTypes.SpecForDefinition(definition);

        /// <summary>The parameter group a definition belongs to.</summary>
        public static ForgeTypeId GetGroupTypeId(this Definition definition) => ForkUnitTypes.GroupFor(definition.ParameterGroup);

        /// <summary>The unit type a schedule field measures, as the 2021 GetSpecTypeId reports it.</summary>
        public static ForgeTypeId GetSpecTypeId(this ScheduleField field) => ForkUnitTypes.SpecFor(field.UnitType);

        /// <summary>The default format options for a spec, which the 2020 API answers by unit type.</summary>
        public static FormatOptions GetFormatOptions(this Units units, ForgeTypeId specTypeId) =>
            units.GetFormatOptions(specTypeId.UnitType);

        /// <summary>The unit a format options object measures.</summary>
        public static ForgeTypeId GetUnitTypeId(this FormatOptions options) => ForkUnitTypes.UnitFor(options.DisplayUnits);
    }
}
#endif
