---
description: "Create a project or family from a template on the Revit workstation."
---

# New Document

`revit_new_document`

<p class="facts"><span><b>Group</b> Document lifecycle</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} |
| --- | :--: | --- | --- |
| `activate` | No | `true` | boolean |
| `kind` | No | `"project"` | string |
| `name` | No | `null` | any |
| `save_as` | No | `null` | any |
| `template` | No | `null` | any |

</div>

The branch contract ships no parameter descriptions.

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} |
| --- | :--: | --- | --- |
| `process_id` | No | `null` | any |

</div>

The branch contract ships no parameter descriptions.

## Behavior (registry text) {#behavior}

```text
Create a project or family from a template on the Revit workstation.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
