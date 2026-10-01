# Name catalog

`revit_list_catalog`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.1.0</span></p>

Discover categories, family types, levels, area schemes, views, worksets, phases and parameters

!!! note "Usage notes"
    Queries and filters use these exact names

## Copyable prompts {#prompts}

```text
List the parameter names this model offers
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `section` | Yes | — | `string` | which catalogue to list: categories, family types, levels, area schemes, views, worksets, phases or parameters |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `pickup_timeout_seconds` | No | `300` | `integer` | Positive seconds to wait for pickup over local or SSH (default 300); ignored over HTTP. A pending job may still execute after pickup times out |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Discover valid model names before filtering.

Returns data with section and items containing names and section-specific IDs, categories, types or counts; an empty catalog returns items=[].
section is required: categories, family-types, levels, area-schemes, views, worksets, phases or parameters.
The parameters section reports localized names, categories and value types.
Start universal queries here, then prefer revit_aggregate_elements for counts and breakdowns; use revit_query_elements only for individual rows.
An unknown section, missing document, read failure or timeout raises an error; partial data is not returned.


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
