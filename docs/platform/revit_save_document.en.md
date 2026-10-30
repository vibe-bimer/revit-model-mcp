---
description: "Save a document. Needs confirm_token from a first call, which changes nothing."
---

# Save Document

`revit_save_document`

<p class="facts"><span><b>Group</b> Document lifecycle</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `compact` | No | False | boolean |  |
| `confirm_token` | No | None | any |  |
| `overwrite` | No | False | boolean |  |
| `save_as` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | Yes | — | string |  |
| `process_id` | No | None | any |  |

## Behavior (registry text) {#behavior}

```text
Save a document. Needs confirm_token from a first call, which changes nothing.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
