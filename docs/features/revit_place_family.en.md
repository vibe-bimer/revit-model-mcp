# Place unhosted family

`revit_place_family`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.2.0</span><span><b>Effect</b> Model elements / parameters</span></p>

Place a loaded unhosted family on a named level with optional Z rotation

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Not run live on 2026

## Copyable prompts {#prompts}

```text
Place an instance of a loaded unhosted furniture family at 3000,4000 on 1F, dry run first
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `family` | Yes | — | `string` | family name |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `type_name` | Yes | — | `string / null` | type name, together with the family |
| `x_mm` | Yes | — | `number` | model X in millimetres |
| `y_mm` | Yes | — | `number` | model Y in millimetres |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `rotation_deg` | No | `0` | `number` | rotation about Z in degrees |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Place a loaded unhosted family on a named level for layout.

family accepts a family name or Family: Type, case-insensitively.
null type_name uses the embedded type or the first type. Conflicting types
are rejected. Missing families return similar names with categories.
Model XY is in millimetres and Z rotation in degrees.
Use roomCenterMm when placing something inside a room.

dry_run executes and rolls back, returning the same verification block without changing the model.
Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
