using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;

namespace RevitModelMcp.Compatibility;

/// <summary>
/// Reads the project base point and the survey point.
/// The <c>BasePoint.GetProjectBasePoint</c> and <c>BasePoint.GetSurveyPoint</c> accessors arrived in a
/// Revit 2020 update, so builds that must also run on an unpatched Revit 2020 collect both points.
/// </summary>
internal static class BasePoints
{
    internal static BasePoint GetProjectBasePoint(Document document)
    {
#if REVIT2022_OR_GREATER
        return BasePoint.GetProjectBasePoint(document);
#else
        return Collect(document).FirstOrDefault(point => !point.IsShared)
               ?? throw new InvalidOperationException("The document has no project base point.");
#endif
    }

    internal static BasePoint GetSurveyPoint(Document document)
    {
#if REVIT2022_OR_GREATER
        return BasePoint.GetSurveyPoint(document);
#else
        return Collect(document).FirstOrDefault(point => point.IsShared)
               ?? throw new InvalidOperationException("The document has no survey point.");
#endif
    }

#if !REVIT2022_OR_GREATER
    private static IEnumerable<BasePoint> Collect(Document document)
    {
        using var collector = document.CollectElements().OfClass<BasePoint>();
        return collector.Cast<BasePoint>().ToList();
    }
#endif
}
