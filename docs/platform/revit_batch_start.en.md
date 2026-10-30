---
description: "Start a persistent, read-only run over local, UNC or RSN models. open_timeout_minutes is the per-model open deadline (default 30, 45 when upgrading in memory)."
---

# Start batch collection

`revit_batch_start`

<p class="facts"><span><b>Group</b> Batch and reports</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `folder` | No | None | any |  |
| `open_timeout_minutes` | No | None | any |  |
| `parameter_rules` | No | None | any |  |
| `paths` | No | None | any |  |
| `recursive` | No | False | boolean |  |
| `years` | No | None | any |  |

## Behavior (registry text) {#behavior}

```text
Start a persistent, read-only run over local, UNC or RSN models. open_timeout_minutes is the per-model open deadline (default 30, 45 when upgrading in memory).
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
