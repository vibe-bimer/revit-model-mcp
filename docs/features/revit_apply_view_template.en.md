---
description: "Apply a matching view template to one or more views"
---

# Apply view template

`revit_apply_view_template`

<p class="facts"><span><b>Group</b> Views and snapshots</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Apply a matching view template to one or more views

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_apply_view_template.md)

## Copyable prompts {#prompts}

```text
Apply the "MEP Documentation" view template to all HVAC plan views
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `template` | Yes | — | `string` | name of the view template to apply |
| `views` | Yes | — | `array<string>` | names of the views to apply the template to |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Apply a matching view template to one or more views.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
