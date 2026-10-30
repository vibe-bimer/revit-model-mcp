---
description: "Change category, workset and filter visibility in one view; dry_run previews. Categories accept the Revit UI name, the BuiltInCategory name (OST_StructuralColumns), the English name or an ID."
---

# Set View Visibility

`revit_set_view_visibility`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `category_classes` | No | `null` | any |  |
| `dry_run` | No | `false` | boolean |  |
| `filters` | No | `null` | any |  |
| `hide_categories` | No | `null` | any |  |
| `hide_categories_by_type` | No | `null` | any |  |
| `show_categories` | No | `null` | any |  |
| `template_mode` | No | `null` | any |  |
| `view` | Yes | — | string |  |
| `worksets` | No | `null` | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Change category, workset and filter visibility in one view; dry_run previews. Categories accept the Revit UI name, the BuiltInCategory name (OST_StructuralColumns), the English name or an ID.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
