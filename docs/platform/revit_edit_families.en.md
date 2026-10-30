# Edit Families

`revit_edit_families`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | False | boolean |  |
| `families` | No | None | any |  |
| `operations` | Yes | — | array |  |
| `overwrite_parameter_values` | No | False | boolean |  |
| `stop_on_error` | No | True | boolean |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | 1800 | integer |  |

## Behavior (registry text) {#behavior}

```text
Edit an open family in place, or named project families (exact names or ["*"]), one load cycle each. A dry run rolls back all changes. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
