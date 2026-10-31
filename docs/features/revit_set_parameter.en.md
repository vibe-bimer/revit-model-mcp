---
description: "Set a named parameter; lengths use mm, areas m² and other doubles internal units"
---

# Edit parameter

`revit_set_parameter`

<p class="facts"><span><b>Group</b> Editing</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.1.0</span><span><b>Version</b> Released 0.9.0</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Set a named parameter; lengths use mm, areas m² and other doubles internal units

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Supports dry_run

[Same-name integration branch page](../platform/revit_set_parameter.md)

## Copyable prompts {#prompts}

```text
Set the fire rating of these walls to two hours
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `element_id` | Yes | — | `integer` | one element id |
| `parameter` | Yes | — | `string` | parameter name as the model reports it |
| `value` | Yes | — | `string / integer / number` | value to write; lengths in millimetres, areas in m², other doubles in internal units |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `parameter_id` | No | `null` | `string / null` | parameter identifier: BuiltInParameter name, shared GUID or parameter id |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Set one instance or type parameter. parameter_id selects by BuiltInParameter name, shared GUID or ParameterElement ID; otherwise parameter takes a localized UI name, BuiltInParameter name or English alias, and ambiguous matches are refused. Value is a string, integer or number by storage type; lengths in mm, areas in m2. Group members fail with a clear message. dry_run rolls back and returns the verification block.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
