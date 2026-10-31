---
description: "Compare host grids and levels with one loaded Revit link; changes nothing"
---

# Compare link datums

`revit_compare_link_datums`

<p class="facts"><span><b>Group</b> Links and coordination</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Compare host grids and levels with one loaded Revit link; changes nothing

[Same-name integration branch page](../platform/revit_compare_link_datums.md)

## Copyable prompts {#prompts}

```text
Compare the grids and levels of the linked model "Structure Ref.rvt" against the current project
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `link` | Yes | — | `string` | name of the loaded Revit link to compare against |
| `kinds` | No | `null` | `array<string> / null` | link kinds to compare |
| `level_offset_mm` | No | `0` | `number` | vertical offset applied to link levels while comparing (mm) |
| `name_map` | No | `null` | `object / null` | Mapping of host datum names to link datum names. |
| `prefix` | No | `""` | `string` | name prefix filter for links |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |
| `reuse_matching` | No | `true` | `boolean` | reuse already matched grids and levels |
| `suffix` | No | `""` | `string` | Suffix appended to matched grid and level names. |
| `tolerance_mm` | No | `0.5` | `number` | tolerance when comparing datum points (in mm) |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Compare host grids and levels with one loaded Revit link. Changes nothing. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
