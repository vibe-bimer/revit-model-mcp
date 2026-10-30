# Set View Visibility

Change category, workset and filter visibility in one view; dry_run previews.

**Group:** Views and sheets · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `view` | Yes | — | `string` | view name (or its Revit id) |
| `category_classes` | No | null | `object / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `filters` | No | null | `array of object / null` | — |
| `hide_categories` | No | null | `array of string / integer / null` | — |
| `hide_categories_by_type` | No | null | `array of string / null` | — |
| `show_categories` | No | null | `array of string / integer / null` | — |
| `template_mode` | No | null | `string (detach, edit_template, duplicate_view) / null` | — |
| `worksets` | No | null | `object / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Change category, workset and filter visibility in one view; dry_run previews. Categories accept the Revit UI name, the BuiltInCategory name (OST_StructuralColumns), the English name or an ID.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
