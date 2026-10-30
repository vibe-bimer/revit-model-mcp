namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The fork's own action registry. Fork actions register here as one self-contained entry each;
/// upstream files consult this registry only at their fallback points, so an empty registry
/// reproduces upstream behavior exactly. See adr/0005.
/// </summary>
public static class ForkRegistry
{
    /// <summary>Wire commands the fork adds. Never reuses an upstream command.</summary>
    public static IReadOnlyList<string> Commands => [];

    /// <summary>Whether the command is a fork action.</summary>
    public static bool IsAction(string command) => false;

    /// <summary>Attempts to build the activity summary line for a fork action.</summary>
    public static bool TrySummarize(string command, string documentTitle, bool dryRun, out string summary)
    {
        summary = string.Empty;
        return false;
    }

    /// <summary>
    /// Title phrases the fork adds to the activity pane: past and process tense plus the optional
    /// count noun. Returns command-relative entries in upstream's shape.
    /// </summary>
    public static IReadOnlyList<(string Command, string Past, string Process, string? NounOne, string? NounMany)>
        Phrases => [];
}
