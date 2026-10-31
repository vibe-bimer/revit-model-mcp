# Export Navisworks NWC

Export NWC on the Revit workstation; needs the Navisworks exporter.

**Group:** Export · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `path` | Yes | — | `string` | — |
| `confirm_token` | No | null | `string / null` | — |
| `convert_element_properties` | No | null | `boolean / null` | — |
| `convert_lights` | No | null | `boolean / null` | — |
| `convert_linked_cad_formats` | No | null | `boolean / null` | — |
| `coordinates` | No | null | `string (shared, internal) / null` | — |
| `divide_file_into_levels` | No | null | `boolean / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `element_ids` | No | null | `array of integer / null` | element ids (unitless Revit ids) |
| `export_element_ids` | No | null | `boolean / null` | — |
| `export_links` | No | null | `boolean / null` | — |
| `export_parts` | No | null | `boolean / null` | — |
| `export_room_as_attribute` | No | null | `boolean / null` | — |
| `export_room_geometry` | No | null | `boolean / null` | — |
| `export_urls` | No | null | `boolean / null` | — |
| `faceting_factor` | No | null | `number / null` | — |
| `find_missing_materials` | No | null | `boolean / null` | — |
| `overwrite` | No | false | `boolean` | replace the destination when it exists |
| `parameters` | No | null | `string (all, elements, none) / null` | — |
| `scope` | No | null | `string (model, view, selection) / null` | — |
| `settings_xml` | No | null | `string / null` | — |
| `view` | No | null | `string / integer / null` | view name (or its Revit id) |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Export NWC on the Revit workstation; needs the Navisworks exporter. settings_xml applies exporter XML values, explicit arguments take precedence. Replacing an existing file (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
