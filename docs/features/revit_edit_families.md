# Edit Families

Edit an open family in place, or named project families (exact names or ["*"]), one load cycle each.

**Group:** Families · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `operations` | Yes | — | `array of any` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `families` | No | null | `array of string / null` | — |
| `overwrite_parameter_values` | No | false | `boolean` | — |
| `stop_on_error` | No | true | `boolean` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Edit an open family in place, or named project families (exact names or ["*"]), one load cycle each. A dry run rolls back all changes. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
