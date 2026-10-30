# Link CAD Drawing

`revit_link_cad`

<p class="facts"><span><b>Group</b> CAD and MEP</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | False | boolean |  |
| `layers` | No | None | any |  |
| `level` | No | None | any |  |
| `link` | No | True | boolean |  |
| `origin` | No | internal | string |  |
| `path` | Yes | — | string |  |
| `units` | No | auto | string |  |
| `view` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | 600 | integer |  |

## Behavior (registry text) {#behavior}

```text
Link or import a DWG into a plan view on the Revit workstation. Returns CAD layers and extents in mm.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
