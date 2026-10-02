# Actions (opt-in)

Read-only by default. Actions are a separate tool set you enable on purpose.
Transaction warnings are dismissed and reported in `warningsDismissed` (omitted when empty); errors that cannot be safely resolved roll back the action.

## Instance and document targeting

Every action tool accepts `document=null`; none exposes custom timeout arguments.
They use the default 120-second response and 300-second pickup budgets; pickup applies only to local and SSH transports.
The MCP transport must discover exactly one running Revit instance before sending any action, even when `document` is provided.
Otherwise, the call fails with `Actions require exactly one running Revit instance.`
HTTP addresses one endpoint; the file transports discover workstation instances.
`document` selects an open document inside that one process, not an instance from a list of processes.
All IDs are unitless, positive integer Revit element IDs, up to 9,223,372,036,854,775,807.
Revit 2020–2023 accept IDs up to 2,147,483,647 only; larger IDs fail on those years.

The MCP `document` argument becomes `targetDocument` in the action job.
Provide it when the target process has multiple open documents; omit it only when a single document is open.
Action jobs with `targetDocument` resolve that reference when the add-in executes the job.
The reference must match exactly one open document by a case-insensitive substring of its title or file name.
The resolved document is bound by its title and full path for all mutations and verification, even if another document is active.
An unknown or closed target returns `The addressed document '<TargetDocument>' is not open.`
An ambiguous target returns `The document reference '<TargetDocument>' is ambiguous (N open documents match); use a more specific substring.`
Resolution failure aborts the whole batch before any step runs; an addressed job never falls back to the active document.
The target is resolved once before the batch loop, and a later document or transaction failure is reported as a step error.
`select`, `show` and `isolate` (including `reset=true`) require the resolved document to be active.
Otherwise, they return `Cannot run '<command>' on '<title>' because it is not the active document; activate it in Revit first.`
Jobs without `targetDocument` retain the active-document behavior.
`activeView` always reports the actual active view, even when a mutation targets another document.

## Tool catalogue

Every row also accepts the common `document=null` argument. Arguments without defaults are required, even when they accept `null`.
See the [feature overview](features/index.md) for each tool's full parameter table, prompts and Revit-year validation status.

