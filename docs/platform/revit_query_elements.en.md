---
description: "Read a page of matching element rows. Lengths use mm, areas m2, volumes m3; optional geometry is in model mm. roomCenterMm is a point inside the room, a bounding-box centre can lie outside it. hasMore=true means further pages exist. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries."
---

# Query Elements

`revit_query_elements`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 1.0.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, with identical parameters</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_query_elements.md)

## Contract differences from the release {#contract-diff}

The same-name tool has an identical contract to release 1.0.0.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `area_scheme` | No | `null` | any | Exact area-scheme name, case-insensitive. |
| `categories` | No | `null` | any | (not documented in the branch contract) |
| `family` | No | `null` | any | (not documented in the branch contract) |
| `fields` | No | `null` | any | (not documented in the branch contract) |
| `include_geometry` | No | `false` | boolean | Include location, boundingBox and roomCenterMm in model mm. Default false; true enlarges the response. |
| `level` | No | `null` | any | (not documented in the branch contract) |
| `limit` | No | `100` | integer | (not documented in the branch contract) |
| `offset` | No | `0` | integer | (not documented in the branch contract) |
| `parameter_filters` | No | `null` | any | AND-combined filters: parameter (exact localized name), operator (equals, contains, greater, less, empty, not-empty, exists) and value. Numbers use mm, m2, m3 or display units. |
| `phase` | No | `null` | any | (not documented in the branch contract) |
| `sort_direction` | No | `"asc"` | string | asc (default) or desc, case-insensitive. |
| `sort_field` | No | `"id"` | string | System field (e.g. id, category, level) or exact localized parameter name to sort by; default id. |
| `type_name` | No | `null` | any | Exact type name, case-insensitive. |
| `view` | No | `null` | any | Exact non-template view name; limits the search to that view. |
| `workset` | No | `null` | any | (not documented in the branch contract) |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | `null` | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | `120` | integer | Seconds to wait for a result (default 120). |

</div>

## Behavior (registry text) {#behavior}

```text
Read a page of matching element rows. Lengths use mm, areas m2, volumes m3; optional geometry is in model mm. roomCenterMm is a point inside the room, a bounding-box centre can lie outside it. hasMore=true means further pages exist. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
