using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Core.Tests.Fork;

/// <summary>
/// The rules a hosted placement uses to pick its host wall, exercised without Revit: which walls can
/// carry the family at the placement's storey, how far each one is, and which single wall may be used.
/// These read as the refusal messages a caller sees, because that is the whole of the answer when the
/// search finds no single best wall.
/// </summary>
public sealed class HostSearchTests
{
    private static HostSearch.Candidate At(long id, double millimetres) => new(id, millimetres);

    [Test]
    public async Task NearestWall_TakesTheClosestWallInsideTheRadius()
    {
        var chosen = HostSearch.Nearest([At(357484, 12800.1), At(357458, 500.1), At(357593, 15200.1)], 2000);
        await Assert.That(chosen.Id).IsEqualTo(357458L);
        await Assert.That(Math.Round(chosen.DistanceMm, 1)).IsEqualTo(500.1);
    }

    [Test]
    public async Task NearestWall_RefusesWhenNothingIsInsideTheRadiusAndListsTheNearbyWalls()
    {
        await Assert.That(() => HostSearch.Nearest([At(357458, 500.1), At(357484, 12800.1), At(357593, 15200.1)], 1))
            .Throws<ArgumentException>()
            .WithMessage("No wall within hostSearchRadiusMm 1. Nearest: 357458 at 500.1 mm, 357484 at 12800.1 mm, 357593 at 15200.1 mm.");
    }

    [Test]
    public async Task NearestWall_AsksForTheHostIdWhenTwoWallsAreEquallyFar()
    {
        await Assert.That(() => HostSearch.Nearest([At(357503, 1000), At(357458, 1000)], 2000))
            .Throws<ArgumentException>()
            .WithMessage("Walls 357458 at 1000 mm, 357503 at 1000 mm are equally far from the placement point. Name one with hostElementId.");
    }

    [Test]
    public async Task NearestWall_TreatsADifferenceUnderATenthOfAMillimetreAsATie()
    {
        await Assert.That(() => HostSearch.Nearest([At(12, 1000), At(13, 1000.06)], 2000))
            .Throws<ArgumentException>()
            .WithMessage("Walls 12 at 1000 mm, 13 at 1000.1 mm are equally far from the placement point. Name one with hostElementId.");
    }

    [Test]
    public async Task NearestWall_AnswersTheRadiusBeforeTheTie()
    {
        await Assert.That(() => HostSearch.Nearest([At(12, 5000), At(13, 5000)], 2000))
            .Throws<ArgumentException>()
            .WithMessage("No wall within hostSearchRadiusMm 2000. Nearest: 12 at 5000 mm, 13 at 5000 mm.");
    }

    [Test]
    public async Task Storey_TakesAWallThatSpansTheLevel()
    {
        await Assert.That(HostSearch.SpansStorey(0, 3000, 0)).IsTrue();
        await Assert.That(HostSearch.SpansStorey(0, 3000, 1500)).IsTrue();
    }

    [Test]
    public async Task Storey_RefusesAWallThatEndsAtTheLevelAbove()
    {
        await Assert.That(HostSearch.SpansStorey(0, 3000, 3000)).IsFalse();
        await Assert.That(HostSearch.SpansStorey(3000, 6000, 0)).IsFalse();
    }

    [Test]
    public async Task RightAngle_TakesAPointInFrontOfTheWall()
    {
        await Assert.That(HostSearch.MeetsAtRightAngles(1, 0, 0, 500)).IsTrue();
    }

    [Test]
    public async Task RightAngle_RefusesAPointPastTheEndOfTheWall()
    {
        await Assert.That(HostSearch.MeetsAtRightAngles(1, 0, 800, 500)).IsFalse();
    }

    [Test]
    public async Task RightAngle_TakesADiagonalPerpendicularAtFullPrecision()
    {
        // Revit's feet for the offset (-300.00048, 400.00064) mm against a (0.8, 0.6) tangent: the dot
        // product is zero at full precision. Rounding the offsets to display millimetres first would
        // turn it into 0.0006 against a threshold of 0.0005 and refuse a true perpendicular.
        await Assert.That(
            HostSearch.MeetsAtRightAngles(0.8, 0.6, -0.98425354330708648, 1.3123380577427821)).IsTrue();
    }

    [Test]
    public async Task NearestWall_RefusesAWallAWhiskerOutsideTheRadius()
    {
        // 2000.0004 mm is outside a 2000 mm radius and must stay outside: the search compares the
        // measured distance as it is, and rounding it for the report must not let it slip in.
        await Assert.That(() => HostSearch.Nearest([At(357458, 2000.0004)], 2000))
            .Throws<ArgumentException>()
            .WithMessage("No wall within hostSearchRadiusMm 2000. Nearest: 357458 at 2000 mm.");
    }
}
