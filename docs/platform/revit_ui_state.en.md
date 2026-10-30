# Revit UI State

`revit_ui_state`

<p class="facts"><span><b>Group</b> Connection and instances</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

No additional business parameters; use the common parameters below.

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |

## Behavior (registry text) {#behavior}

```text
Read the active document, open views, selection and open documents. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
