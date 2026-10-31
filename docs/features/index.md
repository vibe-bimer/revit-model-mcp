# Feature overview

The server serves 87 tools: 35 read and 52 action. A read returns model data and changes nothing; an action changes the model or a file.

## Browse by Revit year

| Revit year | Tools | Details |
| --- | --- | --- |
| 2020 | 0 of 87 | [Revit 2020](v2020.md) |
| 2022–2025, 2027 | 87 built | [Version support matrix](matrix.md) |
| 2026 | 87 built, not live-verified | [Revit 2026](v2026.md) |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

## Read tools (35)

### Element registers

| Tool | Summary |
| --- | --- |
| [Export element ID register](revit_export_element_ids.md) | Write the ID register of drawn model components to an Excel workbook. |

### Connection and core

| Tool | Summary |
| --- | --- |
| [List Revit Jobs](revit_jobs.md) | List recent jobs, or wait up to wait_seconds (0 to 50, default 40) for the result of an action jobId. |
| [Check Revit Connection](revit_ping.md) | Check the connection to Revit without reading the model. |
| [Document Info](revit_document_info.md) | Read the active model's file name, Revit version, levels (elevations in mm), area schemes, worksets and view count. |
| [Open Documents](revit_documents.md) | List every open document in one Revit process, including background documents. |
| [Revit UI State](revit_ui_state.md) | Read the active document, open views, selection and open documents. |
| [List Instances](revit_list_instances.md) | List Revit processes with documentName, documentPath, revitVersion, processId and pluginResponding. |

### Model queries

| Tool | Summary |
| --- | --- |
| [Model Snapshot](revit_model_snapshot.md) | Read a schema version 1 project snapshot for batch audits. |
| [Model Health Check](revit_model_health.md) | Read model quality counts: project metadata, file size, counts, units and the ten most frequent warning groups. |
| [Links Status](revit_links_status.md) | Read RVT, CAD and image link status. |
| [Shared Coordinates](revit_shared_coordinates.md) | Read project and survey coordinates: base and survey points, active site, project locations and link offsets (mm, degrees). |
| [Parameter Fill Check](revit_parameter_fill_check.md) | Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs. |
| [List Catalog](revit_list_catalog.md) | List catalog names for one section: categories, family-types, levels, area-schemes, views, worksets, phases or parameters. |
| [Aggregate Elements](revit_aggregate_elements.md) | Summarize matching elements by one or two fields, with optional sum and average. |
| [Query Elements](revit_query_elements.md) | Read a page of matching element rows. |
| [Read Schedule Data](revit_schedule_data.md) | Read displayed schedule header and body cell text, with paging. |
| [Element Details](revit_element_details.md) | Read parameters and geometry of an element by Revit ID, with its type parameters and related warnings. |
| [List Warnings](revit_list_warnings.md) | Group model warnings by description text. |
| [List Relations](revit_list_relations.md) | Read model object membership or dependencies. |

### Views and sheets

| Tool | Summary |
| --- | --- |
| [List Views](revit_list_views.md) | List non-template views with id, name, type, level, scale and template. |
| [View Info](revit_view_info.md) | Inspect one view's template, display, categories, worksets, filters and links. |
| [View Summary](revit_view_summary.md) | Read element categories and counts for a selected view. |
| [Capture Elements](revit_capture_elements.md) | Render a highlighted PNG that marks 1 to 500 elements, for issue evidence. |
| [Export View to PNG](revit_export_view.md) | Export a selected view to a PNG file on the MCP client. |
| [View Elements](revit_view_elements.md) | Read one page of elements in a selected view, with IDs, category, family, type, level and measurements (mm, m2, m3). |
| [View Warnings](revit_view_warnings.md) | Read warnings involving elements present in a selected view. |

### Families

| Tool | Summary |
| --- | --- |
| [Audit Families](revit_family_audit.md) | Audit an open family or named project families without saving or loading changes. |

### Links

| Tool | Summary |
| --- | --- |
| [Compare Link Datums](revit_compare_link_datums.md) | Compare host grids and levels with one loaded Revit link. |

### Export

| Tool | Summary |
| --- | --- |
| [Check NWC Settings](revit_nwc_settings_check.md) | Parse a Navisworks exporter XML file on the Revit workstation without exporting. |
| [Issue Register](revit_issue_register.md) | Write a new local .xlsx issue register with element snapshots and review documents. |

### Batch processing

| Tool | Summary |
| --- | --- |
| [Start batch collection](revit_batch_start.md) | Start a persistent, read-only run over local, UNC or RSN models. |
| [Batch collection status](revit_batch_status.md) | Read durable run and model status after the initiating client exits. |
| [Cancel batch collection](revit_batch_cancel.md) | Persist cancellation and prevent unstarted models from running. |
| [Fetch batch snapshots](revit_batch_fetch.md) | Download completed snapshots to new local files without overwriting. |
| [Build Snapshot Report](revit_build_report.md) | Build a local Excel report from snapshots without contacting Revit. |

## Action tools (52)

### Model editing

| Tool | Summary |
| --- | --- |
| [Create level](revit_create_level.md) | Create a level at a given elevation in millimetres. |
| [Create floor](revit_create_floor.md) | Create a floor from a closed XY boundary with at least three vertices. |

### Phases

| Tool | Summary |
| --- | --- |
| [Set element phases](revit_set_phase.md) | Assign created and demolished phases; an empty string clears one and null leaves it unchanged. |
| [Merge project phases](revit_merge_phases.md) | Reassign references to another phase and attempt to delete the emptied phase. |

### Id management

| Tool | Summary |
| --- | --- |
| [Replace IDs in place](revit_reset_element_ids.md) | Replace eligible standalone elements with copies to obtain new IDs. |
| [Rebuild IDs in new models](revit_rebuild_model_ids.md) | Copy selectable 3D-view components into one or more new models with fresh IDs. |

