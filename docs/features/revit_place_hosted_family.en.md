---
description: "Place a door or window on a wall, named or found nearby, and report which wall it hangs on"
---

# Place hosted family

`revit_place_hosted_family`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.10.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> No</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span><span><b>Origin</b> Fork (this repository)</span></p>

Place a door or window on a wall, named or found nearby, and report which wall it hangs on

!!! warning "Actions are allowed by default; read-only is explicit"
    Actions are allowed unless one of three switches is on: the machine policy `ReadOnly`, the workstation `read-only` file, or `REVIT_MCP_READ_ONLY=1`. A fresh install ships with the machine policy read-only. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    The nearby search only looks at walls of the placement level; a host that is not a wall, a point outside host_search_radius_mm or two equally near walls are refused with the candidates; level-based families belong to revit_place_family; rotation_deg is only 0, flip_facing turns the family around; nothing is attached

## Copyable prompts {#prompts}

```text
Hang a door at 3000,0 on 1F, taking the nearest wall
```

```text
Put this window on wall 105 with a 900 mm sill
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `family` | Yes | — | `string` | door, window or other one-level hosted family name, already in the project (load it with revit_load_family_file first) |
| `x_mm` | Yes | — | `number` | placement X in millimetres in model coordinates |
| `y_mm` | Yes | — | `number` | placement Y in millimetres in model coordinates |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `flip_facing` | No | `null` | `boolean / null` | call flipFacing() to reverse the facing when true; empty leaves it alone |
| `host_element_id` | No | `null` | `integer / null` | element id of the host wall; empty finds the nearest wall instead |
| `host_search_radius_mm` | No | `2000` | `number` | largest horizontal distance from the point to a wall location line when the host is found nearby, in millimetres; 2000 by default |
| `level` | No | `null` | `string / null` | placement level name; empty takes the level whose elevation is closest to the placement point, which counts as elevation 0 |
| `rotation_deg` | No | `0` | `number` | 0 only; the host wall decides the orientation, so use flip_facing to turn the family |
| `sill_height_mm` | No | `null` | `number / null` | sill height in millimetres, written to the family's own INSTANCE_SILL_HEIGHT_PARAM |
| `type_name` | No | `null` | `string / null` | family type name; empty takes the family's first type |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Place one door, window or other one-level hosted family of `family` at `x_mm`, `y_mm`.

The host is either the wall named by `host_element_id`, or the nearest wall of the placement
level whose location line passes within `host_search_radius_mm` of the point; `level` defaults
to the level whose elevation is closest to the point. A missing host, a distance over the
radius or two equally near walls are refused with the candidates, so the caller can name one.
The response reports `fork.hostResolution` ({mode, hostId, distanceMm}), which is why a dry
run already shows the wall the family would hang on. `sill_height_mm` writes the family's own
INSTANCE_SILL_HEIGHT_PARAM and `flip_facing` calls flipFacing(). `rotation_deg` must be 0: a
hosted instance takes its orientation from its host wall, so use `flip_facing` to turn it
around. Families that are not one-level hosted are refused: revit_place_family places those,
and it is the one that rotates. Nothing is attached to the host, because a door or a window
has no attachment target. dry_run returns the same verification block without changing the
model.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
