# View Summary

`revit_view_summary`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | string | Exact non-template view name from revit_list_views, or a view ID as a decimal string. |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | 120 | integer | Seconds to wait for a result (default 120). |

## Behavior (registry text) {#behavior}

```text
Read element categories and counts for a selected view. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
