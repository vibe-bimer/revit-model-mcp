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
        switch (command)
        {
            case "set-view-lighting":
                result = ForkLighting.Apply(document, action);
                return true;
            case "create-level":
                result = ForkLevels.Apply(document, action);
                return true;
            case "create-floor":
                result = ForkFloors.Apply(document, action);
                return true;
            case "set-phase":
                result = ForkPhases.Set(document, action, ids);
                return true;
            case "merge-phases":
                result = ForkPhases.Merge(document, action);
                return true;
            case "reset-element-ids":
                result = ForkReset.Reset(document, action, ids);
                return true;
            default:
                result = null;
                return false;
        }
    }

    /// <summary>
    /// Attempts to run one fork action that must stay outside the caller's transaction. A rebuild writes a
    /// second document and manages its own transactions there, so it cannot run inside one.
    /// </summary>
    internal static bool TryRunBeforeTransaction(
        Document document,
        string command,
        ActionJobContract action,
        out ActionResultData? result)
    {
        if (command != "rebuild-model-ids")
        {
            result = null;
            return false;
        }

        result = ForkRebuild.Rebuild(document, action);
        return true;
    }

    /// <summary>Attempts to capture before-facts for a fork action, and refuses bad input before it runs.</summary>
    internal static ActionFacts? CaptureBefore(
        Document document,
        string command,
        ActionJobContract action,
        List<ElementId> ids)
    {
        switch (command)
        {
            case "set-view-lighting":
                ForkLighting.Validate(action);
                return new ActionFacts
                {
                    Lighting = ForkLighting.Read(document, ForkLighting.Resolve(document, action.View))
                };
            case "create-level":
                ForkLevels.Validate(action);
                return null;
            case "create-floor":
                ForkFloors.Validate(action);
                return null;
            case "set-phase":
                return ForkPhases.ReadAssignment(document, ids);
            case "merge-phases":
                return ForkPhases.ReadSource(document, action);
            case "reset-element-ids":
                ForkReset.Validate(action);
                return null;
            default:
                return null;
        }
    }

    /// <summary>Fills after-facts on the fork action's verification block. Returns whether it did.</summary>
    internal static bool CaptureAfter(
        Document document,
        string command,
        ActionJobContract action,
        ActionResultData result)
    {
        var verification = result.Verification!;
        switch (command)
        {
            case "set-view-lighting":
                {
                    var lighting = ForkLighting.Read(document, ForkLighting.Resolve(document, action.View));
                    verification.After = new ActionFacts { Lighting = lighting };
                    // A view change has no element id to report, so the settings that moved are the changed set.
                    result.ChangedSettings = ViewLightingComparison.Differences(verification.Before?.Lighting, lighting);
                    return true;
                }
            case "create-level":
                {
                    if (result.Id is not { } id) return false;
                    verification.After = new ActionFacts { Fork = ForkLevels.Read(document, ForkLookup.CreateId(id)) };
                    verification.WouldCreate = action.DryRun ? true : null;
                    return true;
                }
            case "create-floor":
                {
                    if (result.Id is not { } id) return false;
                    verification.After = ForkFloors.Read(document, ForkLookup.CreateId(id));
                    verification.WouldCreate = action.DryRun ? true : null;
                    return true;
                }
            case "set-phase":
                verification.After = ForkPhases.ReadAssignment(document, action.ElementIds ?? []);
                verification.Changed = ForkPhases.ChangedBetween(verification.Before, verification.After);
                return true;
            case "merge-phases":
                // The merge knows its own reassigned counts, so it fills the after-facts as it runs.
                return false;
            default:
                return false;
        }
    }
}
