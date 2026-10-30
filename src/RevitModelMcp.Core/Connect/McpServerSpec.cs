using System.Reflection;

namespace RevitModelMcp.Core.Connect;

/// <summary>
///     The one server entry the add-in writes into AI app configurations: the launcher program and its arguments.
///     The bundled executable of the MSI needs neither uv nor Python; a uvx launch from this fork's own source is
///     the fallback.
/// </summary>
public sealed record McpServerSpec(string Command, IReadOnlyList<string> Args)
{
    /// <summary>The key of the entry in every client configuration.</summary>
    public const string Name = "revit-model-mcp";

    /// <summary>The file name of the bundled server executable.</summary>
    public const string ExecutableName = "revit-model-mcp.exe";

    /// <summary>The install folder the MSI creates; a different UpgradeCode with the same folder would collide.</summary>
    public const string ProductFolder = "Revit Model MCP (vibe-bimer)";

    /// <summary>
    ///     The source this fork's server is installed from when no bundled executable exists. A bare
    ///     <c>uvx revit-model-mcp</c> would fetch upstream's package from PyPI, and both projects publish the same
    ///     version numbers, so that form would install upstream's server while appearing to work.
    /// </summary>
    public static string ForkSource => ForkSourceFor(InformationalVersion());

    /// <summary>
    ///     The source for one release version. A release build carries the tag's version, so it installs the tag;
    ///     a development build carries a prerelease suffix that no tag matches, so it follows the main archive.
    /// </summary>
    /// <param name="version">The version the build reports, with or without a prerelease suffix.</param>
    public static string ForkSourceFor(string version) =>
        string.IsNullOrWhiteSpace(version) || version.Contains('-') || version == "0.0.0"
            ? "https://github.com/vibe-bimer/revit-model-mcp/archive/refs/heads/main.tar.gz#subdirectory=server"
            : $"https://github.com/vibe-bimer/revit-model-mcp/archive/refs/tags/v{version}.tar.gz#subdirectory=server";

    /// <summary>The documented local registration through uv, resolved from this fork's own source.</summary>
    public static McpServerSpec Uvx => UvxFor(InformationalVersion());

    /// <summary>The local registration for one release version.</summary>
    /// <param name="version">The version the build reports.</param>
    public static McpServerSpec UvxFor(string version) => new("uvx", ["--from", ForkSourceFor(version), Name]);

    /// <summary>The version this assembly reports, without the build metadata after <c>+</c>.</summary>
    private static string InformationalVersion()
    {
        var text = typeof(McpServerSpec).Assembly
            .GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion;
        if (string.IsNullOrWhiteSpace(text)) return "0.0.0";
        var plus = text.IndexOf('+');
        return plus < 0 ? text : text[..plus];
    }

    /// <summary>The environment the server needs to talk to the Revit on this workstation.</summary>
    public static IReadOnlyList<KeyValuePair<string, string>> Env { get; } =
    [
        new("REVIT_MCP_HOST", "local"),
        new("REVIT_MCP_REDACT_PATHS", "1")
    ];

    /// <summary>Runs the bundled server executable at <paramref name="path" /> directly.</summary>
    public static McpServerSpec ForExecutable(string path) => new(path, []);

    /// <summary>
    ///     Picks the first candidate path of the bundled executable that exists. Without one the uvx fallback is used,
    ///     except in the store channel, which never starts a package download: there the result is <see langword="null" />.
    /// </summary>
    /// <param name="candidates">Absolute executable paths in order of preference.</param>
    /// <param name="fileExists">Tests whether a file exists.</param>
    /// <param name="storeChannel">Whether this is the store build, which has no uvx fallback.</param>
    public static McpServerSpec? Resolve(IEnumerable<string> candidates, Func<string, bool> fileExists, bool storeChannel = false)
    {
        foreach (var candidate in candidates)
        {
            if (!string.IsNullOrWhiteSpace(candidate) && fileExists(candidate)) return ForExecutable(candidate);
        }

        return storeChannel ? null : Uvx;
    }

    /// <summary>
    ///     The places the bundled executable can be, for an add-in assembly in <paramref name="addinDirectory" />:
    ///     the store bundle (<c>Contents\server</c>, two levels above <c>Contents\&lt;year&gt;\RevitModelMcp</c>),
    ///     then the machine-wide and per-user MSI install folders.
    /// </summary>
    public static IReadOnlyList<string> BundledCandidates(string? addinDirectory, string? programFiles, string? localAppData)
    {
        var candidates = new List<string>();
        var contents = BundleContentsFolder(addinDirectory);
        if (contents is not null)
            candidates.Add(Combine(contents, "server", ExecutableName));
        if (!string.IsNullOrWhiteSpace(programFiles))
            candidates.Add(Combine(programFiles, ProductFolder, "server", ExecutableName));
        if (!string.IsNullOrWhiteSpace(localAppData))
            candidates.Add(Combine(localAppData, "Programs", ProductFolder, "server", ExecutableName));
        return candidates;
    }

    // <bundle>\Contents\<year>\RevitModelMcp -> <bundle>\Contents. Only a folder really named Contents counts, so
    // a server planted next to a machine-wide Addins folder is never picked up.
    private static string? BundleContentsFolder(string? addinDirectory)
    {
        if (string.IsNullOrWhiteSpace(addinDirectory)) return null;
        var parts = addinDirectory!.TrimEnd('\\', '/').Split('\\', '/');
        if (parts.Length < 3) return null;
        var contents = parts.Take(parts.Length - 2).ToArray();
        return string.Equals(contents[contents.Length - 1], "Contents", StringComparison.OrdinalIgnoreCase) ? string.Join("\\", contents) : null;
    }

    /// <summary>The Claude Code registration command, as documented in the README.</summary>
    public string ClaudeCodeCommand =>
        "claude mcp add " + Name + " " + string.Join(" ", Env.Select(pair => "-e " + pair.Key + "=" + pair.Value)) +
        " -- " + string.Join(" ", new[] { Command }.Concat(Args).Select(ShellQuote));

    /// <summary>
    ///     Whether an existing entry launches the same program with the same arguments as <paramref name="spec" />.
    ///     Commands compare case-insensitively (Windows paths); arguments exactly. The environment is not compared.
    /// </summary>
    public static bool SameLaunch(string command, IReadOnlyList<string> args, McpServerSpec spec) =>
        string.Equals(command, spec.Command, StringComparison.OrdinalIgnoreCase) && args.SequenceEqual(spec.Args);

    /// <summary>A short label for the dialog text.</summary>
    public string Display => string.Join(" ", new[] { Command }.Concat(Args));

    // Windows separators regardless of the host, so a path stays valid in the clients' configuration files.
    private static string Combine(string first, params string[] rest) =>
        string.Join('\\', new[] { first.TrimEnd('\\', '/') }.Concat(rest));

    private static string ShellQuote(string value) =>
        value.Any(char.IsWhiteSpace) ? "\"" + value + "\"" : value;
}
