# 0002. Rewrite the eight fork actions by remapping contracts, not by rewriting them

- Status: Accepted
- Date: 2026-10-30

## Context

The eight actions carry most of this fork's value: element-id export, reset, and a model rebuild that spans two documents; floor, level, phase, phase-merge and view-lighting creation. Their code is not the valuable part. Their behaviour is.

Evidence that behaviour, not code, is the asset: the rebuild action alone took 22 commits to become correct. Each commit records a Revit fact that cannot be guessed from the API surface. MEP system members cannot be treated as ordinary elements. Each element needs its own sub-transaction or one failure loses the rest. Sketch lines and reference planes must be excluded or the rebuild corrupts the model. Copies need rehosting and their joins restored, or the geometry silently detaches. Revit raises a duplicate-name dialog that must be answered rather than bypassed. Pasted types must be cleared. Copy retries must be refused, or the farm produces a model with two of everything.

The contract those actions are written against changed in 1.0. `ActionJobContract` and `ActionResultData` grew, several argument names moved (`save_to` became `output_path`), the step vocabulary is a closed union, and the verification DTO already carries most of the fields the fork needed to add.

## Decision

Rewrite by remapping contracts. Keep the behaviour.

The test for what survives: read a line of the action body. If it calls the Revit API, it stays. If it names a fork DTO field or a fork argument, it gets remapped onto the upstream shape. A line that does neither is dead and goes.

Concretely:

- Argument names follow upstream. The fork invents no new names for things upstream already names.
- Verification fields that upstream already has are not duplicated. `ActionFacts` already reports elements, ids, category, bounding box, family, type, level, parameter, value, storage type, owner, requested dependents, and still-present. The fork appends only its genuine difference: name, elevation in millimetres, the four phase fields, the two reassignment flags, the remaining-source count, and the lighting block.
- Every action keeps its `dry_run` and its verification block. That is the fork's product thesis, not an upstream feature.
- No action saves the model. Upstream's rule holds.

## Consequences

The rewrite is a per-action exercise in reading two contracts side by side. Expect each action to lose lines rather than gain them, because upstream already implements the neighbouring cases.

Behaviour that depends on a fork-side helper with no upstream equivalent must be re-derived, or re-hosted in the fork layer. The rebuild action is the extreme case: its 1003-line body is behaviour the fork must keep and upstream has no place for.

A line-by-line port would drag the v0.5.x DTOs along and force a second schema in the same assembly. That is the failure mode this decision exists to prevent.

## Alternatives rejected

**Rewrite from scratch.** Tempting because the upstream contracts are cleaner. Rejected: it discards the 22 commits of Revit facts that are the actual asset, and nobody can re-derive them from the API reference.

**Lift the actions as they are.** Fastest to compile, and it drags the fork's old DTOs, old argument names and old verification model into a new base. The result would be two contracts for the same concept in one assembly, which is the state the merge alternative in ADR 0001 produces anyway.
