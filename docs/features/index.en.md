# Feature overview

19 read + 15 action tools, 34 in total

## Browse by Revit year {#by-version}

| Revit year | Validation |
| --- | --- |
| [Revit 2020](v2020.md) | 19/19 reads and 15/15 actions validated live; the rest are build-only |
| [Revit 2026](v2026.md) | 18/19 reads and 8/15 actions validated live; the rest are build-only |
| 2022–2025 / 2027 | Build only, not live-tested |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

## All features {#all-features}

### Connection and documents (3) {#group-connection}

| Tool | Purpose |
| --- | --- |
| [Check connection](revit_ping.md)<br>`revit_ping` | Check whether the Revit add-in is reachable |
| [Document overview](revit_document_info.md)<br>`revit_document_info` | Read document metadata, levels, area schemes, worksets and view count |
| [Revit instance list](revit_list_instances.md)<br>`revit_list_instances` | List running Revit instances and their active documents |

### Query and totals (5) {#group-query}

| Tool | Purpose |
| --- | --- |
| [Name catalog](revit_list_catalog.md)<br>`revit_list_catalog` | Discover categories, family types, levels, area schemes, views, worksets, phases and parameters |
| [Grouped totals](revit_aggregate_elements.md)<br>`revit_aggregate_elements` | Group by one or two fields, with counts and optional sum and average |
| [Element query](revit_query_elements.md)<br>`revit_query_elements` | Filter and page through individual element rows |
| [Element details](revit_element_details.md)<br>`revit_element_details` | Read instance/type parameters and geometry for one element ID |
| [Element relations](revit_list_relations.md)<br>`revit_list_relations` | Read level rooms, area-scheme membership, group members, nested families and view-template dependents |

### Views and snapshots (6) {#group-views}

| Tool | Purpose |
| --- | --- |
| [View catalog](revit_list_views.md)<br>`revit_list_views` | List views filtered by type and name |
| [View summary](revit_view_summary.md)<br>`revit_view_summary` | Read view metadata, category counts and number of distinct types |
| [Export view image](revit_export_view.md)<br>`revit_export_view` | Export a view as a PNG, from 1 to 4000 pixels |
| [View element rows](revit_view_elements.md)<br>`revit_view_elements` | Page through elements in a selected view, optionally filtered by category |
| [View warnings](revit_view_warnings.md)<br>`revit_view_warnings` | Read warnings involving elements present in a selected view |
| [Set view lighting](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme |

### Export and checks (6) {#group-export}

| Tool | Purpose |
| --- | --- |
| [Model health](revit_model_health.md)<br>`revit_model_health` | Check file size, model counts, units and frequent warnings |
| [Link status](revit_links_status.md)<br>`revit_links_status` | Inspect RVT, CAD and image link status, paths and instance counts |
| [Shared coordinates](revit_shared_coordinates.md)<br>`revit_shared_coordinates` | Read base/survey points, sites and link offsets in mm and degrees |
| [Parameter fill check](revit_parameter_fill_check.md)<br>`revit_parameter_fill_check` | Count filled, empty and missing parameter values and sample element IDs |
| [Export element ID register](revit_export_element_ids.md)<br>`revit_export_element_ids` | Write the ID register of drawn model components to an Excel workbook |
| [Model warnings](revit_list_warnings.md)<br>`revit_list_warnings` | Group model warnings by description and inspect affected elements |

### Selection and display (3) {#group-display}

| Tool | Purpose |
| --- | --- |
| [Select elements](revit_select.md)<br>`revit_select` | Select elements in Revit; an empty list clears the selection |
| [Show elements](revit_show.md)<br>`revit_show` | Locate and highlight elements, opening a suitable view when needed |
| [Temporary isolation](revit_isolate.md)<br>`revit_isolate` | Temporarily isolate selected elements or reset the active view |

### Editing (6) {#group-edit}

| Tool | Purpose |
| --- | --- |
| [Move elements](revit_move.md)<br>`revit_move` | Move elements by offsets along model axes in millimetres |
| [Place unhosted family](revit_place_family.md)<br>`revit_place_family` | Place a loaded unhosted family on a named level with optional Z rotation |
| [Create straight wall](revit_create_wall.md)<br>`revit_create_wall` | Create a wall from two XY points, a level, type and height |
| [Create floor](revit_create_floor.md)<br>`revit_create_floor` | Create a floor from a closed XY boundary with at least three vertices |
| [Edit parameter](revit_set_parameter.md)<br>`revit_set_parameter` | Set a named parameter; lengths use mm, areas m² and other doubles internal units |
| [Delete elements](revit_delete.md)<br>`revit_delete` | Delete selected elements and their Revit dependencies |

### Phases (2) {#group-phases}

| Tool | Purpose |
| --- | --- |
| [Set element phases](revit_set_phase.md)<br>`revit_set_phase` | Assign created/demolished phases; an empty string clears and null leaves unchanged |
| [Merge project phases](revit_merge_phases.md)<br>`revit_merge_phases` | Reassign references to another phase and attempt to delete the emptied phase |

### Batch and ids (3) {#group-ids}

| Tool | Purpose |
| --- | --- |
| [Replace IDs in place](revit_reset_element_ids.md)<br>`revit_reset_element_ids` | Replace eligible standalone elements with copies to obtain new IDs |
| [Rebuild IDs in new models](revit_rebuild_model_ids.md)<br>`revit_rebuild_model_ids` | Copy selectable 3D-view components into one or more new models with fresh IDs |
| [Batch actions](revit_batch.md)<br>`revit_batch` | Execute 1–50 actions as one undo step and roll back on the first failed step |

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.
