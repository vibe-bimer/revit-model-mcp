# Start batch collection

`revit_batch_start`

<p class="facts"><span><b>Group</b> Batch and reports</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

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
