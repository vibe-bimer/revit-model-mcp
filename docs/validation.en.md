# Validation evidence

Validation status as of 2026-09-29; ✅ denotes a completed check and — denotes no validation evidence for that check.
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
Live action checks cover `select`, `show`, `isolate`, `move`, `create_wall`, `set_parameter`, `delete` and `batch`, with dry runs and real writes for actions that support them; `revit_reset_element_ids` and `revit_rebuild_model_ids` are validated on 2020 only.
Installer checks cover `-Source Build` for 2024 and 2026 with `-SignThumbprint`, `-Source Release` for 2024 from v0.1.0, and `-Uninstall`.
Revit 2022–2025 and 2027 have build evidence only for add-in behavior; no live reads or actions are validated on those years in this validation pass.

The Revit 2020 checks ran on 2026-09-28 and 2026-09-29 against Revit 2020 (20.0.0.377) with `E:\revitmcp-test\MEP文件.rvt` and `E:\revitmcp-test\建筑结构.rvt` on a Windows workstation, called from Linux over the add-in HTTP channel.
All 19 read tools are live-validated, including `revit_export_view`, `revit_export_element_ids` and all four coordinator tools.
All 14 action tools ran on that year: `select`, `show` and `isolate` ran for real, and `move`, `place_family`, `create_wall`, `create_floor`, `set_parameter`, `delete`, `set_phase`, `merge_phases`, `batch`, `reset_element_ids` and `rebuild_model_ids` were checked with `dry_run` and returned `verification`.
`revit_create_floor` exercised the Revit 2020 `Document.Create.NewFloor` path, and `revit_set_phase` exercised the phase-order check that Revit only exposes from 2022.
`revit_export_element_ids` wrote a workbook for the components of `MEP文件.rvt` with the frozen header, the autofilter and the category→family→type order intact.
`revit_reset_element_ids` reset 27 unconnected components of `MEP文件.rvt` with the register unchanged, and its system guard kept every pipe, duct and connected accessory out of the run.
`revit_rebuild_model_ids` copied the 899 selectable elements of `建筑结构.rvt` into a new model and the source stayed untouched; the new model opened without a prompt, carried 900 elements in its three-dimensional view, and kept the source wall and level types.
On the 0.9.0 build, one task wrote ten copies of that model in 165 s (16.5 s a copy): every copy held 899 components with `idMappingVerified=true`, no id appeared in two copies, and the ids ran 2473–4256, 19259–21042, … 44771–46554.
Screenshots and JSON evidence are on the [`validation-assets` branch](https://github.com/sharafutdinovdi/revit-model-mcp/tree/validation-assets).
The Revit undo menu label for a batch (`revit_batch`) cannot be verified through the API.
