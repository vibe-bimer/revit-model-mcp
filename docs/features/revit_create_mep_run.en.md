---
description: "Create connected duct, pipe, tray or conduit runs from points in mm"
---

# Create MEP run

`revit_create_mep_run`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Create connected duct, pipe, tray or conduit runs from points in mm

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_create_mep_run.md)

## Copyable prompts {#prompts}

```text
Draw a DN100 pipe through these points on Level 3
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `kind` | Yes | — | `string` | run kind: `duct`, `pipe`, `cable_tray` or `conduit` |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `points_mm` | Yes | — | `array<array<number>>` | At least three model XY vertices, each [x,y] in millimetres; the boundary closes automatically |
| `connect_to` | No | `null` | `integer / null` | Element ID the new run connects to. |
| `diameter_mm` | No | `null` | `number / null` | diameter of the pipe run (in mm) |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `height_mm` | No | `null` | `number / null` | section height of the duct or cable tray (mm) |
| `offset_mm` | No | `null` | `number / null` | Offset of the run from the level, in mm. |
| `system_type` | No | `null` | `string / null` | mechanical system type of the pipe run |
| `type_name` | No | `null` | `string / null` | type name, together with the family |
| `width_mm` | No | `null` | `number / null` | section width of the duct or cable tray (mm) |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Create connected duct, pipe, cable tray or conduit segments from model mm points. A missing Z uses the level elevation plus the kind's default offset. Unplaceable elbows are reported as unjoined pairs.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
