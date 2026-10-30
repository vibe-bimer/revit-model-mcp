# Place Families

`revit_place_families`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `at_rooms` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `load` | No | None | any |  |
| `placements` | No | None | any |  |
| `stop_on_error` | No | True | boolean |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | 600 | integer |  |

## Behavior (registry text) {#behavior}

```text
Load optional families and place instances in one transaction and undo entry.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
