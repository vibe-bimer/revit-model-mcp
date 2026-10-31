---
description: "Create connected duct, pipe, cable tray or conduit segments from model mm points. A missing Z uses the level elevation plus the kind's default offset. Unplaceable elbows are reported as unjoined pairs."
---

# Create MEP Run

`revit_create_mep_run`

<p class="facts"><span><b>Group</b> CAD and MEP</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} |
| --- | :--: | --- | --- |
| `connect_to` | No | `null` | any |
| `diameter_mm` | No | `null` | any |
| `dry_run` | No | `false` | boolean |
| `height_mm` | No | `null` | any |
| `kind` | Yes | — | string |
| `level` | Yes | — | string |
| `offset_mm` | No | `null` | any |
| `points_mm` | Yes | — | array |
| `system_type` | No | `null` | any |
| `type_name` | No | `null` | any |
| `width_mm` | No | `null` | any |

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
Create connected duct, pipe, cable tray or conduit segments from model mm points. A missing Z uses the level elevation plus the kind's default offset. Unplaceable elbows are reported as unjoined pairs.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
