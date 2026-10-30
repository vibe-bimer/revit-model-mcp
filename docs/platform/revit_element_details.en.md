# Element Details

`revit_element_details`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `element_id` | Yes | — | integer | Revit element ID from revit_query_elements or revit_view_elements. |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | 120 | integer | Seconds to wait for a result (default 120). |

## Behavior (registry text) {#behavior}

```text
Read parameters and geometry of an element by Revit ID, with its type parameters and related warnings. Geometry is in model mm; roomCenterMm is a point inside the room. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
