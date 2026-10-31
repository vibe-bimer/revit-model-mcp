---
description: "Colour elements in selected model views; reset restores overrides saved in this Revit session."
---

# Highlight Elements

`revit_override_graphics`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} |
| --- | :--: | --- | --- |
| `color` | No | `"#FF0000"` | string |
| `dry_run` | No | `false` | boolean |
| `element_ids` | Yes | — | array |
| `fill` | No | `true` | boolean |
| `halftone_others` | No | `false` | boolean |
| `line_weight` | No | `null` | any |
| `reset` | No | `false` | boolean |
| `transparency` | No | `0` | integer |
| `views` | No | `"active"` | any |

</div>

The branch contract ships no parameter descriptions.

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |

</div>

## Behavior (registry text) {#behavior}

```text
Colour elements in selected model views; reset restores overrides saved in this Revit session.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
