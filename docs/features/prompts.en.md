# Prompt library

19 read + 16 action tools, 35 in total

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

### [Set view lighting](revit_set_view_lighting.md)

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

### [Export element ID register](revit_export_element_ids.md)

`revit_export_element_ids` — Write the ID register of drawn model components to an Excel workbook

```text
Export the ID register of drawn model components to Excel, ordered by category, family and type
```

### [Model warnings](revit_list_warnings.md)

`revit_list_warnings` — Group model warnings by description and inspect affected elements

```text
Group the model warnings by text
```

## Selection and display {#group-display}

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

## Editing {#group-edit}

### [Move elements](revit_move.md)

`revit_move` — Move elements by offsets along model axes in millimetres

```text
Move these three elements 500 mm along X, dry run first
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

### [Create floor](revit_create_floor.md)

`revit_create_floor` — Create a floor from a closed XY boundary with at least three vertices

```text
Create a floor on 2F from these four points
```

### [Create level](revit_create_level.md)

`revit_create_level` — Create a level at a given elevation in millimetres

```text
Create a level named 4F at 15000 mm
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

## Phases {#group-phases}

### [Set element phases](revit_set_phase.md)

`revit_set_phase` — Assign created/demolished phases; an empty string clears and null leaves unchanged

```text
Mark these elements as demolished in the Existing phase
```

### [Merge project phases](revit_merge_phases.md)

`revit_merge_phases` — Reassign references to another phase and attempt to delete the emptied phase

```text
Merge phase 1 into New Construction
```

## Batch and ids {#group-ids}

### [Replace IDs in place](revit_reset_element_ids.md)

`revit_reset_element_ids` — Replace eligible standalone elements with copies to obtain new IDs

```text
Give these 27 standalone components new ids
```

### [Rebuild IDs in new models](revit_rebuild_model_ids.md)

`revit_rebuild_model_ids` — Copy selectable 3D-view components into one or more new models with fresh IDs

```text
Rebuild the selectable components into E:\out\copy-{n}.rvt, ten copies, no id shared between them
```

```text
Rehearse the rebuild first: how many components, which new id range, write nothing yet
```

### [Batch actions](revit_batch.md)

`revit_batch` — Execute 1–50 actions as one undo step and roll back on the first failed step

```text
Move and retag these ten elements as one undo step
```

```text
Show this batch of changes as a dry run first
```
