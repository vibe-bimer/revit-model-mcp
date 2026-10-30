# Issue Register

`revit_issue_register`

<p class="facts"><span><b>Group</b> Export and registers</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `issues` | Yes | — | array |  |
| `output_path` | Yes | — | string | New .xlsx issue register path, resolved on the machine running this server; existing files are refused. |
| `pixel_size` | No | 900 | integer | PNG size in pixels along the fitted dimension, 32 to 4000 (default 1600); Revit rejects smaller images. |
| `project` | Yes | — | object |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |

## Behavior (registry text) {#behavior}

```text
Write a new local .xlsx issue register with element snapshots and review documents. Takes 1 to 60 issues; captures at most 25 snapshots (by severity) within a 210-second budget, and failed snapshots become cell notes. Snapshots need local or SSH transport. Existing output files are refused. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
