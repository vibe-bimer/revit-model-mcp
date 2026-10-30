---
description: "Delete elements and their Revit dependencies; the count includes dependents. dry_run returns the count. Above 500 elements including dependents a confirm_token from a first call is needed; revit_run_actions refuses such deletions."
---

# Delete Elements

`revit_delete`

<p class="facts"><span><b>Group</b> Editing primitives</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, but the parameters differ</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_delete.md)

## Contract differences from the release {#contract-diff}

The table below is computed from the registry inputSchema; it is not a hand-written list.

- Parameter confirm_token exists only on the integration branch

This contract belongs to the integration branch, not to release 0.9.0; copying the branch parameters fails on the release.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `confirm_token` | No | `null` | any |  |
| `dry_run` | No | `false` | boolean |  |
| `element_ids` | Yes | — | array |  |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |

</div>

## Behavior (registry text) {#behavior}

```text
Delete elements and their Revit dependencies; the count includes dependents. dry_run returns the count. Above 500 elements including dependents a confirm_token from a first call is needed; revit_run_actions refuses such deletions.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
