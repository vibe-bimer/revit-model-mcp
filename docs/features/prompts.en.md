---
description: "Copyable prompt library with a sample prompt and purpose summary for every tool."
---

# Prompt library

35 read + 52 action tools, 87 in total

Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

## Connection and documents {#group-connection}

### [Check connection](revit_ping.md)

`revit_ping` — Check whether the Revit add-in is reachable

```text
Is the Revit add-in reachable?
```

### [Document overview](revit_document_info.md)

`revit_document_info` — Read document metadata, levels, area schemes, worksets and view count

```text
Which model is open, and which levels does it have?
```

### [Revit instance list](revit_list_instances.md)

`revit_list_instances` — List running Revit instances and their active documents

```text
Which Revit instances are running, and what does each hold?
```

## Query and totals {#group-query}

### [Revit UI state](revit_ui_state.md)

`revit_ui_state` — Read the active document, open views, selection and open documents

```text
What is selected right now, and which views are open?
```

### [Name catalog](revit_list_catalog.md)

`revit_list_catalog` — Discover categories, family types, levels, area schemes, views, worksets, phases and parameters

```text
List the parameter names this model offers
```

### [Grouped totals](revit_aggregate_elements.md)

`revit_aggregate_elements` — Group by one or two fields, with counts and optional sum and average

```text
How many of each wall type sit on 1F?
```

```text
Count the doors per level and their total width
```

### [Element query](revit_query_elements.md)

`revit_query_elements` — Filter and page through individual element rows

```text
List the doors on 2F whose fire rating is empty, with ids
```

### [Element details](revit_element_details.md)

`revit_element_details` — Read instance/type parameters and geometry for one element ID

```text
Show every parameter and the geometry of element 357640
```

### [Element relations](revit_list_relations.md)

`revit_list_relations` — Read level rooms, area-scheme membership, group members, nested families and view-template dependents

```text
Which rooms sit on level 1F?
```

## Views and snapshots {#group-views}

### [View catalog](revit_list_views.md)

`revit_list_views` — List views filtered by type and name

```text
List every floor plan view
```

### [View Info](revit_view_info.md)

`revit_view_info` — Inspect one view's template, display, categories, worksets, filters and links

```text
Tell me the category visibility, worksets and filters of the 'Level 1' floor plan view.
```

### [View summary](revit_view_summary.md)

`revit_view_summary` — Read view metadata, category counts and number of distinct types

```text
What does the 3D view hold, category by category?
```

### [Export view image](revit_export_view.md)

`revit_export_view` — Export a view as a PNG, from 1 to 4000 pixels

```text
Export the 1F plan as a PNG, 2000 pixels wide
```

### [View element rows](revit_view_elements.md)

`revit_view_elements` — Page through elements in a selected view, optionally filtered by category

```text
Page through the elements of the 3D view, 200 at a time
```

### [View warnings](revit_view_warnings.md)

`revit_view_warnings` — Read warnings involving elements present in a selected view

```text
Which warnings touch this view?
```

### [Activate view](revit_activate_view.md)

`revit_activate_view` — Activate a non-template view, then zoom to fit or frame element ids

```text
Open the Level 1 plan and zoom to fit
```

### [Close views](revit_close_views.md)

`revit_close_views` — Close open UI views in the active document

```text
Close every open view except the "L1 Plan"
```

### [Set View Visibility](revit_set_view_visibility.md)

`revit_set_view_visibility` — Change category, workset and filter visibility in one view, with a dry-run preview

```text
Hide the OST_StructuralColumns category in the 'A-101' plan view, previewing with a dry run first.
```

### [Create view](revit_create_view.md)

`revit_create_view` — Create a plan, section, 3D or drafting view; box coordinates are model mm

```text
Create a floor plan named Level 3 Plan at scale 1:100
```

### [Duplicate view](revit_duplicate_view.md)

`revit_duplicate_view` — Duplicate a view, optionally with detailing or as a dependent view

```text
Duplicate the Level 1 plan with detailing
```

### [Apply view template](revit_apply_view_template.md)

`revit_apply_view_template` — Apply a matching view template to one or more views

```text
Apply the "MEP Documentation" view template to all HVAC plan views
```

### <span class="state part">Fork</span> [Set view lighting](revit_set_view_lighting.md)

`revit_set_view_lighting` — Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme

```text
Turn on shadows in the 3D view, set the shadow intensity to 60, use a sky background and light the rendering with exterior sun
```

```text
Set the sun in {3D} to 2026-06-21 15:00 with a sunlight intensity of 80, and rehearse it first
```

```text
Fix the sun in lighting mode at azimuth 135° and altitude 45°, and turn on the ground plane at level 01
```

## Export and checks {#group-export}

### [Check NWC Settings](revit_nwc_settings_check.md)

