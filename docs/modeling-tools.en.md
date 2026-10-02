# Modeling tool specification: first batch

This page is the deliverable of the wayfinder map [Architectural/structural base modeling tools: first-batch specification map](https://github.com/vibe-bimer/revit-model-mcp/issues/8).

!!! warning "This is a specification, not an implemented feature"
    The tools on this page are **not implemented yet**. This specification pins down the contract, the 2020/2026 API approach and the validation method for the first 7 tools, so implementation tickets can follow it directly. Implementation progress follows the [changelog](changelog.md) and the [validation evidence](validation.md).

<a id="scope"></a>
## Scope and batches

| Batch | Content |
| --- | --- |
| **First batch (this page)** | `create_level`, `create_grid`, `load_family`, `place_hosted_family`, `create_column`, `create_beam`, `copy_elements` |
| Second batch | Rooms, element type duplication, openings, materials, wall joins |
| Third batch | Roofs, stairs, railings, curtain walls, annotations, views and sheets; ceilings on 2026 only |

The goal is to build one usable architectural/structural skeleton from a project template. The structural discipline builds **geometry only**; it does not touch the analytical model, loads, boundary conditions or rebar.

<a id="conventions"></a>
## General conventions

These carry over from the repository as it stands; they are not new decisions:

- Lengths are millimetres and model coordinates are XY; length parameters take and return mm.
- Levels and types are resolved by **exact name**; parameters such as `type_name` and `wall_type` are **required parameters that accept `null`**.
- Every action accepts the common `document=null` argument and supports `dry_run=false`; a dry run executes, rolls back and returns a `verification` block of the same shape.
- A successful create action carries `verification.after = { id, category, family, type, level, boundingBoxMinMm, boundingBoxMaxMm }`, and a dry run adds `wouldCreate: true`.
- Every first-batch tool can go into `revit_batch` (one undo step, at most 50 steps).
- The two write gates (`REVIT_MCP_ALLOW_WRITE=1` and the workstation `allow-write` file) and the rule that actions must not save the model are not relaxed for the new tools.

<a id="batch-one"></a>
## First-batch tools

<a id="create-level"></a>
### `revit_create_level`

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `name` | Yes | — | `string` | Level name |
| `elevation_mm` | Yes | — | `number` | Elevation (mm) |
| `create_view` | No | `false` | `boolean` | Also create the matching floor plan view |

- Create with `Level.Create(Document, elevation)`.
- **A duplicate name is rejected**, and the error gives the existing level's name and elevation. The check matches the repository's existing `FindLevel`: an exact match on `BuiltInParameter.DATUM_TEXT`.
- With `create_view=true` it uses `ViewPlan.Create`, and the view type is resolved **by `ViewFamilyType.ViewFamily == ViewFamily.FloorPlan`, not by name** — the template's view type names are in neither the 2020 nor the 2026 corpus, so a name lookup is certain to be brittle.
- Renaming, changing the elevation and copying to an upper level by spacing are **not part of the first batch**.

<a id="create-grid"></a>
### `revit_create_grid`

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `label` | Yes | — | `string` | Grid label |
| `start_mm` / `end_mm` | Yes | — | `array<number>` | Start and end point `[x, y]` |
| `mid_mm` | No | `null` | `array<number>` | When given, defines the arc from three points and uses `Grid.Create(Document, Arc)` |

- A straight line goes through `Grid.Create(Document, Line)`; a curve must lie in a horizontal plane, otherwise it is rejected with the reason.
- The label is written to `Grid.Name`; a duplicate name is rejected.
- **Extents and bubbles are not exposed**: those APIs all live on `DatumPlane`, split between `Model` / `ViewSpecific` semantics and requiring a named view, so they belong to the second batch.

<a id="load-family"></a>
### `revit_load_family`

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `path` | Yes | — | `string` | Absolute path of the family file on the **Revit workstation** |
| `type_name` | No | `null` | `string` | Load only this type; empty loads the whole family |
| `overwrite_parameters` | No | `false` | `boolean` | Whether values from the family overwrite the parameter values of a type already in the project |

- **Always** pass `IFamilyLoadOptions`. Without it Revit uses its default handler and opens a **modal dialog**, which hangs every unattended run — the only reason this tool must accept that interface.
- Default semantics: keep loading, but **do not overwrite** existing parameter values; when a family or type of the same name already exists, reuse the project's version.
- The response reports `state: "new" | "existing"` and the type list `types: [{ id, name }]`.
- A missing `path` is rejected, with the closest file name in the same directory.

<a id="place-hosted-family"></a>
### `revit_place_hosted_family`

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `family` / `type_name` | Yes / No | — / `null` | `string / null` | Loaded family and type |
| `x_mm` / `y_mm` | Yes | — | `number` | Placement point |
| `host_element_id` | No | `null` | `integer` | Explicit host (wall) ID |
| `host_search_radius_mm` | No | `2000` | `number` | Nearest-host search radius when no host is given |
| `level` | No | `null` | `string / null` | Placement level; when empty, the nearest level is used |
| `rotation_deg` | No | `0` | `number` | Rotation about the Z axis |
| `sill_height_mm` | No | `null` | `number` | Sill height (`INSTANCE_SILL_HEIGHT_PARAM`) |
| `flip_facing` | No | `null` | `boolean` | Calls `flipFacing()` when needed |

Host resolution has two paths:

1. **Explicit `host_element_id`**: check that the element exists, is a `Wall`, and that the symbol's `Family.FamilyPlacementType == OneLevelBasedHosted`. Revit does not validate the host itself, and a failure has no documented exception type, so the tool must own this layer.
2. **Find the nearest wall**: project the placement point onto each candidate wall's location line and take the smallest horizontal distance; the distance must not exceed `host_search_radius_mm` and the projection parameter must fall in 0..1 (the point really lies on that wall segment). **Nothing found, a distance over the radius, or a tie for the nearest distance** are all rejected with the candidate list `{ id, distanceMm }`, so the caller can name a host explicitly.

The response reports `hostResolution: { mode: "explicit" | "nearest", hostId, distanceMm }`, so a dry run also shows which wall it would host on.

The existing `revit_place_family` (unhosted, level-based) **keeps its name unchanged**; the two coexist.

<a id="create-column"></a>
### `revit_create_column`

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `family` / `type_name` | Yes / No | — / `null` | `string / null` | Loaded structural column family and type |
| `level` | Yes | — | `string` | Base level |
| `x_mm` / `y_mm` | Yes | — | `number` | Placement point |
| `top_level` | No | `null` | `string / null` | Top level |
| `height_mm` | No | `null` | `number` | Derives the top from the height when `top_level` is absent (default 3000) |
| `base_offset_mm` / `top_offset_mm` | No | `0` | `number` | Base and top offsets |
| `rotation_deg` | No | `0` | `number` | Rotation about the Z axis |

- Create with `document.Create.NewFamilyInstance(point, symbol, level, StructuralType.Column)`. Between the two years only the **declaring type** differs (2020 on `Creation.Document`, 2026 on `ItemFactoryBase`), so a `document.Create.*` call site compiles on both and **needs no `#if`**.
- The tool writes the base and top levels **directly, inside the tool**, through `FAMILY_BASE_LEVEL_PARAM` / `FAMILY_TOP_LEVEL_PARAM` and the two offset parameters. These are ElementId values, and the existing `revit_set_parameter` explicitly rejects ElementId parameters, so they can only be set here.
- **No attachment**: the legal targets of `ColumnAttachment` are floors, roofs, ceilings, beams and braces — **a level is not a legal target**, so "attach to the top level" is not possible in the API.

<a id="create-beam"></a>
### `revit_create_beam`

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `family` / `type_name` | Yes / No | — / `null` | `string / null` | Loaded structural framing family and type |
| `level` | Yes | — | `string` | Reference level |
| `start_mm` / `end_mm` | Yes | — | `array<number>` | Both ends of the axis line `[x, y]` |
| `structural_usage` | No | `null` | `string / null` | Structural usage, written to `FamilyInstance.StructuralUsage` |
| `z_offset_mm` | No | `0` | `number` | Vertical offset |

- It takes the "curve + level" route: `NewFamilyInstance(Curve, FamilySymbol, Level, StructuralType.Beam)`, present in both years, with the axis line and the reference level given directly.
- **The work plane route is not used**: `NewFamilyInstance(Reference, Line, FamilySymbol)` needs a face reference, which an MCP caller cannot obtain.
- **No snapping at the ends**: Revit has no programmatic snap API, and `StructuralFramingUtils.SetEndReference` only works on an end that is already connected. The caller supplies the coordinates.
- Which parameter `z_offset_mm` actually lands on must be settled by a live read-back at implementation time — the corpus has only identifier entries for `STRUCTURAL_BEAM_END0_ELEVATION` / `END1_ELEVATION` / `INSTANCE_ELEVATION_PARAM` and no matching API documentation, so do not pin it down by guessing.

<a id="copy-elements"></a>
### `revit_copy_elements`

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `element_ids` | Yes | — | `array<integer>` | Components to copy |
| `target_level` | No | `null` | `string / null` | Target level; when given, `dz` is derived from the level difference |
| `dz_mm` / `dx_mm` / `dy_mm` | No | `0` | `number` | Offsets given directly |
| `dry_run` | No | `false` | `boolean` | Dry run |

- It uses the **only overload that rehosts**: `ElementTransformUtils.CopyElements(Document, ids, Document, Transform, CopyPasteOptions)`. The documentation of the `(Document, ids, XYZ)` overload states outright that it does not rehost, so using it would take doors and windows off their hosts.
- It **must** set `CopyPasteOptions.SetDuplicateTypeNamesHandler(...)` (a method, not a property). Without it Revit opens a modal dialog asking whether to copy only new types or cancel, which hangs every unattended run; the default returns `DuplicateTypeAction.UseDestinationTypes`.
- Across levels the `Transform` is a pure translation; no overload accepts a target-level argument, so the caller must compute the level difference.
- **The host of a hosted component must be in `element_ids`**, otherwise the whole batch is rejected and the offending component is named. Revit documents the consequence: "when no new host is found, that component is deleted when the paste completes" — silently losing components is worse than a rejection.
- **Failure granularity is per element**: a copy destroys nothing, so there is no need for the whole-batch rejection that `revit_reset_element_ids` uses. Each element reports `old → new` or a failure reason.
- `CopyElements` returns only the set of new IDs and **guarantees no order and gives no mapping**. Pairs are verified by category + type + position, and when no exact pair can be found the response clearly marks `idMappingVerified: false`.

<a id="verification"></a>
## Verification matrix and definition of done

Every first-batch tool runs three cases in **both 2020 and 2026**:

1. The success path (a real write, checking `verification.after`).
2. A `dry_run` rollback (returns the same `verification` shape with `wouldCreate: true`).
3. One error path (a duplicate level name, an invalid host, a missing family file).

Plus two global assertions: after a `dry_run`, `revit_document_info.isModified` must still be `false`, which proves the rollback happened; after a real write, the test model **file**'s mtime must not change. An action never saves the model, so the in-memory document does go dirty (`isModified=true`) — that is expected, not a failure.

| Revit year | Test model |
| --- | --- |
| 2020 | `E:\revitmcp-test\建筑结构.rvt` |
| 2026 | `E:\revitmcp-test\mcp-verify-2026.rvt` (upgraded and saved from that model, keeping its 52 views) |

**Definition of done**: the first 7 tools are done only when a live run passes on both years — this is a **batch gate**, not a per-PR gate. Evidence lands in the [validation evidence](validation.md) and the `validation-assets` branch under the repository's existing convention; when a tool cannot pass on 2026, record a known limit and mark it "build only" in the [version support matrix](features/matrix.md), and a passing build must never stand in for completion.

<a id="later-batches"></a>
## Second and third batches

- **Second batch**: rooms → element type duplication (including composite structure layer edits) → openings → materials → wall joins.
- **Third batch**: roofs → stairs → railings → curtain walls → annotations → views and sheets.

The API entry points for these two batches are **identical** in 2020 and 2026; no year fork is needed.

<a id="known-limits"></a>
## Settled facts and limits

These are already settled, so there is no need to check them again:

- **Revit 2020 has no ceiling creation path**: in the installed `RevitAPI.dll` (20.0.0.377) the `Ceiling` class has 0 public declared members, and the whole assembly has no method that returns `Ceiling` and none that accepts a `CeilingType`; `Ceiling.Create` only appears in 2026. On 2020 a ceiling can only be **read**, or copied from an existing one.
- **A wall's "attach to floor / top" has no API entry point in either year**, only the `WALL_TOP_IS_ATTACHED` / `WALL_BOTTOM_IS_ATTACHED` parameters.
- **There is no programmatic snap API**; `ObjectSnapTypes` only serves interactive picking.
- **`revit_set_parameter` rejects ElementId parameters**, so writing level parameters must happen inside a dedicated tool.
- **`Room.IsEnclosed` does not exist in either year**; room enclosure can only be judged with `Room.IsPointInRoom` / `ClosedShell`.
- **The 2026 workstation's family library is incomplete**: `RVT 2026\Libraries` holds only 446 `.rfa` files (structural precast and path analysis) and no doors, windows, columns or beams; `RVT 2020\Libraries` holds 4,514, and its Chinese library has a full set of doors, windows, columns and beams. Validating `load_family` on 2026 needs family files from the 2020 library (families are backward compatible) or families already loaded in the model.
- **`CloseMainWindow()` works on neither Revit 2020 nor Revit 2026 on that workstation**; before force-killing, confirm `isModified=false`, then clear the `%LOCALAPPDATA%\RevitModelMcp\instance_*.json` heartbeat.
- **The "geometry only" boundary**: the corpus can neither confirm nor deny whether Revit creates analytical elements alongside a structural component. The contract only guarantees that these tools call no analytical API; whether analytical elements appear is decided by project settings, so record `IsStructuralAnalysisEnabled` as an environment fact during validation.
