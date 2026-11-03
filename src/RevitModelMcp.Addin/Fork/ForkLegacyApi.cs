// Revit 2020 lacks a handful of members the add-in calls, mostly read-side questions that 2021 added
// to the same classes. The members below restore them as extensions for the 2020 build only, so the
// capture code compiles and reports what 2020 can actually answer.
#if REVIT2020_BUILD
using System.Collections.Generic;

namespace Autodesk.Revit.DB
{
    /// <summary>The members 2020 does not carry, re-expressed over the 2020 surface.</summary>
    public static class ForkLegacyApi
    {
        /// <summary>
        /// Whether a filter is enabled on the view. Revit 2020 removes the per-filter enabled flag from the
        /// API, so a filter that reaches the caller through View.GetFilters is reported as enabled.
        /// </summary>
        public static bool GetIsFilterEnabled(this View view, ElementId filterId) => true;

        /// <summary>
        /// Every element an independent tag points at. Revit 2020 tags one element per tag, so the answer is
        /// the single tagged element, empty when the tag is orphaned.
        /// </summary>
        public static ICollection<ElementId> GetTaggedLocalElementIds(this IndependentTag tag)
        {
            var tagged = tag.TaggedLocalElementId;
            return tagged is null || tagged == ElementId.InvalidElementId
                ? new List<ElementId>()
                : new List<ElementId> { tagged };
        }
    }
}
#endif
