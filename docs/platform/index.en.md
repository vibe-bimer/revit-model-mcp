---
description: "Complete tool list of the integration branch (the upstream 1.0 base plus this repository's fork tools), grouped with purpose, parameters and contract differences."
---

# Platform tool catalog

This section records the tool surface of the integration branch, kept apart from the released catalog under Features. The branch is unreleased and 7 fork tools are still missing from it, so the catalog is a migration scoreboard, not a delivery list.

80 tools: 79 base and 1 fork; 34 read and 46 action.

## Two catalogs {#catalogs}

The current release is 0.9.0. The integration branch is the new line built on the upstream 1.0 base. Their tool counts and names differ, so they are not interchangeable.

| | Current release | Integration branch |
| --- | --- | --- |
| Tools | 35 | 80 |
| Read | 19 | 34 |
| Action | 16 | 46 |
| Released | Released | Unreleased |
| Branch | main | `integration/upstream-1.0` |

## Base and fork tools {#origin}

Every page carries an origin marker: base means the tool came with the upstream base, fork means this repository designed it. Only 1 fork tool is grafted so far.

| Group | Base (upstream) | Fork (this repository) |
| --- | --- | --- |
| Connection and instances | 8 | 0 |
| Query and totals | 12 | 0 |
| Editing primitives | 9 | 0 |
| Document lifecycle | 6 | 0 |
| Views, sheets and schedules | 21 | 1 |
| Families | 5 | 0 |
| Links and datums | 3 | 0 |
| CAD and MEP | 4 | 0 |
| Export and registers | 4 | 0 |
| Batch and reports | 6 | 0 |
| C# escape hatch | 1 | 0 |
| **Total** | **79** | **1** |

