# Aggregate Elements

`revit_aggregate_elements`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `area_scheme` | No | None | any | Exact area-scheme name, case-insensitive. |
| `categories` | No | None | any |  |
| `family` | No | None | any |  |
| `group_by` | Yes | — | array | One or two distinct fields (e.g. category, family, type, level) or exact localized parameter names. |
| `level` | No | None | any |  |
| `parameter_filters` | No | None | any | AND-combined filters: parameter (exact localized name), operator (equals, contains, greater, less, empty, not-empty, exists) and value. Numbers use mm, m2, m3 or display units. |
| `phase` | No | None | any |  |
| `sum_field` | No | None | any | Numeric field or parameter name to sum and average per group; lengths in mm, areas m2, volumes m3. |
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
Summarize matching elements by one or two fields, with optional sum and average. Lengths use mm, areas m2, volumes m3. For area totals, group by level and select the area scheme. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
