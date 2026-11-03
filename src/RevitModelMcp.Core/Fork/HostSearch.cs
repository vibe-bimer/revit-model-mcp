using System.Globalization;

namespace RevitModelMcp.Core.Fork;

/// <summary>
/// The host search a hosted placement runs before it creates anything: which walls can carry the family
/// at the placement's storey, how far each one is, and which single wall the placement may use.
/// Kept out of the add-in so the rules that decide a host - the storey span, the foot of the
/// perpendicular, the range before the tie - are tested without Revit.
/// </summary>
public static class HostSearch
{
    /// <summary>The search radius a caller gets when it names none.</summary>
    public const double DefaultRadiusMm = 2000;

    /// <summary>
    /// A wall is "equally far" from the point when the two distances differ by less than this. A tenth
    /// of a millimetre is the precision a model is drawn at, so a smaller difference is a modelling
    /// accident and not a reason to pick one wall over the other.
    /// </summary>
    public const double TieToleranceMm = 0.1;

    /// <summary>How many near walls a refusal lists.</summary>
    public const int CandidateCount = 5;

    /// <summary>One wall that can host the family, with its distance from the placement point.</summary>
    /// <param name="Id">The wall's element id, as the wire reports it.</param>
    /// <param name="DistanceMm">Distance to the wall's location line in millimetres, unrounded.</param>
    public readonly record struct Candidate(long Id, double DistanceMm);

    /// <summary>Whether a wall spanning <paramref name="baseMm"/> to <paramref name="topMm"/> sits at the level.</summary>
    /// <remarks>
    /// The top is open: a wall that stops at the level above belongs to the storey below it, and a
    /// wall that starts at this level belongs to this one. The tolerance keeps a wall drawn to the
    /// millimetre from falling out of its own storey.
    /// </remarks>
    public static bool SpansStorey(double baseMm, double topMm, double levelMm) =>
        levelMm >= baseMm - TieToleranceMm && levelMm < topMm - TieToleranceMm;

    /// <summary>Whether the offset from the foot to the point crosses the wall's run at a right angle.</summary>
    /// <remarks>
    /// A projection that ran to the end of the wall is not the foot of a perpendicular: the point
    /// stands beside the wall, not in front of it, so that wall does not host it. Measuring the angle
    /// keeps that rule whatever clamping the projection itself does. Both sides scale with the unit,
    /// so the test reads the same in millimetres as in Revit's feet - but only for unrounded inputs:
    /// the caller must pass the raw offsets, because rounding them first puts the rounding error into
    /// the product and with it true perpendiculars that fail the test.
    /// </remarks>
    public static bool MeetsAtRightAngles(double tangentX, double tangentY, double dxMm, double dyMm)
    {
        var run = Math.Sqrt((tangentX * tangentX) + (tangentY * tangentY));
        var offset = Math.Sqrt((dxMm * dxMm) + (dyMm * dyMm));
        if (run <= 1e-9) return true;
        if (offset <= 1e-9) return true;
        var along = Math.Abs((dxMm * tangentX) + (dyMm * tangentY));
        return along <= 1e-6 * offset * run;
    }

    /// <summary>The closest wall, refused when it is out of range or when another wall ties with it.</summary>
    /// <remarks>
    /// The range is answered before the tie: a search that found nothing inside its radius owed no tie
    /// verdict. A tie is the caller's decision, not the tool's - two walls equally far means the intent
    /// is unknown - so it is refused rather than guessed. Ordering is by distance, then by id, so the
    /// same document always yields the same answer.
    /// </remarks>
    public static Candidate Nearest(IReadOnlyList<Candidate> candidates, double radiusMm)
    {
        if (candidates.Count == 0) throw new ArgumentException("The placement point has no wall to search.");
        var ordered = candidates.OrderBy(candidate => candidate.DistanceMm)
            .ThenBy(candidate => candidate.Id)
            .ToList();
        var nearest = ordered[0];

        if (nearest.DistanceMm > radiusMm)
            throw new ArgumentException(
                $"No wall within hostSearchRadiusMm {Number(radiusMm)}. Nearest: {Describe(ordered)}.");

        var equallyNear = ordered
            .TakeWhile(candidate => candidate.DistanceMm - nearest.DistanceMm <= TieToleranceMm)
            .ToList();
        if (equallyNear.Count > 1)
            throw new ArgumentException(
                $"Walls {Describe(equallyNear)} are equally far from the placement point. "
                + "Name one with hostElementId.");

        return nearest;
    }

    /// <summary>The near walls as <c>id at distance mm</c>, closest first, for a refusal to name.</summary>
    public static string Describe(IReadOnlyList<Candidate> candidates) =>
        string.Join(", ", candidates.Take(CandidateCount).Select(candidate =>
            $"{candidate.Id} at {Number(Math.Round(candidate.DistanceMm, 1))} mm"));

    private static string Number(double value) => value.ToString("R", CultureInfo.InvariantCulture);
}
