---
description: "Write a new local .xlsx issue register with element snapshots and review documents. Takes 1 to 60 issues; captures at most 25 snapshots (by severity) within a 210-second budget, and failed snapshots become cell notes. Snapshots need local or SSH transport. Existing output files are refused. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries."
---

# Issue Register

`revit_issue_register`

<p class="facts"><span><b>Group</b> Export and registers</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 1.0.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, with identical parameters</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_issue_register.md)

## Contract differences from the release {#contract-diff}

The same-name tool has an identical contract to release 1.0.0.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `issues` | Yes | — | array | (not documented in the branch contract) |
| `output_path` | Yes | — | string | New .xlsx issue register path, resolved on the machine running this server; existing files are refused. |
| `pixel_size` | No | `900` | integer | PNG size in pixels along the fitted dimension, 32 to 4000 (default 1600); Revit rejects smaller images. |
| `project` | Yes | — | object | (not documented in the branch contract) |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | `null` | any | Revit process ID; takes precedence over document. |

</div>

## Behavior (registry text) {#behavior}

```text
Write a new local .xlsx issue register with element snapshots and review documents. Takes 1 to 60 issues; captures at most 25 snapshots (by severity) within a 210-second budget, and failed snapshots become cell notes. Snapshots need local or SSH transport. Existing output files are refused. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
