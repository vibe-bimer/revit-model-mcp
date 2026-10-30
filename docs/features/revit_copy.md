# Copy Elements

Create 1 to 100 successive copies at multiples of the model-axis offset in mm.

**Group:** Model actions · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `dx_mm` | Yes | — | `number` | — |
| `dy_mm` | Yes | — | `number` | — |
| `element_ids` | Yes | — | `array of integer` | element ids (unitless Revit ids) |
| `count` | No | 1 | `integer` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `dz_mm` | No | 0 | `number` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Create 1 to 100 successive copies at multiples of the model-axis offset in mm. dry_run rolls back. Group members are reported in skipped.inGroup; the call is refused if every element is a group member.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
