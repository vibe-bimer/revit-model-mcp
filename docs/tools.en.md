# Read tool reference

All tools support local, SSH and HTTP transports. They do not change the model; the two export tools write files.

## Transports and output files

`revit_export_view` downloads PNG through `/views/{name}/image` in HTTP mode.
`revit_export_element_ids` writes its workbook on the Revit workstation, so `save_to` is a workstation path and HTTP clients read the returned `path` instead of downloading the file.
The identifier column holds the Revit element ID, which the API cannot assign: the tool lists identifiers and never changes them.
`revit_list_instances` reports the connected Revit process in HTTP mode.

## Common arguments and tool catalogue

Every read tool except `revit_export_view` and `revit_list_instances` accepts `timeout_seconds=120`, `pickup_timeout_seconds=300` and `document=null`.
Timeouts are positive integer seconds; pickup timeout applies only to local and SSH transports and is ignored over HTTP.
`revit_export_view` uses the default 120-second response and 300-second pickup budgets without exposing timeout arguments.
When more than one Revit instance is running, provide a unique `document` substring of the active document title or file name; otherwise any instance may respond.
`revit_list_instances(document=null)` lists all instances, and a document filter returns all matching instances rather than selecting one.
Arguments without defaults in these tables are required.
The query filters shared by aggregation and queries are `categories`, `family`, `type_name`, `level`, `view`, `workset`, `phase`, `area_scheme` and `parameter_filters`; each defaults to `null`.

| Tool | Arguments beyond the common read options | Purpose |
| --- | --- | --- |
| `revit_ping` | None | Check connectivity; returns `data:"pong"`. |
| `revit_document_info` | None | Read document, levels, area schemes and worksets. |
| `revit_list_catalog` | `section` | Discover valid category, family, view and parameter names. |
| `revit_aggregate_elements` | `group_by`, `sum_field=null`, shared query filters | Group by one or two fields; return counts and optional sum/average. |
| `revit_query_elements` | Shared query filters, `fields=null`, `offset=0`, `limit=100`, `sort_field="id"`, `sort_direction="asc"`, `include_geometry=false` | Read a page of matching elements. |
| `revit_list_views` | `view_type=null`, `name_contains=null` | Find views in the active document. |
| `revit_view_summary` | `view` | Read view metadata and category counts. |
| `revit_export_view` | `view`, `pixel_size=1600`, `save_to=null`, `document=null`; no timeout arguments | Download a PNG; `pixel_size` is 1-4000 pixels on the fitted image dimension. |
| `revit_export_element_ids` | `fields=null`, `save_to=null`, `timeout_seconds=120`, `pickup_timeout_seconds=300`, `document=null` | Write the identifier register of the drawn components to an xlsx workbook on the Revit workstation, ordered by category, family and type. |
| `revit_view_elements` | `view`, `categories=null`, `offset=0`, `limit=100` | Read a page of elements in a view. |
| `revit_element_details` | `element_id` | Read instance/type parameters and geometry by unitless Revit ID. |
| `revit_view_warnings` | `view` | Read warnings involving elements in a view. |
| `revit_list_warnings` | `warning_text=null`, `include_elements=false` | Group warnings or inspect a specific warning group. |
| `revit_list_relations` | `relation`, `source_id=null`, `source_name=null` | Read membership or dependencies. |
| `revit_list_instances` | `document=null`; no timeout arguments | List endpoint or heartbeat information. |
| `revit_model_health` | None | Read model quality counts and top warnings before hand-over. |
| `revit_links_status` | None | Read RVT, CAD and image status, paths and instance counts. |
| `revit_shared_coordinates` | None | Read base/survey points, sites and link transforms in mm and degrees. |
| `revit_parameter_fill_check` | `categories`, `parameters`, `level=null`, `workset=null`, `view=null`, `sample_limit=20`, `include_types=true` | Count filled, empty and missing values; sample unitless element IDs. |

## Coordinator checks

Call `revit_model_health` → `revit_links_status` → `revit_shared_coordinates` → `revit_parameter_fill_check(categories=["Walls","Doors"], parameters=["Mark","Comments"])` before an export or hand-over.
Category and parameter names use the model language; the fill check accepts 1–20 categories, 1–30 parameters and a sample limit of 1–100.
Coordinator location and link lists are capped at 100 without pagination; locations are sorted by name and links by ID.
`pinned` and `viewSpecific` are true when any instance of the reported type qualifies.
Parameter names resolve through `LookupParameter(name)`, which returns the first match by name; GUID and BuiltInParameter selection are unavailable.

## Filters, units and pagination

Call `revit_list_catalog` before a universal model query, then prefer `revit_aggregate_elements` for counts and breakdowns; use `revit_query_elements` when individual rows are needed.
Offsets are zero-based row counts; limits are positive row counts. Advance the offset while `hasMore=true`.
Lengths use mm, areas m2 and volumes m3 where metric fields are provided.
Other numeric filter values follow document display units; returned query values carry a `unit` field when available.
See the [feed format](feed-format.md#jobs) for the distinction between filter inputs and numeric outputs.
Parameter names come from the model's language; use `revit_list_catalog(section="parameters")` before filtering.
Query parameter filters are AND-combined and use exact localized names. Supported operators are `equals`, `contains`, `greater`, `less`, `empty`, `not-empty` and `exists`; `contains` requires text, and `empty`/`not-empty`/`exists` need no value.
For area totals, group by level and select the area scheme.

## Export destinations

For `revit_export_view`, `save_to` is a new PNG file path on the MCP client's machine; the default downloads to a local temporary directory and returns `localPath`, image width/height, `sizeBytes` and view metadata without base64.
For `revit_export_element_ids`, `save_to` is an absolute `.xlsx` path on the Revit workstation. The default is `Documents\RevitModelMcp\Exports\构件ID清单_<model>_<timestamp>.xlsx`; the response returns `path`, `fileName`, `sheetName`, `columns`, `rowCount`, `totalCandidates`, `truncated`, `sizeBytes` and `categoryCounts`.
Neither export overwrites an existing destination. The workbook has at most 50,000 rows; more candidates set `truncated=true`.
Its default columns are `类别`, `族`, `类型`, `标高`, `构件ID`, `名称` and `工作集`; `fields` replaces them with built-in field names or parameter names.
The level column is empty for components without a level, including most MEP pipe and duct runs.
Exporting a view does not change the active view or write to the model.

## Geometry

`revit_element_details` returns geometry alongside parameters in `data`.
`revit_query_elements(include_geometry=True)` adds the same fields to each element in the returned page.
The query flag defaults to `False`; default queries omit geometry.
All coordinates use model axes in millimetres rounded to one decimal place.

| Field | Contents |
| --- | --- |
| `location` | Point: `type:"point"`, `xMm`, `yMm`, `zMm`. Curve: `type:"curve"`, `startMm`, `endMm`, `lengthMm`. |
| `boundingBox` | `minMm`, `maxMm`, `centerMm` as `[x,y,z]` arrays from the element's model bounding box. Rooms use their own bounding box. |
| `roomCenterMm` | `[x,y,z]` from a placed room's location. Use `roomCenterMm` when placing something inside a room. A bounding box centre may lie outside a nonrectangular room. |

Unavailable geometry is omitted.
