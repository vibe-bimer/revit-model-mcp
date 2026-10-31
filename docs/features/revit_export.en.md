---
description: "Export PDF, DWG, IFC or schedule CSV files; a dry run returns planned names"
---

# Export Model Files

`revit_export`

<p class="facts"><span><b>Group</b> Export and checks</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Export PDF, DWG, IFC or schedule CSV files; a dry run returns planned names

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_export.md)

## Copyable prompts {#prompts}

```text
Export the 'A-101' view to PDF in 'C:\Out', showing the planned file names with a dry run first.
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `format` | Yes | — | `string` | export format: `pdf`, `dwg`, `ifc` or `csv` |
| `all_sheets` | No | `false` | `boolean` | whether to export all sheets |
| `confirm_token` | No | `null` | `string / null` | token returned by a first call and passed to a second confirming call |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `options` | No | `null` | `object / null` | Export options, by output format. |
| `output_dir` | No | `null` | `string / null` | output directory for the exported files |
| `overwrite` | No | `false` | `boolean` | replace the destination when it exists |
| `sheet_set` | No | `null` | `string / null` | name of the sheet set to export |
| `sheets` | No | `null` | `array<string / integer> / null` | names or ids of the sheets to export |
| `views` | No | `null` | `array<string / integer> / null` | Views to export. |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `1800` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

Export PDF, DWG, IFC or schedule CSV files on the Revit workstation; dry_run returns planned file names. Replacing existing files (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
