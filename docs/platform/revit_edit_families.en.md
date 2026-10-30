---
description: "Edit an open family in place, or named project families (exact names or [\"*\"]), one load cycle each. A dry run rolls back all changes. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action."
---

# Edit Families

`revit_edit_families`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | `false` | boolean |  |
| `families` | No | `null` | any |  |
| `operations` | Yes | — | array |  |
| `overwrite_parameter_values` | No | `false` | boolean |  |
| `stop_on_error` | No | `true` | boolean |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | `1800` | integer |  |

## Behavior (registry text) {#behavior}

```text
Edit an open family in place, or named project families (exact names or ["*"]), one load cycle each. A dry run rolls back all changes. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
