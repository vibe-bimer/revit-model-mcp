---
description: "Colour elements in selected model views; reset restores overrides saved in this Revit session."
---

# Highlight Elements

`revit_override_graphics`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

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
