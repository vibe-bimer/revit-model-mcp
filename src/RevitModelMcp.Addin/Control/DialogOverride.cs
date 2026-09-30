using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Events;

namespace RevitModelMcp.Control;

/// <summary>
/// Answers Revit's modal questions while an unattended rebuild runs. Revit asks how to resolve a name the
/// paste would duplicate, and that question blocks the external event until somebody clicks it. Overriding
/// the question with OK keeps the version from the pasted document, which is the source model's own type,
/// so the copy needs neither a rename of the destination's template nor a cleanup of that rename afterwards.
/// The override only applies between <see cref="Scope"/> and the end of that scope, so reading tools and
/// interactive use of Revit keep their dialogs.
/// </summary>
internal static class DialogOverride
{
    private const string AnswerEverythingVariable = "REVIT_MCP_ANSWER_DIALOGS";
    private static int _scopes;
    private static int _answered;
    private static bool _answerEverything;

    /// <summary>How many dialogs were answered since Revit started.</summary>
    public static int Answered => Volatile.Read(ref _answered);

    public static void Attach(UIControlledApplication application)
    {
        // An instance that runs unattended - a copy farm, a build agent - must never wait for an answer, and
        // Revit asks about an already open file before any job runs. Only such an instance sets the variable.
        _answerEverything = Environment.GetEnvironmentVariable(AnswerEverythingVariable) == "1";
        if (_answerEverything) PluginLog.Info($"Every dialog of this instance is answered automatically ({AnswerEverythingVariable}=1).");
        application.DialogBoxShowing += OnDialogBoxShowing;
    }

    /// <summary>Answers dialogs until the returned scope is disposed.</summary>
    public static IDisposable Scope() => new ScopeGuard();

    private static void OnDialogBoxShowing(object? sender, DialogBoxShowingEventArgs args)
    {
        if (!_answerEverything && Volatile.Read(ref _scopes) <= 0) return;
        try
        {
            Interlocked.Increment(ref _answered);
            var accepted = args.OverrideResult(1);
            PluginLog.Info($"A rebuild answered dialog '{args.DialogId}' with OK ({accepted}).");
        }
        catch (Exception exception)
        {
            PluginLog.Warn($"A rebuild could not answer dialog '{args.DialogId}': {exception.Message}");
        }
    }

    private sealed class ScopeGuard : IDisposable
    {
        private bool _disposed;

        public ScopeGuard() => Interlocked.Increment(ref _scopes);

        public void Dispose()
        {
            if (_disposed) return;
            _disposed = true;
            Interlocked.Decrement(ref _scopes);
        }
    }
}
