---
description: "Activate a non-template view, then zoom to fit or frame element ids"
---

# Activate view

`revit_activate_view`

<p class="facts"><span><b>Group</b> Views and snapshots</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Activate a non-template view, then zoom to fit or frame element ids

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_activate_view.md)

## Copyable prompts {#prompts}

```text
Open the Level 1 plan and zoom to fit
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | `string` | view name (or its Revit id) |
| `activate_document` | No | `false` | `boolean` | whether the document is activated as well |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |
| `view_type` | No | `null` | `string / null` | view type, for example FloorPlan or ThreeD |
| `zoom` | No | `"fit"` | `string / array<integer>` | Zoom handling, fit the view, keep the current zoom, or frame element IDs. |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Activate a non-template view. Zoom to fit, preserve zoom, or frame element IDs.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
