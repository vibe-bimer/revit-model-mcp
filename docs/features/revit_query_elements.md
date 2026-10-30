# Query Elements

Read a page of matching element rows.

**Group:** Model queries · **Kind:** Read (read-only)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `area_scheme` | No | null | `string / null` | Exact area-scheme name, case-insensitive. |
| `categories` | No | null | `array of string / null` | — |
| `family` | No | null | `string / null` | — |
| `fields` | No | null | `array of string / null` | fields to return or write; the tool picks its usual ones by default |
| `include_geometry` | No | false | `boolean` | Include location, boundingBox and roomCenterMm in model mm. Default false; true enlarges the response. |
| `level` | No | null | `string / null` | level name, as revit_list_catalog reports it |
| `limit` | No | 100 | `integer` | — |
| `offset` | No | 0 | `integer` | — |
| `parameter_filters` | No | null | `array of object / null` | AND-combined filters: parameter (exact localized name), operator (equals, contains, greater, less, empty, not-empty, exists) and value. Numbers use mm, m2, m3 or display units. |
| `phase` | No | null | `string / null` | — |
| `process_id` | No | null | `integer / null` | Revit process ID; takes precedence over document. |
| `sort_direction` | No | "asc" | `string` | asc (default) or desc, case-insensitive. |
| `sort_field` | No | "id" | `string` | System field (e.g. id, category, level) or exact localized parameter name to sort by; default id. |
| `type_name` | No | null | `string / null` | Exact type name, case-insensitive. |
| `view` | No | null | `string / null` | view name (or its Revit id) |
| `workset` | No | null | `string / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Read a page of matching element rows. Lengths use mm, areas m2, volumes m3; optional geometry is in model mm. roomCenterMm is a point inside the room, a bounding-box centre can lie outside it. hasMore=true means further pages exist. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
