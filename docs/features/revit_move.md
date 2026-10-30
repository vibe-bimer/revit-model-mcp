# Move Elements

Move elements by dx_mm, dy_mm and dz_mm on model axes.

**Group:** Model actions · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `dx_mm` | Yes | — | `number` | — |
| `dy_mm` | Yes | — | `number` | — |
| `element_ids` | Yes | — | `array of integer` | element ids (unitless Revit ids) |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `dz_mm` | No | 0 | `number` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Move elements by dx_mm, dy_mm and dz_mm on model axes. dry_run rolls back and returns the verification block. Group members, pinned, hosted and constrained elements are reported in skipped.inGroup, skipped.pinned, skipped.hosted and skipped.constrained and are not changed; the call is refused if every element is a group member.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
