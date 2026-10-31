---
description: "Render a PNG marking 1 to 500 elements; the temporary view is rolled back"
---

# Capture elements

`revit_capture_elements`

<p class="facts"><span><b>Group</b> Selection and display</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Render a PNG marking 1 to 500 elements; the temporary view is rolled back

[Same-name integration branch page](../platform/revit_capture_elements.md)

## Copyable prompts {#prompts}

```text
Highlight these beams in the Level 1 plan as a PNG for an issue record
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `element_ids` | Yes | — | `array<integer>` | element ids (unitless Revit ids) |
| `mode` | No | `"3d"` | `string` | capture mode, 3d for the three-dimensional view |
| `output_path` | No | `null` | `string / null` | New PNG path, resolved on the machine running this server; an existing file is an error. Default null downloads to a temporary directory and returns localPath. |
| `padding_mm` | No | `1500` | `number` | padding around the captured elements, in mm |
| `pixel_size` | No | `1600` | `integer` | pixels along the fitted image dimension (1–4000) |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Render a highlighted PNG that marks 1 to 500 elements, for issue evidence. Supports 3d or plan mode over local or SSH transport. The temporary view is rolled back. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
