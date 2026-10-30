# Close Document

`revit_close_document`

<p class="facts"><span><b>Group</b> Document lifecycle</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `confirm_token` | No | None | any |  |
| `save` | No | False | boolean |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | Yes | — | string |  |
| `process_id` | No | None | any |  |

## Behavior (registry text) {#behavior}

```text
Close a background document. Needs confirm_token from a first call, which changes nothing.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
