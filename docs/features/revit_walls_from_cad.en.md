---
description: "Pair CAD lines into joined basic walls, bridging openings, with millimetre dimensions"
---

# Build Walls from CAD

`revit_walls_from_cad`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Pair CAD lines into joined basic walls, bridging openings, with millimetre dimensions

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_walls_from_cad.md)

## Copyable prompts {#prompts}

```text
Build basic walls from the 'Level 1' underlay CAD lines, 3000 mm high, and join the ends.
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `cad_id` | Yes | — | `integer` | Element ID of the imported CAD instance. |
| `layers` | Yes | — | `array<string>` | CAD layer names used to create walls |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `height_mm` | No | `3000` | `number` | default height of generated walls (in mm) |
| `join` | No | `true` | `boolean` | whether the created walls are joined at their ends |
| `max_gap_mm` | No | `3000` | `number` | Largest gap bridged between CAD lines, in mm. |
| `max_thickness_mm` | No | `700` | `number` | maximum wall thickness to detect (in mm) |
| `min_length_mm` | No | `300` | `number` | minimum length of a CAD segment that becomes a wall (mm) |
| `min_thickness_mm` | No | `80` | `number` | minimum thickness of the created walls, in mm |
| `wall_type` | No | `null` | `string / null` | Basic wall-type name; required argument, but null selects the first basic wall type |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `600` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

Bridge openings, pair parallel CAD lines and join basic walls in one undo entry. Dimensions are mm. Joins Revit rejects are left out and reported as unjoinedEnds with unjoinedReasons; dry_run reports the same join numbers.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
