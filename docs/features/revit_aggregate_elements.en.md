# Grouped totals

`revit_aggregate_elements`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.1.0</span></p>

Group by one or two fields, with counts and optional sum and average

!!! note "Usage notes"
    First choice for “how many” questions

## Copyable prompts {#prompts}

```text
How many of each wall type sit on 1F?
```

```text
Count the doors per level and their total width
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `group_by` | Yes | — | `array<string>` | one or two grouping fields: category, family, type, level or a parameter name |
| `area_scheme` | No | `null` | `string / null` | Exact localized area-scheme name from the area-schemes catalog; restricts results to its areas and combines with the other filters |
| `categories` | No | `null` | `array<string> / null` | category filter (several are combined with OR) |
| `family` | No | `null` | `string / null` | family name filter |
| `level` | No | `null` | `string / null` | level name, as revit_list_catalog reports it |
| `parameter_filters` | No | `null` | `array<object> / null` | parameter filters: equals, contains, greater, less, empty, not-empty or exists |
| `phase` | No | `null` | `string / null` | phase filter |
| `sum_field` | No | `null` | `string / null` | numeric field or parameter to total, with sum and average |
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

Summarize matching elements by one or two fields after revit_list_catalog.

Returns data with matchedElements and groups containing keys, count and optional numericCount, sum, average and unit.
Lengths use mm, areas m2 and volumes m3; groups without numeric values have null sum and average.
No matches return groups=[]; invalid field or filter names raise errors even for empty results.
Call revit_list_catalog first; prefer this tool for counts and breakdowns, and revit_query_elements only for individual rows.
For area totals, group by level and select the area scheme.
A missing document, read failure or timeout raises an error; partial data is not returned.


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
