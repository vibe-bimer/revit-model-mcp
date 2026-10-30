using RevitModelMcp.Core.Activity;

namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The fork's own action registry. Fork actions register here as one self-contained entry each;
/// upstream files consult this registry only at their fallback points, so an empty registry
/// reproduces upstream behavior exactly. A fork action's command and phrases live here rather than in the
/// add-in, because the parser asks this registry whether a command is a fork action before any add-in type
/// loads. Its behaviour stays in <c>Addin/Fork</c>. See adr/0005.
/// </summary>
public static class ForkRegistry
{
    /// <summary>Every fork action's wire command, activity phrases and summary sentence.</summary>
    static ForkRegistry()
    {
        Register("set-view-lighting", "Changed view lighting", "Changing view lighting", null, null, context =>
            string.IsNullOrWhiteSpace(context.ViewName)
                ? $"{(context.DryRun ? "Would change" : "Changed")} the view lighting in {Subject(context)}."
                : $"{(context.DryRun ? "Would change" : "Changed")} the lighting of {context.ViewName} in {Subject(context)}.");
        Register("create-level", "Created level", "Creating level", "level", "levels", context =>
            $"{(context.DryRun ? "Would create" : "Created")} a level in {Subject(context)}.");
        Register("create-floor", "Created floor", "Creating floor", "floor", "floors", context =>
            $"{(context.DryRun ? "Would create" : "Created")} a floor in {Subject(context)}.");
        Register("set-phase", "Set element phase", "Setting element phase", "element", "elements", context =>
            $"{(context.DryRun ? "Would set" : "Set")} the phase of {Plural(context.Count, "element")} in {Subject(context)}.");
        Register("merge-phases", "Merged phases", "Merging phases", null, null, context =>
            $"{(context.DryRun ? "Would merge" : "Merged")} phases in {Subject(context)}.");
        Register("reset-element-ids", "Reset element ids", "Resetting element ids", "element", "elements", context =>
            $"{(context.DryRun ? "Would reset" : "Reset")} the ids of {Plural(context.Count, "element")} in {Subject(context)}.");
        Register("rebuild-model-ids", "Rebuilt model ids", "Rebuilding model ids", null, null, context =>
            $"{(context.DryRun ? "Would rebuild" : "Rebuilt")} {Plural(context.Count, "element")} with new ids in {Subject(context)}.");
    }

    private static readonly List<string> Commands_ = [];
    private static readonly List<(string Command, string Past, string Process, string? NounOne, string? NounMany)> Phrases_ = [];
    private static readonly Dictionary<string, Func<ActionSummaryContext, string>> Summarizers = new(StringComparer.Ordinal);

    /// <summary>
    /// Registers one fork action: its wire command, its activity-pane title phrase and the summary it reports.
    /// </summary>
    public static void Register(string command, string past, string process, string? nounOne, string? nounMany,
        Func<ActionSummaryContext, string> summarizer)
    {
        if (string.IsNullOrWhiteSpace(command)) throw new ArgumentException("A fork command name is required.");
        if (Summarizers.ContainsKey(command)) throw new InvalidOperationException($"Fork command '{command}' is already registered.");
        Commands_.Add(command);
        Phrases_.Add((command, past, process, nounOne, nounMany));
        Summarizers[command] = summarizer;
    }

    /// <summary>Wire commands the fork adds. Never reuses an upstream command.</summary>
    public static IReadOnlyList<string> Commands => Commands_;

    /// <summary>Whether the command is a fork action.</summary>
    public static bool IsAction(string command) => Summarizers.ContainsKey(command);

    /// <summary>Attempts to build the summary line for a fork action.</summary>
    public static bool TrySummarize(ActionSummaryContext context, out string summary)
    {
        if (Summarizers.TryGetValue(context.Command, out var summarizer))
        {
            summary = summarizer(context);
            return true;
        }

        summary = string.Empty;
        return false;
    }

    /// <summary>
    /// Title phrases the fork adds to the activity pane: past and process tense plus the optional
    /// count noun, in upstream's shape.
    /// </summary>
    public static IReadOnlyList<(string Command, string Past, string Process, string? NounOne, string? NounMany)>
        Phrases => Phrases_;

    private static string Subject(ActionSummaryContext context) =>
        string.IsNullOrWhiteSpace(context.DocumentTitle) ? "the model" : context.DocumentTitle;

    private static string Plural(int count, string noun) => count == 1 ? $"1 {noun}" : $"{count} {noun}s";
}