| Tool | Arguments beyond `document=null` | Action and units |
| --- | --- | --- |
| `revit_select` | `element_ids` | Select IDs; `[]` clears selection. Return `count`, the current selection size after the call. |
| `revit_show` | `element_ids`, `select=true` | Show nonempty IDs; return `activeView`, `viewOpened` and `count`, the current selection size after the call. With `select=false`, `count` reports the previous selection. |
| `revit_isolate` | `element_ids`, `reset=false` | Temporarily isolate IDs; `element_ids=[]` with `reset=true` clears hide/isolate. |
| `revit_move` | `element_ids`, `dx_mm`, `dy_mm`, `dz_mm=0` | Move by model-axis offsets in mm. |
| `revit_place_family` | `family`, `type_name`, `x_mm`, `y_mm`, `level`, `rotation_deg=0` | Place a loaded family at model XY in mm on a named level; rotate about Z in degrees. |
| `revit_create_wall` | `start_mm`, `end_mm`, `level`, `wall_type`, `height_mm=3000` | Create a straight wall; endpoints are `[x,y]` in model mm. |
| `revit_create_floor` | `points_mm`, `level`, `floor_type` | Create a floor from a closed boundary; `points_mm` are `[x,y]` polygon vertices in model mm, at least 3, closed automatically; null `floor_type` chooses the first floor type. |
| `revit_create_level` | `name`, `elevation_mm`, `create_view=false` | Create a level at a given elevation in mm; an existing level with that exact name is refused, so a later tool never resolves an ambiguous level; `create_view=true` also creates the matching floor plan, whose view type is chosen by view family rather than by name. |
| `revit_set_phase` | `element_ids`, `created_phase`, `demolished_phase` | Assign project phases by exact name; each phase argument is a name, `""` to clear that assignment, or null to leave it unchanged; at least one non-null. These tools do not create or rename phases — add new phases in the UI first. |
| `revit_merge_phases` | `source_phase`, `target_phase` | Move every creation and demolition reference off the source phase into the target, then delete the empty source phase; a refused deletion is reported with `sourceDeleted:false` and `phaseDeleteError`. Not batchable. |
| `revit_set_parameter` | `element_id`, `parameter`, `value` | Set a string value by parameter name; lengths use mm, areas m2, other doubles internal units. |
| `revit_set_view_lighting` | `view`, `shadows=null`, `shadow_intensity=null`, `sunlight_intensity=null`, `sun_date=null`, `sun_time=null`, `sun_azimuth_deg=null`, `sun_altitude_deg=null`, `ground_plane=null`, `ground_plane_level=null`, `background=null`, `background_colors=null`, `lighting_scheme=null`, `dry_run=false` | Set one non-template view's lighting by view name or view ID: shadows, sun and shadow intensities, sun date and time or a fixed lighting-study azimuth and altitude, ground plane, background and rendering lighting scheme. The response reports the readings before and after under `verification.before.lighting` and `verification.after.lighting`, and names what moved in `changedSettings`. |
| `revit_delete` | `element_ids` | Delete nonempty IDs and their dependents. |
| `revit_reset_element_ids` | `element_ids`, `dry_run=false` | Replace elements with copies so Revit assigns new IDs; reports `idMapping` and refuses an element when deletion would remove dependents, when it is hosted or grouped, when it is an MEP curve or an MEP system member (a copy does not rejoin the network, and Revit re-heals the run around the deleted original), or when Revit cannot copy it. |
| `revit_batch` | `steps`, `dry_run=false` | Execute 1–50 actions with a single undo entry named `revit_batch`. |
| `revit_rebuild_model_ids` | `destination_path`, `view=null`, `template_path=null`, `overwrite=false`, `remove_template_levels=true`, `seed=0`, `duplicate_names="override"`, `copies=1`, `dry_run=false` | Copy the selectable components of a 3D view into a new model, so Revit assigns every element a fresh ID; the open model is never changed. Levels, grids and reference planes travel first so hosts resolve; cameras, the sun path, the section box, views and elements without a category are left behind and reported under `excluded`. Views, sheets, schedules, annotations, phases, worksets, MEP systems and unselected hosts do not travel, so the result is geometry, types and parameters. Data reports `count`, `newIdMin`/`newIdMax`, `sourceCategoryCounts`, `copiedCategoryCounts` and an `idMapping` verified against category and type. |

`type_name`, `wall_type` and `floor_type` are required arguments that accept `null`.

## Dry runs and ID replacement

`revit_move`, `revit_place_family`, `revit_create_wall`, `revit_create_floor`, `revit_create_level`, `revit_set_phase`, `revit_merge_phases`, `revit_set_parameter`, `revit_set_view_lighting` and `revit_delete` also accept `dry_run=false`, before the common `document` argument.
A dry run executes the mutation, reads its prospective result, and rolls back the transaction.
A successful dry run includes `data.dryRun:true`, `data.rolledBack:true` and the same `verification` shape as a real write.
An action that throws returns an error without a verification block; a missing family also returns `closestFamilies` on the single-action tool.
`revit_select`, `revit_show` and `revit_isolate` have no `dry_run` argument; isolation is temporary only.
`revit_reset_element_ids` also supports `dry_run`; run it first because a real exchange cannot be undone.
It refuses the entire selection if any element is ineligible, never changes an ID in place and never writes the old ID into a parameter.
Created IDs in a dry run are provisional and do not identify persisted elements.

## View lighting

