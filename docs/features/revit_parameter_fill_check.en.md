---
description: "Count filled, empty and missing parameter values and sample element IDs"
---

# Parameter fill check

`revit_parameter_fill_check`

<p class="facts"><span><b>Group</b> Export and checks</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.2.0</span><span><b>Version</b> Released 0.9.0</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Count filled, empty and missing parameter values and sample element IDs

[Same-name integration branch page](../platform/revit_parameter_fill_check.md)

## Copyable prompts {#prompts}

```text
How well is the fire rating filled in on walls? Give me the empty ids
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `categories` | Yes | — | `array<string>` | category names, combined with OR |
| `parameters` | Yes | — | `array<string>` | parameter names to count |
| `include_types` | No | `true` | `boolean` | fall back to type parameters when absent on the instance (true by default); does not add type elements to the count |
| `level` | No | `null` | `string / null` | restrict to one level |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |
| `sample_limit` | No | `20` | `integer` | how many sample ids to return per parameter |
| `view` | No | `null` | `string / null` | view name (or its Revit id) |
| `workset` | No | `null` | `string / null` | restrict to one workset |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs. Numeric zero counts as filled. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
