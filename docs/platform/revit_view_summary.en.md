---
description: "Read element categories and counts for a selected view. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries."
---

# View Summary

`revit_view_summary`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, but the parameters differ</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_view_summary.md)

## Contract differences from the release {#contract-diff}

The table below is computed from the registry inputSchema; it is not a hand-written list.

- Parameter pickup_timeout_seconds exists only in the release
- Parameter process_id exists only on the integration branch

This contract belongs to the integration branch, not to release 0.9.0; copying the branch parameters fails on the release.

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | string | Exact non-template view name from revit_list_views, or a view ID as a decimal string. |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | `null` | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | `120` | integer | Seconds to wait for a result (default 120). |

## Behavior (registry text) {#behavior}

```text
Read element categories and counts for a selected view. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