`revit_set_view_lighting` addresses one non-template view by name or decimal view ID and changes only the arguments you pass.
`shadows` switches that view's sun and shadow display, which is `SunAndShadowSettings.Visible`: with it off Revit draws neither the sun path nor cast shadows, so the intensity settings stop showing, and a view that shares its sun and shadow settings cannot switch them alone and is refused.
Revit offers no API for the Graphic Display Options Shadows checkbox — `GRAPHIC_DISPLAY_OPTIONS_SHADOWS` is only an enum member and the parameter cannot be read from a view (verified live on Revit 2020) — so `shadows` is the switch the API really provides.
`shadow_intensity` (0 to 100, where 0 means no cast shadow) and `sunlight_intensity` (0 to 100) set the cast shadow density and the simulated sunlight.
A view without sun and shadow settings, such as a schedule, is refused instead of being silently ignored.

`sun_date` (`yyyy-MM-dd`) and `sun_time` (24-hour `HH:mm`) fix a still-image sun position and are handed to Revit as local time; the reading reports the result as `sunDateAndTimeUtc` with `sunTimeZoneHours`, so what Revit stored is always checkable. Passing one keeps the other half of what the view already shows, and both switch a one-day or multi-day sun study back to a still image.
For a fixed sun position use `sun_azimuth_deg` (clockwise from north) and `sun_altitude_deg` (degrees above the horizon) instead: they must be passed together and switch the sun settings to lighting mode.

`ground_plane` uses the ground plane and `ground_plane_level` names the level it sits on.
Revit only accepts a level it knows as a ground plane, so a level that is not one is marked as a ground plane first (`LEVEL_IS_GROUND_PLANE`) and the response says so under `notes`; choosing a ground plane level while the ground plane is off also switches it on.
`background` is `sky` or `gradient` and works on 3D, section and elevation views; `background_colors` gives the gradient's sky, horizon and ground colors as `#RRGGBB` and defaults to the current gradient, or to `#C8DEF0`/`#F5F5F5`/`#BFBFBF` when the current background is not a gradient.
Revit's API can set a background to sky, gradient or image but cannot return it to none, and it cannot clear a chosen ground plane level; both are API limits recorded for this project, so check the view's current state before changing them.
`lighting_scheme` sets the rendering lighting source: `exterior-sun`, `exterior-sun-and-artificial`, `exterior-artificial`, `interior-sun`, `interior-sun-and-artificial` or `interior-artificial`; it affects renderings, not the shaded display.

Sun and shadow settings belong to the view. When a view shares them, the reading reports `sunSettingsShared:true`, the change reaches every view that shares them, and the response says so under `notes`.
`verification.before.lighting` and `verification.after.lighting` carry the full readings on both sides: view ID, name and type, shadows, both intensities, sun type and time (UTC), project time zone and daylight saving, lighting-mode azimuth and altitude, ground plane and level, background type and colors, and the rendering lighting scheme.
A view has no element ID to report, so the settings that actually moved are listed in `changedSettings` (for example `["shadows","sun_date_time"]`) instead of `verification.changed`.

## Rebuilding into new model files

