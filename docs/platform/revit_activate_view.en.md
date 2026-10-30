# Activate View

`revit_activate_view`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `activate_document` | No | False | boolean |  |
| `view` | Yes | — | string |  |
| `view_type` | No | None | any |  |
| `zoom` | No | fit | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Target document title or path reference. |
| `process_id` | No | None | any |  |

## Behavior (registry text) {#behavior}

```text
Activate a non-template view. Zoom to fit, preserve zoom, or frame element IDs.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
