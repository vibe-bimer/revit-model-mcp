---
description: "Update a parameter on elements matching the same filters as revit_query_elements. Group members are reported in skipped.inGroup instead of failing the call; dry_run predicts this."
---

# Update Parameters

`revit_update_parameters`

<p class="facts"><span><b>Group</b> Editing primitives</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | `false` | boolean |  |
| `filters` | Yes | — |  |  |
| `include_type_parameters` | No | `false` | boolean |  |
| `max_elements` | No | `5000` | integer |  |
| `parameter` | Yes | — | string |  |
| `parameter_id` | No | `null` | any |  |
| `value` | Yes | — | any |  |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |

</div>

## Behavior (registry text) {#behavior}

```text
Update a parameter on elements matching the same filters as revit_query_elements. Group members are reported in skipped.inGroup instead of failing the call; dry_run predicts this.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
