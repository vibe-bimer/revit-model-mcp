# Update Parameters

Update a parameter on elements matching the same filters as revit_query_elements.

**Group:** Model actions · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `filters` | Yes | — | `any` | — |
| `parameter` | Yes | — | `string` | — |
| `value` | Yes | — | `string / integer / number` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `include_type_parameters` | No | false | `boolean` | — |
| `max_elements` | No | 5000 | `integer` | — |
| `parameter_id` | No | null | `string / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Update a parameter on elements matching the same filters as revit_query_elements. Group members are reported in skipped.inGroup instead of failing the call; dry_run predicts this.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
