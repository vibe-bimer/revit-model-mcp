# Query Elements

`revit_query_elements`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `area_scheme` | No | None | any | Exact area-scheme name, case-insensitive. |
| `categories` | No | None | any |  |
| `family` | No | None | any |  |
| `fields` | No | None | any |  |
| `include_geometry` | No | False | boolean | Include location, boundingBox and roomCenterMm in model mm. Default false; true enlarges the response. |
| `level` | No | None | any |  |
| `limit` | No | 100 | integer |  |
| `offset` | No | 0 | integer |  |
| `parameter_filters` | No | None | any | AND-combined filters: parameter (exact localized name), operator (equals, contains, greater, less, empty, not-empty, exists) and value. Numbers use mm, m2, m3 or display units. |
| `phase` | No | None | any |  |
| `sort_direction` | No | asc | string | asc (default) or desc, case-insensitive. |
| `sort_field` | No | id | string | System field (e.g. id, category, level) or exact localized parameter name to sort by; default id. |
| `type_name` | No | None | any | Exact type name, case-insensitive. |
| `view` | No | None | any | Exact non-template view name; limits the search to that view. |
| `workset` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | 120 | integer | Seconds to wait for a result (default 120). |

## Behavior (registry text) {#behavior}

```text
Read a page of matching element rows. Lengths use mm, areas m2, volumes m3; optional geometry is in model mm. roomCenterMm is a point inside the room, a bounding-box centre can lie outside it. hasMore=true means further pages exist. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
