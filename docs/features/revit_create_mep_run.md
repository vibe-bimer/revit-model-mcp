# Create MEP Run

Create connected duct, pipe, cable tray or conduit segments from model mm points.

**Group:** CAD and MEP · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `kind` | Yes | — | `string (duct, pipe, cable_tray, conduit)` | — |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `points_mm` | Yes | — | `array of array of number` | at least three model XY vertices, each [x,y] in millimetres; the boundary closes automatically |
| `connect_to` | No | null | `integer / null` | — |
| `diameter_mm` | No | null | `number / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `height_mm` | No | null | `number / null` | — |
| `offset_mm` | No | null | `number / null` | — |
| `system_type` | No | null | `string / null` | — |
| `type_name` | No | null | `string / null` | — |
| `width_mm` | No | null | `number / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Create connected duct, pipe, cable tray or conduit segments from model mm points. A missing Z uses the level elevation plus the kind's default offset. Unplaceable elbows are reported as unjoined pairs.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
