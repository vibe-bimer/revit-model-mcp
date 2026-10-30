# Open Document

`revit_open_document`

<p class="facts"><span><b>Group</b> Document lifecycle</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `activate` | No | False | boolean |  |
| `audit` | No | False | boolean |  |
| `mode` | No | detached | string |  |
| `path` | Yes | — | string |  |
| `worksets` | No | all | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `process_id` | No | None | any |  |

## Behavior (registry text) {#behavior}

```text
Open a local, UNC or RSN model. Central models open detached by default. Cloud paths are unsupported. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
