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
   parser method), taking the hand-written total to 99 insertions across 12 files. Measured against the base, the
   six dispatch hooks in `build/fork.json` are 42 insertions and 48 changed lines, and the three read-side sites the
   budget also carries (`ControlJobParser.cs`, `ReadCommandExecutor.cs`, `ActionVerificationModels.cs`) are 25 changed
   lines, so the layer spends 73 of its 80 changed lines on hand-written upstream code. The bound now measures every
   hand-written site, including the read side, which 0005 did not cover.
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

The default `policy.json` that 0003 also asked for ships with the MultiUser MSI. `build/install/Installer.Scripts.cs`
holds the shipped content and a script that writes it to `%ProgramData%\RevitModelMcp` only where no file exists, so
an administrator's file survives a repair and an upgrade; uninstall deletes it only while it still holds exactly the
shipped default, and then removes the folder only when nothing else is left in it. All three behaviours are asserted in
`InstallerScriptsTests`; the MSI run itself needs a Windows workstation.

Two gaps stay open. A SingleUser (per-user) install cannot write machine policy, writes no `policy.json`, and neither
reader consults a per-user source, so that install is read-write until an administrator configures the machine; the
store channel builds that same package. Closing the gap needs a decision 0003 did not make: either a per-user policy
source, or a single machine-scope install.

A server started from source — `uvx`, a wheel or a source archive without the MSI — has no machine policy either, so
it is read-write unless something else refuses. The documented registrations therefore pass `REVIT_MCP_READ_ONLY=1`,
which the server already honours as a force, and the reader who wants actions on such a machine sets it to `0`. That
keeps the promise the pages make without inventing a second gate.

## Consequences

A rebase of the fork onto a newer upstream touches nine sites and roughly 99 lines. Reading the list above is enough
to find them: `rg 'Fork\.' src/` returns every one, and `python build/check_fork_budget.py` fails when a site the
budget does not know about appears.

Revit 2020 stays out of the port, as [0006](0006-port-on-2026-first-restore-revit-2020-as-required-follow-up.md)
requires. The floor action calls `Floor.Create` without a version guard because the add-in has no Revit 2020 build
configuration; the guard returns with the 2020 configuration.

## Alternatives rejected

**Carry the trunk's 50 conflicted files.** [0001](0001-base-on-upstream-with-a-bounded-fork-layer.md) rejected it and
the measurements here do not reopen it.

**Raise the budget by trimming upstream descriptions.** The fork already spends 2,434 bytes on its own eight tools.
Paying for a fork decision with upstream text is spending someone else's budget.
