---
description: "Filter and page through individual element rows"
---

# Element query

`revit_query_elements`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.1.0</span><span><b>Version</b> Released 0.9.0</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Filter and page through individual element rows

[Same-name integration branch page](../platform/revit_query_elements.md)

## Copyable prompts {#prompts}

```text
List the doors on 2F whose fire rating is empty, with ids
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `area_scheme` | No | `null` | `string / null` | Exact localized area-scheme name from the area-schemes catalog; restricts results to its areas and combines with the other filters |
| `categories` | No | `null` | `array<string> / null` | category filter (several are combined with OR) |
| `family` | No | `null` | `string / null` | family name filter |
| `fields` | No | `null` | `array<string> / null` | fields to return; the tool picks its usual ones by default |
| `include_geometry` | No | `false` | `boolean` | include location, bounding box and the placing room centre in model millimetres |
| `level` | No | `null` | `string / null` | level filter |
| `limit` | No | `100` | `integer` | rows per page |
| `offset` | No | `0` | `integer` | first row to return, for paging with limit |
| `parameter_filters` | No | `null` | `array<object> / null` | parameter filters: equals, contains, greater, less, empty, not-empty or exists |
| `phase` | No | `null` | `string / null` | phase filter |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |
| `sort_direction` | No | `"asc"` | `string` | sort direction: asc or desc |
| `sort_field` | No | `"id"` | `string` | field to sort by (element id by default) |
| `type_name` | No | `null` | `string / null` | type name, together with the family |
| `view` | No | `null` | `string / null` | view name (or its Revit id) |
| `workset` | No | `null` | `string / null` | workset filter |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Read a page of matching element rows. Lengths use mm, areas m2, volumes m3; optional geometry is in model mm. roomCenterMm is a point inside the room, a bounding-box centre can lie outside it. hasMore=true means further pages exist. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
