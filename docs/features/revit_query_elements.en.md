# Element query

`revit_query_elements`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.1.0</span></p>

Filter and page through individual element rows

## Copyable prompts {#prompts}

```text
List the doors on 2F whose fire rating is empty, with ids
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
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
| `sort_direction` | No | `"asc"` | `string` | sort direction: asc or desc |
| `sort_field` | No | `"id"` | `string` | field to sort by (element id by default) |
| `type_name` | No | `null` | `string / null` | type name, together with the family |
| `view` | No | `null` | `string / null` | view name (or its Revit id) |
| `workset` | No | `null` | `string / null` | workset filter |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `pickup_timeout_seconds` | No | `300` | `integer` | Positive seconds to wait for pickup over local or SSH (default 300); ignored over HTTP. A pending job may still execute after pickup times out |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Read a page of matching element rows after revit_list_catalog.

Returns data with elements (id and values), fields, total, offset, limit and hasMore; values include availability, source and units when available.
Lengths use mm, areas m2 and volumes m3; optional geometry uses model mm rounded to one decimal, and unavailable geometry is omitted.
Use roomCenterMm for placement inside rooms; a bounding-box centre can lie outside the room.
No matches or an offset beyond the result return elements=[]; advance offset while hasMore=true.
Call revit_list_catalog first and prefer revit_aggregate_elements for counts and breakdowns.
Invalid fields or filters, a missing document, read failure or timeout raise errors; partial data is not returned.


If more than one Revit instance is running, document is required; otherwise any instance may respond.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
