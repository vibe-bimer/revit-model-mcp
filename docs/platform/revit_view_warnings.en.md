---
description: "Read warnings involving elements present in a selected view. A warning may also involve elements outside the view. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries."
---

# View Warnings

`revit_view_warnings`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 1.0.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, with identical parameters</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_view_warnings.md)

## Contract differences from the release {#contract-diff}

The same-name tool has an identical contract to release 1.0.0.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | string | Exact non-template view name from revit_list_views, or a view ID as a decimal string. |

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
Read warnings involving elements present in a selected view. A warning may also involve elements outside the view. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
