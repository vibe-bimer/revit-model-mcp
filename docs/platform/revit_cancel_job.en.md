# Cancel Action Job

`revit_cancel_job`

<p class="facts"><span><b>Group</b> Connection and instances</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `job_id` | Yes | — | string |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `process_id` | No | None | any |  |

## Behavior (registry text) {#behavior}

```text
Request cancellation of an action jobId. Process-models stops before the next model and marks unstarted models cancelled; a single running Revit operation finishes, and completed changes stay committed.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
