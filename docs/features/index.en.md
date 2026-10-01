# Overview

<p class="facts">19 read + 14 action tools, 33 in total</p>

## By version

| Year | State |
| --- | --- |
| [Revit 2020](v2020.md) | <span class="state ok">validated</span> |
| [Revit 2026](v2026.md) | <span class="state ok">validated</span> <span class="state part">build only</span> |
| 2022–2025 / 2027 | <span class="state part">build only</span> |

## All tools

### Connection and documents（3）

| Tool | In one line | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_ping](revit_ping.md) | Check the RevitModelMcp connection without reading the model. | ✅ | ✅ |
| [revit_document_info](revit_document_info.md) | Read general information about the active Revit model. | ✅ | ✅ |
| [revit_list_instances](revit_list_instances.md) | List Revit processes and their active documents. | ✅ | ✅ |

### Query and totals（5）

| Tool | In one line | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_list_catalog](revit_list_catalog.md) | Discover valid model names before filtering. | ✅ | ✅ |
| [revit_aggregate_elements](revit_aggregate_elements.md) | Summarize matching elements by one or two fields after revit_list_catalog. | ✅ | ✅ |
| [revit_query_elements](revit_query_elements.md) | Read a page of matching element rows after revit_list_catalog. | ✅ | ✅ |
| [revit_element_details](revit_element_details.md) | Read parameters and geometry of an element by Revit ID. | ✅ | ✅ |
| [revit_list_relations](revit_list_relations.md) | Read model object membership or dependencies. | ✅ | ✅ |

### Views and snapshots（5）

| Tool | In one line | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_list_views](revit_list_views.md) | Find non-template views before analyzing a view. | ✅ | ✅ |
| [revit_view_summary](revit_view_summary.md) | Read element categories and counts for a selected view. | ✅ | ✅ |
| [revit_export_view](revit_export_view.md) | Export a selected view to PNG when numbers do not explain geometry. | ✅ | ✅ |
| [revit_view_elements](revit_view_elements.md) | Read one page of elements in a selected view. | ✅ | ✅ |
| [revit_view_warnings](revit_view_warnings.md) | Read warnings involving elements present in a selected view. | ✅ | ✅ |

### Export and checks（6）

| Tool | In one line | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_model_health](revit_model_health.md) | Read model quality counts before an export or hand-over. | ✅ | ✅ |
| [revit_links_status](revit_links_status.md) | Read RVT, CAD and image link status before an export or hand-over. | ✅ | ✅ |
| [revit_shared_coordinates](revit_shared_coordinates.md) | Read project and survey coordinates before an export or hand-over. | ✅ | ✅ |
| [revit_parameter_fill_check](revit_parameter_fill_check.md) | Count filled, empty and missing parameters before an export or hand-over. | ✅ | ✅ |
| [revit_export_element_ids](revit_export_element_ids.md) | Write the identifier register of the drawn components to an xlsx file on the Revit workstation. | ✅ | ✅ |
| [revit_list_warnings](revit_list_warnings.md) | Group model warnings by description text. | ✅ | ✅ |

### Selection and display（3）

| Tool | In one line | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_select](revit_select.md) | Select element IDs for inspection in Revit; an empty list clears selection; IDs are unitless. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. | ✅ | ✅ |
| [revit_show](revit_show.md) | Show elements, optionally selecting them; open a level plan or 3D view when needed. Returns activeView, viewOpened and dialogsSuppressed; IDs are unitless. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. | ✅ | ✅ |
| [revit_isolate](revit_isolate.md) | Temporarily isolate IDs for visual review in the active view, or reset with an empty list; IDs are unitless. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. | ✅ | ✅ |

### Editing（6）

| Tool | In one line | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_move](revit_move.md) | Move elements when adjusting their position; dx_mm, dy_mm and dz_mm are offsets in millimetres on model axes. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. | ✅ | ✅ |
| [revit_place_family](revit_place_family.md) | Place a loaded unhosted family on a named level for layout. | ✅ | 🟡 |
| [revit_create_wall](revit_create_wall.md) | Create a straight wall for layout on a named level; model XY endpoints and height are millimetres; null wall_type chooses the first basic type. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. | ✅ | ✅ |
| [revit_create_floor](revit_create_floor.md) | Create a floor from a closed boundary for layout on a named level. points_mm are model XY polygon vertices in millimetres (at least 3; the boundary closes automatically); null floor_type chooses the first floor type. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. | ✅ | 🟡 |
| [revit_set_parameter](revit_set_parameter.md) | Set a named instance parameter, falling back to its shared type; use for edits, with length in mm, area in m2 and other doubles in internal units. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. | ✅ | ✅ |
| [revit_delete](revit_delete.md) | Delete elements and their Revit dependencies when removal is intended; IDs are unitless and the returned count includes dependents. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected. | ✅ | ✅ |

### Phases（2）

| Tool | In one line | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_set_phase](revit_set_phase.md) | Assign the created or demolished project phase of elements by exact phase name. | ✅ | 🟡 |
| [revit_merge_phases](revit_merge_phases.md) | Merge one project phase into another by moving every element reference. | ✅ | 🟡 |

### Batch and ids（3）

| Tool | In one line | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_reset_element_ids](revit_reset_element_ids.md) | Replace elements with copies so Revit assigns new element IDs; the API cannot assign one itself. | ✅ | 🟡 |
| [revit_rebuild_model_ids](revit_rebuild_model_ids.md) | Give every component new IDs by copying a 3D view's selectable elements into a new model, because Revit does not allow assigning an element ID. | ✅ | 🟡 |
| [revit_batch](revit_batch.md) | Execute up to 50 actions with one undo step; roll back the batch on its first failure. | ✅ | ✅ |

!!! warning "Write gate: REVIT_MCP_ALLOW_WRITE=1 in the client plus the allow-write file on the workstation, with one Revit instance"
