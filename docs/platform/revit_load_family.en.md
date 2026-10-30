---
description: "Load workstation .rfa files in one undo entry. Existing families are skipped unless overwrite is true."
---

# Load Families

`revit_load_family`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | `false` | boolean |  |
| `overwrite` | No | `false` | boolean |  |
| `overwrite_parameter_values` | No | `false` | boolean |  |
| `paths` | Yes | — | array |  |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | `600` | integer |  |

</div>

## Behavior (registry text) {#behavior}

```text
Load workstation .rfa files in one undo entry. Existing families are skipped unless overwrite is true.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
