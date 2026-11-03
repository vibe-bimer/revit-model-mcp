---
description: "Place a structural column on a level at a point, with its top on a level or at a height"
---

# Create column

`revit_create_column`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.10.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> No</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span><span><b>Origin</b> Fork (this repository)</span></p>

Place a structural column on a level at a point, with its top on a level or at a height

!!! warning "Actions are allowed by default; read-only is explicit"
    Actions are allowed unless one of three switches is on: the machine policy `ReadOnly`, the workstation `read-only` file, or `REVIT_MCP_READ_ONLY=1`. A fresh install ships with the machine policy read-only. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    The tool writes both levels and both offsets itself, because set_parameter refuses ElementId parameters; nothing is attached, so the top is a level or a height

## Copyable prompts {#prompts}

```text
Put a 600x600 concrete column at 3000,4500 on 1F, topping out at 3F
```

```text
Put a column at the origin of 1F, 4200 high
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `family` | Yes | — | `string` | column family name, already in the project (load it with revit_load_family_file first) |
| `level` | Yes | — | `string` | base level name |
| `x_mm` | Yes | — | `number` | placement X in millimetres in model coordinates |
| `y_mm` | Yes | — | `number` | placement Y in millimetres in model coordinates |
| `base_offset_mm` | No | `0` | `number` | base offset in millimetres; 0 by default |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `height_mm` | No | `null` | `number / null` | column height in millimetres above the base offset when top_level is absent; 3000 by default |
| `rotation_deg` | No | `0` | `number` | rotation about the vertical axis in degrees; 0 by default |
| `top_level` | No | `null` | `string / null` | top level name; height_mm is ignored when it is given |
| `top_offset_mm` | No | `0` | `number` | top offset in millimetres above the top level; 0 by default |
| `type_name` | No | `null` | `string / null` | family type name; empty takes the family's first type |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Place one structural column of `family` (optionally `type_name`) at `x_mm`, `y_mm` on `level`.

The top is either `top_level` or `height_mm` above the base (3000 mm when neither is given).
Base and top levels and both offsets are written by the tool itself, because they are
ElementId-valued parameters that revit_set_parameter refuses on purpose. The column is not
attached to anything: no attachment is attempted. dry_run returns the same verification
block without changing the model.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
