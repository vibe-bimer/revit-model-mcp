# Process Many Models

Open each model in the interactive session, run steps and C# code, export, save as requested, and close.

**Group:** Batch processing · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `code` | No | null | `any / null` | — |
| `confirm_token` | No | null | `string / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `exports` | No | null | `array of any / null` | — |
| `folder` | No | null | `string / null` | — |
| `open` | No | null | `any / null` | — |
| `paths` | No | null | `array of string / null` | — |
| `pattern` | No | "*.rvt" | `string` | — |
| `process_id` | No | null | `integer / null` | — |
| `recursive` | No | false | `boolean` | — |
| `save` | No | null | `any / null` | — |
| `steps` | No | null | `array of any / null` | — |
| `stop_on_error` | No | false | `boolean` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Open each model in the interactive session, run steps and C# code, export, save as requested, and close. In-place saves and code need a confirm_token from the preview response. dry_run forces code.transaction="auto" and reports the override in warnings. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
