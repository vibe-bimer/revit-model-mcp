using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Core.Tests.Control;

public sealed class ViewLightingTests
{
    [Test]
    public async Task Parse_SetViewLighting_KeepsEverySetting()
    {
        var result = ControlJobParser.Parse(
            """
            {"command":"set-view-lighting","view":" {3D} ","shadows":true,"shadowIntensity":40,
             "sunlightIntensity":70,"sunDate":" 2026-03-01 ","sunTime":"09:30","groundPlane":true,
             "groundPlaneLevel":" 01 ","background":" Gradient ","backgroundColors":["#C8DEF0","#F5F5F5","#BFBFBF"],
             "lightingScheme":" Interior-Sun-And-Artificial ","dryRun":true}
            """);

        await Assert.That(result.Kind).IsEqualTo(ControlJobKind.Action);
        var action = result.Action!;
        await Assert.That(action.View).IsEqualTo("{3D}");
        await Assert.That(action.Shadows).IsTrue();
        await Assert.That(action.ShadowIntensity).IsEqualTo(40);
        await Assert.That(action.SunlightIntensity).IsEqualTo(70);
        await Assert.That(action.SunDate).IsEqualTo("2026-03-01");
        await Assert.That(action.SunTime).IsEqualTo("09:30");
        await Assert.That(action.GroundPlane).IsTrue();
        await Assert.That(action.GroundPlaneLevel).IsEqualTo("01");
        await Assert.That(action.Background).IsEqualTo("gradient");
        await Assert.That(action.BackgroundColors).IsEquivalentTo(new[] { "#C8DEF0", "#F5F5F5", "#BFBFBF" });
        await Assert.That(action.LightingScheme).IsEqualTo("interior-sun-and-artificial");
        await Assert.That(action.DryRun).IsTrue();
        await Assert.That(action.ElementIds).IsEmpty();
    }

    [Test]
    public async Task Parse_SetViewLighting_KeepsAFixedSunPosition()
    {
        var result = ControlJobParser.Parse(
            """{"command":"set-view-lighting","view":"{3D}","sunAzimuthDeg":135,"sunAltitudeDeg":45}""");

        await Assert.That(result.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(result.Action!.SunAzimuthDeg).IsEqualTo(135);
        await Assert.That(result.Action.SunAltitudeDeg).IsEqualTo(45);
    }

    [Test]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}"}""")]
    [Arguments("""{"command":"set-view-lighting","view":" "}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","shadowIntensity":101}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","sunlightIntensity":-1}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","sunDate":"2026-3-1"}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","sunTime":"9:30"}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","sunAzimuthDeg":90}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","sunAltitudeDeg":20}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","sunAzimuthDeg":400,"sunAltitudeDeg":20}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","sunAzimuthDeg":90,"sunAltitudeDeg":120}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","background":"solid"}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","backgroundColors":["#FFFFFF","#FFFFFF","#FFFFFF"]}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","background":"gradient","backgroundColors":["#FFFFFF","#FFFFFF"]}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","background":"gradient","backgroundColors":["#FFFFFF","#FFFFFF","white"]}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","lightingScheme":"exterior-moon"}""")]
    [Arguments("""{"command":"set-view-lighting","view":"{3D}","groundPlaneLevel":"  "}""")]
    public async Task Parse_SetViewLighting_RejectsAnUnusableRequest(string json)
    {
        var result = ControlJobParser.Parse(json);

        await Assert.That(result.Kind).IsEqualTo(ControlJobKind.Invalid);
    }

    [Test]
    public async Task Parse_SetViewLighting_IsABatchStep()
    {
        var result = ControlJobParser.Parse(
            """{"command":"batch","steps":[{"command":"set-view-lighting","view":"{3D}","shadows":true}]}""");

        await Assert.That(result.Kind).IsEqualTo(ControlJobKind.Action);
        await Assert.That(result.Action!.Steps[0].Action!.Shadows).IsTrue();
    }

    [Test]
    public async Task Differences_NamesEveryChangedSetting()
    {
        var before = new ViewLightingFacts
        {
            Shadows = false,
            ShadowIntensity = 50,
            SunType = "OneDayStudy",
            SunDateAndTimeUtc = "2026-03-01T01:00:00Z",
            Background = "None",
            BackgroundColors = ["#FFFFFF", "#FFFFFF", "#FFFFFF"],
            LightingScheme = "exterior-sun"
        };
        var after = new ViewLightingFacts
        {
            Shadows = true,
            ShadowIntensity = 50,
            SunType = "StillImage",
            SunDateAndTimeUtc = "2026-03-01T01:30:00Z",
            Background = "Gradient",
            BackgroundColors = ["#C8DEF0", "#F5F5F5", "#BFBFBF"],
            LightingScheme = "interior-sun-and-artificial"
        };

        var changed = ViewLightingComparison.Differences(before, after);

        await Assert.That(changed).IsEquivalentTo(
            new[] { "shadows", "sun_type", "sun_date_time", "background", "background_colors", "lighting_scheme" });
    }

    [Test]
    public async Task Differences_IsEmptyForAnUnchangedReadingOrAMissingOne()
    {
        var facts = new ViewLightingFacts { Shadows = true, ShadowIntensity = 25 };

        await Assert.That(ViewLightingComparison.Differences(facts, new ViewLightingFacts { Shadows = true, ShadowIntensity = 25 })).IsEmpty();
        await Assert.That(ViewLightingComparison.Differences(facts, null)).IsEmpty();
        await Assert.That(ViewLightingComparison.Differences(null, facts)).IsEmpty();
    }

    [Test]
    public async Task Differences_ComparesGradientColorsAsAWhole()
    {
        var before = new ViewLightingFacts { BackgroundColors = ["#C8DEF0", "#F5F5F5", "#BFBFBF"] };
        var after = new ViewLightingFacts { BackgroundColors = ["#C8DEF0", "#F5F5F5", "#808080"] };

        await Assert.That(ViewLightingComparison.Differences(before, after)).IsEquivalentTo(new[] { "background_colors" });
    }
}
