---
description: "Write a new .xlsx issue register with element snapshots and review documents"
---

# Issue register

`revit_issue_register`

<p class="facts"><span><b>Group</b> Export and checks</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Write a new .xlsx issue register with element snapshots and review documents

[Same-name integration branch page](../platform/revit_issue_register.md)

## Copyable prompts {#prompts}

```text
Turn these eight issues into an .xlsx issue register
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `issues` | Yes | — | `array<object>` | Issue objects with title, category, finding and severity. |
| `output_path` | Yes | — | `string` | New .xlsx issue register path, resolved on the machine running this server; existing files are refused. |
| `project` | Yes | — | `object` | project metadata object |
| `pixel_size` | No | `900` | `integer` | pixels along the fitted image dimension (1–4000) |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Write a new local .xlsx issue register with element snapshots and review documents. Takes 1 to 60 issues; captures at most 25 snapshots (by severity) within a 210-second budget, and failed snapshots become cell notes. Snapshots need local or SSH transport. Existing output files are refused. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
