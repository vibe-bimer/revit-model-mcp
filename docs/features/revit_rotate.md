# Rotate Elements

Rotate elements about a vertical axis through center_mm, or through their combined bounding box center.

**Group:** Model actions · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `angle_deg` | Yes | — | `number` | — |
| `element_ids` | Yes | — | `array of integer` | element ids (unitless Revit ids) |
| `center_mm` | No | null | `array of number / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Rotate elements about a vertical axis through center_mm, or through their combined bounding box center. dry_run rolls back. Group members, pinned, hosted and constrained elements are reported in skipped.inGroup, skipped.pinned, skipped.hosted and skipped.constrained and are not changed; the call is refused if every element is a group member.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
