---
description: "Read model quality counts: project metadata, file size, counts, units and the ten most frequent warning groups. Unavailable metrics are null and listed in skipped. output_path also writes an .xlsx health report with up to five snapshots. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries."
---

# Model Health Check

`revit_model_health`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 1.0.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, with identical parameters</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_model_health.md)

## Contract differences from the release {#contract-diff}

The same-name tool has an identical contract to release 1.0.0.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `output_path` | No | `null` | any | New .xlsx health report path, resolved on the machine running this server; parent must exist and existing files are refused. |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | `null` | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | `120` | integer | Seconds to wait for a result (default 120). |

</div>

## Behavior (registry text) {#behavior}

```text
Read model quality counts: project metadata, file size, counts, units and the ten most frequent warning groups. Unavailable metrics are null and listed in skipped. output_path also writes an .xlsx health report with up to five snapshots. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
