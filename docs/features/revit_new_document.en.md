---
description: "Create a project or family from a template on the Revit workstation"
---

# New Document

`revit_new_document`

<p class="facts"><span><b>Group</b> Documents and processes</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Create a project or family from a template on the Revit workstation

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_new_document.md)

## Copyable prompts {#prompts}

```text
Create a new project from the 'Metric Generic Model.rte' template named 'Tower Scheme'.
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `activate` | No | `true` | `boolean` | Whether the new document becomes the active document. |
| `kind` | No | `"project"` | `string` | kind of new document: project or family |
| `name` | No | `null` | `string / null` | name given to the new document |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |
| `save_as` | No | `null` | `string / null` | Path the new document is saved to. |
| `template` | No | `null` | `string / null` | template file for the new document |

</div>

## Behavior and returned data {#contract}

Create a project or family from a template on the Revit workstation.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
