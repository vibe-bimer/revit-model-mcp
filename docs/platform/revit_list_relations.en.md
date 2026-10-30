# List Relations

`revit_list_relations`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `relation` | Yes | — | string |  |
| `source_id` | No | None | any | Revit ID of the source group (group-elements) or family instance (nested-family). |
| `source_name` | No | None | any | Source name, case-insensitive: a level (level-rooms), area scheme (area-scheme-elements) or view template (view-template-dependents). |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | 120 | integer | Seconds to wait for a result (default 120). |

## Behavior (registry text) {#behavior}

```text
Read model object membership or dependencies. relation is level-rooms, area-scheme-elements or view-template-dependents (with source_name), or group-elements or nested-family (with source_id). A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
