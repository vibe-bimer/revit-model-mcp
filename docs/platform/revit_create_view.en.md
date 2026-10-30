# Create View

`revit_create_view`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `box` | No | None | any |  |
| `detail_level` | No | None | any |  |
| `display_style` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `element_ids` | No | None | any |  |
| `kind` | Yes | — | string |  |
| `level` | No | None | any |  |
| `name` | No | None | any |  |
| `scale` | No | None | any |  |
| `template` | No | None | any |  |
| `view_family_type` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Create a plan, section, 3D or drafting view. Unbounded 3D views show the whole model, shaded, fine detail. Box coordinates are model mm.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
