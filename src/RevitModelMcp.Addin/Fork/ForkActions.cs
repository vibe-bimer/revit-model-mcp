using Autodesk.Revit.DB;
using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Execution side of the fork's action registry. The empty registry runs nothing: every Try
/// member answers false or null, so upstream dispatch falls through to its own handling.
/// Fork actions implement the Revit-facing parts here because the capture and mutation helpers
/// they build on are internal to the add-in assembly. See adr/0005.
/// </summary>
internal static class ForkActions
{
    /// <summary>Attempts to run one fork action inside the caller's transaction scope.</summary>
    internal static bool TryRun(
        Document document,
        string command,
        ActionJobContract action,
        List<ElementId> ids,
        PreflightState? preflight,
        out ActionResultData? result)
    {
        result = null;
        return false;
    }

    /// <summary>Attempts to capture before-facts for a fork action.</summary>
    internal static ActionFacts? CaptureBefore(Document targetDocument, string command, ActionJobContract action, List<ElementId> ids) => null;

    /// <summary>Fills after-facts on the fork action's verification block. Returns whether it did.</summary>
    internal static bool CaptureAfter(Document targetDocument, string command, ActionJobContract action, ActionResultData result) => false;
}
