---
description: "Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs. Numeric zero counts as filled. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries."
---

# Parameter Fill Check

`revit_parameter_fill_check`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, but the parameters differ</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_parameter_fill_check.md)

## Contract differences from the release {#contract-diff}

The table below is computed from the registry inputSchema; it is not a hand-written list.

- Parameter pickup_timeout_seconds exists only in the release
- Parameter process_id exists only on the integration branch

This contract belongs to the integration branch, not to release 0.9.0; copying the branch parameters fails on the release.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `categories` | Yes | — | array | Category names (1 to 20) from the categories catalog; matches any listed category. |
| `include_types` | No | `true` | boolean | (not documented in the branch contract) |
| `level` | No | `null` | any | (not documented in the branch contract) |
| `parameters` | Yes | — | array | Exact localized parameter names (1 to 30); names that do not match count as missing. |
| `sample_limit` | No | `20` | integer | Maximum sampled element IDs per empty and missing list, 1 to 100 (default 20); counts always cover all elements. |
| `view` | No | `null` | any | Exact non-template view name; limits the search to that view. |
| `workset` | No | `null` | any | (not documented in the branch contract) |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | `null` | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | `120` | integer | Seconds to wait for a result (default 120). |

</div>

## Behavior (registry text) {#behavior}

```text
Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs. Numeric zero counts as filled. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
