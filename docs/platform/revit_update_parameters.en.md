# Update Parameters

`revit_update_parameters`

<p class="facts"><span><b>Group</b> Editing primitives</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | False | boolean |  |
| `filters` | Yes | — |  |  |
| `include_type_parameters` | No | False | boolean |  |
| `max_elements` | No | 5000 | integer |  |
| `parameter` | Yes | — | string |  |
| `parameter_id` | No | None | any |  |
| `value` | Yes | — | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Update a parameter on elements matching the same filters as revit_query_elements. Group members are reported in skipped.inGroup instead of failing the call; dry_run predicts this.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
