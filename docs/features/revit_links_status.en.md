---
description: "Inspect RVT, CAD and image link status, paths and instance counts"
---

# Link status

`revit_links_status`

<p class="facts"><span><b>Group</b> Export and checks</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.2.0</span><span><b>Version</b> Released 0.9.0</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Inspect RVT, CAD and image link status, paths and instance counts

[Same-name integration branch page](../platform/revit_links_status.md)

## Copyable prompts {#prompts}

```text
Check every link: RVT, CAD and images
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |

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

Read RVT, CAD and image link status. Each list is capped at 100 entries; summary counts cover all links. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
