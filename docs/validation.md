# Validation evidence

Validation status as of 2026-09-28; ✅ denotes a completed check and — denotes no validation evidence for that check.
CI evidence includes the v0.1.0 release builds for R22–R26 and the R22/R26/R27 CI builds.
Local build evidence includes `Release.R26` and `Release.R27`, plus the Revit 2024 build through `install.ps1 -Source Build`.

| Revit year | Build in CI | Local build | Live reads | Live actions | Install script |
| --- | --- | --- | --- | --- | --- |
| 2020 | — | ✅ | ✅ | ✅ | — |
| 2022 | ✅ | — | — | — | — |
| 2023 | ✅ | — | — | — | — |
| 2024 | ✅ | ✅ | — | — | ✅ |
| 2025 | ✅ | — | — | — | — |
| 2026 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2027 | ✅ | ✅ | — | — | — |

Live checks use Revit 2026.4 with Autodesk's `Snowdon Towers Sample Architectural.rvt`, called from macOS over the SSH transport.
All 18 read tools, including the four coordinator tools, are live-validated.
Live action checks cover `select`, `show`, `isolate`, `move`, `create_wall`, `set_parameter`, `delete` and `batch`, with dry runs and real writes for actions that support them.
Installer checks cover `-Source Build` for 2024 and 2026 with `-SignThumbprint`, `-Source Release` for 2024 from v0.1.0, and `-Uninstall`.
Revit 2022–2025 and 2027 have build evidence only for add-in behavior; no live reads or actions are validated on those years in this validation pass.

The Revit 2020 checks ran on 2026-09-28 against Revit 2020 (20.0.0.377) with `E:\revitmcp-test\MEP文件.rvt` on a Windows workstation, called from Linux over the add-in HTTP channel.
All 18 read tools are live-validated, including `revit_export_view` and all four coordinator tools.
All 12 action tools ran on that year: `select`, `show` and `isolate` ran for real, and `move`, `place_family`, `create_wall`, `create_floor`, `set_parameter`, `delete`, `set_phase`, `merge_phases` and `batch` were checked with `dry_run` and returned `verification`.
`revit_create_floor` exercised the Revit 2020 `Document.Create.NewFloor` path, and `revit_set_phase` exercised the phase-order check that Revit only exposes from 2022.
The R20 build step in PR CI was added in the same change and has not run yet, which is why its CI cell stays unmarked.
Screenshots and JSON evidence are on the [`validation-assets` branch](https://github.com/sharafutdinovdi/revit-model-mcp/tree/validation-assets).
The Revit undo menu label for a batch (`revit_batch`) cannot be verified through the API.
