# Highlight Elements

Colour elements in selected model views; reset restores overrides saved in this Revit session.

**Group:** Views and sheets · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `element_ids` | Yes | — | `array of integer` | element ids (unitless Revit ids) |
| `color` | No | "#FF0000" | `string` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `fill` | No | true | `boolean` | — |
| `halftone_others` | No | false | `boolean` | — |
| `line_weight` | No | null | `integer / null` | — |
| `reset` | No | false | `boolean` | — |
| `transparency` | No | 0 | `integer` | — |
| `views` | No | "active" | `string (active, all) / array of string / integer` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Colour elements in selected model views; reset restores overrides saved in this Revit session.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
