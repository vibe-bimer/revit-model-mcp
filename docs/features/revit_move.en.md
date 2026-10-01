# Move elements

`revit_move`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.1.0</span><span><b>Effect</b> Model elements / parameters</span></p>

Move elements by offsets along model axes in millimetres

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Supports dry_run

## Copyable prompts {#prompts}

```text
Move these three elements 500 mm along X, dry run first
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dx_mm` | Yes | — | `number` | Offset along model X in millimetres, not the final coordinate |
| `dy_mm` | Yes | — | `number` | Offset along model Y in millimetres, not the final coordinate |
| `element_ids` | Yes | — | `array<integer>` | element ids to move |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `dz_mm` | No | `0` | `number` | Offset along model Z in millimetres (default 0), not the final coordinate |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Move elements when adjusting their position; dx_mm, dy_mm and dz_mm are offsets in millimetres on model axes.
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
