# Document overview

`revit_document_info`

<p class="facts"><span><b>Group</b> Connection and documents</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.1.0</span></p>

Read document metadata, levels, area schemes, worksets and view count

## Copyable prompts {#prompts}

```text
Which model is open, and which levels does it have?
```

## Parameters {#parameters}

No additional business parameters; use the common parameters below.

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `pickup_timeout_seconds` | No | `300` | `integer` | Positive seconds to wait for pickup over local or SSH (default 300); ignored over HTTP. A pending job may still execute after pickup times out |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Read general information about the active Revit model.

Returns data with file name, Revit version, levels (elevations in mm), area schemes, worksets and view count.
Absent collections are empty; non-workshared models have no worksets.
Call revit_list_views next for view analysis.
A missing active document, read failure or timeout raises an error; partial data is not returned.


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