`revit_nwc_settings_check` — Parse a Navisworks exporter XML on the workstation without exporting

```text
Check what the Navisworks exporter settings XML on the Revit workstation contains, without exporting.
```

### [Model snapshot](revit_model_snapshot.md)

`revit_model_snapshot` — Read a schema version 1 project snapshot for batch audits; closed worksets can leave it incomplete

```text
Export a model snapshot of the current project for a batch audit
```

### [Model health](revit_model_health.md)

`revit_model_health` — Check file size, model counts, units and frequent warnings

```text
Run a pre-handover health check: size, counts, units, top warnings
```

### [Link status](revit_links_status.md)

`revit_links_status` — Inspect RVT, CAD and image link status, paths and instance counts

```text
Check every link: RVT, CAD and images
```

### [Shared coordinates](revit_shared_coordinates.md)

`revit_shared_coordinates` — Read base/survey points, sites and link offsets in mm and degrees

```text
Report the shared coordinates and link offsets
```

### [Parameter fill check](revit_parameter_fill_check.md)

`revit_parameter_fill_check` — Count filled, empty and missing parameter values and sample element IDs

```text
How well is the fire rating filled in on walls? Give me the empty ids
```

### [Model warnings](revit_list_warnings.md)

`revit_list_warnings` — Group model warnings by description and inspect affected elements

```text
Group the model warnings by text
```

### [Export Model Files](revit_export.md)

`revit_export` — Export PDF, DWG, IFC or schedule CSV files; a dry run returns planned names

```text
Export the 'A-101' view to PDF in 'C:\Out', showing the planned file names with a dry run first.
```

### [Export Navisworks NWC](revit_export_nwc.md)

`revit_export_nwc` — Export NWC on the Revit workstation; needs the Navisworks exporter, and overwriting needs a confirm token

```text
Export the current view to D:\output\tower.nwc and overwrite it if it already exists
```

### <span class="state part">Fork</span> [Export element ID register](revit_export_element_ids.md)

`revit_export_element_ids` — Write the ID register of drawn model components to an Excel workbook

```text
Export the ID register of drawn model components to Excel, ordered by category, family and type
```

### [Build snapshot report](revit_build_report.md)

`revit_build_report` — Build a local Excel report from snapshots without contacting Revit

```text
Turn the snapshots in the snapshots folder into an Excel report
```

### [Issue register](revit_issue_register.md)

`revit_issue_register` — Write a new .xlsx issue register with element snapshots and review documents

```text
Turn these eight issues into an .xlsx issue register
```

## Selection and display {#group-display}

### [Capture elements](revit_capture_elements.md)

`revit_capture_elements` — Render a PNG marking 1 to 500 elements; the temporary view is rolled back

```text
Highlight these beams in the Level 1 plan as a PNG for an issue record
```

### [Select elements](revit_select.md)

`revit_select` — Select elements in Revit; an empty list clears the selection

```text
Select element 123456
```

### [Show elements](revit_show.md)

`revit_show` — Locate and highlight elements, opening a suitable view when needed

```text
Show me those columns in the view
```

### [Temporary isolation](revit_isolate.md)

`revit_isolate` — Temporarily isolate selected elements or reset the active view

```text
Isolate the windows of this level
```

### [Highlight elements](revit_override_graphics.md)

`revit_override_graphics` — Colour elements in selected views; reset restores this session's overrides

```text
Colour these columns red in the Level 1 plan and halftone the rest
```

### [Tag elements](revit_tag_elements.md)

`revit_tag_elements` — Tag elements by category or element ids in a view; room tags need a plan view

```text
Tag every door on the Level 1 plan
```

## Editing {#group-edit}

### [Execute C# code](revit_execute_code.md)

`revit_execute_code` — Compile and run C# on the Revit thread; auto mode owns one transaction and undo entry

```text
Run C# that sets the Comments parameter on every wall to Review
```

### [Undo last action](revit_undo_last.md)

`revit_undo_last` — Undo the last MCP action via Revit's own undo command, only when the target document is active and the session's undo entry matches

```text
Undo the last action you just made in the active document
```

### [Move elements](revit_move.md)

`revit_move` — Move elements by offsets along model axes in millimetres

```text
Move these three elements 500 mm along X, dry run first
```

### [Rotate elements](revit_rotate.md)

`revit_rotate` — Rotate elements about a vertical axis through center_mm or their bounding-box center; dry_run rolls back, group, pinned and hosted elements are skipped

```text
Rotate the three selected columns 30 degrees around the origin; preview with dry_run first
```

### [Copy Elements](revit_copy.md)

`revit_copy` — Copy elements 1 to 100 times at a millimetre offset, rolled back on a dry run

```text
Copy the selected walls 5 times with a 3000 mm offset along X.
```

