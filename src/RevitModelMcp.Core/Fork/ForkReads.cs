namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The fork's own read commands. A read is dispatched by upstream's read path rather than by the action
/// registry, so it is listed here: the add-in advertises this list in its handshake, and a client that reads
/// the handshake learns the command exists. See adr/0008.
/// </summary>
public static class ForkReads
{
    /// <summary>Wire commands the fork adds to the read surface.</summary>
    public static IReadOnlyList<string> Commands { get; } = ["export-element-ids"];
}
