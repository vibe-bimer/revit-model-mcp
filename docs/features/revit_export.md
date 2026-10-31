# Export Model Files

Export PDF, DWG, IFC or schedule CSV files on the Revit workstation; dry_run returns planned file names.

**Group:** Export · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `format` | Yes | — | `string (pdf, dwg, ifc, csv)` | — |
| `all_sheets` | No | false | `boolean` | — |
| `confirm_token` | No | null | `string / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `options` | No | null | `object / null` | — |
| `output_dir` | No | null | `string / null` | — |
| `overwrite` | No | false | `boolean` | replace the destination when it exists |
| `sheet_set` | No | null | `string / null` | — |
| `sheets` | No | null | `array of string / integer / null` | — |
| `views` | No | null | `array of string / integer / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Export PDF, DWG, IFC or schedule CSV files on the Revit workstation; dry_run returns planned file names. Replacing existing files (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
