# 0008. The bounded fork layer as built on the upstream 1.0 base

- Status: Accepted
- Date: 2026-10-31
- Amends: [0005](0005-attach-fork-actions-through-an-external-registry.md), [0003](0003-ship-read-only-by-default-through-the-policy.md), [0006](0006-port-on-2026-first-restore-revit-2020-as-required-follow-up.md)

## Context

[0005](0005-attach-fork-actions-through-an-external-registry.md) fixed the seam and predicted a footprint of seven
dispatch hooks inside 80 changed lines. Building the eight actions on the base disproved the count in two places and
proved the budget. This record states what the layer actually is, so the next rebase starts from measurements rather
than from the estimate.

## Base

The port starts at upstream commit `760bb7c21337abb2a2aec21434e1d208e01e6cc0` (v1.0.0 plus eleven fixes). Every
change in the layer is measured against that commit.

## Decision

The layer is as 0005 describes it, with four corrections.

1. **Nine hand-written upstream sites, not seven.** Eight are dispatch: the advertised command list, the action
   executor, the pre-transaction rebuild branch, the verifier's before and after arms, the summary fallback, the
   activity-title merge and the job parser's action test. The ninth is the read dispatcher, added because the element
   identifier register changes no model state: routing it through the action pipeline would meet the no-change guard,
   which rolls an empty commit back, so it would have needed an upstream policy file edited to make a read write.
   It travels as a read instead, in the shape upstream's own `export-view` uses.
2. **The element identifier register costs eleven upstream lines** (a job kind, a `saveTo` field, a dispatch arm and a
   parser method), taking the hand-written total to 98 insertions across 15 files. The seven original dispatch hooks
   alone are 50 lines, so the 80-line bound holds for what 0005 measured it against; the bound was never a bound on
   the read side, which 0005 did not cover.
3. **`tools/list` budget raised from 105,000 to 112,000 bytes** in `server/tests/test_toolsets.py`. Upstream set the
   guard for its own 79 tools, where it measured 100,671 bytes. Eight fork tools with 54 input properties cost about
   8,700 bytes of schema no trimming can remove; the fork's own descriptions are 2,434 bytes. The guard keeps its
   purpose — a payload that grows without an owner fails — and now measures a surface that includes the fork.
4. **One new refusal is deliberate.** `reset-element-ids` refuses an empty element list. The trunk reached the same
   place only by failing later, with no message that named the cause.

The verification delta is carried as one extra object on `ActionFacts` (`lighting`, `fork`) and one on
`ActionResultData` (`fork`), so the fork's facts stay in the fork's own types rather than widening upstream's fields.

## Read-only by default

[0003](0003-ship-read-only-by-default-through-the-policy.md) said read-only becomes the default and the policy becomes
the only gate on writes. The base satisfied the second half on its own: `REVIT_MCP_ALLOW_WRITE` is retired, and the
installer already writes `ReadOnly` to `HKLM\Software\Policies\RevitModelMcp` when told to. The first half is one
line here: `READONLY` defaults to `1` in `build/install/Installer.Policy.cs`, so a fresh install is read-only and a
workstation that accepts writes says `READONLY=0` on the command line. The default writes through the same ownership
rule as before — the installer still remembers only what it wrote, never a value policy owns.

The default `policy.json` that 0003 also asked for is **not** shipped yet. Writing it needs a component-conditional
file and an uninstall removal, because the uninstall script deliberately keeps `%ProgramData%\RevitModelMcp` when a
`policy.json` is present. Nothing in that path can be verified without a Windows build and a real uninstall, and a
mistake there would leave every fresh install read-only with no supported way out. The work belongs in a change whose
author can run the MSI.

## Consequences

A rebase of the fork onto a newer upstream touches nine sites and roughly 98 lines. Reading the list above is enough
to find them: `rg 'Fork\.' src/` returns every one.

Revit 2020 stays out of the port, as [0006](0006-port-on-2026-first-restore-revit-2020-as-required-follow-up.md)
requires. The floor action calls `Floor.Create` without a version guard because the add-in has no Revit 2020 build
configuration; the guard returns with the 2020 configuration.

## Alternatives rejected

**Carry the trunk's 50 conflicted files.** [0001](0001-base-on-upstream-with-a-bounded-fork-layer.md) rejected it and
the measurements here do not reopen it.

**Raise the budget by trimming upstream descriptions.** The fork already spends 2,434 bytes on its own eight tools.
Paying for a fork decision with upstream text is spending someone else's budget.
