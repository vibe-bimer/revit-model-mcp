---
description: "Bridge openings, pair parallel CAD lines and join basic walls in one undo entry. Dimensions are mm. Joins Revit rejects are left out and reported as unjoinedEnds with unjoinedReasons; dry_run reports the same join numbers."
---

# Build Walls from CAD

`revit_walls_from_cad`

<p class="facts"><span><b>Group</b> CAD and MEP</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `cad_id` | Yes | — | integer |  |
| `dry_run` | No | `false` | boolean |  |
| `height_mm` | No | `3000` | number |  |
| `join` | No | `true` | boolean |  |
| `layers` | Yes | — | array |  |
| `level` | Yes | — | string |  |
| `max_gap_mm` | No | `3000` | number |  |
| `max_thickness_mm` | No | `700` | number |  |
| `min_length_mm` | No | `300` | number |  |
| `min_thickness_mm` | No | `80` | number |  |
| `wall_type` | No | `null` | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | `600` | integer |  |

## Behavior (registry text) {#behavior}

```text
Bridge openings, pair parallel CAD lines and join basic walls in one undo entry. Dimensions are mm. Joins Revit rejects are left out and reported as unjoinedEnds with unjoinedReasons; dry_run reports the same join numbers.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
