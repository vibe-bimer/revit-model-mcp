# Validation evidence

Validation status as of 2026-10-02; ✅ denotes a completed check and — denotes no validation evidence for that check.
CI evidence includes the v0.1.0 release builds for R22–R26 and the R22/R26/R27 CI builds.
Local build evidence includes `Release.R26` and `Release.R27`, plus the Revit 2024 build through `install.ps1 -Source Build`.

| Revit year | Build in CI | Local build | Live reads | Live actions | Install script |
| --- | --- | --- | --- | --- | --- |
| 2020 | ✅ | ✅ | ✅ | ✅ | — |
| 2022 | ✅ | — | — | — | — |
| 2023 | ✅ | — | — | — | — |
| 2024 | ✅ | ✅ | — | — | ✅ |
| 2025 | ✅ | — | — | — | — |
| 2026 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2027 | ✅ | ✅ | — | — | — |

Live checks use Revit 2026.4 with Autodesk's `Snowdon Towers Sample Architectural.rvt`, called from macOS over the SSH transport.
All 18 of the 19 read tools, including the four coordinator tools, are live-validated; `revit_export_element_ids` is validated on 2020 only.
Live action checks cover nine of the sixteen actions: `select`, `show`, `isolate`, `move`, `create_wall`, `create_level`, `set_parameter`, `delete` and `batch`, with dry runs and real writes for actions that support them; `revit_reset_element_ids` and `revit_rebuild_model_ids` are validated on 2020 only.
Installer checks cover `-Source Build` for 2024 and 2026 with `-SignThumbprint`, `-Source Release` for 2024 from v0.1.0, and `-Uninstall`.
Revit 2022–2025 and 2027 have build evidence only for add-in behavior; no live reads or actions are validated on those years in this validation pass.