`revit_rebuild_model_ids` is not a transaction: `dry_run=true` performs the copy and reports the mapping without saving a file, and a real run writes the new model while the source is never modified or saved.
`destination_path` is a path on the Revit workstation, not the MCP client.
Without `view`, the tool uses the first non-perspective 3D view; only components selectable in that view are copied.
`template_path` chooses a template instead of the default metric template; `remove_template_levels=true` removes the template's own levels.
`overwrite=true` explicitly replaces an existing destination; the default is false.
The response also includes `destinationPath`, `saved`, `sourceView`, `sourceElementCount`, `datumCount` and a reason for each excluded element.
The template the new model starts from carries no real view, so the rebuild adds a three-dimensional view when one is missing; without it Revit refuses to open the file.
When a name the source uses already exists in the new project, Revit asks the user how to resolve the duplicate while it pastes, and that question blocks an unattended run; by default the rebuild answers it with OK (`duplicate_names=override`), which keeps the source model's own types and reports how many questions it answered under `autoAnsweredDialogs`. `duplicate_names=rename` renames the template's elements first and removes them again afterwards: it costs about 30 seconds per copy and Revit refuses many of those deletes, so it is only a fallback.
`duplicate_names=reuse` never asks about a duplicated name and keeps the version the new model already holds; a run that writes several copies uses it by default, because asking is what makes Revit refuse a paste. A copy Revit refuses anyway is retried with that same setting; the recorded retry recovered a copy that was eleven elements short, but callers must still verify the returned mapping.
`copies=2` and up write several files from one new model, one copy after another, and remove the elements of each copy before the next one: Revit keeps handing out higher ids in a document, so every copy holds the same components with ids of its own and no ids have to be burned first. `destination_path` may carry `{n}` for the copy number; without it the number is appended before the extension. The per-copy paths, sizes and ID mappings are reported under `copyResults`. Revit sometimes refuses the bulk paste of a later copy: that copy then falls back to the element-by-element path and comes out smaller with `idMappingVerified=false` in its `copyResults` entry, so callers must check every entry. One copy per run was the reliable shape in the recorded tests; see [rebuild performance](rebuild-performance.md) for the measurements. For parallel runs across several Revit instances, use separate HTTP endpoints or transports that each discover exactly one instance; `document` does not bypass the single-instance gate. The instances take their port, token and channel directory from `REVIT_MCP_HTTP_PORT`, `REVIT_MCP_TOKEN` and `REVIT_MCP_CHANNEL_DIR`.
Revit assigns the copied elements the IDs that follow the ones the new model already holds, so two rebuilds of the same source produce the same IDs; `seed` adds that many temporary levels to the new model before the copy and removes them again, which moves a copy's IDs into a block of their own.
Created IDs reported by a rebuild dry run likewise do not identify a saved output model.

## Verification and committed changes

Successful real writes return `data.dryRun:false` and re-read the affected elements after commit.
`verification.before` is captured before the change; `verification.after` is re-read after commit or before rollback on a dry run.
`verification.error` reports a failed post-commit re-read; the change is committed.
Single-action responses include `failedStep:null`.
The `verification` block contains model facts: bounding boxes for moves, parameter values and ownership for parameter edits, element metadata for creation, and deleted/dependent IDs with a survival check for deletion.
Bounding boxes use model XYZ in mm rounded to one decimal; unavailable bounding boxes are omitted.
For example, setting Comments on element 123 returns:

```json
{
  "dryRun": false,
  "verification": {
    "before": {"id": 123, "parameter": "Comments", "value": "", "storageType": "String", "owner": "instance"},
    "after": {"id": 123, "parameter": "Comments", "value": "Reviewed", "storageType": "String", "owner": "instance"},
    "changed": [123]
  }
}
```

## Batch execution

`revit_batch` takes action names and their normal snake_case arguments. Set `document` once on the batch, not inside each step's `args`:

```json
{
  "steps": [
    {"action": "move", "args": {"element_ids": [123], "dx_mm": 100, "dy_mm": 0}},
    {"action": "set_parameter", "args": {"element_id": 123, "parameter": "Comments", "value": "Reviewed"}}
  ],
  "dry_run": false
}
```

A successful batch assimilates its transactions into one undo entry named `revit_batch`.
The first failed step rolls back the entire batch; every attempted step, including the failing one, carries `rolledBack:true`.
An `Assimilate` failure is reported on the last step with `failedStep` pointing at it.
All steps are validated before execution; an invalid later step rejects the whole batch without executing anything and without `failedStep`.
Results include zero-based `index`, `command`, `success` and `data` or `error` per attempted step, plus `undoName`, `committed` and `failedStep` (null on success).
A batch dry run executes every step against preceding steps' changes, then rolls back the group and restores the original selection.
A per-step `dry_run:true` inside a real batch is accepted and previews only that step.
Verification describes each step's immediate result; subsequent steps may change those elements again.
Batches accept 1–50 steps; `select` and `isolate` are allowed, while `show`, nested batches and unknown argument keys are rejected.

