# Align Link Datums

Align host grids and levels to a loaded link, with optional creation and rollback preview.

**Group:** Links · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `link` | Yes | — | `string` | — |
| `create_missing` | No | true | `boolean` | — |
| `create_plan_views` | No | false | `boolean` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `grid_type` | No | null | `string / null` | — |
| `include_pinned` | No | false | `boolean` | — |
| `kinds` | No | null | `array of string / null` | — |
| `level_offset_mm` | No | 0 | `number` | — |
| `level_type` | No | null | `string / null` | — |
| `name_map` | No | null | `object / null` | — |
| `plan_view_type` | No | null | `string / null` | — |
| `prefix` | No | "" | `string` | — |
| `reuse_matching` | No | true | `boolean` | — |
| `suffix` | No | "" | `string` | — |
| `tolerance_mm` | No | 0.5 | `number` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Align host grids and levels to a loaded link, with optional creation and rollback preview. Does not create a monitor relationship.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
