using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Core.Tests.Fork;

/// <summary>
/// The fork's action inputs ride in one bag on the read job, so these tests drive the real wire path:
/// JSON in, parsed action out. See adr/0005.
/// </summary>
public sealed class ForkInputTests
{
    [Test]
    public async Task ForkBag_ReachesTheActionContract()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"set-view-lighting","view":"L1","fork":{"shadows":true,"shadowIntensity":40}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(parsed.Action!.Options.Shadows).IsTrue();
        await Assert.That(parsed.Action!.Options.ShadowIntensity).IsEqualTo(40);
    }

    [Test]
    public async Task ForkBag_CoercesTextNumbersAndColorLists()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"set-view-lighting","view":"L1","fork":{"sunAzimuthDeg":"135.5","background":"gradient","backgroundColors":["#C8DEF0","#F5F5F5","#BFBFBF"]}}""");
        await Assert.That(parsed.Action!.Options.SunAzimuthDeg).IsEqualTo(135.5);
        await Assert.That(parsed.Action!.Options.BackgroundColors).IsEquivalentTo(["#C8DEF0", "#F5F5F5", "#BFBFBF"]);
    }

    [Test]
    public async Task ForkBag_AbsentLeavesEveryForkInputEmpty()
    {
        var parsed = ControlJobParser.Parse("""{"command":"set-view-lighting","view":"L1"}""");
        await Assert.That(parsed.Action!.Options.Shadows).IsNull();
        await Assert.That(parsed.Action!.Options.BackgroundColors).IsNull();
    }

    [Test]
    public async Task ForkBag_RefusesAKeyTheCommandDoesNotAccept()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"set-view-lighting","view":"L1","fork":{"sunIntensity":40}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Invalid);
        await Assert.That(parsed.Error).IsEqualTo("set-view-lighting does not accept fork.sunIntensity.");
    }

    [Test]
    public async Task ForkBag_RefusesAValueOfTheWrongType()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"set-view-lighting","view":"L1","fork":{"shadows":"sometimes"}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Invalid);
        await Assert.That(parsed.Error).IsEqualTo("fork.shadows must be true or false.");
    }

    [Test]
    public async Task ForkBag_IsRefusedOnACommandWithoutForkInputs()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"move","elementIds":[1],"dxMm":10,"fork":{"shadows":true}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Invalid);
        await Assert.That(parsed.Error).IsEqualTo("move accepts no fork inputs.");
    }
}