## Navigation, dialogs and family names

`revit_show` checks the open UI views before calling `ShowElements`.
If none contains a requested element, it opens a non-template plan for an element's level.
Floor plans take priority, followed by names starting with the level name.
Without a matching plan it uses the first non-template 3D view.
The handler sets `UIDocument.ActiveView` synchronously inside its ExternalEvent without a transaction; `ShowElements` needs the view active immediately.
`RequestViewChange` defers the change until control returns to Revit.
The response includes `activeView` and `viewOpened`, which reports whether the handler opened a previously closed view.

During action execution, the handler attempts to dismiss TaskDialog prompts with OK and then Yes.
Messages from successful overrides appear in `dialogsSuppressed`.
The dialog handler is removed in `finally`, including on errors.
For the single-action `revit_place_family` tool, missing families return up to five similar names with their family categories in `closestFamilies`; unrelated names are omitted.
Inside `revit_batch`, a missing family surfaces only as `steps[].error` text; `closestFamilies` is unavailable.
For `Family: Type`, `type_name=null` uses the embedded type; a conflicting `type_name` is rejected.
For a family name alone, `type_name=null` selects the first loaded type.

## Gates {#gates}

Both gates must be enabled:

1. Set `REVIT_MCP_ALLOW_WRITE=1` in the Python server process environment and restart the server.
   The boolean parser trims whitespace and ignores case: `1`, `true`, `yes` and `on` enable actions; `0`, `false`, `no` and `off` disable them.
   When unset, actions are disabled and MCP `list_tools` omits them. Unrecognized values raise a configuration error rather than silently disabling actions.
2. Create `%LOCALAPPDATA%\RevitModelMcp\allow-write` on the Revit workstation:

   ```powershell
   New-Item -ItemType Directory -Force "$env:LOCALAPPDATA\RevitModelMcp" | Out-Null
   New-Item -ItemType File -Force "$env:LOCALAPPDATA\RevitModelMcp\allow-write" | Out-Null
   ```

The add-in checks the gate file for every action, including selection and navigation.
Without it, the response contains `success:false` and `error:"actions disabled on the workstation"`.
Removing the file disables actions immediately; restarting Revit is unnecessary.
The gate stays in the default local application data directory even if the transport uses `REVIT_MCP_CHANNEL_DIR`.

Direct HTTP action requests require authentication and the workstation gate; the Python environment gate controls exposure of the MCP action tools.

## Units and parameter scope

Actions address the process ID reported by the transport.
Coordinates use model axes and the named level's project elevation.
Pass `null` for `type_name` to choose the family's first type, or for `wall_type` to choose the first basic wall type.
Family placement uses the level-based, nonstructural overload; hosted, face-based and adaptive families may require another placement API and return an error.
The single-action family placement tool returns up to five closest loaded names for an unloaded family.
Parameter values use invariant numeric notation; other Double parameters use Revit internal units.
Type parameter edits affect all instances of that type and return `parameterScope:"type"`.
ElementId and read-only parameters cannot be set.

## Transactions and timeout safety

Responses from the action executor include `activeView`, including action errors.
Transport rejection and target-mismatch responses may omit action metadata.
Model changes and temporary isolation use individual transactions named after the tool.
`revit_batch` wraps the per-step transactions in a `TransactionGroup` named `revit_batch` and assimilates them into one undo entry.
Warnings at commit are dismissed and reported on successful actions.
Errors permit one `FixElements` or `SetValue` resolution when Revit allows it; unresolved or repeated errors roll back the transaction.
Selection and navigation use UI calls without model transactions.
Actions do not save the addressed source model; `revit_rebuild_model_ids` saves only its new output model files on the workstation.
A timeout does not prove that an action rolled back or never ran; even a pickup timeout can leave a pending job that executes later.
After a timeout or a post-commit verification failure, inspect the model and any output files before retrying; the previous call may have executed.
