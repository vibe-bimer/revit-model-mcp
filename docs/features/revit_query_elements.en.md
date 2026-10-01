# revit_query_elements

<p class="facts"><b>Group</b> Query and totals　<b>Kind</b> Read (read-only)　<b>Since</b> 0.1.0</p>

Read a page of matching element rows after revit_list_catalog.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `area_scheme` | — | Exact area-scheme name from the area-schemes catalog, matched case-insensitively. Default null applies no scheme filter; selecting a scheme restricts results to its areas and combines with the other filters.（any） |
| `categories` | — | any |
| `family` | — | any |
| `fields` | — | any |
| `include_geometry` | `false` | Whether each query row includes available location, boundingBox and placed-room roomCenterMm coordinates in model millimetres, rounded to one decimal. Default false omits geometry; true increases the response size.（boolean） |
| `level` | — | any |
| `limit` | `100` | integer |
| `offset` | `0` | integer |
| `parameter_filters` | — | AND-combined objects with an exact localized parameter name in parameter, an operator (equals, contains, greater, less, empty, not-empty, exists), and value for comparisons; default null applies no parameter filters. Numeric values use mm, m2, m3 or other document display units; contains requires text, and empty/not-empty/exists need no value.（any） |
| `phase` | — | any |
| `sort_direction` | `"asc"` | Sort order: asc or desc, case-insensitively; default asc means ascending. Applies to sort_field before offset and limit.（string） |
| `sort_field` | `"id"` | System field (e.g. id, category, level) or exact localized parameter name to sort before pagination; default id sorts by Revit element ID. Uses sort_direction, with element ID breaking ties for other fields.（string） |
| `type_name` | — | Exact type name to match, case-insensitively, combined with the other model filters. Default null applies no type filter; discover names with the family-types catalog.（any） |
| `view` | — | Exact non-template view name from the views catalog, matched case-insensitively, to restrict the element collector. Default null searches the document without a view filter; combines with the other model filters.（any） |
| `workset` | — | any |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |
    | `pickup_timeout_seconds` | `300` | Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later.（integer） |
    | `timeout_seconds` | `120` | Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits.（integer） |

## Prompts

```text
List the doors on 2F whose fire rating is empty, with ids
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
