# Open Document

Open a local, UNC or RSN model.

**Group:** Documents · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `path` | Yes | — | `string` | — |
| `activate` | No | false | `boolean` | — |
| `audit` | No | false | `boolean` | — |
| `mode` | No | "detached" | `string (detached, detached_discard_worksets, local_copy, read_only_local)` | — |
| `process_id` | No | null | `integer / null` | — |
| `worksets` | No | "all" | `string (all, none) / object` | — |

## Behavior and returned data

Open a local, UNC or RSN model. Central models open detached by default. Cloud paths are unsupported. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