### [Mirror elements](revit_mirror.md)

`revit_mirror` — Mirror elements across a model X or Y parallel line through point_mm; dry_run rolls back

```text
Mirror the three selected walls across the Y-parallel line through (0, 0) and keep the originals
```

### [Change element type](revit_change_type.md)

`revit_change_type` — Change each element to one compatible type; group members are skipped

```text
Change these walls to the 200 mm concrete wall type
```

### [Update parameters](revit_update_parameters.md)

`revit_update_parameters` — Update a parameter on elements matching the same filters as revit_query_elements; group members are skipped and dry_run predicts the outcome

```text
Set the Comments parameter to "to be checked" on all level 1 walls; predict the impact with dry_run first
```

### [Place unhosted family](revit_place_family.md)

`revit_place_family` — Place a loaded unhosted family on a named level with optional Z rotation

```text
Place an instance of a loaded unhosted furniture family at 3000,4000 on 1F, dry run first
```

### [Create straight wall](revit_create_wall.md)

`revit_create_wall` — Create a wall from two XY points, a level, type and height

```text
Draw a 200 mm wall on 1F from 0,0 to 6000,0
```

### [Create MEP run](revit_create_mep_run.md)

`revit_create_mep_run` — Create connected duct, pipe, tray or conduit runs from points in mm

```text
Draw a DN100 pipe through these points on Level 3
```

### [Build Walls from CAD](revit_walls_from_cad.md)

`revit_walls_from_cad` — Pair CAD lines into joined basic walls, bridging openings, with millimetre dimensions

```text
Build basic walls from the 'Level 1' underlay CAD lines, 3000 mm high, and join the ends.
```

### [Edit parameter](revit_set_parameter.md)

`revit_set_parameter` — Set a named parameter; lengths use mm, areas m² and other doubles internal units

```text
Set the fire rating of these walls to two hours
```

### [Delete elements](revit_delete.md)

`revit_delete` — Delete selected elements and their Revit dependencies

```text
Delete these two elements, dry run first
```

### [Process many models](revit_process_models.md)

`revit_process_models` — Open each model in the interactive session, run steps and C# code, and export or save as requested; in-place saves and code need a confirm_token

```text
Batch-open the models under D:/models, export PNGs and save as new files instead of saving in place
```

### <span class="state part">Fork</span> [Create level](revit_create_level.md)

`revit_create_level` — Create a level at a given elevation in millimetres

```text
Create a level named 4F at 15000 mm
```

### <span class="state part">Fork</span> [Create floor](revit_create_floor.md)

`revit_create_floor` — Create a floor from a closed XY boundary with at least three vertices

```text
Create a floor on 2F from these four points
```

## Phases {#group-phases}

### <span class="state part">Fork</span> [Set element phases](revit_set_phase.md)

`revit_set_phase` — Assign created/demolished phases; an empty string clears and null leaves unchanged

```text
Mark these elements as demolished in the Existing phase
```

### <span class="state part">Fork</span> [Merge project phases](revit_merge_phases.md)

`revit_merge_phases` — Reassign references to another phase and attempt to delete the emptied phase

```text
Merge phase 1 into New Construction
```

## Batch and ids {#group-ids}

### <span class="state part">Fork</span> [Replace IDs in place](revit_reset_element_ids.md)

`revit_reset_element_ids` — Replace eligible standalone elements with copies to obtain new IDs

```text
Give these 27 standalone components new ids
```

### <span class="state part">Fork</span> [Rebuild IDs in new models](revit_rebuild_model_ids.md)

`revit_rebuild_model_ids` — Copy selectable 3D-view components into one or more new models with fresh IDs

```text
Rebuild the selectable components into E:\out\copy-{n}.rvt, ten copies, no id shared between them
```

```text
Rehearse the rebuild first: how many components, which new id range, write nothing yet
```

## Documents and processes {#group-documents}

### [List open documents](revit_documents.md)

`revit_documents` — List every open document in one Revit process, including background documents

```text
Which documents are open right now, including linked ones?
```

### [Open Document](revit_open_document.md)

`revit_open_document` — Open a local, UNC or RSN model on the workstation; central models open detached

```text
Open the central model 'Tower.rvt' for me in detached mode.
```

### [Activate document](revit_activate_document.md)

`revit_activate_document` — Activate an already open document by title or path reference

```text
Make the background document Tower B.rvt active
```

### [New Document](revit_new_document.md)

`revit_new_document` — Create a project or family from a template on the Revit workstation

```text
Create a new project from the 'Metric Generic Model.rte' template named 'Tower Scheme'.
```

### [Close document](revit_close_document.md)

`revit_close_document` — Close a background document; the first call changes nothing and returns the confirm token

```text
Close the background document Old Sample Tower.rvt without saving
```

### [Save document](revit_save_document.md)

