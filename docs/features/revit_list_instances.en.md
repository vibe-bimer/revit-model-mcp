---
description: "List running Revit instances and their active documents"
---

# Revit instance list

`revit_list_instances`

<p class="facts"><span><b>Group</b> Connection and documents</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.6.0</span><span><b>Version</b> Released 0.9.0</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

List running Revit instances and their active documents

[Same-name integration branch page](../platform/revit_list_instances.md)

## Copyable prompts {#prompts}

```text
Which Revit instances are running, and what does each hold?
```

## Parameters {#parameters}

No additional business parameters; use the common parameters below.

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

List Revit processes with documentName, documentPath, revitVersion, processId and pluginResponding. Busy or unresponsive processes stay listed with pluginResponding=false. HTTP mode reports only its connected process.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
