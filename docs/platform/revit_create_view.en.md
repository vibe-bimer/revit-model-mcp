---
description: "Create a plan, section, 3D or drafting view. Unbounded 3D views show the whole model, shaded, fine detail. Box coordinates are model mm."
---

# Create View

`revit_create_view`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `box` | No | `null` | any |  |
| `detail_level` | No | `null` | any |  |
| `display_style` | No | `null` | any |  |
| `dry_run` | No | `false` | boolean |  |
| `element_ids` | No | `null` | any |  |
| `kind` | Yes | — | string |  |
| `level` | No | `null` | any |  |
| `name` | No | `null` | any |  |
| `scale` | No | `null` | any |  |
| `template` | No | `null` | any |  |
| `view_family_type` | No | `null` | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Create a plan, section, 3D or drafting view. Unbounded 3D views show the whole model, shaded, fine detail. Box coordinates are model mm.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
