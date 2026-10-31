---
description: "Create a level at a given elevation in millimetres"
---

# Create level

`revit_create_level`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.10.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> No</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span><span><b>Origin</b> Fork (this repository)</span></p>

Create a level at a given elevation in millimetres

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    An existing level with the same name is refused, so a later tool never resolves an ambiguous level

## Copyable prompts {#prompts}

```text
Create a level named 4F at 15000 mm
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `elevation_mm` | Yes | — | `number` | elevation in millimetres |
| `name` | Yes | — | `string` | level name |
| `create_view` | No | `false` | `boolean` | also create the matching floor plan view |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Create a level at an elevation, optionally with its floor plan.

A level whose name already exists is refused. dry_run returns the same verification block
without changing the model.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
