---
description: "Align host grids and levels to a loaded link, with optional creation and rollback preview. Does not create a monitor relationship."
---

# Align Link Datums

`revit_align_link_datums`

<p class="facts"><span><b>Group</b> Links and datums</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `create_missing` | No | True | boolean |  |
| `create_plan_views` | No | False | boolean |  |
| `dry_run` | No | False | boolean |  |
| `grid_type` | No | None | any |  |
| `include_pinned` | No | False | boolean |  |
| `kinds` | No | None | any |  |
| `level_offset_mm` | No | 0 | number |  |
| `level_type` | No | None | any |  |
| `link` | Yes | — | string |  |
| `name_map` | No | None | any |  |
| `plan_view_type` | No | None | any |  |
| `prefix` | No | — | string |  |
| `reuse_matching` | No | True | boolean |  |
| `suffix` | No | — | string |  |
| `tolerance_mm` | No | 0.5 | number |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | 600 | integer |  |

## Behavior (registry text) {#behavior}

```text
Align host grids and levels to a loaded link, with optional creation and rollback preview. Does not create a monitor relationship.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
