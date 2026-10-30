# Synchronize Document

`revit_sync_document`

<p class="facts"><span><b>Group</b> Document lifecycle</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `comment` | Yes | — | string |  |
| `compact` | No | False | boolean |  |
| `confirm_token` | No | None | any |  |
| `relinquish` | No | all | any |  |
| `save_local_after` | No | True | boolean |  |
| `save_local_before` | No | True | boolean |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | Yes | — | string |  |
| `process_id` | No | None | any |  |

## Behavior (registry text) {#behavior}

```text
Synchronize a workshared document with central. Needs confirm_token from a first call, which changes nothing.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
