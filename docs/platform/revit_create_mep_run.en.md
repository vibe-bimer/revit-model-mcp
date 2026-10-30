# Create MEP Run

`revit_create_mep_run`

<p class="facts"><span><b>Group</b> CAD and MEP</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `connect_to` | No | None | any |  |
| `diameter_mm` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `height_mm` | No | None | any |  |
| `kind` | Yes | — | string |  |
| `level` | Yes | — | string |  |
| `offset_mm` | No | None | any |  |
| `points_mm` | Yes | — | array |  |
| `system_type` | No | None | any |  |
| `type_name` | No | None | any |  |
| `width_mm` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Create connected duct, pipe, cable tray or conduit segments from model mm points. A missing Z uses the level elevation plus the kind's default offset. Unplaceable elbows are reported as unjoined pairs.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