[Fork tool migration status](fork-tools.md) · [Integration specification and decision records](https://github.com/vibe-bimer/revit-model-mcp/issues/27)

## Tools per group {#groups}

| Group | Tools | Read | Action |
| --- | ---: | ---: | ---: |
| [Connection and instances](#group-core) | 8 | 6 | 2 |
| [Query and totals](#group-read) | 12 | 12 | 0 |
| [Editing primitives](#group-actions) | 9 | 0 | 9 |
| [Document lifecycle](#group-documents) | 6 | 0 | 6 |
| [Views, sheets and schedules](#group-views-sheets) | 22 | 7 | 15 |
| [Families](#group-family) | 5 | 1 | 4 |
| [Links and datums](#group-links) | 3 | 1 | 2 |
| [CAD and MEP](#group-cad-mep) | 4 | 0 | 4 |
| [Export and registers](#group-export) | 4 | 2 | 2 |
| [Batch and reports](#group-batch) | 6 | 5 | 1 |
| [C# escape hatch](#group-code) | 1 | 0 | 1 |

## Connection and instances {#group-core}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Cancel Action Job](revit_cancel_job.md)<br>`revit_cancel_job` | Action | <span class="state part">Base (upstream)</span> |
| [Document Info](revit_document_info.md)<br>`revit_document_info` | Read | <span class="state part">Base (upstream)</span> |
| [Open Documents](revit_documents.md)<br>`revit_documents` | Read | <span class="state part">Base (upstream)</span> |
| [List Revit Jobs](revit_jobs.md)<br>`revit_jobs` | Read | <span class="state part">Base (upstream)</span> |
| [List Instances](revit_list_instances.md)<br>`revit_list_instances` | Read | <span class="state part">Base (upstream)</span> |
| [Check Revit Connection](revit_ping.md)<br>`revit_ping` | Read | <span class="state part">Base (upstream)</span> |
| [Revit UI State](revit_ui_state.md)<br>`revit_ui_state` | Read | <span class="state part">Base (upstream)</span> |
| [Undo Last Action](revit_undo_last.md)<br>`revit_undo_last` | Action | <span class="state part">Base (upstream)</span> |

## Query and totals {#group-read}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Aggregate Elements](revit_aggregate_elements.md)<br>`revit_aggregate_elements` | Read | <span class="state part">Base (upstream)</span> |
| [Element Details](revit_element_details.md)<br>`revit_element_details` | Read | <span class="state part">Base (upstream)</span> |
| [Links Status](revit_links_status.md)<br>`revit_links_status` | Read | <span class="state part">Base (upstream)</span> |
| [List Catalog](revit_list_catalog.md)<br>`revit_list_catalog` | Read | <span class="state part">Base (upstream)</span> |
| [List Relations](revit_list_relations.md)<br>`revit_list_relations` | Read | <span class="state part">Base (upstream)</span> |
| [List Warnings](revit_list_warnings.md)<br>`revit_list_warnings` | Read | <span class="state part">Base (upstream)</span> |
| [Model Health Check](revit_model_health.md)<br>`revit_model_health` | Read | <span class="state part">Base (upstream)</span> |
| [Model Snapshot](revit_model_snapshot.md)<br>`revit_model_snapshot` | Read | <span class="state part">Base (upstream)</span> |
| [Parameter Fill Check](revit_parameter_fill_check.md)<br>`revit_parameter_fill_check` | Read | <span class="state part">Base (upstream)</span> |
| [Query Elements](revit_query_elements.md)<br>`revit_query_elements` | Read | <span class="state part">Base (upstream)</span> |
| [Read Schedule Data](revit_schedule_data.md)<br>`revit_schedule_data` | Read | <span class="state part">Base (upstream)</span> |
| [Shared Coordinates](revit_shared_coordinates.md)<br>`revit_shared_coordinates` | Read | <span class="state part">Base (upstream)</span> |

## Editing primitives {#group-actions}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Change Element Type](revit_change_type.md)<br>`revit_change_type` | Action | <span class="state part">Base (upstream)</span> |
| [Copy Elements](revit_copy.md)<br>`revit_copy` | Action | <span class="state part">Base (upstream)</span> |
| [Delete Elements](revit_delete.md)<br>`revit_delete` | Action | <span class="state part">Base (upstream)</span> |
| [Mirror Elements](revit_mirror.md)<br>`revit_mirror` | Action | <span class="state part">Base (upstream)</span> |
| [Move Elements](revit_move.md)<br>`revit_move` | Action | <span class="state part">Base (upstream)</span> |
| [Rotate Elements](revit_rotate.md)<br>`revit_rotate` | Action | <span class="state part">Base (upstream)</span> |
| [Run Actions](revit_run_actions.md)<br>`revit_run_actions` | Action | <span class="state part">Base (upstream)</span> |
| [Set Parameter](revit_set_parameter.md)<br>`revit_set_parameter` | Action | <span class="state part">Base (upstream)</span> |
| [Update Parameters](revit_update_parameters.md)<br>`revit_update_parameters` | Action | <span class="state part">Base (upstream)</span> |

## Document lifecycle {#group-documents}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Activate Document](revit_activate_document.md)<br>`revit_activate_document` | Action | <span class="state part">Base (upstream)</span> |
| [Close Document](revit_close_document.md)<br>`revit_close_document` | Action | <span class="state part">Base (upstream)</span> |
| [New Document](revit_new_document.md)<br>`revit_new_document` | Action | <span class="state part">Base (upstream)</span> |
| [Open Document](revit_open_document.md)<br>`revit_open_document` | Action | <span class="state part">Base (upstream)</span> |
| [Save Document](revit_save_document.md)<br>`revit_save_document` | Action | <span class="state part">Base (upstream)</span> |
| [Synchronize Document](revit_sync_document.md)<br>`revit_sync_document` | Action | <span class="state part">Base (upstream)</span> |

## Views, sheets and schedules {#group-views-sheets}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Activate View](revit_activate_view.md)<br>`revit_activate_view` | Action | <span class="state part">Base (upstream)</span> |
| [Apply View Template](revit_apply_view_template.md)<br>`revit_apply_view_template` | Action | <span class="state part">Base (upstream)</span> |
| [Capture Elements](revit_capture_elements.md)<br>`revit_capture_elements` | Read | <span class="state part">Base (upstream)</span> |
| [Close Views](revit_close_views.md)<br>`revit_close_views` | Action | <span class="state part">Base (upstream)</span> |
| [Create Schedule](revit_create_schedule.md)<br>`revit_create_schedule` | Action | <span class="state part">Base (upstream)</span> |
| [Create Sheet](revit_create_sheet.md)<br>`revit_create_sheet` | Action | <span class="state part">Base (upstream)</span> |
| [Create View](revit_create_view.md)<br>`revit_create_view` | Action | <span class="state part">Base (upstream)</span> |
| [Duplicate View](revit_duplicate_view.md)<br>`revit_duplicate_view` | Action | <span class="state part">Base (upstream)</span> |
| [Export View to PNG](revit_export_view.md)<br>`revit_export_view` | Read | <span class="state part">Base (upstream)</span> |
| [Isolate Elements](revit_isolate.md)<br>`revit_isolate` | Action | <span class="state part">Base (upstream)</span> |
| [List Views](revit_list_views.md)<br>`revit_list_views` | Read | <span class="state part">Base (upstream)</span> |
| [Highlight Elements](revit_override_graphics.md)<br>`revit_override_graphics` | Action | <span class="state part">Base (upstream)</span> |
| [Place Views on Sheet](revit_place_views_on_sheet.md)<br>`revit_place_views_on_sheet` | Action | <span class="state part">Base (upstream)</span> |
| [Select Elements](revit_select.md)<br>`revit_select` | Action | <span class="state part">Base (upstream)</span> |
| [Set View Lighting](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | Action | <span class="state ok">Fork (this repository)</span> <span class="state ok">Grafted</span> |
| [Set View Visibility](revit_set_view_visibility.md)<br>`revit_set_view_visibility` | Action | <span class="state part">Base (upstream)</span> |
| [Show Elements](revit_show.md)<br>`revit_show` | Action | <span class="state part">Base (upstream)</span> |
| [Tag Elements](revit_tag_elements.md)<br>`revit_tag_elements` | Action | <span class="state part">Base (upstream)</span> |
| [View Elements](revit_view_elements.md)<br>`revit_view_elements` | Read | <span class="state part">Base (upstream)</span> |
| [View Info](revit_view_info.md)<br>`revit_view_info` | Read | <span class="state part">Base (upstream)</span> |
| [View Summary](revit_view_summary.md)<br>`revit_view_summary` | Read | <span class="state part">Base (upstream)</span> |
| [View Warnings](revit_view_warnings.md)<br>`revit_view_warnings` | Read | <span class="state part">Base (upstream)</span> |

## Families {#group-family}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Edit Families](revit_edit_families.md)<br>`revit_edit_families` | Action | <span class="state part">Base (upstream)</span> |
| [Audit Families](revit_family_audit.md)<br>`revit_family_audit` | Read | <span class="state part">Base (upstream)</span> |
| [Load Families](revit_load_family.md)<br>`revit_load_family` | Action | <span class="state part">Base (upstream)</span> |
| [Place Families](revit_place_families.md)<br>`revit_place_families` | Action | <span class="state part">Base (upstream)</span> |
| [Place Family](revit_place_family.md)<br>`revit_place_family` | Action | <span class="state part">Base (upstream)</span> |

## Links and datums {#group-links}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Align Link Datums](revit_align_link_datums.md)<br>`revit_align_link_datums` | Action | <span class="state part">Base (upstream)</span> |
| [Compare Link Datums](revit_compare_link_datums.md)<br>`revit_compare_link_datums` | Read | <span class="state part">Base (upstream)</span> |
| [Remove Links](revit_remove_links.md)<br>`revit_remove_links` | Action | <span class="state part">Base (upstream)</span> |

## CAD and MEP {#group-cad-mep}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Create MEP Run](revit_create_mep_run.md)<br>`revit_create_mep_run` | Action | <span class="state part">Base (upstream)</span> |
| [Create Wall](revit_create_wall.md)<br>`revit_create_wall` | Action | <span class="state part">Base (upstream)</span> |
| [Link CAD Drawing](revit_link_cad.md)<br>`revit_link_cad` | Action | <span class="state part">Base (upstream)</span> |
| [Build Walls from CAD](revit_walls_from_cad.md)<br>`revit_walls_from_cad` | Action | <span class="state part">Base (upstream)</span> |

## Export and registers {#group-export}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Export Model Files](revit_export.md)<br>`revit_export` | Action | <span class="state part">Base (upstream)</span> |
| [Export Navisworks NWC](revit_export_nwc.md)<br>`revit_export_nwc` | Action | <span class="state part">Base (upstream)</span> |
| [Issue Register](revit_issue_register.md)<br>`revit_issue_register` | Read | <span class="state part">Base (upstream)</span> |
| [Check NWC Settings](revit_nwc_settings_check.md)<br>`revit_nwc_settings_check` | Read | <span class="state part">Base (upstream)</span> |

## Batch and reports {#group-batch}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Cancel batch collection](revit_batch_cancel.md)<br>`revit_batch_cancel` | Read | <span class="state part">Base (upstream)</span> |
| [Fetch batch snapshots](revit_batch_fetch.md)<br>`revit_batch_fetch` | Read | <span class="state part">Base (upstream)</span> |
| [Start batch collection](revit_batch_start.md)<br>`revit_batch_start` | Read | <span class="state part">Base (upstream)</span> |
| [Batch collection status](revit_batch_status.md)<br>`revit_batch_status` | Read | <span class="state part">Base (upstream)</span> |
| [Build Snapshot Report](revit_build_report.md)<br>`revit_build_report` | Read | <span class="state part">Base (upstream)</span> |
| [Process Many Models](revit_process_models.md)<br>`revit_process_models` | Action | <span class="state part">Base (upstream)</span> |

## C# escape hatch {#group-code}

| Tools | Kind | Base and fork tools |
| --- | --- | --- |
| [Execute C# Code](revit_execute_code.md)<br>`revit_execute_code` | Action | <span class="state part">Base (upstream)</span> |

## What the status means {#status}

Every tool here is registered in the Python registry, and its parameters and description come from that registry. The C# side has not been compiled locally and nothing has been validated on a live workstation. Read these pages as contracts and progress, not as <q>available now</q>.
