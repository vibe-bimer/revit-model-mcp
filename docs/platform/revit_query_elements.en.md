# Query Elements

`revit_query_elements`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, but the parameters differ</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_query_elements.md)

## Contract differences from the release {#contract-diff}

The table below is computed from the registry inputSchema; it is not a hand-written list.

- Parameter limit minimum: release — / integration 1
- Parameter offset minimum: release — / integration 0
- Parameter pickup_timeout_seconds exists only in the release
- Parameter process_id exists only on the integration branch

This contract belongs to the integration branch, not to release 0.9.0; copying the branch parameters fails on the release.

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
