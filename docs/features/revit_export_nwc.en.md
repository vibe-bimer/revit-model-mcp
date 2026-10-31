---
description: "Export NWC on the Revit workstation; needs the Navisworks exporter, and overwriting needs a confirm token"
---

# Export Navisworks NWC

`revit_export_nwc`

<p class="facts"><span><b>Group</b> Export and checks</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Export NWC on the Revit workstation; needs the Navisworks exporter, and overwriting needs a confirm token

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_export_nwc.md)

## Copyable prompts {#prompts}

```text
Export the current view to D:\output\tower.nwc and overwrite it if it already exists
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `path` | Yes | — | `string` | path of the exported `.nwc` file |
| `confirm_token` | No | `null` | `string / null` | token returned by the first call and passed to a second confirming call |
| `convert_element_properties` | No | `null` | `boolean / null` | whether element properties are converted to NWC attributes |
| `convert_lights` | No | `null` | `boolean / null` | convert lights into NWC geometry |
| `convert_linked_cad_formats` | No | `null` | `boolean / null` | Whether linked CAD formats are converted during export. |
| `coordinates` | No | `null` | `string / null` | coordinate system used for the export |
| `divide_file_into_levels` | No | `null` | `boolean / null` | whether the exported file is divided into levels |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `element_ids` | No | `null` | `array<integer> / null` | element ids (unitless Revit ids) |
| `export_element_ids` | No | `null` | `boolean / null` | export element ids into the NWC file |
| `export_links` | No | `null` | `boolean / null` | Whether linked models are exported with the file. |
| `export_parts` | No | `null` | `boolean / null` | parts of the model to export |
| `export_room_as_attribute` | No | `null` | `boolean / null` | whether rooms are exported as attributes |
| `export_room_geometry` | No | `null` | `boolean / null` | export room geometry into the NWC file |
| `export_urls` | No | `null` | `boolean / null` | Whether URLs are exported with the file. |
| `faceting_factor` | No | `null` | `number / null` | faceting factor applied to the export |
| `find_missing_materials` | No | `null` | `boolean / null` | whether missing materials are found and reported |
| `overwrite` | No | `false` | `boolean` | replace the destination when it exists |
| `parameters` | No | `null` | `string / null` | parameter names to count |
| `scope` | No | `null` | `string / null` | Export scope, model, view, or selection. |
| `settings_xml` | No | `null` | `string / null` | path of the export settings file |
| `view` | No | `null` | `string / integer / null` | view name (or its Revit id) |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `1800` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

Export NWC on the Revit workstation; needs the Navisworks exporter. settings_xml applies exporter XML values, explicit arguments take precedence. Replacing an existing file (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
