using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Core.Tests.Fork;

internal sealed class UnitSpecNamesTests
{
    [Test]
    public async Task SpecForUnit_KeepsTheSpelledOutIdentifiersTheCaptureSurfaceReliesOn()
    {
        await Assert.That(UnitSpecNames.SpecForUnit("UT_Length")).IsEqualTo("autodesk.spec.aec:length-2.0.0");
        await Assert.That(UnitSpecNames.SpecForUnit("UT_Area")).IsEqualTo("autodesk.spec.aec:area-2.0.0");
        await Assert.That(UnitSpecNames.SpecForUnit("UT_Volume")).IsEqualTo("autodesk.spec.aec:volume-2.0.0");
        await Assert.That(UnitSpecNames.SpecForUnit("UT_Angle")).IsEqualTo("autodesk.spec:angle-1.0.0");
        await Assert.That(UnitSpecNames.SpecForUnit("UT_Number")).IsEqualTo("autodesk.spec:number-1.0.0");
    }

    [Test]
    public async Task SpecForUnit_DerivesTheIdentifierForEveryOtherUnitType()
    {
        await Assert.That(UnitSpecNames.SpecForUnit("UT_Mass_per_Unit_Length"))
            .IsEqualTo("autodesk.spec.unit:massPerUnitLength-1.0.0");
    }

    [Test]
    public async Task SpecForParameterType_MarksTheKindsTheCaptureSurfaceClassifiesOn()
    {
        await Assert.That(UnitSpecNames.SpecForParameterType("Text")).Contains("spec:string");
        await Assert.That(UnitSpecNames.SpecForParameterType("URL")).Contains("spec:string");
        await Assert.That(UnitSpecNames.SpecForParameterType("YesNo")).Contains("yesno");
        await Assert.That(UnitSpecNames.SpecForParameterType("Integer")).Contains("int");
    }

    [Test]
    public async Task SpecForParameterType_FallsBackToTheDerivedNameForAnUnlistedType()
    {
        await Assert.That(UnitSpecNames.SpecForParameterType("Force"))
            .IsEqualTo("autodesk.spec.unit:force-1.0.0");
    }

    [Test]
    public async Task UnitFor_NamesTheUnitOfADisplayUnit()
    {
        await Assert.That(UnitSpecNames.UnitFor("DUT_MILLIMETERS"))
            .IsEqualTo("autodesk.unit.unit:millimeters-1.0.0");
        await Assert.That(UnitSpecNames.UnitFor("DUT_SQUARE_METERS"))
            .IsEqualTo("autodesk.unit.unit:squareMeters-1.0.0");
    }

    [Test]
    public async Task GroupFor_NamesTheGroupOfAParameterGroup()
    {
        await Assert.That(UnitSpecNames.GroupFor("PG_IDENTITY_DATA"))
            .IsEqualTo("autodesk.parameter.group:identityData-1.0.0");
    }

    [Test]
    public async Task IsMeasurableUnit_AnswersOnlyForAUnitThatCarriesAMeasurement()
    {
        await Assert.That(UnitSpecNames.IsMeasurableUnit("UT_Length")).IsTrue();
        await Assert.That(UnitSpecNames.IsMeasurableUnit("UT_Undefined")).IsFalse();
        await Assert.That(UnitSpecNames.IsMeasurableUnit(null)).IsFalse();
    }
}
