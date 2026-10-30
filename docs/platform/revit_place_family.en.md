# Place Family

`revit_place_family`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | False | boolean |  |
| `family` | Yes | — | string |  |
| `level` | Yes | — | string |  |
| `rotation_deg` | No | 0 | number |  |
| `type_name` | Yes | — | any |  |
| `x_mm` | Yes | — | number |  |
| `y_mm` | Yes | — | number |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Place a loaded unhosted family on a named level. family is a name or Family: Type; a null type_name uses the embedded or first type. XY is in mm, rotation in degrees.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
