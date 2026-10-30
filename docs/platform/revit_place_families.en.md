---
description: "Load optional families and place instances in one transaction and undo entry."
---

# Place Families

`revit_place_families`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `at_rooms` | No | `null` | any |  |
| `dry_run` | No | `false` | boolean |  |
| `load` | No | `null` | any |  |
| `placements` | No | `null` | any |  |
| `stop_on_error` | No | `true` | boolean |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | `600` | integer |  |

## Behavior (registry text) {#behavior}

```text
Load optional families and place instances in one transaction and undo entry.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
