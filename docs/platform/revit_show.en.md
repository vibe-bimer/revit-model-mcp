# Show Elements

`revit_show`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `element_ids` | Yes | — | array |  |
| `select` | No | True | boolean |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Display elements in Revit, optionally selecting them; opens a level plan or 3D view when needed.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
