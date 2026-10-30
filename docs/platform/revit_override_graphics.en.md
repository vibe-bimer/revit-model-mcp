# Highlight Elements

`revit_override_graphics`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `color` | No | #FF0000 | string |  |
| `dry_run` | No | False | boolean |  |
| `element_ids` | Yes | — | array |  |
| `fill` | No | True | boolean |  |
| `halftone_others` | No | False | boolean |  |
| `line_weight` | No | None | any |  |
| `reset` | No | False | boolean |  |
| `transparency` | No | 0 | integer |  |
| `views` | No | active | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Colour elements in selected model views; reset restores overrides saved in this Revit session.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
