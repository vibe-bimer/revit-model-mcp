using Autodesk.Revit.DB;
using RevitModelMcp.Compatibility;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Models;

namespace RevitModelMcp.Capture;

internal static class SharedCoordinatesReader
{
    public static SharedCoordinatesData Read(Document document, ControlJobContract job)
    {
        const int listLimit = 100;
        var location = document.ActiveProjectLocation;
        var basePoint = BasePoints.GetProjectBasePoint(document);
        var surveyPoint = BasePoints.GetSurveyPoint(document);
        var locations = document.ProjectLocations.Cast<ProjectLocation>().Select(site => site.Name)
            .OrderBy(name => name, StringComparer.Ordinal).ToList();
        using var links = new FilteredElementCollector(document).OfClass(typeof(RevitLinkInstance));
        return new SharedCoordinatesData
        {
            ActiveProjectLocation = location.Name,
            SiteName = location.Name,
            ProjectLocations = locations.Take(listLimit).ToList(),
            ProjectLocationsTotal = locations.Count,
            ListLimit = listLimit,
            LinkInstancesTotal = links.GetElementCount(),
            ProjectBasePoint = ReadPoint(basePoint, true),
            SurveyPoint = ReadPoint(surveyPoint, false),
            InternalOriginToBasePointMm = Offset(basePoint.Position),
            TrueNorthAngleDeg = Degrees(location.GetProjectPosition(XYZ.Zero).Angle),
            SharedSiteFromLinks = links.Cast<RevitLinkInstance>().OrderBy(link => RevitValueReader.GetId(link.Id))
                .Take(listLimit).Select(link =>
                {
                    var transform = link.GetTotalTransform();
                    return new LinkSharedSite
                    {
                        LinkName = link.Name,
                        HasOffset = !transform.AlmostEqual(Transform.Identity),
                        OffsetMm = Offset(transform.Origin),
                        RotationDeg = Degrees(Math.Atan2(transform.BasisX.Y, transform.BasisX.X))
                    };
                }).ToList()
        };
    }

    private static CoordinatePoint ReadPoint(BasePoint point, bool project)
    {
        return new CoordinatePoint
        {
            EastWestMm = Millimeters(point.get_Parameter(BuiltInParameter.BASEPOINT_EASTWEST_PARAM).AsDouble()),
            NorthSouthMm = Millimeters(point.get_Parameter(BuiltInParameter.BASEPOINT_NORTHSOUTH_PARAM).AsDouble()),
            ElevationMm = Millimeters(point.get_Parameter(BuiltInParameter.BASEPOINT_ELEVATION_PARAM).AsDouble()),
            AngleToTrueNorthDeg = project
                ? Degrees(point.get_Parameter(BuiltInParameter.BASEPOINT_ANGLETON_PARAM).AsDouble()) : null,
            Clipped = project ? ReadClipped(point) : null
        };
    }

    private static bool? ReadClipped(BasePoint point)
    {
#if REVIT2022_OR_GREATER
        try { return point.Clipped; }
        catch (Exception) { return null; }
#else
        // Revit 2020 has no BasePoint.Clipped. Only the survey point can be clipped, and the
        // project base point read here is never shared, so Revit reports it unclipped.
        return false;
#endif
    }

    private static CoordinateOffset Offset(XYZ point) => new()
    {
        X = Millimeters(point.X),
        Y = Millimeters(point.Y),
        Z = Millimeters(point.Z)
    };

    private static double Millimeters(double value) =>
        Math.Round(RevitUnits.InternalUnitsToMillimeters(value), 1);

    private static double Degrees(double value) => Math.Round(value * 180 / Math.PI, 1);
}
