# Compare Link Datums

Compare host grids and levels with one loaded Revit link.

**Group:** Links · **Kind:** Read (read-only)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `link` | Yes | — | `string` | — |
| `kinds` | No | null | `array of string / null` | — |
| `level_offset_mm` | No | 0 | `number` | — |
| `name_map` | No | null | `object / null` | — |
| `prefix` | No | "" | `string` | — |
| `process_id` | No | null | `integer / null` | Revit process ID; takes precedence over document. |
| `reuse_matching` | No | true | `boolean` | — |
| `suffix` | No | "" | `string` | — |
| `tolerance_mm` | No | 0.5 | `number` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Compare host grids and levels with one loaded Revit link. Changes nothing. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
