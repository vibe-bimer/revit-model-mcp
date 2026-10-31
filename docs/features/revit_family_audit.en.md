---
description: "Audit an open family or named project families without saving or loading changes; detail=full returns all parameter metadata"
---

# Audit families

`revit_family_audit`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Audit an open family or named project families without saving or loading changes; detail=full returns all parameter metadata

[Same-name integration branch page](../platform/revit_family_audit.md)

## Copyable prompts {#prompts}

```text
Audit all families in the project with the wildcard and show which parameters are unused
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `detail` | No | `"summary"` | `string` | Detail level of the family audit, summary or full. |
| `families` | No | `null` | `array<string> / null` | families to audit |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `600` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Audit an open family or named project families without saving or loading changes. Project mode takes exact family names or ["*"]; family mode takes none. detail="summary" returns parameter counts and up to 20 unused parameter names; detail="full" returns all parameter metadata with group IDs and groupName labels. The wildcard audits the first 200 editable families sorted by name; data.skipped lists each remaining name and reason, with skippedCount. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
