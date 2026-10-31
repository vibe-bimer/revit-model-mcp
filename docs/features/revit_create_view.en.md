---
description: "Create a plan, section, 3D or drafting view; box coordinates are model mm"
---

# Create view

`revit_create_view`

<p class="facts"><span><b>Group</b> Views and snapshots</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Create a plan, section, 3D or drafting view; box coordinates are model mm

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_create_view.md)

## Copyable prompts {#prompts}

```text
Create a floor plan named Level 3 Plan at scale 1:100
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `kind` | Yes | — | `string` | view kind: `floor_plan`, `ceiling_plan`, `structural_plan`, `section`, `3d` or `drafting` |
| `box` | No | `null` | `any / null` | View box with min_mm and max_mm model coordinates. |
| `detail_level` | No | `null` | `string / null` | detail level of the new view |
| `display_style` | No | `null` | `string / null` | display style of the view: hidden_line, shaded, consistent_colors or realistic |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `element_ids` | No | `null` | `array<integer> / null` | element ids (unitless Revit ids) |
| `level` | No | `null` | `string / null` | level name, as revit_list_catalog reports it |
| `name` | No | `null` | `string / null` | Name of the new view. |
| `scale` | No | `null` | `integer / null` | scale of the new view |
| `template` | No | `null` | `string / null` | name of the view template applied to the new view |
| `view_family_type` | No | `null` | `string / null` | view family type name for the new view |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Create a plan, section, 3D or drafting view. Unbounded 3D views show the whole model, shaded, fine detail. Box coordinates are model mm.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
