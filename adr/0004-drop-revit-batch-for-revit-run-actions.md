# 0004. Drop the fork's revit_batch and use upstream revit_run_actions

- Status: Accepted
- Date: 2026-10-30

## Context

This fork has a tool called `revit_batch`. It runs up to 50 actions as a single undo step, rolls the whole thing back on the first failure, and supports `dry_run`.

Upstream 1.0 has `revit_run_actions`. Its signature is a list of 1 to 50 steps, `dry_run`, and a document. Its documentation reads: "Execute up to 50 actions with one undo step; the whole batch rolls back on its first failure. `dry_run` rolls back and returns the verification block." It sends the command `batch`.

The two are the same tool under two names. Upstream arrived at the fork's design independently.

## Decision

Delete the fork's `revit_batch`. Keep upstream's `revit_run_actions`.

The fork's exclusive tool count drops from nine to eight. The eight that remain were all confirmed absent from upstream: `revit_create_floor`, `revit_create_level`, `revit_export_element_ids`, `revit_merge_phases`, `revit_rebuild_model_ids`, `revit_reset_element_ids`, `revit_set_phase`, `revit_set_view_lighting`.

No compatibility alias is added. A user who calls `revit_batch` gets a missing tool, which is the honest answer.

## Consequences

The base's behaviour on batch semantics is now upstream's to define. If upstream changes the step limit or the rollback rule, the fork follows.

The fork loses a name it introduced. Anything in this repository that says `revit_batch` in a tool-facing sense now says `revit_run_actions`; the C# command stays `batch`, and the supervisor tools keep their own names. `CONTEXT.md` records the four meanings so that the bare word stops appearing.

The step vocabulary is upstream's closed union. Fork actions become legal step names by extending that union once, in the fork layer, rather than by forking the tool.

## Alternatives rejected

**Keep both.** Two tools with identical semantics is a documentation bug that never closes. It also doubles the surface a user has to disambiguate, and the fork would have to keep its own batch implementation working against a contract that upstream keeps editing.

**Alias `revit_batch` to `revit_run_actions`.** Hides the decision and makes the tool list lie. Every tool name in this product is also a documentation anchor, a manifest entry, a drift test assertion and a policy subject; an alias multiplies all four.
