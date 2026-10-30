---
description: "Open each model in the interactive session, run steps and C# code, export, save as requested, and close. In-place saves and code need a confirm_token from the preview response. dry_run forces code.transaction=\"auto\" and reports the override in warnings. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action."
---

# Process Many Models

`revit_process_models`

<p class="facts"><span><b>Group</b> Batch and reports</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `code` | No | None | any |  |
| `confirm_token` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `exports` | No | None | any |  |
| `folder` | No | None | any |  |
| `open` | No | None | any |  |
| `paths` | No | None | any |  |
| `pattern` | No | *.rvt | string |  |
| `recursive` | No | False | boolean |  |
| `save` | No | None | any |  |
| `steps` | No | None | any |  |
| `stop_on_error` | No | False | boolean |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `process_id` | No | None | any |  |
| `timeout_seconds` | No | 14400 | integer |  |

## Behavior (registry text) {#behavior}

```text
Open each model in the interactive session, run steps and C# code, export, save as requested, and close. In-place saves and code need a confirm_token from the preview response. dry_run forces code.transaction="auto" and reports the override in warnings. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
