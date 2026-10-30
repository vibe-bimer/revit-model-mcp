---
description: "List recent jobs, or wait up to wait_seconds (0 to 50, default 40) for the result of an action jobId. Results stay on the workstation for 24 hours, across server restarts. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries."
---

# List Revit Jobs

`revit_jobs`

<p class="facts"><span><b>Group</b> Connection and instances</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `job_id` | No | `null` | any |  |
| `wait_seconds` | No | `40` | integer | Seconds to wait, 0 through 50. |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | `null` | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | `120` | integer | Seconds to wait for a result (default 120). |

## Behavior (registry text) {#behavior}

```text
List recent jobs, or wait up to wait_seconds (0 to 50, default 40) for the result of an action jobId. Results stay on the workstation for 24 hours, across server restarts. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
