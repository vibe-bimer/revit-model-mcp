---
description: "Render a highlighted PNG that marks 1 to 500 elements, for issue evidence. Supports 3d or plan mode over local or SSH transport. The temporary view is rolled back. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries."
---

# Capture Elements

`revit_capture_elements`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `element_ids` | Yes | — | array |  |
| `mode` | No | `"3d"` | string |  |
| `output_path` | No | `null` | any | New PNG path, resolved on the machine running this server; an existing file is an error. Default null downloads to a temporary directory and returns localPath. |
| `padding_mm` | No | `1500` | number |  |
| `pixel_size` | No | `1600` | integer | PNG size in pixels along the fitted dimension, 32 to 4000 (default 1600); Revit rejects smaller images. |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | `null` | any | Revit process ID; takes precedence over document. |

## Behavior (registry text) {#behavior}

```text
Render a highlighted PNG that marks 1 to 500 elements, for issue evidence. Supports 3d or plan mode over local or SSH transport. The temporary view is rolled back. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
