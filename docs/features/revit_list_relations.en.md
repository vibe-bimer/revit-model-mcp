---
description: "Read level rooms, area-scheme membership, group members, nested families and view-template dependents"
---

# Element relations

`revit_list_relations`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.7.0</span><span><b>Version</b> Released 0.9.0</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span></p>

Read level rooms, area-scheme membership, group members, nested families and view-template dependents

[Same-name integration branch page](../platform/revit_list_relations.md)

## Copyable prompts {#prompts}

```text
Which rooms sit on level 1F?
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `relation` | Yes | — | `string` | which relation to read: level-rooms, area-scheme-elements, group-elements, nested-family or view-template-dependents |
| `process_id` | No | `null` | `integer / null` | Revit process ID; takes precedence over document. |
| `source_id` | No | `null` | `integer / null` | Revit id of the source object, a group or a family instance |
| `source_name` | No | `null` | `string / null` | name of the source, a level, area scheme or view template |

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

Read model object membership or dependencies. relation is level-rooms, area-scheme-elements or view-template-dependents (with source_name), or group-elements or nested-family (with source_id). A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
