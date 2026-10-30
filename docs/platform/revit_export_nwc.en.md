# Export Navisworks NWC

`revit_export_nwc`

<p class="facts"><span><b>Group</b> Export and registers</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `confirm_token` | No | None | any |  |
| `convert_element_properties` | No | None | any |  |
| `convert_lights` | No | None | any |  |
| `convert_linked_cad_formats` | No | None | any |  |
| `coordinates` | No | None | any |  |
| `divide_file_into_levels` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `element_ids` | No | None | any |  |
| `export_element_ids` | No | None | any |  |
| `export_links` | No | None | any |  |
| `export_parts` | No | None | any |  |
| `export_room_as_attribute` | No | None | any |  |
| `export_room_geometry` | No | None | any |  |
| `export_urls` | No | None | any |  |
| `faceting_factor` | No | None | any |  |
| `find_missing_materials` | No | None | any |  |
| `overwrite` | No | False | boolean |  |
| `parameters` | No | None | any |  |
| `path` | Yes | — | string |  |
| `scope` | No | None | any |  |
| `settings_xml` | No | None | any |  |
| `view` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | 1800 | integer |  |

## Behavior (registry text) {#behavior}

```text
Export NWC on the Revit workstation; needs the Navisworks exporter. settings_xml applies exporter XML values, explicit arguments take precedence. Replacing an existing file (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
