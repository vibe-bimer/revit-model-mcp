# View element rows

`revit_view_elements`

<p class="facts"><span><b>Group</b> Views and snapshots</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.2.0</span></p>

Page through elements in a selected view, optionally filtered by category

## Copyable prompts {#prompts}

```text
Page through the elements of the 3D view, 200 at a time
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | `string` | view name (or its Revit id) |
| `categories` | No | `null` | `array<string> / null` | only list these categories |
| `limit` | No | `100` | `integer` | rows per page |
| `offset` | No | `0` | `integer` | first row to return, for paging with limit |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `pickup_timeout_seconds` | No | `300` | `integer` | Positive seconds to wait for pickup over local or SSH (default 300); ignored over HTTP. A pending job may still execute after pickup times out |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Read one page of elements in a selected view.

Returns data with elements, total, offset, limit and hasMore; rows include IDs, category, family, type, level and available measurements in mm, m2 and m3.
No matches or an offset beyond the result return elements=[]; advance offset while hasMore=true.
Prefer revit_view_summary for counts and category discovery; use this tool for individual rows and revit_element_details for all parameters.
A missing document, unknown or unsupported view, read failure or timeout raises an error; partial data is not returned.


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
