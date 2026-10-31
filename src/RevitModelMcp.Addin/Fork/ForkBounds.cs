using Autodesk.Revit.DB;
using RevitModelMcp.Capture;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Millimetre bounds of an element, the way upstream's element facts report them. Upstream keeps the same
/// helper private to its verifier, so the fork keeps one copy for the elements it creates.
/// </summary>
internal static class ForkBounds
{
    /// <summary>Lower corner in millimetres, rounded to one decimal.</summary>
    internal static List<double> Minimum(BoundingBoxXYZ box) =>
        [ForkLookup.MillimetersFromInternal(box.Min.X),
         ForkLookup.MillimetersFromInternal(box.Min.Y),
         ForkLookup.MillimetersFromInternal(box.Min.Z)];

    /// <summary>Upper corner in millimetres, rounded to one decimal.</summary>
    internal static List<double> Maximum(BoundingBoxXYZ box) =>
        [ForkLookup.MillimetersFromInternal(box.Max.X),
         ForkLookup.MillimetersFromInternal(box.Max.Y),
         ForkLookup.MillimetersFromInternal(box.Max.Z)];
}
