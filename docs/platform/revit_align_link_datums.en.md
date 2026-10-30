---
description: "Align host grids and levels to a loaded link, with optional creation and rollback preview. Does not create a monitor relationship."
---

# Align Link Datums

`revit_align_link_datums`

<p class="facts"><span><b>Group</b> Links and datums</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `create_missing` | No | `true` | boolean |  |
| `create_plan_views` | No | `false` | boolean |  |
| `dry_run` | No | `false` | boolean |  |
| `grid_type` | No | `null` | any |  |
| `include_pinned` | No | `false` | boolean |  |
| `kinds` | No | `null` | any |  |
| `level_offset_mm` | No | `0` | number |  |
| `level_type` | No | `null` | any |  |
| `link` | Yes | — | string |  |
| `name_map` | No | `null` | any |  |
| `plan_view_type` | No | `null` | any |  |
| `prefix` | No | `""` | string |  |
| `reuse_matching` | No | `true` | boolean |  |
| `suffix` | No | `""` | string |  |
| `tolerance_mm` | No | `0.5` | number |  |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | `600` | integer |  |

</div>

## Behavior (registry text) {#behavior}

```text
Align host grids and levels to a loaded link, with optional creation and rollback preview. Does not create a monitor relationship.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
