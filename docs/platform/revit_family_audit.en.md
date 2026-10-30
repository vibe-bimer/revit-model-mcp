# Audit Families

`revit_family_audit`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `detail` | No | summary | string |  |
| `families` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | 600 | integer |  |

## Behavior (registry text) {#behavior}

```text
Audit an open family or named project families without saving or loading changes. Project mode takes exact family names or ["*"]; family mode takes none. detail="summary" returns parameter counts and up to 20 unused parameter names; detail="full" returns all parameter metadata with group IDs and groupName labels. The wildcard audits the first 200 editable families sorted by name; data.skipped lists each remaining name and reason, with skippedCount. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