`revit_save_document` — Save a document; the first call only returns a confirm_token and changes nothing

```text
Save the current model over the existing file
```

### [Synchronize document](revit_sync_document.md)

`revit_sync_document` — Synchronize a workshared document with central; the first call changes nothing and returns the confirm_token needed to proceed

```text
Synchronize the current workshared document with central, comment "update door and window tags"
```

## Batch jobs {#group-batch}

### [List jobs](revit_jobs.md)

`revit_jobs` — List recent jobs, or wait up to wait_seconds for one action result

```text
Which jobs ran recently? Also wait for the jobId 3 result
```

### [Cancel action job](revit_cancel_job.md)

`revit_cancel_job` — Request cancellation of an action job; completed changes stay committed

```text
Cancel the batch job job-1234 that is still running
```

### [Run actions](revit_run_actions.md)

`revit_run_actions` — Run up to 50 actions as one undo step; the batch rolls back on first failure

```text
Export these 20 views to PDF in one go
```

### [Start batch collection](revit_batch_start.md)

`revit_batch_start` — Start a persistent, read-only run over local, UNC or RSN models

```text
Scan all RVT models under \\fileserver\models and start a batch collection
```

### [Batch collection status](revit_batch_status.md)

`revit_batch_status` — Read durable run and model status after the initiating client exits

```text
Did that batch finish? The client already closed
```

### [Cancel batch collection](revit_batch_cancel.md)

`revit_batch_cancel` — Persist cancellation and prevent unstarted models from running

```text
Cancel the batch run with run_id a1b2c3 so the unstarted models do not run
```

### [Fetch Batch Snapshots](revit_batch_fetch.md)

`revit_batch_fetch` — Download completed snapshots to new local files without overwriting them

```text
Download the snapshots for batch run 'run-2026-10-31' into 'C:\Snapshots' without overwriting existing files.
```

## Families {#group-families}

### [Audit families](revit_family_audit.md)

`revit_family_audit` — Audit an open family or named project families without saving or loading changes; detail=full returns all parameter metadata

```text
Audit all families in the project with the wildcard and show which parameters are unused
```

### [Load Families](revit_load_family.md)

`revit_load_family` — Load .rfa family files on the workstation in a single undo entry

```text
Load 'C:\Families\M_Column.rfa' and 'M_Beam.rfa' into the current model.
```

### [Place families](revit_place_families.md)

`revit_place_families` — Load optional families and place instances in one transaction and undo entry

```text
Load the Double Door family, then place two instances in the meeting room
```

### [Edit Families](revit_edit_families.md)

`revit_edit_families` — Edit an open family in place or named project families, rolled back on a dry run

```text
Edit the visibility parameter of the project family 'M_Column', previewing with a dry run first.
```

## Sheets and schedules {#group-sheets}

### [Read schedule data](revit_schedule_data.md)

`revit_schedule_data` — Read displayed schedule header and body cell text, with paging

```text
Read the first 100 rows of the Door Schedule
```

### [Create Sheet](revit_create_sheet.md)

`revit_create_sheet` — Create a sheet with the first loaded or a named title block

```text
Create a sheet numbered 'A-102' named 'Level 2 Floor Plan' using the 'A1' title block.
```

### [Place views on sheet](revit_place_views_on_sheet.md)

`revit_place_views_on_sheet` — Place views and schedules on a sheet; coordinates are sheet mm

```text
Place the Level 1 Plan view on sheet A101 at (300, 200)
```

### [Create schedule](revit_create_schedule.md)

`revit_create_schedule` — Create a schedule for one category with named fields in order, with filtering and sorting/grouping; dry_run rolls back

```text
Create a schedule for the Doors category with fields Mark, Level, Count in that order, named "Door and Window Takeoff"
```

## Links and coordination {#group-links}

### [Compare link datums](revit_compare_link_datums.md)

`revit_compare_link_datums` — Compare host grids and levels with one loaded Revit link; changes nothing

```text
Compare the grids and levels of the linked model "Structure Ref.rvt" against the current project
```

### [Remove links](revit_remove_links.md)

`revit_remove_links` — Delete selected link types and their instances; dry_run previews, and Revit cannot undo it

```text
Preview with dry_run first, then remove all Revit links from this document
```

### [Align Link Datums](revit_align_link_datums.md)

`revit_align_link_datums` — Align host grids and levels to a loaded link, with a dry-run rollback preview

```text
Align the host grids and levels to the loaded link 'StructureLink.rvt' with a 5 mm tolerance.
```

### [Link CAD drawing](revit_link_cad.md)

`revit_link_cad` — Link or import a DWG into a plan view on the Revit workstation and return CAD layers and extents in mm

```text
Link D:/drawings/L1-plan.dwg into the "L1 Plan" view
```
