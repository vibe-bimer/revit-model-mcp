# Prompt library

<p class="facts">33 Tool</p>

## Connection and documents

**`revit_ping`** — Check the RevitModelMcp connection without reading the model.

```text
Is the Revit add-in reachable?
```

**`revit_document_info`** — Read general information about the active Revit model.

```text
Which model is open, and which levels does it have?
```

**`revit_list_instances`** — List Revit processes and their active documents.

```text
Which Revit instances are running, and what does each hold?
```

## Query and totals

**`revit_list_catalog`** — Discover valid model names before filtering.

```text
List the parameter names this model offers
```

**`revit_aggregate_elements`** — Summarize matching elements by one or two fields after revit_list_catalog.

```text
How many of each wall type sit on 1F?
```

```text
Count the doors per level and their total width
```

**`revit_query_elements`** — Read a page of matching element rows after revit_list_catalog.

```text
List the doors on 2F whose fire rating is empty, with ids
```

**`revit_element_details`** — Read parameters and geometry of an element by Revit ID.

```text
Show every parameter and the geometry of element 357640
```

**`revit_list_relations`** — Read model object membership or dependencies.

```text
Which rooms sit on level 1F?
```

## Views and snapshots

**`revit_list_views`** — Find non-template views before analyzing a view.

```text
List every floor plan view
```

**`revit_view_summary`** — Read element categories and counts for a selected view.

```text
What does the 3D view hold, category by category?
```

**`revit_export_view`** — Export a selected view to PNG when numbers do not explain geometry.

```text
Export the 1F plan as a PNG, 2000 pixels wide
```

**`revit_view_elements`** — Read one page of elements in a selected view.

```text
Page through the elements of the 3D view, 200 at a time
```

**`revit_view_warnings`** — Read warnings involving elements present in a selected view.

```text
Which warnings touch this view?
```

## Export and checks

**`revit_model_health`** — Read model quality counts before an export or hand-over.

```text
Run a pre-handover health check: size, counts, units, top warnings
```

**`revit_links_status`** — Read RVT, CAD and image link status before an export or hand-over.

```text
Check every link: RVT, CAD and images
```

**`revit_shared_coordinates`** — Read project and survey coordinates before an export or hand-over.

```text
Report the shared coordinates and link offsets
```

**`revit_parameter_fill_check`** — Count filled, empty and missing parameters before an export or hand-over.

```text
How well is the fire rating filled in on walls? Give me the empty ids
```

**`revit_export_element_ids`** — Write the identifier register of the drawn components to an xlsx file on the Revit workstation.

```text
Export the 3D view components to Excel, ordered by category and family
```

**`revit_list_warnings`** — Group model warnings by description text.

```text
Group the model warnings by text
```

## Selection and display

**`revit_select`** — Select element IDs for inspection in Revit; an empty list clears selection; IDs are unitless. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

```text
Select element 123456
```

**`revit_show`** — Show elements, optionally selecting them; open a level plan or 3D view when needed. Returns activeView, viewOpened and dialogsSuppressed; IDs are unitless. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

```text
Show me those columns in the view
```

**`revit_isolate`** — Temporarily isolate IDs for visual review in the active view, or reset with an empty list; IDs are unitless. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

```text
Isolate the windows of this level
```

## Editing

**`revit_move`** — Move elements when adjusting their position; dx_mm, dy_mm and dz_mm are offsets in millimetres on model axes. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

```text
Move these three elements 500 mm along X, dry run first
```

**`revit_place_family`** — Place a loaded unhosted family on a named level for layout.

```text
Place a 900x2100 door at 3000,4000 on 1F
```

**`revit_create_wall`** — Create a straight wall for layout on a named level; model XY endpoints and height are millimetres; null wall_type chooses the first basic type. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

```text
Draw a 200 mm wall on 1F from 0,0 to 6000,0
```

**`revit_create_floor`** — Create a floor from a closed boundary for layout on a named level. points_mm are model XY polygon vertices in millimetres (at least 3; the boundary closes automatically); null floor_type chooses the first floor type. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

```text
Create a floor on 2F from these four points
```

**`revit_set_parameter`** — Set a named instance parameter, falling back to its shared type; use for edits, with length in mm, area in m2 and other doubles in internal units. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

```text
Set the fire rating of these walls to two hours
```

**`revit_delete`** — Delete elements and their Revit dependencies when removal is intended; IDs are unitless and the returned count includes dependents. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

```text
Delete these two elements, dry run first
```

## Phases

**`revit_set_phase`** — Assign the created or demolished project phase of elements by exact phase name.

```text
Mark these elements as demolished in the Existing phase
```

**`revit_merge_phases`** — Merge one project phase into another by moving every element reference.

```text
Merge phase 1 into New Construction
```

## Batch and ids

**`revit_reset_element_ids`** — Replace elements with copies so Revit assigns new element IDs; the API cannot assign one itself.

```text
Give these 27 standalone components new ids
```

**`revit_rebuild_model_ids`** — Give every component new IDs by copying a 3D view's selectable elements into a new model, because Revit does not allow assigning an element ID.

```text
Rebuild the selectable components into E:\out\copy-{n}.rvt, ten copies, no id shared between them
```

```text
Rehearse the rebuild first: how many components, which new id range, write nothing yet
```

**`revit_batch`** — Execute up to 50 actions with one undo step; roll back the batch on its first failure.

```text
Move and retag these ten elements as one undo step
```

```text
Show this batch of changes as a dry run first
```
