# Compare Link Datums

`revit_compare_link_datums`

<p class="facts"><span><b>Group</b> Links and datums</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `kinds` | No | None | any |  |
| `level_offset_mm` | No | 0 | number |  |
| `link` | Yes | — | string |  |
| `name_map` | No | None | any |  |
| `prefix` | No | — | string |  |
| `reuse_matching` | No | True | boolean |  |
| `suffix` | No | — | string |  |
| `tolerance_mm` | No | 0.5 | number |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | 120 | integer | Seconds to wait for a result (default 120). |

## Behavior (registry text) {#behavior}

```text
Compare host grids and levels with one loaded Revit link. Changes nothing. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
