# revit_aggregate_elements

<p class="facts"><b>Group</b> Query and totals　<b>Kind</b> Read (read-only)　<b>Since</b> 0.1.0</p>

Summarize matching elements by one or two fields after revit_list_catalog.

!!! note "Notes"
    First choice for “how many” questions

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `group_by` ✔ | — | one or two grouping fields: category, family, type, level or a parameter name（array） |
| `area_scheme` | — | Exact area-scheme name from the area-schemes catalog, matched case-insensitively. Default null applies no scheme filter; selecting a scheme restricts results to its areas and combines with the other filters.（any） |
| `categories` | — | category filter (several are combined with OR)（any） |
| `family` | — | family name filter（any） |
| `level` | — | level name, as revit_list_catalog reports it（any） |
| `parameter_filters` | — | parameter filters: equals, contains, greater, less, empty, not-empty or exists（any） |
| `phase` | — | phase filter（any） |
| `sum_field` | — | numeric field or parameter to total, with sum and average（any） |
| `type_name` | — | type name, together with the family（any） |
| `view` | — | view name (or its Revit id)（any） |
| `workset` | — | workset filter（any） |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |
    | `pickup_timeout_seconds` | `300` | Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later.（integer） |
    | `timeout_seconds` | `120` | Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits.（integer） |

## Prompts

```text
How many of each wall type sit on 1F?
```

```text
Count the doors per level and their total width
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
