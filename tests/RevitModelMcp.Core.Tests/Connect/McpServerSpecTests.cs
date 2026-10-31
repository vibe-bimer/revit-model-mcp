using RevitModelMcp.Core.Connect;
using static RevitModelMcp.Core.Tests.Connect.ConnectTestSupport;

namespace RevitModelMcp.Core.Tests.Connect;

public sealed class McpServerSpecTests
{
    private const string BundledPath = @"C:\Program Files\Revit Model MCP (vibe-bimer)\server\revit-model-mcp.exe";

    // Pinned on purpose: these two literals are the only place the launcher is written out, so a changed URL, a
    // reordered argument or a dropped --from fails here instead of passing everywhere that reads the spec.
    private const string ReleaseSource =
        "https://github.com/vibe-bimer/revit-model-mcp/archive/refs/tags/v1.0.0.tar.gz#subdirectory=server";

    private const string DevelopmentSource =
        "https://github.com/vibe-bimer/revit-model-mcp/archive/refs/heads/main.tar.gz#subdirectory=server";

    [Test]
    public async Task ReleaseBuildInstallsTheTagThatCarriesItsVersion()
    {
        await Assert.That(McpServerSpec.ForkSourceFor("1.0.0")).IsEqualTo(ReleaseSource);
        await Assert.That(string.Join("|", McpServerSpec.UvxFor("1.0.0").Args)).IsEqualTo("--from|" + ReleaseSource + "|revit-model-mcp");
    }

    [Test]
    public async Task DevelopmentBuildFollowsTheMainArchiveBecauseNoTagMatchesItsVersion()
    {
        await Assert.That(McpServerSpec.ForkSourceFor("1.0.1-dev+abc123")).IsEqualTo(DevelopmentSource);
        await Assert.That(string.Join("|", McpServerSpec.UvxFor("1.0.1-dev").Args)).IsEqualTo("--from|" + DevelopmentSource + "|revit-model-mcp");
    }

    [Test]
    public async Task TheShippedLauncherAlwaysNamesThisForkAndNeverThePackageNameAlone()
    {
        await Assert.That(McpServerSpec.Uvx.Command).IsEqualTo("uvx");
        await Assert.That(McpServerSpec.Uvx.Args.Count).IsEqualTo(3);
        await Assert.That(McpServerSpec.Uvx.Args[0]).IsEqualTo("--from");
        await Assert.That(McpServerSpec.Uvx.Args[1]).StartsWith("https://github.com/vibe-bimer/revit-model-mcp/archive/refs/");
        await Assert.That(McpServerSpec.Uvx.Args[1]).EndsWith("#subdirectory=server");
        await Assert.That(McpServerSpec.Uvx.Args[2]).IsEqualTo("revit-model-mcp");
    }

    [Test]
    public async Task ClaudeCodeCommandMatchesTheDocumentedLocalRegistration() =>
        await Assert.That(McpServerSpec.UvxFor("1.0.0").ClaudeCodeCommand)
            .IsEqualTo("claude mcp add revit-model-mcp -e REVIT_MCP_HOST=local -e REVIT_MCP_REDACT_PATHS=1 -- uvx --from " + ReleaseSource + " revit-model-mcp");

    [Test]
    public async Task ClaudeCodeCommandQuotesTheBundledPathWithSpaces() =>
        await Assert.That(McpServerSpec.ForExecutable(BundledPath).ClaudeCodeCommand)
            .IsEqualTo("claude mcp add revit-model-mcp -e REVIT_MCP_HOST=local -e REVIT_MCP_REDACT_PATHS=1 -- \"" + BundledPath + "\"");

    [Test]
    public async Task ResolvePrefersTheFirstExistingBundledExecutable()
    {
        var spec = McpServerSpec.Resolve([@"C:\a\revit-model-mcp.exe", @"C:\b\revit-model-mcp.exe", @"C:\c\revit-model-mcp.exe"],
            path => path != @"C:\a\revit-model-mcp.exe");
        await Assert.That(spec!.Command).IsEqualTo(@"C:\b\revit-model-mcp.exe");
        await Assert.That(spec!.Args).IsEmpty();
    }

    [Test]
    public async Task ResolveFallsBackToUvxWhenNothingIsBundled()
    {
        await Assert.That(McpServerSpec.Resolve(["x.exe"], _ => false)).IsEqualTo(McpServerSpec.Uvx);
        await Assert.That(McpServerSpec.Resolve([], _ => true)).IsEqualTo(McpServerSpec.Uvx);
        await Assert.That(McpServerSpec.Uvx.Command).IsEqualTo("uvx");
    }

    [Test]
    public async Task ResolveSkipsBlankCandidates() =>
        await Assert.That(McpServerSpec.Resolve([" ", ""], _ => true)).IsEqualTo(McpServerSpec.Uvx);

    [Test]
    public async Task BundledCandidatesListBundleThenMachineThenUserFolders()
    {
        var candidates = McpServerSpec.BundledCandidates(
            @"C:\Users\Ann\AppData\Roaming\Autodesk\ApplicationPlugins\Model MCP.bundle\Contents\2025\RevitModelMcp",
            @"C:\Program Files", @"C:\Users\Ann\AppData\Local");
        await Assert.That(candidates).IsEquivalentTo(
        [
            @"C:\Users\Ann\AppData\Roaming\Autodesk\ApplicationPlugins\Model MCP.bundle\Contents\server\revit-model-mcp.exe",
            @"C:\Program Files\Revit Model MCP (vibe-bimer)\server\revit-model-mcp.exe",
            @"C:\Users\Ann\AppData\Local\Programs\Revit Model MCP (vibe-bimer)\server\revit-model-mcp.exe"
        ]);
    }

