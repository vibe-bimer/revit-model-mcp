---
description: "Open a local, UNC or RSN model on the workstation; central models open detached"
---

# Open Document

`revit_open_document`

<p class="facts"><span><b>Group</b> Documents and processes</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Open a local, UNC or RSN model on the workstation; central models open detached

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_open_document.md)

## Copyable prompts {#prompts}

```text
Open the central model 'Tower.rvt' for me in detached mode.
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `path` | Yes | — | `string` | path of the model to open on the Revit workstation |
| `activate` | No | `false` | `boolean` | activate the document after opening it |
| `audit` | No | `false` | `boolean` | Whether the model is audited after opening. |
| `mode` | No | `"detached"` | `string` | open mode: detached, detached_discard_worksets, local_copy or read_only_local |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |
| `worksets` | No | `"all"` | `string / object` | Workset handling, all, none, or open and close name lists. |

</div>

## Behavior and returned data {#contract}

Open a local, UNC or RSN model. Central models open detached by default. Cloud paths are unsupported. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
