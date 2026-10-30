---
description: "Export NWC on the Revit workstation; needs the Navisworks exporter. settings_xml applies exporter XML values, explicit arguments take precedence. Replacing an existing file (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action."
---

# Export Navisworks NWC

`revit_export_nwc`

<p class="facts"><span><b>Group</b> Export and registers</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `confirm_token` | No | `null` | any |  |
| `convert_element_properties` | No | `null` | any |  |
| `convert_lights` | No | `null` | any |  |
| `convert_linked_cad_formats` | No | `null` | any |  |
| `coordinates` | No | `null` | any |  |
| `divide_file_into_levels` | No | `null` | any |  |
| `dry_run` | No | `false` | boolean |  |
| `element_ids` | No | `null` | any |  |
| `export_element_ids` | No | `null` | any |  |
| `export_links` | No | `null` | any |  |
| `export_parts` | No | `null` | any |  |
| `export_room_as_attribute` | No | `null` | any |  |
| `export_room_geometry` | No | `null` | any |  |
| `export_urls` | No | `null` | any |  |
| `faceting_factor` | No | `null` | any |  |
| `find_missing_materials` | No | `null` | any |  |
| `overwrite` | No | `false` | boolean |  |
| `parameters` | No | `null` | any |  |
| `path` | Yes | — | string |  |
| `scope` | No | `null` | any |  |
| `settings_xml` | No | `null` | any |  |
| `view` | No | `null` | any |  |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | `1800` | integer |  |

</div>

## Behavior (registry text) {#behavior}

```text
Export NWC on the Revit workstation; needs the Navisworks exporter. settings_xml applies exporter XML values, explicit arguments take precedence. Replacing an existing file (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
