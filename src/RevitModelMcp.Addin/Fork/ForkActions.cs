using Autodesk.Revit.DB;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Execution side of the fork's action registry. Each fork action declares its command and phrases in
/// <see cref="ForkRegistry"/> (it lives in Core, because parsing asks it before any add-in type loads) and
/// adds its behaviour here; upstream dispatch falls through to this runner only at its default points.
/// Fork actions implement the Revit-facing parts here because the capture and mutation helpers they build
/// on are internal to the add-in assembly. See adr/0005.
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
        if (command != "set-view-lighting")
        {
            result = null;
            return false;
        }

        result = ForkLighting.Apply(document, action);
        return true;
    }

    /// <summary>Attempts to capture before-facts for a fork action.</summary>
    internal static ActionFacts? CaptureBefore(Document targetDocument, string command, ActionJobContract action, List<ElementId> ids)
    {
        if (command != "set-view-lighting")
        {
            return null;
        }

        ForkLighting.Validate(action);
        return new ActionFacts
        {
            Lighting = ForkLighting.Read(targetDocument, ForkLighting.Resolve(targetDocument, action.View))
        };
    }

    /// <summary>Fills after-facts on the fork action's verification block. Returns whether it did.</summary>
    internal static bool CaptureAfter(Document targetDocument, string command, ActionJobContract action, ActionResultData result)
    {
        if (command != "set-view-lighting")
        {
            return false;
        }

        var verification = result.Verification!;
        var lighting = ForkLighting.Read(targetDocument, ForkLighting.Resolve(targetDocument, action.View));
        verification.After = new ActionFacts { Lighting = lighting };
        // A view change has no element id to report, so the settings that moved are the changed set.
        result.ChangedSettings = ViewLightingComparison.Differences(verification.Before?.Lighting, lighting);
        return true;
    }
}
