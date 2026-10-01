# Export view image

`revit_export_view`

<p class="facts"><span><b>Group</b> Views and snapshots</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.3.0</span></p>

Export a view as a PNG, from 1 to 4000 pixels

## Copyable prompts {#prompts}

```text
Export the 1F plan as a PNG, 2000 pixels wide
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | `string` | view name (or its Revit id) |
| `pixel_size` | No | `1600` | `integer` | pixels along the fitted image dimension (1–4000) |
| `save_to` | No | `null` | `string / null` | New PNG path on the MCP client machine, not the Revit workstation; an existing file is an error |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Export a selected view to PNG when numbers do not explain geometry.

Returns data with localPath on the MCP client, image width/height in pixels, sizeBytes and view metadata, without base64.
The export does not change the active view or write to the model; use it to inspect outlines, zones and room boundaries.
A missing document, unknown or unsupported view, existing destination, missing PNG or download failure raises an error.
Uses the default 120-second response and 300-second pickup budgets; timeouts raise errors without partial data.


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
