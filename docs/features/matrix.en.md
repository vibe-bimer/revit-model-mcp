# Version matrix

<p class="facts">✅ validated　🟡 build only</p>

## Read tools（19）

| Tool | 2020 | 2026 | Other years | Note |
| --- | :--: | :--: | :--: | --- |
| [revit_ping](revit_ping.md) | ✅ | ✅ | 🟡 | Check the RevitModelMcp connection without reading the model. |
| [revit_document_info](revit_document_info.md) | ✅ | ✅ | 🟡 | Read general information about the active Revit model. |
| [revit_model_health](revit_model_health.md) | ✅ | ✅ | 🟡 | Read model quality counts before an export or hand-over. |
| [revit_links_status](revit_links_status.md) | ✅ | ✅ | 🟡 | Read RVT, CAD and image link status before an export or hand-over. |
| [revit_shared_coordinates](revit_shared_coordinates.md) | ✅ | ✅ | 🟡 | Read project and survey coordinates before an export or hand-over. |
| [revit_parameter_fill_check](revit_parameter_fill_check.md) | ✅ | ✅ | 🟡 | Count filled, empty and missing parameters before an export or hand-over. |
| [revit_list_catalog](revit_list_catalog.md) | ✅ | ✅ | 🟡 | Queries and filters use these exact names |
| [revit_aggregate_elements](revit_aggregate_elements.md) | ✅ | ✅ | 🟡 | First choice for “how many” questions |
| [revit_query_elements](revit_query_elements.md) | ✅ | ✅ | 🟡 | Read a page of matching element rows after revit_list_catalog. |
| [revit_list_views](revit_list_views.md) | ✅ | ✅ | 🟡 | Find non-template views before analyzing a view. |
| [revit_view_summary](revit_view_summary.md) | ✅ | ✅ | 🟡 | Read element categories and counts for a selected view. |
| [revit_export_view](revit_export_view.md) | ✅ | ✅ | 🟡 | Export a selected view to PNG when numbers do not explain geometry. |
| [revit_export_element_ids](revit_export_element_ids.md) | ✅ | ✅ | 🟡 | The workbook is written on the Revit workstation |
| [revit_view_elements](revit_view_elements.md) | ✅ | ✅ | 🟡 | Read one page of elements in a selected view. |
| [revit_element_details](revit_element_details.md) | ✅ | ✅ | 🟡 | Rooms also return area, volume and boundaries |
| [revit_view_warnings](revit_view_warnings.md) | ✅ | ✅ | 🟡 | Read warnings involving elements present in a selected view. |
| [revit_list_warnings](revit_list_warnings.md) | ✅ | ✅ | 🟡 | Group model warnings by description text. |
| [revit_list_relations](revit_list_relations.md) | ✅ | ✅ | 🟡 | Read model object membership or dependencies. |
| [revit_list_instances](revit_list_instances.md) | ✅ | ✅ | 🟡 | List Revit processes and their active documents. |

## Action tools（14）

| Tool | 2020 | 2026 | Other years | Note |
| --- | :--: | :--: | :--: | --- |
| [revit_select](revit_select.md) | ✅ | ✅ | 🟡 | Does not change the model |
| [revit_show](revit_show.md) | ✅ | ✅ | 🟡 | Does not change the model |
| [revit_isolate](revit_isolate.md) | ✅ | ✅ | 🟡 | Temporary effect only |
| [revit_move](revit_move.md) | ✅ | ✅ | 🟡 | Supports dry_run |
| [revit_place_family](revit_place_family.md) | ✅ | 🟡 | 🟡 | Not run live on 2026 |
| [revit_create_wall](revit_create_wall.md) | ✅ | ✅ | 🟡 | Create a straight wall for layout on a named level; model XY endpoints and height are millimetres; null wall_type chooses the first basic type. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. |
| [revit_create_floor](revit_create_floor.md) | ✅ | 🟡 | 🟡 | On 2020 it uses Document.Create.NewFloor, from 2022 Floor.Create |
| [revit_set_phase](revit_set_phase.md) | ✅ | 🟡 | 🟡 | The phase order API exists from 2022; 2020 uses a fallback |
| [revit_merge_phases](revit_merge_phases.md) | ✅ | 🟡 | 🟡 | Cannot run inside batch |
| [revit_set_parameter](revit_set_parameter.md) | ✅ | ✅ | 🟡 | Supports dry_run |
| [revit_delete](revit_delete.md) | ✅ | ✅ | 🟡 | Supports dry_run |
| [revit_reset_element_ids](revit_reset_element_ids.md) | ✅ | 🟡 | 🟡 | Limited coverage: MEP 27/1089, building 373/954, structure 0% |
| [revit_rebuild_model_ids](revit_rebuild_model_ids.md) | ✅ | 🟡 | 🟡 | The source stays read-only; 899 components a copy, no shared ids |
| [revit_batch](revit_batch.md) | ✅ | ✅ | 🟡 | Rolls the whole batch back when a step fails |
