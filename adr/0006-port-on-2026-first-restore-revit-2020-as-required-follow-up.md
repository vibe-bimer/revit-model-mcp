# 0006. Port on 2026 first, restore Revit 2020 as a required follow-up

- Status: Accepted
- Date: 2026-10-30
- Revises: the initial deferral of Revit 2020 recorded before the workstation years were confirmed

## Context

This fork supports Revit 2020. Upstream 1.0 supports 2022 through 2027, one build configuration per year, each pinned to the lowest build of that year through `MinimumRevitApiPackageVersion` and the `RevitApiReferencePin` build step.

The fork's 2020 support is not a configuration flag. It is a 305-line compatibility layer under `src/RevitModelMcp.Addin/Compatibility/`: `ParameterDataType.cs` (172 lines), `RevitUnits.cs` (93), `BasePoints.cs` (40). It exists because the 2020 API package this fork builds against is a later revision than the one on the actual workstation, and the difference is around ninety missing members. The fork also reaches 2020 by widening the version range, where upstream pins an exact build per year.

The workstations that matter run Revit 2020 and Revit 2026. Both are primary years, not one primary and one legacy. That fact changes the standing of 2020: it is not a nice-to-have that can quietly lapse, it is a support commitment with a deadline.

The upstream pin mechanism cannot express "2020 with a substitute for ninety missing members". The fork's floating version range can, which is why the compatibility layer exists at all.

## Decision

Sequence, not a question of whether.

1. Port the eight actions on 2022 through 2027, using upstream's year configuration as shipped. The tracer action and the rebuild run on 2026.
2. Revit 2020 is a required follow-up inside the same effort, not a deferred maybe and not a drop. Its deadline is the first fork release after the port, so that no shipped fork release is 2020-blind.
3. When 2020 lands, it goes behind upstream's pin mechanism: one year configuration for 2020 pinned to the build the workstations actually run, with the compatibility layer supplying the missing members. The floating version range retires.
4. Until then, the compatibility layer stays in the tree as source material. It does not get a fourth year configuration bolted on while the port is in flight.

## Consequences

The port itself is not blocked on 2020, and a failure during the port is unambiguous: it is the port, not the old year.

The first release after the port carries a visible gap for 2020 workstations, closed in the next release. The release notes must say both the gap and the date.

The 2020 work is more than a build configuration: the compatibility layer must be checked against the rewritten actions, because the actions call the exact API surface the layer substitutes for. Expect the `Compatibility/` directory to grow before it shrinks.

Users on 2020 keep running the current release until the follow-up lands. That is stated, dated, and short.

## Alternatives rejected

**Solve 2020 in the same change as the port.** Doubles the build matrix and the compatibility surface in the change that already re-expresses eight actions. A failure would be ambiguous between "the port is wrong" and "2020 is wrong".

**Drop 2020.** Rejected outright once the workstation years were confirmed: half the primary fleet runs it.
