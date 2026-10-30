# Build Walls from CAD

Bridge openings, pair parallel CAD lines and join basic walls in one undo entry.

**Group:** CAD and MEP · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `cad_id` | Yes | — | `integer` | — |
| `layers` | Yes | — | `array of string` | — |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `height_mm` | No | 3000 | `number` | — |
| `join` | No | true | `boolean` | — |
| `max_gap_mm` | No | 3000 | `number` | — |
| `max_thickness_mm` | No | 700 | `number` | — |
| `min_length_mm` | No | 300 | `number` | — |
| `min_thickness_mm` | No | 80 | `number` | — |
| `wall_type` | No | null | `string / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Bridge openings, pair parallel CAD lines and join basic walls in one undo entry. Dimensions are mm. Joins Revit rejects are left out and reported as unjoinedEnds with unjoinedReasons; dry_run reports the same join numbers.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
