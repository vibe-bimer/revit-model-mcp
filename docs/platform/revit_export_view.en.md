# Export View to PNG

`revit_export_view`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `output_path` | No | None | any | New PNG path, resolved on the machine running this server; an existing file is an error. Default null downloads to a temporary directory and returns localPath. |
| `pixel_size` | No | 1600 | integer | PNG size in pixels along the fitted dimension, 32 to 4000 (default 1600); Revit rejects smaller images. |
| `view` | Yes | — | string | Exact non-template view name from revit_list_views, or a view ID as a decimal string. |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |

## Behavior (registry text) {#behavior}

```text
Export a selected view to a PNG file on the MCP client. Does not change the active view or the model. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
