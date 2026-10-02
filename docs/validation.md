# 验证证据

以下为截至 2026-09-29 的验证状态；✅ 表示检查已完成，— 表示没有该项检查的验证证据。
CI 证据包括 v0.1.0 发布时的 R22–R26 构建，以及 R22 / R26 / R27 的 CI 构建。
本地构建证据包括 `Release.R26`、`Release.R27`，以及通过 `install.ps1 -Source Build` 完成的 Revit 2024 构建。

| Revit 年份 | CI 构建 | 本地构建 | 真机读取 | 真机动作 | 安装脚本 |
| --- | --- | --- | --- | --- | --- |
| 2020 | ✅ | ✅ | ✅ | ✅ | — |
| 2022 | ✅ | — | — | — | — |
| 2023 | ✅ | — | — | — | — |
| 2024 | ✅ | ✅ | — | — | ✅ |
| 2025 | ✅ | — | — | — | — |
| 2026 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2027 | ✅ | ✅ | — | — | — |

真机检查使用 Revit 2026.4 和 Autodesk 的 `Snowdon Towers Sample Architectural.rvt`，由 macOS 通过 SSH 传输调用。
19 个读取工具中有 18 个已经过真机验证，包括全部四个协调工具；`revit_export_element_ids` 仅在 2020 上验证。
真机动作检查覆盖 `select`、`show`、`isolate`、`move`、`create_wall`、`set_parameter`、`delete` 和 `batch`；支持试运行的动作同时检查了试运行与真实写入。`revit_reset_element_ids` 和 `revit_rebuild_model_ids` 仅在 2020 上验证。
安装器检查覆盖：2024 和 2026 上带 `-SignThumbprint` 的 `-Source Build`、2024 上从 v0.1.0 安装的 `-Source Release`，以及 `-Uninstall`。
在这一轮验证中，Revit 2022–2025 和 2027 的插件行为只有构建证据，没有这些年份的真机读取或动作验证。

Revit 2020 检查于 2026-09-28 和 2026-09-29 进行，使用 Windows 工作站上的 Revit 2020（20.0.0.377）、`E:\revitmcp-test\MEP文件.rvt` 和 `E:\revitmcp-test\建筑结构.rvt`，由 Linux 通过插件 HTTP 通道调用。
全部 19 个读取工具均已真机验证，包括 `revit_export_view`、`revit_export_element_ids` 和全部四个协调工具。
全部 14 个动作工具都在该年份执行过：`select`、`show` 和 `isolate` 真实执行；`move`、`place_family`、`create_wall`、`create_floor`、`set_parameter`、`delete`、`set_phase`、`merge_phases`、`batch`、`reset_element_ids` 和 `rebuild_model_ids` 使用 `dry_run` 检查，并返回了 `verification`。
`revit_create_floor` 覆盖了 Revit 2020 的 `Document.Create.NewFloor` 路径；`revit_set_phase` 覆盖了阶段顺序检查的兼容路径，而对应检查 API 直到 Revit 2022 才公开。
`revit_export_element_ids` 为 `MEP文件.rvt` 的构件写出了工作簿，冻结表头、自动筛选，以及类别 → 族 → 类型的排序均保持完整。
`revit_reset_element_ids` 重置了 `MEP文件.rvt` 中 27 个未连接构件的 ID，清单保持不变；其系统保护检查将所有管道、风管和已连接附件排除在执行范围外。
`revit_rebuild_model_ids` 将 `建筑结构.rvt` 中 899 个可选元素复制到新模型，源模型保持不变；新模型打开时没有提示框，其三维视图包含 900 个元素，并保留源模型的墙和标高类型。
在 0.9.0 构建上，单个任务用 165 s 写出该模型的十份副本（每份 16.5 s）：每份包含 899 个构件，`idMappingVerified=true`，没有任何 ID 出现在两份副本中，ID 区间为 2473–4256、19259–21042、……、44771–46554。
截图和 JSON 证据位于 [`validation-assets` 分支](https://github.com/sharafutdinovdi/revit-model-mcp/tree/validation-assets)。
Revit 批处理（`revit_batch`）在撤销菜单中的标签无法通过 API 验证。

`revit_create_level`（首批建模工具的第一个，2026-10-02）在 2020 与 2026 两个年份都完成了真机验收，使用 `建筑结构.rvt` 与由它升级另存而来的 `mcp-verify-2026.rvt`。
两个年份上：`dry_run` 回滚后 `isModified` 仍为 `false`；真实写入建出标高并回报 `verification.after = { id, category: "标高", name, elevationMm }`；同名标高被拒绝并回报 `Level '1F' already exists at 0 mm.`；`create_view=true` 使视图数从 52 增到 53。
两个年份的真实写入之后，模型文件的大小与 mtime 都没有变化——动作没有保存模型。

!!! note "历史记录，不是本次新增验证"
    本页保留英文原文的日期、构建与真机检查范围。翻译工作没有执行新的 Revit 验证，也不将构建通过等同于真机行为已验证。
