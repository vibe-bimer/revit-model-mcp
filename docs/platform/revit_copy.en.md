# Copy Elements

`revit_copy`

<p class="facts"><span><b>Group</b> Editing primitives</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `count` | No | 1 | integer |  |
| `dry_run` | No | False | boolean |  |
| `dx_mm` | Yes | — | number |  |
| `dy_mm` | Yes | — | number |  |
| `dz_mm` | No | 0 | number |  |
| `element_ids` | Yes | — | array |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Create 1 to 100 successive copies at multiples of the model-axis offset in mm. dry_run rolls back. Group members are reported in skipped.inGroup; the call is refused if every element is a group member.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
