---
description: "Feature overview of every tool in the current release, grouped with each tool's purpose, parameters and Revit year support."
---

# Feature overview

35 read + 52 action tools, 87 in total

This section covers the 87 tools of the current release. The integration branch's 80 tools, split into base and fork, are in the [platform tool catalog](../platform/index.md).

## Version entries {#versions}

This catalog records the released version. The integration branch is unreleased, and the two differ in both count and tool list. The status, version number and counts below are read from the registries.

| | Released 0.9.0 | Integration branch |
| --- | --- | --- |
| Version | 0.9.0 | 1.0.0 Unreleased (integration branch) |
| Branch | main | `integration/upstream-1.0` |
| Tool | 87 | 80 |
| Catalog | index.md | [Platform tool catalog](../platform/index.md) |

## Browse by Revit year {#by-version}

| Revit year | Validation |
| --- | --- |
| [Revit 2020](v2020.md) | 19/35 reads and 15/52 actions validated live; the rest are build-only |
| [Revit 2026](v2026.md) | 18/35 reads and 8/52 actions validated live; the rest are build-only |
| 2022–2025 / 2027 | Build only, not live-tested |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

## All features {#all-features}

### Connection and documents (3) {#group-connection}

| Tool | Purpose |
| --- | --- |
| [Check connection](revit_ping.md)<br>`revit_ping` | Check whether the Revit add-in is reachable |
| [Document overview](revit_document_info.md)<br>`revit_document_info` | Read document metadata, levels, area schemes, worksets and view count |
| [Revit instance list](revit_list_instances.md)<br>`revit_list_instances` | List running Revit instances and their active documents |

### Query and totals (6) {#group-query}

| Tool | Purpose |
| --- | --- |
| [Revit UI state](revit_ui_state.md)<br>`revit_ui_state` | Read the active document, open views, selection and open documents |
| [Name catalog](revit_list_catalog.md)<br>`revit_list_catalog` | Discover categories, family types, levels, area schemes, views, worksets, phases and parameters |
| [Grouped totals](revit_aggregate_elements.md)<br>`revit_aggregate_elements` | Group by one or two fields, with counts and optional sum and average |
| [Element query](revit_query_elements.md)<br>`revit_query_elements` | Filter and page through individual element rows |
| [Element details](revit_element_details.md)<br>`revit_element_details` | Read instance/type parameters and geometry for one element ID |
| [Element relations](revit_list_relations.md)<br>`revit_list_relations` | Read level rooms, area-scheme membership, group members, nested families and view-template dependents |

### Views and snapshots (13) {#group-views}

