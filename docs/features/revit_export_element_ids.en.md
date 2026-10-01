# Export element ID register

`revit_export_element_ids`

<p class="facts"><span><b>Group</b> Export and checks</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.8.0</span></p>

Write the ID register of drawn model components to an Excel workbook

!!! note "Usage notes"
    The workbook is written on the Revit workstation

## Copyable prompts {#prompts}

```text
Export the ID register of drawn model components to Excel, ordered by category, family and type
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `fields` | No | `null` | `array<string> / null` | columns to write; the defaults are category, family, type, level, component id, name and workset |
| `save_to` | No | `null` | `string / null` | absolute .xlsx path on the Revit workstation; an existing file is an error |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `pickup_timeout_seconds` | No | `300` | `integer` | Positive seconds to wait for pickup over local or SSH (default 300); ignored over HTTP. A pending job may still execute after pickup times out |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Write the identifier register of the drawn components to an xlsx file on the Revit workstation.

Returns data with path, fileName, sheetName, columns, rowCount, totalCandidates, truncated, sizeBytes and categoryCounts.
Rows are ordered by category, then family, then type; the default columns are 类别, 族, 类型, 标高, 构件ID, 名称 and 工作集, and fields replaces them with built-in fields or parameter names.
The 构件ID column holds the Revit element ID, which the API cannot assign: this tool lists identifiers and never changes them.
Level stays empty for components without a level, which is most MEP pipe and duct runs.
Default null writes Documents\RevitModelMcp\Exports\构件ID清单_<model>_<timestamp>.xlsx on the workstation; an existing save_to file raises an error, and more than 50,000 rows sets truncated=true.
The export writes one file outside the model and never writes to the model; a missing document, read failure or timeout raises an error.


If more than one Revit instance is running, document is required; otherwise any instance may respond.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
