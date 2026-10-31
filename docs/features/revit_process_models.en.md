---
description: "Open each model in the interactive session, run steps and C# code, and export or save as requested; in-place saves and code need a confirm_token"
---

# Process many models

`revit_process_models`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Open each model in the interactive session, run steps and C# code, and export or save as requested; in-place saves and code need a confirm_token

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_process_models.md)

## Copyable prompts {#prompts}

```text
Batch-open the models under D:/models, export PNGs and save as new files instead of saving in place
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `code` | No | `null` | `any / null` | C# code to run in each model, with its transaction mode |
| `confirm_token` | No | `null` | `string / null` | token returned by the first call, sent in the second confirming call |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `exports` | No | `null` | `array<any> / null` | Export requests applied to each processed model. |
| `folder` | No | `null` | `string / null` | folder of models to process |
| `open` | No | `null` | `any / null` | how each model is opened, with mode and workset settings |
| `paths` | No | `null` | `array<string> / null` | paths of the models to process |
| `pattern` | No | `"*.rvt"` | `string` | File name pattern ending in .rvt. |
| `process_id` | No | `null` | `integer / null` | Revit process ID of the instance to process |
| `recursive` | No | `false` | `boolean` | whether subfolders of the folder are included |
| `save` | No | `null` | `any / null` | save settings: `none`, `output_dir` or `in_place` |
| `steps` | No | `null` | `array<any> / null` | one to fifty action steps; the batch rolls back when a step fails |
| `stop_on_error` | No | `false` | `boolean` | Whether processing stops at the first error. |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `timeout_seconds` | No | `14400` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

Open each model in the interactive session, run steps and C# code, export, save as requested, and close. In-place saves and code need a confirm_token from the preview response. dry_run forces code.transaction="auto" and reports the override in warnings. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
