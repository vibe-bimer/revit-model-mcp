# Build Walls from CAD

`revit_walls_from_cad`

<p class="facts"><span><b>Group</b> CAD and MEP</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `cad_id` | Yes | — | integer |  |
| `dry_run` | No | False | boolean |  |
| `height_mm` | No | 3000 | number |  |
| `join` | No | True | boolean |  |
| `layers` | Yes | — | array |  |
| `level` | Yes | — | string |  |
| `max_gap_mm` | No | 3000 | number |  |
| `max_thickness_mm` | No | 700 | number |  |
| `min_length_mm` | No | 300 | number |  |
| `min_thickness_mm` | No | 80 | number |  |
| `wall_type` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | 600 | integer |  |

## Behavior (registry text) {#behavior}

```text
Bridge openings, pair parallel CAD lines and join basic walls in one undo entry. Dimensions are mm. Joins Revit rejects are left out and reported as unjoinedEnds with unjoinedReasons; dry_run reports the same join numbers.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