### View settings

| Tool | Summary |
| --- | --- |
| [Set view lighting](revit_set_view_lighting.md) | Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme. |

### Connection and core

| Tool | Summary |
| --- | --- |
| [Undo Last Action](revit_undo_last.md) | Undo the last MCP action through Revit's own undo command. |
| [Cancel Action Job](revit_cancel_job.md) | Request cancellation of an action jobId. |

### Model actions

| Tool | Summary |
| --- | --- |
| [Move Elements](revit_move.md) | Move elements by dx_mm, dy_mm and dz_mm on model axes. |
| [Rotate Elements](revit_rotate.md) | Rotate elements about a vertical axis through center_mm, or through their combined bounding box center. |
| [Copy Elements](revit_copy.md) | Create 1 to 100 successive copies at multiples of the model-axis offset in mm. |
| [Mirror Elements](revit_mirror.md) | Mirror across a model X or Y parallel line through point_mm; copy keeps originals. |
| [Change Element Type](revit_change_type.md) | Change each element to one compatible type; family resolves duplicate type names. |
| [Update Parameters](revit_update_parameters.md) | Update a parameter on elements matching the same filters as revit_query_elements. |
| [Set Parameter](revit_set_parameter.md) | Set one instance or type parameter. |
| [Delete Elements](revit_delete.md) | Delete elements and their Revit dependencies; the count includes dependents. |
| [Run Actions](revit_run_actions.md) | Execute up to 50 actions with one undo step; the whole batch rolls back on its first failure. |

### Documents

| Tool | Summary |
| --- | --- |
| [Open Document](revit_open_document.md) | Open a local, UNC or RSN model. |
| [Activate Document](revit_activate_document.md) | Activate an already open document by title or path reference. |
| [New Document](revit_new_document.md) | Create a project or family from a template on the Revit workstation. |
| [Close Document](revit_close_document.md) | Close a background document. |
| [Save Document](revit_save_document.md) | Save a document. |
| [Synchronize Document](revit_sync_document.md) | Synchronize a workshared document with central. |

### Views and sheets

| Tool | Summary |
| --- | --- |
| [Activate View](revit_activate_view.md) | Activate a non-template view. |
| [Close Views](revit_close_views.md) | Close open UI views in the active document. |
| [Set View Visibility](revit_set_view_visibility.md) | Change category, workset and filter visibility in one view; dry_run previews. |
| [Select Elements](revit_select.md) | Select element IDs for inspection in Revit; an empty list clears the selection. |
| [Show Elements](revit_show.md) | Display elements in Revit, optionally selecting them; opens a level plan or 3D view when needed. |
| [Isolate Elements](revit_isolate.md) | Temporarily isolate element IDs in the active view; an empty list resets. |
| [Highlight Elements](revit_override_graphics.md) | Colour elements in selected model views; reset restores overrides saved in this Revit session. |
| [Create View](revit_create_view.md) | Create a plan, section, 3D or drafting view. |
| [Duplicate View](revit_duplicate_view.md) | Duplicate a view, optionally with detailing or as a dependent view. |
| [Apply View Template](revit_apply_view_template.md) | Apply a matching view template to one or more views. |
| [Create Sheet](revit_create_sheet.md) | Create a sheet with the first loaded or a named title block. |
| [Place Views on Sheet](revit_place_views_on_sheet.md) | Place views and schedules on a sheet. |
| [Tag Elements](revit_tag_elements.md) | Tag elements in a view, chosen by category names or by element IDs (exactly one of the two). |
| [Create Schedule](revit_create_schedule.md) | Create a schedule for one category with the named fields in the given order, using Revit UI names such as Mark, Level or Count. |

### Families

| Tool | Summary |
| --- | --- |
| [Place Family](revit_place_family.md) | Place a loaded unhosted family on a named level. |
| [Load Families](revit_load_family.md) | Load workstation .rfa files in one undo entry. |
| [Place Families](revit_place_families.md) | Load optional families and place instances in one transaction and undo entry. |
| [Edit Families](revit_edit_families.md) | Edit an open family in place, or named project families (exact names or ["*"]), one load cycle each. |

### Links

| Tool | Summary |
| --- | --- |
| [Remove Links](revit_remove_links.md) | Delete selected link types and their instances; dry_run previews. |
| [Align Link Datums](revit_align_link_datums.md) | Align host grids and levels to a loaded link, with optional creation and rollback preview. |

### CAD and MEP

| Tool | Summary |
| --- | --- |
| [Create Wall](revit_create_wall.md) | Create a straight wall on a named level. |
| [Create MEP Run](revit_create_mep_run.md) | Create connected duct, pipe, cable tray or conduit segments from model mm points. |
| [Link CAD Drawing](revit_link_cad.md) | Link or import a DWG into a plan view on the Revit workstation. |
| [Build Walls from CAD](revit_walls_from_cad.md) | Bridge openings, pair parallel CAD lines and join basic walls in one undo entry. |

### Export

| Tool | Summary |
| --- | --- |
| [Export Model Files](revit_export.md) | Export PDF, DWG, IFC or schedule CSV files on the Revit workstation; dry_run returns planned file names. |
| [Export Navisworks NWC](revit_export_nwc.md) | Export NWC on the Revit workstation; needs the Navisworks exporter. |

### Batch processing

| Tool | Summary |
| --- | --- |
| [Process Many Models](revit_process_models.md) | Open each model in the interactive session, run steps and C# code, export, save as requested, and close. |

### Code execution

| Tool | Summary |
| --- | --- |
| [Execute C# Code](revit_execute_code.md) | Compile and run C# against the live Revit API on the Revit thread. |

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
