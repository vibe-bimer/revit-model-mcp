---
description: "Build a local Excel report from snapshots without contacting Revit"
---

# Build snapshot report

`revit_build_report`

<p class="facts"><span><b>Group</b> Export and checks</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Build a local Excel report from snapshots without contacting Revit

[Same-name integration branch page](../platform/revit_build_report.md)

## Copyable prompts {#prompts}

```text
Turn the snapshots in the snapshots folder into an Excel report
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `output_path` | Yes | — | `string` | New .xlsx file path, resolved on the machine running this server; existing files are never replaced. |
| `snapshots_dir` | Yes | — | `string` | Directory of schema-version-1 JSON snapshots on the MCP client machine. |
| `findings` | No | `null` | `array<object> / null` | Optional findings with model, severity, rule, element_ids (or elementIds), and recommendation. |
| `previous_dir` | No | `null` | `string / null` | Optional directory of earlier snapshots matched by model title for the Changes sheet. |

</div>

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Build a local Excel report from snapshots without contacting Revit.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
