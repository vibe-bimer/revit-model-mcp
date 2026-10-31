---
description: "Write the ID register of drawn model components to an Excel workbook"
---

# Export element ID register

`revit_export_element_ids`

<p class="facts"><span><b>Group</b> Export and checks</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.8.0</span><span><b>Version</b> Released 0.9.0</span><span><b>Same-name tool on the integration branch</b> No</span><span><b>This contract applies to the release</b> Yes</span><span><b>Origin</b> Fork (this repository)</span></p>

Write the ID register of drawn model components to an Excel workbook

!!! note "Usage notes"
    The workbook is written on the Revit workstation. The column headers are Chinese Revit UI labels — 类别, 族, 类型, 标高, 构件ID, 名称 and 工作集 are category, family, type, level, element id, name and workset.

## Copyable prompts {#prompts}

```text
Export the ID register of drawn model components to Excel, ordered by category, family and type
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `fields` | No | `null` | `array<string> / null` | columns to write; the defaults are category, family, type, level, component id, name and workset |
| `path` | No | `null` | `string / null` | path of the exported element id file |

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

Write the element identifier register of the drawn components to a workbook, read-only.

`fields` picks the columns and `path` names the file, which must not already exist; without
one the workbook goes to Documents/RevitModelMcp/Exports with a timestamp. Non-component
categories are reported under skippedCategories and the list is capped at 50,000 rows.
The workbook is written on the Revit workstation; nothing is downloaded.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
