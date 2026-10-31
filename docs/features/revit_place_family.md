# Place Family

Place a loaded unhosted family on a named level.

**Group:** Families · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `family` | Yes | — | `string` | — |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `type_name` | Yes | — | `string / null` | — |
| `x_mm` | Yes | — | `number` | — |
| `y_mm` | Yes | — | `number` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `rotation_deg` | No | 0 | `number` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Place a loaded unhosted family on a named level. family is a name or Family: Type; a null type_name uses the embedded or first type. XY is in mm, rotation in degrees.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