| Tool | Purpose |
| --- | --- |
| [View catalog](revit_list_views.md)<br>`revit_list_views` | List views filtered by type and name |
| [View Info](revit_view_info.md)<br>`revit_view_info` | Inspect one view's template, display, categories, worksets, filters and links |
| [View summary](revit_view_summary.md)<br>`revit_view_summary` | Read view metadata, category counts and number of distinct types |
| [Export view image](revit_export_view.md)<br>`revit_export_view` | Export a view as a PNG, from 1 to 4000 pixels |
| [View element rows](revit_view_elements.md)<br>`revit_view_elements` | Page through elements in a selected view, optionally filtered by category |
| [View warnings](revit_view_warnings.md)<br>`revit_view_warnings` | Read warnings involving elements present in a selected view |
| [Activate view](revit_activate_view.md)<br>`revit_activate_view` | Activate a non-template view, then zoom to fit or frame element ids |
| [Close views](revit_close_views.md)<br>`revit_close_views` | Close open UI views in the active document |
| [Set View Visibility](revit_set_view_visibility.md)<br>`revit_set_view_visibility` | Change category, workset and filter visibility in one view, with a dry-run preview |
| [Create view](revit_create_view.md)<br>`revit_create_view` | Create a plan, section, 3D or drafting view; box coordinates are model mm |
| [Duplicate view](revit_duplicate_view.md)<br>`revit_duplicate_view` | Duplicate a view, optionally with detailing or as a dependent view |
| [Apply view template](revit_apply_view_template.md)<br>`revit_apply_view_template` | Apply a matching view template to one or more views |
| <span class="state part">Fork</span> [Set view lighting](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme |

### Export and checks (12) {#group-export}

| Tool | Purpose |
| --- | --- |
| [Check NWC Settings](revit_nwc_settings_check.md)<br>`revit_nwc_settings_check` | Parse a Navisworks exporter XML on the workstation without exporting |
| [Model snapshot](revit_model_snapshot.md)<br>`revit_model_snapshot` | Read a schema version 1 project snapshot for batch audits; closed worksets can leave it incomplete |
| [Model health](revit_model_health.md)<br>`revit_model_health` | Check file size, model counts, units and frequent warnings |
| [Link status](revit_links_status.md)<br>`revit_links_status` | Inspect RVT, CAD and image link status, paths and instance counts |
| [Shared coordinates](revit_shared_coordinates.md)<br>`revit_shared_coordinates` | Read base/survey points, sites and link offsets in mm and degrees |
| [Parameter fill check](revit_parameter_fill_check.md)<br>`revit_parameter_fill_check` | Count filled, empty and missing parameter values and sample element IDs |
| [Model warnings](revit_list_warnings.md)<br>`revit_list_warnings` | Group model warnings by description and inspect affected elements |
| [Export Model Files](revit_export.md)<br>`revit_export` | Export PDF, DWG, IFC or schedule CSV files; a dry run returns planned names |
| [Export Navisworks NWC](revit_export_nwc.md)<br>`revit_export_nwc` | Export NWC on the Revit workstation; needs the Navisworks exporter, and overwriting needs a confirm token |
| <span class="state part">Fork</span> [Export element ID register](revit_export_element_ids.md)<br>`revit_export_element_ids` | Write the ID register of drawn model components to an Excel workbook |
| [Build snapshot report](revit_build_report.md)<br>`revit_build_report` | Build a local Excel report from snapshots without contacting Revit |
| [Issue register](revit_issue_register.md)<br>`revit_issue_register` | Write a new .xlsx issue register with element snapshots and review documents |

### Selection and display (6) {#group-display}

| Tool | Purpose |
| --- | --- |
| [Capture elements](revit_capture_elements.md)<br>`revit_capture_elements` | Render a PNG marking 1 to 500 elements; the temporary view is rolled back |
| [Select elements](revit_select.md)<br>`revit_select` | Select elements in Revit; an empty list clears the selection |
| [Show elements](revit_show.md)<br>`revit_show` | Locate and highlight elements, opening a suitable view when needed |
| [Temporary isolation](revit_isolate.md)<br>`revit_isolate` | Temporarily isolate selected elements or reset the active view |
| [Highlight elements](revit_override_graphics.md)<br>`revit_override_graphics` | Colour elements in selected views; reset restores this session's overrides |
| [Tag elements](revit_tag_elements.md)<br>`revit_tag_elements` | Tag elements by category or element ids in a view; room tags need a plan view |

### Editing (17) {#group-edit}

| Tool | Purpose |
| --- | --- |
| [Execute C# code](revit_execute_code.md)<br>`revit_execute_code` | Compile and run C# on the Revit thread; auto mode owns one transaction and undo entry |
| [Undo last action](revit_undo_last.md)<br>`revit_undo_last` | Undo the last MCP action via Revit's own undo command, only when the target document is active and the session's undo entry matches |
| [Move elements](revit_move.md)<br>`revit_move` | Move elements by offsets along model axes in millimetres |
| [Rotate elements](revit_rotate.md)<br>`revit_rotate` | Rotate elements about a vertical axis through center_mm or their bounding-box center; dry_run rolls back, group, pinned and hosted elements are skipped |
| [Copy Elements](revit_copy.md)<br>`revit_copy` | Copy elements 1 to 100 times at a millimetre offset, rolled back on a dry run |
| [Mirror elements](revit_mirror.md)<br>`revit_mirror` | Mirror elements across a model X or Y parallel line through point_mm; dry_run rolls back |
| [Change element type](revit_change_type.md)<br>`revit_change_type` | Change each element to one compatible type; group members are skipped |
| [Update parameters](revit_update_parameters.md)<br>`revit_update_parameters` | Update a parameter on elements matching the same filters as revit_query_elements; group members are skipped and dry_run predicts the outcome |
| [Place unhosted family](revit_place_family.md)<br>`revit_place_family` | Place a loaded unhosted family on a named level with optional Z rotation |
| [Create straight wall](revit_create_wall.md)<br>`revit_create_wall` | Create a wall from two XY points, a level, type and height |
| [Create MEP run](revit_create_mep_run.md)<br>`revit_create_mep_run` | Create connected duct, pipe, tray or conduit runs from points in mm |
| [Build Walls from CAD](revit_walls_from_cad.md)<br>`revit_walls_from_cad` | Pair CAD lines into joined basic walls, bridging openings, with millimetre dimensions |
| [Edit parameter](revit_set_parameter.md)<br>`revit_set_parameter` | Set a named parameter; lengths use mm, areas m² and other doubles internal units |
| [Delete elements](revit_delete.md)<br>`revit_delete` | Delete selected elements and their Revit dependencies |
| [Process many models](revit_process_models.md)<br>`revit_process_models` | Open each model in the interactive session, run steps and C# code, and export or save as requested; in-place saves and code need a confirm_token |
| <span class="state part">Fork</span> [Create level](revit_create_level.md)<br>`revit_create_level` | Create a level at a given elevation in millimetres |
| <span class="state part">Fork</span> [Create floor](revit_create_floor.md)<br>`revit_create_floor` | Create a floor from a closed XY boundary with at least three vertices |

### Phases (2) {#group-phases}

| Tool | Purpose |
| --- | --- |
| <span class="state part">Fork</span> [Set element phases](revit_set_phase.md)<br>`revit_set_phase` | Assign created/demolished phases; an empty string clears and null leaves unchanged |
| <span class="state part">Fork</span> [Merge project phases](revit_merge_phases.md)<br>`revit_merge_phases` | Reassign references to another phase and attempt to delete the emptied phase |

### Batch and ids (2) {#group-ids}

| Tool | Purpose |
| --- | --- |
| <span class="state part">Fork</span> [Replace IDs in place](revit_reset_element_ids.md)<br>`revit_reset_element_ids` | Replace eligible standalone elements with copies to obtain new IDs |
| <span class="state part">Fork</span> [Rebuild IDs in new models](revit_rebuild_model_ids.md)<br>`revit_rebuild_model_ids` | Copy selectable 3D-view components into one or more new models with fresh IDs |

### Documents and processes (7) {#group-documents}

| Tool | Purpose |
| --- | --- |
| [List open documents](revit_documents.md)<br>`revit_documents` | List every open document in one Revit process, including background documents |
| [Open Document](revit_open_document.md)<br>`revit_open_document` | Open a local, UNC or RSN model on the workstation; central models open detached |
| [Activate document](revit_activate_document.md)<br>`revit_activate_document` | Activate an already open document by title or path reference |
| [New Document](revit_new_document.md)<br>`revit_new_document` | Create a project or family from a template on the Revit workstation |
| [Close document](revit_close_document.md)<br>`revit_close_document` | Close a background document; the first call changes nothing and returns the confirm token |
| [Save document](revit_save_document.md)<br>`revit_save_document` | Save a document; the first call only returns a confirm_token and changes nothing |
| [Synchronize document](revit_sync_document.md)<br>`revit_sync_document` | Synchronize a workshared document with central; the first call changes nothing and returns the confirm_token needed to proceed |

### Batch jobs (7) {#group-batch}

| Tool | Purpose |
| --- | --- |
| [List jobs](revit_jobs.md)<br>`revit_jobs` | List recent jobs, or wait up to wait_seconds for one action result |
| [Cancel action job](revit_cancel_job.md)<br>`revit_cancel_job` | Request cancellation of an action job; completed changes stay committed |
| [Run actions](revit_run_actions.md)<br>`revit_run_actions` | Run up to 50 actions as one undo step; the batch rolls back on first failure |
| [Start batch collection](revit_batch_start.md)<br>`revit_batch_start` | Start a persistent, read-only run over local, UNC or RSN models |
| [Batch collection status](revit_batch_status.md)<br>`revit_batch_status` | Read durable run and model status after the initiating client exits |
| [Cancel batch collection](revit_batch_cancel.md)<br>`revit_batch_cancel` | Persist cancellation and prevent unstarted models from running |
| [Fetch Batch Snapshots](revit_batch_fetch.md)<br>`revit_batch_fetch` | Download completed snapshots to new local files without overwriting them |

### Families (4) {#group-families}

| Tool | Purpose |
| --- | --- |
| [Audit families](revit_family_audit.md)<br>`revit_family_audit` | Audit an open family or named project families without saving or loading changes; detail=full returns all parameter metadata |
| [Load Families](revit_load_family.md)<br>`revit_load_family` | Load .rfa family files on the workstation in a single undo entry |
| [Place families](revit_place_families.md)<br>`revit_place_families` | Load optional families and place instances in one transaction and undo entry |
| [Edit Families](revit_edit_families.md)<br>`revit_edit_families` | Edit an open family in place or named project families, rolled back on a dry run |

### Sheets and schedules (4) {#group-sheets}

| Tool | Purpose |
| --- | --- |
| [Read schedule data](revit_schedule_data.md)<br>`revit_schedule_data` | Read displayed schedule header and body cell text, with paging |
| [Create Sheet](revit_create_sheet.md)<br>`revit_create_sheet` | Create a sheet with the first loaded or a named title block |
| [Place views on sheet](revit_place_views_on_sheet.md)<br>`revit_place_views_on_sheet` | Place views and schedules on a sheet; coordinates are sheet mm |
| [Create schedule](revit_create_schedule.md)<br>`revit_create_schedule` | Create a schedule for one category with named fields in order, with filtering and sorting/grouping; dry_run rolls back |

### Links and coordination (4) {#group-links}

| Tool | Purpose |
| --- | --- |
| [Compare link datums](revit_compare_link_datums.md)<br>`revit_compare_link_datums` | Compare host grids and levels with one loaded Revit link; changes nothing |
| [Remove links](revit_remove_links.md)<br>`revit_remove_links` | Delete selected link types and their instances; dry_run previews, and Revit cannot undo it |
| [Align Link Datums](revit_align_link_datums.md)<br>`revit_align_link_datums` | Align host grids and levels to a loaded link, with a dry-run rollback preview |
| [Link CAD drawing](revit_link_cad.md)<br>`revit_link_cad` | Link or import a DWG into a plan view on the Revit workstation and return CAD layers and extents in mm |

## Browse by model object {#objects}

The view-related tools are split again by the model object they act on: views, sheets, schedules and viewport display. The release has no sheet or schedule tools, so those rows point at the same-named tools on the integration branch.

### Views {#objects-views}

| Tool | Purpose |
| --- | --- |
| [View catalog](revit_list_views.md)<br>`revit_list_views` | List views filtered by type and name |
| [View Info](revit_view_info.md)<br>`revit_view_info` | Inspect one view's template, display, categories, worksets, filters and links |
| [View summary](revit_view_summary.md)<br>`revit_view_summary` | Read view metadata, category counts and number of distinct types |
| [Export view image](revit_export_view.md)<br>`revit_export_view` | Export a view as a PNG, from 1 to 4000 pixels |
| [View element rows](revit_view_elements.md)<br>`revit_view_elements` | Page through elements in a selected view, optionally filtered by category |
| [View warnings](revit_view_warnings.md)<br>`revit_view_warnings` | Read warnings involving elements present in a selected view |
| [Activate view](revit_activate_view.md)<br>`revit_activate_view` | Activate a non-template view, then zoom to fit or frame element ids |
| [Close views](revit_close_views.md)<br>`revit_close_views` | Close open UI views in the active document |
| [Set View Visibility](revit_set_view_visibility.md)<br>`revit_set_view_visibility` | Change category, workset and filter visibility in one view, with a dry-run preview |
| [Create view](revit_create_view.md)<br>`revit_create_view` | Create a plan, section, 3D or drafting view; box coordinates are model mm |
| [Duplicate view](revit_duplicate_view.md)<br>`revit_duplicate_view` | Duplicate a view, optionally with detailing or as a dependent view |
| [Apply view template](revit_apply_view_template.md)<br>`revit_apply_view_template` | Apply a matching view template to one or more views |
| <span class="state part">Fork</span> [Set view lighting](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme |

### Sheets {#objects-sheets}

| Tool | Purpose |
| --- | --- |
| [Create Sheet](revit_create_sheet.md)<br>`revit_create_sheet` | Create a sheet with the first loaded or a named title block |
| [Place views on sheet](revit_place_views_on_sheet.md)<br>`revit_place_views_on_sheet` | Place views and schedules on a sheet; coordinates are sheet mm |

### Schedules {#objects-schedules}

| Tool | Purpose |
| --- | --- |
| [Read schedule data](revit_schedule_data.md)<br>`revit_schedule_data` | Read displayed schedule header and body cell text, with paging |
| [Create schedule](revit_create_schedule.md)<br>`revit_create_schedule` | Create a schedule for one category with named fields in order, with filtering and sorting/grouping; dry_run rolls back |

### Viewports and display {#objects-view-display}

| Tool | Purpose |
| --- | --- |
| [Capture elements](revit_capture_elements.md)<br>`revit_capture_elements` | Render a PNG marking 1 to 500 elements; the temporary view is rolled back |
| [Select elements](revit_select.md)<br>`revit_select` | Select elements in Revit; an empty list clears the selection |
| [Show elements](revit_show.md)<br>`revit_show` | Locate and highlight elements, opening a suitable view when needed |
| [Temporary isolation](revit_isolate.md)<br>`revit_isolate` | Temporarily isolate selected elements or reset the active view |
| [Highlight elements](revit_override_graphics.md)<br>`revit_override_graphics` | Colour elements in selected views; reset restores this session's overrides |
| [Tag elements](revit_tag_elements.md)<br>`revit_tag_elements` | Tag elements by category or element ids in a view; room tags need a plan view |

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.
