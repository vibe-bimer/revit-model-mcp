---
description: "Synchronize a workshared document with central; the first call changes nothing and returns the confirm_token needed to proceed"
---

# Synchronize document

`revit_sync_document`

<p class="facts"><span><b>Group</b> Documents and processes</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Synchronize a workshared document with central; the first call changes nothing and returns the confirm_token needed to proceed

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_sync_document.md)

## Copyable prompts {#prompts}

```text
Synchronize the current workshared document with central, comment "update door and window tags"
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `comment` | Yes | — | `string` | comment recorded with the sync |
| `compact` | No | `false` | `boolean` | whether the central model is compacted during synchronisation |
| `confirm_token` | No | `null` | `string / null` | token returned by the first call, sent in the second confirming call |
| `process_id` | No | `null` | `integer / null` | Target Revit process chosen among the running instances. |
| `relinquish` | No | `"all"` | `string / object` | users whose ownership is relinquished, all for every user |
| `save_local_after` | No | `true` | `boolean` | whether the local copy is saved after synchronisation |
| `save_local_before` | No | `true` | `boolean` | save the local copy before synchronizing |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | Yes | — | `string` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Synchronize a workshared document with central. Needs confirm_token from a first call, which changes nothing.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