The Revit 2020 checks ran on 2026-09-28 and 2026-09-29 against Revit 2020 (20.0.0.377) with `E:\revitmcp-test\MEP文件.rvt` and `E:\revitmcp-test\建筑结构.rvt` on a Windows workstation, called from Linux over the add-in HTTP channel.
All 19 read tools are live-validated, including `revit_export_view`, `revit_export_element_ids` and all four coordinator tools.
All 16 action tools are live-validated on that year: `select`, `show` and `isolate` ran for real, and `move`, `place_family`, `create_wall`, `create_floor`, `create_level`, `set_parameter`, `delete`, `set_phase`, `merge_phases`, `set_view_lighting`, `batch`, `reset_element_ids` and `rebuild_model_ids` were checked with `dry_run` and returned `verification`.
`revit_create_floor` exercised the Revit 2020 `Document.Create.NewFloor` path, and `revit_set_phase` exercised the phase-order check that Revit only exposes from 2022.
`revit_export_element_ids` wrote a workbook for the components of `MEP文件.rvt` with the frozen header, the autofilter and the category→family→type order intact.
`revit_reset_element_ids` reset 27 unconnected components of `MEP文件.rvt` with the register unchanged, and its system guard kept every pipe, duct and connected accessory out of the run.
`revit_rebuild_model_ids` copied the 899 selectable elements of `建筑结构.rvt` into a new model and the source stayed untouched; the new model opened without a prompt, carried 900 elements in its three-dimensional view, and kept the source wall and level types.
On the 0.9.0 build, one task wrote ten copies of that model in 165 s (16.5 s a copy): every copy held 899 components with `idMappingVerified=true`, no id appeared in two copies, and the ids ran 2473–4256, 19259–21042, … 44771–46554.
Screenshots and JSON evidence are on the [`validation-assets` branch](https://github.com/vibe-bimer/revit-model-mcp/tree/validation-assets).
The Revit undo menu label for a batch (`revit_run_actions`) cannot be verified through the API.

`revit_create_level`, the first of the first-batch modeling tools, was verified live on both 2020 and 2026 on 2026-10-02, using `建筑结构.rvt` and the `mcp-verify-2026.rvt` upgraded from it.
On both years: after a `dry_run` rollback `isModified` was still `false`; a real write created the level and reported `verification.after = { id, category: "标高", name, elevationMm }`; a duplicate name was refused with `Level '1F' already exists at 0 mm.`; and `create_view=true` moved the view count from 52 to 53.
After the real writes on both years the test model file kept its size and mtime — no action saved the model.

`revit_create_grid` was verified live on Revit 2026 on 2026-11-02 with `mcp-verify-2026.rvt`, called from Linux over the SSH transport. There is no matching 2020 record: this tree's csproj carries R22–R27 configurations only, so the 2020 build does not exist here.
On a clean model a `dry_run` rollback left `isModified` at `false` and reported `verification.after = { id, category: "轴网", fork: { name } }` with `wouldCreate: true`; a real write created the grid and left one undo entry, `MCP (mcp): Created a grid in mcp-verify-2026`; a duplicate label was refused with `Grid 'MCP-VERIFY-GRID' already exists.`; `mid_mm` built an arc grid; three collinear points were refused with `start_mm, mid_mm and end_mm must not be collinear: an arc needs a mid point off the start-end line.`; and coincident endpoints were refused with `start_mm and end_mm must not be the same point.`.
A grid is a datum, so the model holds no bounding box for it: `verification.after` identifies the created grid by `fork.name` rather than `boundingBoxMinMm`/`boundingBoxMaxMm`.
After every write the model file kept its size (19,918,848 bytes) and mtime (2026-10-02T12:08:34) — no action saved the model.

`revit_load_family_file` was verified live on Revit 2026 on 2026-11-02 with `入口门厅.rfa` from the 2020 Chinese library, on the same model and transport.
A `dry_run` rollback reported `fork = { state: "new", familyName: "入口门厅", familyTypes: [{ id, name: "3200 x 3000mm" }] }` with `wouldCreate: true`; a real write loaded the whole family and left one undo entry; loading the same file again reported `state: "existing"` and `committed: false` with the summary `It changed nothing, so no undo entry was kept.`, so nothing was loaded twice and the parameter values the model already held were left alone; a mistyped path reported `Family file '…\入口门.rfa' was not found. Closest: 入口门厅.rfa.`; and a `type_name` the family does not hold reported `Type 'NO-SUCH-TYPE' is not in family '入口门厅'. Available types: 3200 x 3000mm.`.
Again, after every write the model file kept its size and mtime.

`revit_create_column` (2026-11-02) was checked live on Revit 2026, on the same model and channel, with the column family `混凝土 - 正方形 - 柱.rfa` from the 2020 Chinese library (four types, `300 x 300mm` through `750 x 750mm`) loaded first by `revit_load_family_file`; 2020 has no record for the same reason as the paragraph above.
Base level plus `height_mm` only: `dry_run` reported `rolledBack: true`, `wouldCreate: true` and `verification.after = { id, category: "结构柱", level: "1F", type: "300 x 300mm", boundingBoxMinMm: [11850, -150, 0], boundingBoxMaxMm: [12150, 150, 3000] }`, and that id is not found by `revit_element_details` after the rollback; the real write created the column (`id 364295`), read back as `底部标高 = 1F`, `顶部标高 = 1F`, `顶部偏移 = 3000 mm`, so the top elevation is the base level plus the base offset plus the height.
With `top_level`: a column with `top_level = "3F"` has a bounding box that reaches 7600 mm, matching the 3F elevation; a `600 x 600mm` column with `base_offset_mm = 500` and `rotation_deg = 45` came back with a bounding box of `[-424.3, 5575.7, 4300]`–`[424.3, 6424.3, 7300]`, so both the offset and the rotation reached the model.
A missing `type_name` reported `Type 'NO-SUCH-TYPE' was not found in family '混凝土 - 正方形 - 柱'. Available types: 300 x 300mm, 450 x 450mm, 600 x 600mm, 750 x 750mm.`; a missing family reported `Family 'NO-SUCH-FAMILY' was not found. Use revit_load_family_file to load it first.`
After every write, the model file's size (19,918,848 bytes) and mtime (2026-10-02T12:08:34) were unchanged — the actions do not save the model.
