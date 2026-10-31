# Cancel Action Job

Request cancellation of an action jobId.

**Group:** Connection and core · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `job_id` | Yes | — | `string` | — |
| `process_id` | No | null | `integer / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Request cancellation of an action jobId. Process-models stops before the next model and marks unstarted models cancelled; a single running Revit operation finishes, and completed changes stay committed.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
