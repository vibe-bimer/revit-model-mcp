# Version support matrix

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

## Read tools (19) {'#read-tools' if read_only else '#action-tools'}

| Tool | 2020 | 2026 | 2022–2025 / 2027 |
| --- | :--: | :--: | :--: |
| [Check connection](revit_ping.md)<br>`revit_ping` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Document overview](revit_document_info.md)<br>`revit_document_info` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Model health](revit_model_health.md)<br>`revit_model_health` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Link status](revit_links_status.md)<br>`revit_links_status` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Shared coordinates](revit_shared_coordinates.md)<br>`revit_shared_coordinates` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Parameter fill check](revit_parameter_fill_check.md)<br>`revit_parameter_fill_check` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Name catalog](revit_list_catalog.md)<br>`revit_list_catalog` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Grouped totals](revit_aggregate_elements.md)<br>`revit_aggregate_elements` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Element query](revit_query_elements.md)<br>`revit_query_elements` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [View catalog](revit_list_views.md)<br>`revit_list_views` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [View summary](revit_view_summary.md)<br>`revit_view_summary` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Export view image](revit_export_view.md)<br>`revit_export_view` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Export element ID register](revit_export_element_ids.md)<br>`revit_export_element_ids` | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> | <span class="state part">Build only, not live-tested</span> |
| [View element rows](revit_view_elements.md)<br>`revit_view_elements` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Element details](revit_element_details.md)<br>`revit_element_details` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [View warnings](revit_view_warnings.md)<br>`revit_view_warnings` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Model warnings](revit_list_warnings.md)<br>`revit_list_warnings` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Element relations](revit_list_relations.md)<br>`revit_list_relations` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Revit instance list](revit_list_instances.md)<br>`revit_list_instances` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |

## Action tools (16) {'#read-tools' if read_only else '#action-tools'}

| Tool | 2020 | 2026 | 2022–2025 / 2027 |
| --- | :--: | :--: | :--: |
| [Select elements](revit_select.md)<br>`revit_select` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Show elements](revit_show.md)<br>`revit_show` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Temporary isolation](revit_isolate.md)<br>`revit_isolate` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Move elements](revit_move.md)<br>`revit_move` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Place unhosted family](revit_place_family.md)<br>`revit_place_family` | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> | <span class="state part">Build only, not live-tested</span> |
| [Create straight wall](revit_create_wall.md)<br>`revit_create_wall` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Create floor](revit_create_floor.md)<br>`revit_create_floor` | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> | <span class="state part">Build only, not live-tested</span> |
| [Create level](revit_create_level.md)<br>`revit_create_level` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Set element phases](revit_set_phase.md)<br>`revit_set_phase` | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> | <span class="state part">Build only, not live-tested</span> |
| [Merge project phases](revit_merge_phases.md)<br>`revit_merge_phases` | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> | <span class="state part">Build only, not live-tested</span> |
| [Edit parameter](revit_set_parameter.md)<br>`revit_set_parameter` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Set view lighting](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> | <span class="state part">Build only, not live-tested</span> |
| [Delete elements](revit_delete.md)<br>`revit_delete` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
| [Replace IDs in place](revit_reset_element_ids.md)<br>`revit_reset_element_ids` | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> | <span class="state part">Build only, not live-tested</span> |
| [Rebuild IDs in new models](revit_rebuild_model_ids.md)<br>`revit_rebuild_model_ids` | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> | <span class="state part">Build only, not live-tested</span> |
| [Batch actions](revit_batch.md)<br>`revit_batch` | <span class="state ok">Validated live</span> | <span class="state ok">Validated live</span> | <span class="state part">Build only, not live-tested</span> |
