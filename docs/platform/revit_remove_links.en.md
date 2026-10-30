# Remove Links

`revit_remove_links`

<p class="facts"><span><b>Group</b> Links and datums</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `confirm_token` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `include_imported_cad` | No | False | boolean |  |
| `kinds` | No | None | any |  |
| `links` | Yes | — | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Delete selected link types and their instances; dry_run previews. Cannot be undone in Revit. Needs confirm_token from a first call, which changes nothing.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
