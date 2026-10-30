# Create Wall

`revit_create_wall`

<p class="facts"><span><b>Group</b> CAD and MEP</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | False | boolean |  |
| `end_mm` | Yes | — | array |  |
| `height_mm` | No | 3000 | number |  |
| `level` | Yes | — | string |  |
| `start_mm` | Yes | — | array |  |
| `wall_type` | Yes | — | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Create a straight wall on a named level. XY endpoints and height are in mm; a null wall_type uses the first basic type.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
