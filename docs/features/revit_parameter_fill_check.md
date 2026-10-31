# Parameter Fill Check

Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs.

**Group:** Model queries · **Kind:** Read (read-only)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `categories` | Yes | — | `array of string` | Category names (1 to 20) from the categories catalog; matches any listed category. |
| `parameters` | Yes | — | `array of string` | Exact localized parameter names (1 to 30); names that do not match count as missing. |
| `include_types` | No | true | `boolean` | — |
| `level` | No | null | `string / null` | level name, as revit_list_catalog reports it |
| `process_id` | No | null | `integer / null` | Revit process ID; takes precedence over document. |
| `sample_limit` | No | 20 | `integer` | Maximum sampled element IDs per empty and missing list, 1 to 100 (default 20); counts always cover all elements. |
| `view` | No | null | `string / null` | view name (or its Revit id) |
| `workset` | No | null | `string / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs. Numeric zero counts as filled. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
