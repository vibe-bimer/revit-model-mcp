---
description: "Place a structural beam on a level along a given axis, with an optional structural usage and vertical offset"
---

# Create beam

`revit_create_beam`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.1.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> No</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span><span><b>Origin</b> Fork (this repository)</span></p>

Place a structural beam on a level along a given axis, with an optional structural usage and vertical offset

!!! warning "Actions are allowed by default; read-only is explicit"
    Actions are allowed unless one of three switches is on: the machine policy `ReadOnly`, the workstation `read-only` file, or `REVIT_MCP_READ_ONLY=1`. A fresh install ships with the machine policy read-only. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    The curve-and-level overload is used and the axis is not snapped; the offset goes through the family's elevation parameters, counts only when the bounding box rises, moves the instance otherwise, and fails rather than leaving the beam on its level

## Copyable prompts {#prompts}

```text
Put a 300x600 concrete beam on 2F from 0,0 to 6000,0, dropped 150
```

```text
Put a steel beam on 1F from 0,0 to 6000,0 and set its structural usage to Girder
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `end_mm` | Yes | — | `array<number>` | axis end as [x, y] in millimetres; a point equal to the start is refused |
| `family` | Yes | — | `string` | family name |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `start_mm` | Yes | — | `array<number>` | axis start as [x, y] in millimetres; placed exactly as given, without snapping |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `structural_usage` | No | `null` | `string / null` | structural usage such as Girder, Joist, Purlin, Bearing or Other; the family's own setting stands when omitted |
| `type_name` | No | `null` | `string / null` | type name, together with the family |
| `z_offset_mm` | No | `0` | `number` | vertical offset relative to the reference level in millimetres; the read-back names where it landed |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Place one structural beam of `family` (optionally `type_name`) along the axis `start_mm`-`end_mm`.

`level` is the reference level of the framing, and the two axis points are [x, y] in
millimetres. The placement uses the curve-and-level overload, so the level and the axis are
both given explicitly; the axis is not snapped, because Revit has no snapping API and
SetEndReference only acts on an end the model already joined. `structural_usage` writes
FamilyInstance.StructuralUsage. `z_offset_mm` is the vertical offset above the reference
level: the tool writes it through the elevation parameters that carry it, and only a write that
lifts the bounding box counts, because a family can take the value and keep the beam on its
level; the instance moves instead when no parameter lifts it, and the call fails when neither
route works, so a refused offset never passes as a beam placed on the level. The read-back names
the parameter holding the offset or leaves it out when the geometry carries the shift. dry_run
returns the same verification block without changing the model.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
