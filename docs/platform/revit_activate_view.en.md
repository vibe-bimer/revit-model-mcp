---
description: "Activate a non-template view. Zoom to fit, preserve zoom, or frame element IDs."
---

# Activate View

`revit_activate_view`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} |
| --- | :--: | --- | --- |
| `activate_document` | No | `false` | boolean |
| `view` | Yes | — | string |
| `view_type` | No | `null` | any |
| `zoom` | No | `"fit"` | any |

</div>

The branch contract ships no parameter descriptions.

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Target document title or path reference. |
| `process_id` | No | `null` | any | (not documented in the branch contract) |

</div>

## Behavior (registry text) {#behavior}

```text
Activate a non-template view. Zoom to fit, preserve zoom, or frame element IDs.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
