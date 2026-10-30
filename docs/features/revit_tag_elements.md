# Tag Elements

Tag elements in a view, chosen by category names or by element IDs (exactly one of the two).

**Group:** Views and sheets · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `view` | Yes | — | `string / integer` | view name (or its Revit id) |
| `categories` | No | null | `array of string / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `element_ids` | No | null | `array of integer / null` | element ids (unitless Revit ids) |
| `leader` | No | false | `boolean` | — |
| `max_elements` | No | 5000 | `integer` | — |
| `orientation` | No | "horizontal" | `string (horizontal, vertical)` | — |
| `skip_tagged` | No | true | `boolean` | — |
| `tag_type` | No | null | `string / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Tag elements in a view, chosen by category names or by element IDs (exactly one of the two). Returns created tag IDs in createdElementIds; already tagged elements are skipped unless skip_tagged is false, and untaggable inputs are listed in skipped. tag_type matches a tag type name, a family name or "Family: Type"; the default tag type is used otherwise. Room tags need a plan view. dry_run rolls back and returns the tags that would be created.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
