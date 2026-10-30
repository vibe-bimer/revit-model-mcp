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

    [Test]
    public async Task CreateLevel_CarriesItsElevationAndViewFlag()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"create-level","name":"L3","fork":{"elevationMm":"9000.5","createView":true}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(parsed.Action!.Name).IsEqualTo("L3");
        await Assert.That(parsed.Action!.Options.ElevationMm).IsEqualTo(9000.5);
        await Assert.That(parsed.Action!.Options.CreateView).IsTrue();
    }

    [Test]
    public async Task CreateFloor_CarriesItsLevelPointsAndType()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"create-floor","level":"L1","pointsMm":[[0,0],[4000,0],[4000,3000]],"fork":{"floorType":"Floor-Slab"}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(parsed.Action!.Level).IsEqualTo("L1");
        await Assert.That(parsed.Action!.PointsMm!.Count).IsEqualTo(3);
        await Assert.That(parsed.Action!.Options.FloorType).IsEqualTo("Floor-Slab");
    }

    [Test]
    public async Task SetPhase_CarriesBothPhasesAndKeepsAnEmptyName()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"set-phase","elementIds":[42],"fork":{"createdPhase":"","demolishedPhase":"Existing"}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(parsed.Action!.Options.CreatedPhase).IsEqualTo(string.Empty);
        await Assert.That(parsed.Action!.Options.DemolishedPhase).IsEqualTo("Existing");
    }

    [Test]
    public async Task MergePhases_CarriesSourceAndTarget()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"merge-phases","fork":{"sourcePhase":"Phase 1","targetPhase":"Phase 2"}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(parsed.Action!.Options.SourcePhase).IsEqualTo("Phase 1");
        await Assert.That(parsed.Action!.Options.TargetPhase).IsEqualTo("Phase 2");
    }

    [Test]
    public async Task ResetElementIds_TakesItsAddressesWithoutAForkBag()
    {
        var parsed = ControlJobParser.Parse("""{"command":"reset-element-ids","elementIds":[7,8]}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(parsed.Action!.ElementIds).IsEquivalentTo([7L, 8L]);
    }

    [Test]
    public async Task ResetElementIds_RefusesAForkBag()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"reset-element-ids","elementIds":[7],"fork":{"seed":1}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Invalid);
        await Assert.That(parsed.Error).IsEqualTo("reset-element-ids does not accept fork.seed.");
    }

    [Test]
    public async Task RebuildModelIds_CarriesEveryRebuildOption()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"rebuild-model-ids","view":"3D","fork":{"destinationPath":"C:/out/model.rvt","overwrite":true,"removeTemplateLevels":false,"seed":7,"duplicateNames":"rename","copies":2}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(parsed.Action!.View).IsEqualTo("3D");
        await Assert.That(parsed.Action!.Options.DestinationPath).IsEqualTo("C:/out/model.rvt");
        await Assert.That(parsed.Action!.Options.Overwrite).IsTrue();
        await Assert.That(parsed.Action!.Options.RemoveTemplateLevels).IsFalse();
        await Assert.That(parsed.Action!.Options.Seed).IsEqualTo(7);
        await Assert.That(parsed.Action!.Options.DuplicateNames).IsEqualTo("rename");
        await Assert.That(parsed.Action!.Options.Copies).IsEqualTo(2);
    }

    [Test]
    public async Task RebuildModelIds_RefusesAWholeNumberItCannotRead()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"rebuild-model-ids","fork":{"destinationPath":"C:/out/model.rvt","copies":"many"}}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Invalid);
        await Assert.That(parsed.Error).IsEqualTo("fork.copies must be a whole number.");
    }

    [Test]
    public async Task ElementIdExport_ParsesAsARead()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"export-element-ids","fields":["category","id"],"saveTo":"C:/out/ids.xlsx"}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.ExportElementIds);
        await Assert.That(parsed.Fields).IsEquivalentTo(["category", "id"]);
        await Assert.That(parsed.SaveTo).IsEqualTo("C:/out/ids.xlsx");
    }

    // The layer must not claim anything upstream answers. If the registry ever listed an upstream command,
    // it would shadow that command's arm in the executor; if it ever missed a fork command, its tools
    // would fail in the add-in with "Unknown command". Both directions are the same assertion.
    [Test]
    public async Task TheRegistryClaimsOnlyItsOwnCommands()
    {
        string[] upstream = ["move", "delete", "set-parameter", "create-wall", "batch", "export-view"];
        foreach (var command in upstream)
        {
            await Assert.That(Core.Fork.ForkRegistry.IsAction(command)).IsFalse();
        }

        foreach (var command in Core.Fork.ForkRegistry.Commands)
        {
            await Assert.That(Core.Fork.ForkRegistry.IsAction(command)).IsTrue();
            await Assert.That(upstream).DoesNotContain(command);
        }

        await Assert.That(Core.Fork.ForkRegistry.Commands).IsEquivalentTo(
        [
            "set-view-lighting", "create-level", "create-floor", "set-phase", "merge-phases",
            "reset-element-ids", "rebuild-model-ids"
        ]);
    }

    // An upstream action keeps parsing exactly as it did: the fork adds a bag reader that returns for a
    // command it does not own, so the upstream initializer is the only thing that fills the contract.
    [Test]
    public async Task AnUpstreamActionParsesWithoutForkInputs()
    {
        var parsed = ControlJobParser.Parse(
            """{"command":"move","elementIds":[7],"dxMm":100,"dyMm":0,"dzMm":0}""");
        await Assert.That(parsed.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(parsed.Action!.DxMm).IsEqualTo(100);
        await Assert.That(parsed.Action!.Options.Shadows).IsNull();
        await Assert.That(parsed.Action!.Options.DestinationPath).IsNull();
    }
}
