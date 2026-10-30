# New Document

`revit_new_document`

<p class="facts"><span><b>Group</b> Document lifecycle</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `activate` | No | True | boolean |  |
| `kind` | No | project | string |  |
| `name` | No | None | any |  |
| `save_as` | No | None | any |  |
| `template` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `process_id` | No | None | any |  |

## Behavior (registry text) {#behavior}

```text
Create a project or family from a template on the Revit workstation.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
