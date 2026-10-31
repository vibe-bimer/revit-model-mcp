---
description: "Align host grids and levels to a loaded link, with a dry-run rollback preview"
---

# Align Link Datums

`revit_align_link_datums`

<p class="facts"><span><b>Group</b> Links and coordination</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Align host grids and levels to a loaded link, with a dry-run rollback preview

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_align_link_datums.md)

## Copyable prompts {#prompts}

```text
Align the host grids and levels to the loaded link 'StructureLink.rvt' with a 5 mm tolerance.
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `link` | Yes | — | `string` | name of the link to align |
| `create_missing` | No | `true` | `boolean` | whether missing host datums are created |
| `create_plan_views` | No | `false` | `boolean` | create plan views for the aligned datums |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `grid_type` | No | `null` | `string / null` | Name of the grid type to align to. |
| `include_pinned` | No | `false` | `boolean` | whether to include pinned links |
| `kinds` | No | `null` | `array<string> / null` | datum kinds to align: grids or levels |
| `level_offset_mm` | No | `0` | `number` | vertical offset applied to the aligned levels, in mm |
| `level_type` | No | `null` | `string / null` | Name of the level type to align to. |
| `name_map` | No | `null` | `object / null` | map from link datum names to host datum names |
| `plan_view_type` | No | `null` | `string / null` | view family type name for the created plan views |
| `prefix` | No | `""` | `string` | Prefix added to matched grid and level names. |
| `reuse_matching` | No | `true` | `boolean` | whether to reuse existing datum matches |
| `suffix` | No | `""` | `string` | suffix appended to the names of created host datums |
| `tolerance_mm` | No | `0.5` | `number` | tolerance for grid and level alignment, in mm |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `600` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

Align host grids and levels to a loaded link, with optional creation and rollback preview. Does not create a monitor relationship.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
