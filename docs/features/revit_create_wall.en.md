# Create straight wall

`revit_create_wall`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.2.0</span><span><b>Effect</b> Model elements / parameters</span></p>

Create a wall from two XY points, a level, type and height

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

## Copyable prompts {#prompts}

```text
Draw a 200 mm wall on 1F from 0,0 to 6000,0
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `end_mm` | Yes | — | `array<number>` | end point [x, y] in millimetres |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `start_mm` | Yes | — | `array<number>` | start point [x, y] in millimetres |
| `wall_type` | Yes | — | `string / null` | Basic wall-type name; required argument, but null selects the first basic wall type |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `height_mm` | No | `3000` | `number` | wall height in millimetres (3000 by default) |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Create a straight wall for layout on a named level; model XY endpoints and height are millimetres; null wall_type chooses the first basic type.
dry_run executes and rolls back, returning the same verification block without changing the model.
Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
