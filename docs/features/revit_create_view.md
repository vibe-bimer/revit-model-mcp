# Create View

Create a plan, section, 3D or drafting view.

**Group:** Views and sheets · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `kind` | Yes | — | `string (floor_plan, ceiling_plan, structural_plan, section, 3d, drafting)` | — |
| `box` | No | null | `any / null` | — |
| `detail_level` | No | null | `string (coarse, medium, fine) / null` | — |
| `display_style` | No | null | `string (hidden_line, shaded, consistent_colors, realistic) / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `element_ids` | No | null | `array of integer / null` | element ids (unitless Revit ids) |
| `level` | No | null | `string / null` | level name, as revit_list_catalog reports it |
| `name` | No | null | `string / null` | — |
| `scale` | No | null | `integer / null` | — |
| `template` | No | null | `string / null` | — |
| `view_family_type` | No | null | `string / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Create a plan, section, 3D or drafting view. Unbounded 3D views show the whole model, shaded, fine detail. Box coordinates are model mm.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
