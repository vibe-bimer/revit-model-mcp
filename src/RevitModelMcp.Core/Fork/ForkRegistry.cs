namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The fork's own action registry. Fork actions register here as one self-contained entry each;
/// upstream files consult this registry only at their fallback points, so an empty registry
/// reproduces upstream behavior exactly. See adr/0005.
/// </summary>
public static class ForkRegistry
{
    private static readonly List<string> Commands_ = [];
    private static readonly List<(string Command, string Past, string Process, string? NounOne, string? NounMany)> Phrases_ = [];
    private static readonly Dictionary<string, Func<string, string, bool, string>> Summarizers = new(StringComparer.Ordinal);

    /// <summary>
    /// Registers one fork action: its wire command, its activity-pane title phrase and the
    /// summary it reports. Called from the fork's add-in assembly; the registry holds only
    /// primitive data so the Core-side hooks stay free of Revit API references.
    /// </summary>
    public static void Register(string command, string past, string process, string? nounOne, string? nounMany,
        Func<string, string, bool, string> summarizer)
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

    /// <summary>Attempts to build the activity summary line for a fork action.</summary>
    public static bool TrySummarize(string command, string documentTitle, string? viewName, bool dryRun, out string summary)
    {
        if (Summarizers.TryGetValue(command, out var summarizer))
        {
            summary = summarizer(documentTitle, viewName ?? string.Empty, dryRun);
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
}