    [Test]
    public async Task BundleLayoutResolvesToTheServerInTheBundle()
    {
        const string server = @"C:\B\Model MCP.bundle\Contents\server\revit-model-mcp.exe";
        var spec = McpServerSpec.Resolve(
            McpServerSpec.BundledCandidates(@"C:\B\Model MCP.bundle\Contents\2026\RevitModelMcp", @"C:\Program Files", null),
            path => path == server, storeChannel: true);
        await Assert.That(spec!.Command).IsEqualTo(server);
    }

    [Test]
    public async Task MsiInstallFoldersResolve()
    {
        const string machine = @"C:\Program Files\Revit Model MCP (vibe-bimer)\server\revit-model-mcp.exe";
        const string user = @"C:\Users\Ann\AppData\Local\Programs\Revit Model MCP (vibe-bimer)\server\revit-model-mcp.exe";
        var candidates = McpServerSpec.BundledCandidates(@"C:\ProgramData\Autodesk\Revit\Addins\2025\RevitModelMcp", @"C:\Program Files", @"C:\Users\Ann\AppData\Local");
        await Assert.That(McpServerSpec.Resolve(candidates, path => path == machine, storeChannel: true)!.Command).IsEqualTo(machine);
        await Assert.That(McpServerSpec.Resolve(candidates, path => path == user, storeChannel: true)!.Command).IsEqualTo(user);
    }

    [Test]
    public async Task ServerPlantedBesideTheAddinsFolderIsNeverACandidate()
    {
        var candidates = McpServerSpec.BundledCandidates(@"C:\ProgramData\Autodesk\Revit\Addins\2025\RevitModelMcp", null, null);
        await Assert.That(candidates).IsEmpty();
    }

    [Test]
    public async Task StoreChannelWithNothingFoundReturnsNoSpec()
    {
        await Assert.That(McpServerSpec.Resolve(["x.exe"], _ => false, storeChannel: true)).IsNull();
        await Assert.That(McpServerSpec.Resolve(["x.exe"], _ => false)).IsEqualTo(McpServerSpec.Uvx);
    }

    [Test]
    public async Task BundledCandidatesTolerateTrailingSeparatorsAndMissingRoots()
    {
        await Assert.That(McpServerSpec.BundledCandidates(@"C:\x\Contents\2025\RevitModelMcp\", null, "")).IsEquivalentTo([@"C:\x\Contents\server\revit-model-mcp.exe"]);
        await Assert.That(McpServerSpec.BundledCandidates(null, null, null)).IsEmpty();
    }

    [Test]
    public async Task JsonEntryUsesTheBundledExecutableWithEscapedWindowsPath()
    {
        var text = JsonConfigEditor.Add(Desktop, "", McpServerSpec.ForExecutable(BundledPath))!;
        await Assert.That(text).Contains(@"""command"": ""C:\\Program Files\\Revit Model MCP (vibe-bimer)\\server\\revit-model-mcp.exe""");
        await Assert.That(text).Contains(@"""args"": []");
        await Assert.That(text).Contains(@"""REVIT_MCP_HOST"": ""local""");
        await Assert.That(JsonConfigEditor.Inspect(Desktop, text).State).IsEqualTo(McpClientState.Configured);
    }

    [Test]
    public async Task TomlEntryUsesTheBundledExecutableWithEscapedWindowsPath()
    {
        var text = TomlConfigEditor.Add("", McpServerSpec.ForExecutable(BundledPath))!;
        await Assert.That(text).IsEqualTo(
            "[mcp_servers.revit-model-mcp]\ncommand = \"C:\\\\Program Files\\\\Revit Model MCP (vibe-bimer)\\\\server\\\\revit-model-mcp.exe\"\nargs = []\n\n" +
            "[mcp_servers.revit-model-mcp.env]\nREVIT_MCP_HOST = \"local\"\nREVIT_MCP_REDACT_PATHS = \"1\"\n");
        await Assert.That(TomlConfigEditor.Inspect(Codex, text).State).IsEqualTo(McpClientState.Configured);
    }

    [Test]
    public async Task ConfiguratorWritesTheChosenSpecAndRemovesIt()
    {
        using var temp = new TempDirectory();
        Directory.CreateDirectory(temp.Combine(".cursor"));
        var target = new McpClientTarget("cursor", "Cursor", temp.Combine(".cursor"), temp.Combine(".cursor", "mcp.json"),
            McpConfigFormat.Json);
        var configurator = new McpClientConfigurator(spec: McpServerSpec.ForExecutable(BundledPath));
        await Assert.That(configurator.Add(target).Changed).IsTrue();
        await Assert.That(File.ReadAllText(target.ConfigPath)).Contains(@"C:\\Program Files\\Revit Model MCP (vibe-bimer)\\server\\revit-model-mcp.exe");
        await Assert.That(configurator.Remove(target).Changed).IsTrue();
        await Assert.That(configurator.Inspect(target).State).IsEqualTo(McpClientState.NotConfigured);
    }
}
