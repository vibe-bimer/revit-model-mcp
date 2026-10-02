# Create level

`revit_create_level`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.10.0</span><span><b>Effect</b> Model elements / parameters</span></p>

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

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `elevation_mm` | Yes | — | `number` | elevation in millimetres |
| `name` | Yes | — | `string` | level name |
| `create_view` | No | `false` | `boolean` | also create the matching floor plan view |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Create a level at a given elevation for layout.
name is the level name; an existing level with that exact name is refused, so a later
tool never resolves an ambiguous level. elevation_mm is the height in millimetres.
create_view also creates the matching floor plan; its view type is chosen by view
family, not by name. dry_run executes and rolls back, returning the same verification
block without changing the model.
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
