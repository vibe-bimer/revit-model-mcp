# 验证证据

以下为截至 2026-10-02 的验证状态；✅ 表示检查已完成，— 表示没有该项检查的验证证据。
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
真机动作检查覆盖 16 个动作中的 9 个：`select`、`show`、`isolate`、`move`、`create_wall`、`create_level`、`set_parameter`、`delete` 和 `batch`；支持试运行的动作同时检查了试运行与真实写入。`revit_reset_element_ids` 和 `revit_rebuild_model_ids` 仅在 2020 上验证。
安装器检查覆盖：2024 和 2026 上带 `-SignThumbprint` 的 `-Source Build`、2024 上从 v0.1.0 安装的 `-Source Release`，以及 `-Uninstall`。
在这一轮验证中，Revit 2022–2025 和 2027 的插件行为只有构建证据，没有这些年份的真机读取或动作验证。

Revit 2020 检查于 2026-09-28 和 2026-09-29 进行，使用 Windows 工作站上的 Revit 2020（20.0.0.377）、`E:\revitmcp-test\MEP文件.rvt` 和 `E:\revitmcp-test\建筑结构.rvt`，由 Linux 通过插件 HTTP 通道调用。
全部 19 个读取工具均已真机验证，包括 `revit_export_view`、`revit_export_element_ids` 和全部四个协调工具。
全部 16 个动作工具都在该年份验证过：`select`、`show` 和 `isolate` 真实执行；`move`、`place_family`、`create_wall`、`create_floor`、`create_level`、`set_parameter`、`delete`、`set_phase`、`merge_phases`、`set_view_lighting`、`batch`、`reset_element_ids` 和 `rebuild_model_ids` 使用 `dry_run` 检查，并返回了 `verification`。
`revit_create_floor` 覆盖了 Revit 2020 的 `Document.Create.NewFloor` 路径；`revit_set_phase` 覆盖了阶段顺序检查的兼容路径，而对应检查 API 直到 Revit 2022 才公开。
`revit_export_element_ids` 为 `MEP文件.rvt` 的构件写出了工作簿，冻结表头、自动筛选，以及类别 → 族 → 类型的排序均保持完整。
`revit_reset_element_ids` 重置了 `MEP文件.rvt` 中 27 个未连接构件的 ID，清单保持不变；其系统保护检查将所有管道、风管和已连接附件排除在执行范围外。
`revit_rebuild_model_ids` 将 `建筑结构.rvt` 中 899 个可选构件复制到新模型，源模型保持不变；新模型打开时没有提示框，其三维视图包含 900 个构件，并保留源模型的墙和标高类型。
在 0.9.0 构建上，单个任务用 165 s 写出该模型的十份副本（每份 16.5 s）：每份包含 899 个构件，`idMappingVerified=true`，没有任何 ID 出现在两份副本中，ID 区间为 2473–4256、19259–21042、……、44771–46554。
截图和 JSON 证据位于 [`validation-assets` 分支](https://github.com/vibe-bimer/revit-model-mcp/tree/validation-assets)。
Revit 批处理（`revit_run_actions`）在撤销菜单中的标签无法通过 API 验证。

`revit_create_level`（首批建模工具的第一个，2026-10-02）在 2020 与 2026 两个年份都完成了真机验收，使用 `建筑结构.rvt` 与由它升级另存而来的 `mcp-verify-2026.rvt`。
两个年份上：`dry_run` 回滚后 `isModified` 仍为 `false`；真实写入建出标高并回报 `verification.after = { id, category: "标高", name, elevationMm }`；同名标高被拒绝并回报 `Level '1F' already exists at 0 mm.`；`create_view=true` 使视图数从 52 增到 53。
两个年份的真实写入之后，模型文件的大小与 mtime 都没有变化——动作没有保存模型。

`revit_create_grid`（2026-11-02）在 Revit 2026 上完成了真机验收，使用 `mcp-verify-2026.rvt`，由 Linux 经 SSH 通道调用；2020 没有对应验收——这一版尚未在 2020 真机上跑过；R20 构建配置已于 2026-11-03 加回并通过构建，2020 的整体状态见下文「Revit 2020 适配与 2020 真机验收」。
在干净模型上 `dry_run` 回滚后 `isModified` 仍为 `false`，回报 `verification.after = { id, category: "轴网", fork: { name } }` 与 `wouldCreate: true`；真实写入建出轴网并留下一条撤销记录 `MCP (mcp): Created a grid in mcp-verify-2026`；同名轴号被拒绝并回报 `Grid 'MCP-VERIFY-GRID' already exists.`；`mid_mm` 三点建出弧轴网；共线三点回报 `start_mm, mid_mm and end_mm must not be collinear: an arc needs a mid point off the start-end line.`；两端点重合回报 `start_mm and end_mm must not be the same point.`。
轴网是基准面，模型里没有包围盒，所以 `verification.after` 用 `fork.name` 标识建出的轴号，而不是 `boundingBoxMinMm`／`boundingBoxMaxMm`。
全部写入之后，模型文件的大小（19,918,848 字节）与 mtime（2026-10-02T12:08:34）都没有变化——动作没有保存模型。

`revit_load_family_file`（2026-11-02）在 Revit 2026 上用 2020 中文库的 `入口门厅.rfa` 完成了真机验收，模型与通道同上。
`dry_run` 回滚后回报 `fork = { state: "new", familyName: "入口门厅", familyTypes: [{ id, name: "3200 x 3000mm" }] }` 与 `wouldCreate: true`；真实写入载入整族并留下撤销记录；同一文件再载入一次回报 `state: "existing"`、`committed: false`，摘要是 `It changed nothing, so no undo entry was kept.`，既没有重复载入，也没有覆盖模型里已有的参数值；路径写错时回报 `Family file '…\入口门.rfa' was not found. Closest: 入口门厅.rfa.`；`type_name` 不在族里时回报 `Type 'NO-SUCH-TYPE' is not in family '入口门厅'. Available types: 3200 x 3000mm.`。
同样，全部写入之后模型文件的大小与 mtime 都没有变化。

`revit_create_column`（2026-11-02）在 Revit 2026 上完成了真机验收，模型与通道同上，柱族用 2020 中文库的 `混凝土 - 正方形 - 柱.rfa`（四个类型 `300 x 300mm`…`750 x 750mm`），先由 `revit_load_family_file` 载入；2020 同样没有验收：这一版没在 2020 真机上跑过，原因不是构建不支持（R20 现已可构建），见下文「Revit 2020 适配与 2020 真机验收」。
只给底标高与 `height_mm`：`dry_run` 回报 `rolledBack: true`、`wouldCreate: true` 与 `verification.after = { id, category: "结构柱", level: "1F", type: "300 x 300mm", boundingBoxMinMm: [11850, -150, 0], boundingBoxMaxMm: [12150, 150, 3000] }`，回滚后该 id 用 `revit_element_details` 查不到；真实写入建出柱子（`id 364295`），读回 `底部标高 = 1F`、`顶部标高 = 1F`、`顶部偏移 = 3000 mm`，即柱顶高程等于底部标高加底部偏移加高度。
给 `top_level`：`top_level = "3F"` 的柱子包围盒高度到 7600 mm，与 3F 的标高一致；给 `base_offset_mm = 500`、`rotation_deg = 45` 的 `600 x 600mm` 柱子包围盒为 `[-424.3, 5575.7, 4300]`–`[424.3, 6424.3, 7300]`，偏移与旋转都落到了模型里。
`type_name` 不存在时回报 `Type 'NO-SUCH-TYPE' was not found in family '混凝土 - 正方形 - 柱'. Available types: 300 x 300mm, 450 x 450mm, 600 x 600mm, 750 x 750mm.`；族不存在时回报 `Family 'NO-SUCH-FAMILY' was not found. Use revit_load_family_file to load it first.`。
全部写入之后，模型文件的大小（19,918,848 字节）与 mtime（2026-10-02T12:08:34）都没有变化——动作没有保存模型。

`revit_place_hosted_family`（2026-11-03）在 Revit 2026 上完成了真机验收，模型与通道同上，门族用 2020 中文库的 `入口门厅.rfa`（唯一类型 `3200 x 3000mm`），先由 `revit_load_family_file` 载入；2020 的真机验收见下文「Revit 2020 适配与 2020 真机验收（2026-11-03）」，那一轮把这些用例逐条重跑了一遍。
显式宿主：指定 `host_element_id = 357458`、`level = "1F"`、定位点 `(0, -70040)`，`dry_run` 回报 `rolledBack: true`、`wouldCreate: true`、`fork.hostResolution = { mode: "explicit", hostId: 357458, distanceMm: 0.1 }` 与 `verification.after = { id: 364860, category: "门", level: "1F", type: "3200 x 3000mm", boundingBoxMinMm: [-2330, -71970.1, 0], boundingBoxMaxMm: [2330, -66120.1, 5660] }`，回滚后该 id 用 `revit_element_details` 查不到；这一轮唯一的撤销记录属于族载入，撤掉它之后 `isModified` 回到 `false`，说明试运行没有留下任何东西。真实写入建出门（`id 364862`），读回 `主体 ID = 357458`、`标高 = 1F`、位置 `(0, -70040.1, 0)`，即确实挂在那面墙上，并留下一条撤销记录 `MCP (acceptance): Placed a hosted family in mcp-verify-2026`。
就近宿主：不给宿主、只给 `(0, -69540)`，`fork.hostResolution` 回报 `{ mode: "nearest", hostId: 357458, distanceMm: 500.1 }`，标高自动解析为 `1F`；把 `level` 改成 `"2F"` 后回报 `hostId: 357896`，即换到了 2F 那一层的墙，包围盒也随之抬到 `[-2330, -71970.1, 3800]`–`[2330, -66120.1, 9460]`。
`sill_height_mm = 500` 让包围盒从 `[-2330, -71970.1, 0]`–`[2330, -66120.1, 5660]` 抬成 `[-2330, -71970.1, 500]`–`[2330, -66120.1, 6160]`；`flip_facing = true` 把门窗翻到墙的另一侧，包围盒从 `[-2330, -71970.1, 0]`–`[2330, -66120.1, 5660]` 变成 `[-2330, -73960.1, 0]`–`[2330, -68110, 5660]`。
拒绝路径：半径内没有墙时回报 `No wall within hostSearchRadiusMm 1. Nearest: 357458 at 500.1 mm, 357484 at 12800.1 mm, 357593 at 15200.1 mm.`；同一层两面墙等距时回报 `Walls 357503 at 1000 mm, 357458 at 1000 mm are equally far from the placement point. Name one with hostElementId.`（并列按 0.1 mm 判定，即模型画图精度；比较用的是原始距离，毫米只用于展示；定位点 `(3211.6, -71040.1)` 与对称点 `(5211.6, -71040.1)` 都能稳定触发，两个点的候选顺序相反）；宿主不是墙时回报 `Host element 357428 is a 标高, not a wall. A hosted family needs a wall.`；族不是单层宿主族时回报 `Family '标记_门' is ViewBased based, not one-level hosted. This tool places doors, windows and similar families that need a host wall; use revit_place_family for a level-based family.`；`type_name` 不存在时回报 `Type '9999 x 9999mm' was not found in family '入口门厅'. Available types: 3200 x 3000mm.`；`rotation_deg = 90` 回报 `A one-level hosted family takes its orientation from its host wall, so rotation_deg must be 0; use flip_facing to turn the family around.`；定位点落在墙端之外、整层没有一面墙的垂足真正落在墙上时回报 `The document has no wall on level '1F' to host the family.`（定位点 `(30000, -70040)`、半径 20000，点在建筑之外）
斜墙补验（修掉宿主判定里的提前取整后）：用 revit_create_wall 真实写入一面 3-4-5 斜墙 (10000, 10000)–(13000, 14000)（不保存模型），定位点取垂足外 10.001 mm 处 (11491.9992, 12006.0006)、半径 500，dry_run 回报 { mode: "nearest", hostId: 364860, distanceMm: 10 }，包围盒随墙斜向 [6966, 8978, 0]–[14442, 16216, 5660]；同一位置半径 10 时如实拒绝 No wall within hostSearchRadiusMm 10. Nearest: 364860 at 10 mm, 357458 at 82046.1 mm, 357492 at 94346.1 mm, 357589 at 96746.1 mm.——真实距离 10.001 mm 在半径之外。几何判定用英尺原值完成，毫米只在回报与层高边界换算；取整提前进判定的版本会把这个垂足当非直角丢掉。
干净模型补验（直接断言，不再借用撤销族载入）：验收模型里本来就带 65 个门、129 个窗实例（族 `平开门-木门-双扇`，类型 `M1527`/`M1227`），所以不用先载族就能走完整放置路径。会话开始时 `activeDocument.isModified` 为 `false`；两次 `dry_run` 之后仍是 `false`。显式宿主：定位点 `(5000, -70040.1)`、`host_element_id = 357458`、`type_name = "M1527"`，回报 `fork.hostResolution = { mode: "explicit", hostId: 357458, distanceMm: 0 }`、`rolledBack: true`、`verification.after = { id: 363381, category: "门", level: "1F", type: "M1527", boundingBoxMinMm: [4250, -70855.1, 0], boundingBoxMaxMm: [5750, -69725.1, 2700] }`。就近宿主：定位点 `(8000, -69540.1)`、`type_name = "M1227"`，回报 `{ mode: "nearest", hostId: 357458, distanceMm: 500 }`、`id 363382`、包围盒 `[7400, -70705.1, 0]`–`[8600, -69725.1, 2700]`。两个被回滚掉的 id 用 `revit_element_details` 分别回报 `Element with id 363381 was not found.` 与 `Element with id 363382 was not found.`，模型文件仍为 19,918,848 字节、mtime `2026-10-02T12:08:34`。

模型里每层各画一遍墙、平面上完全重合，所以就近查找只在放置标高的层里挑候选，否则上下层的墙距离相同，永远判成并列。
全部写入之后，模型文件的大小（19,918,848 字节）与 mtime（2026-10-02T12:08:34）都没有变化——动作没有保存模型。

Revit 2020 适配与 2020 真机验收（2026-11-03）。本树原先只有 R22–R27 构建配置，2020 既不能构建也没有验收。现在 `src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj:18-19` 的 `Configurations` 含 `Debug.R20` 与 `Release.R20`，`src/RevitModelMcp.Core/RevitModelMcp.Core.csproj` 的目标框架为 `net47;net48;net8.0`；Debug.R20 与 R22–R27 共七个配置全部构建通过，Release.R20 也通过（114 条警告、0 错误，警告来自 net47 的 ILRepack 合并）。
条件编译改用 csproj 在求值期定义的 `REVIT2020_BUILD`，不再用 SDK 在 target 阶段注入的 `REVIT2021_OR_GREATER`：WPF 的 `_wpftmp` 临时工程收不到 target 期常量，2020 的兼容层会被编进 2021 及以上的构建。全部 13 处 `#if`（分布在 10 个文件里）都换成了它。
`src/RevitModelMcp.Addin/Fork/ForkUnitTypes.cs` 与 `src/RevitModelMcp.Addin/Fork/ForkLegacyApi.cs` 在 2020 下补齐 2021 的公开面（`ForgeTypeId`、`UnitTypeId`、`SpecTypeId`、`GroupTypeId`、`UnitUtils.IsMeasurableSpec`、`View.GetIsFilterEnabled`、`IndependentTag.GetTaggedLocalElementIds`），调用点零改动；标识串的派生抽到 `src/RevitModelMcp.Core/Fork/UnitSpecNames.cs`，由 `UnitSpecNamesTests` 的 7 条测试脱离 Revit 验证。不可 shim 的走 `#if REVIT2020_BUILD`：PDF 导出在 2020 明确拒绝、图像加载状态留空、基点裁剪标志返回未知、拆除顺序校验交给 Revit、`Floor.Create` 改走 `Document.Create.NewFloor`、`ElementIdSetFilter` 换成 id 集合。
运行时差距：工作站装的是 Revit 2020 原始版 20.0.0.377，而 NuGet 只有 2020.2 的 API 包。用 MetadataLoadContext 比对 2020.2.90 参考程序集与真机 `RevitAPI.dll`，差出 50 条运行时缺失成员；本仓只用到 `BasePoint.GetProjectBasePoint(Document)` 与 `BasePoint.GetSurveyPoint(Document)` 两条，`revit_shared_coordinates` 因此在 2020.0 上抛 `找不到方法:“Autodesk.Revit.DB.BasePoint Autodesk.Revit.DB.BasePoint.GetProjectBasePoint(Autodesk.Revit.DB.Document)”。`。修法：`src/RevitModelMcp.Addin/Capture/SharedCoordinatesReader.cs` 在 2020 下用 `FilteredElementCollector` 收集 `BasePoint`，按 `IsShared` 区分——共享的那个是测量点，不共享的是项目基点；收不到一对应报错，不猜。
在 `建筑结构.rvt` 上取证：模型里只有两个基点，`id 96302` 的 `IsShared=True` 属 `OST_SharedBasePoint`（测量点），`id 96305` 的 `IsShared=False` 属 `OST_ProjectBasePoint`（项目基点）。把测量点移 −2 ft、项目基点移 +1 ft 后，`revit_shared_coordinates` 的 `projectBasePoint.eastWestMm` 由 `0` 变为 `914.4`，`surveyPoint.eastWestMm` 始终为 `0`；各自移回后读数归零。这一轮结束后 `isModified` 为 `true`（两次移动各留一条撤销记录），模型没有保存。
2020 上的放置用例（全部 `dry_run`，门族 `平开门-木门-双扇`，类型 `M1527`/`M1227`，模型本来就带这些实例，不需要载族）：显式宿主 `host_element_id = 357458`、定位点 `(5000, -70040.1)`、`M1527`，回报 `fork.hostResolution = { mode: "explicit", hostId: 357458, distanceMm: 0 }`、`rolledBack: true`、`verification.after = { id: 361713, category: "门", level: "1F", type: "M1527", boundingBoxMinMm: [4250, -70855.1, 0], boundingBoxMaxMm: [5750, -69725.1, 2700] }`；就近宿主 `(8000, -69540.1)`、`M1227` 回报 `{ mode: "nearest", hostId: 357458, distanceMm: 500 }`、`id 361714`、包围盒 `[7400, -70705.1, 0]`–`[8600, -69725.1, 2700]`；`level = "2F"` 时宿主变为 `357896`、包围盒 z 抬到 3800–6500；`sill_height_mm = 500` 把它抬到 500–3200；`flip_facing = true` 翻到 `[4250, -70355.1, 0]`–`[5750, -69225.1, 2700]`。
2020 上的拒绝路径逐字回报：半径 1 → `No wall within hostSearchRadiusMm 1. Nearest: 357458 at 500 mm, 358406 at 1430 mm, 358407 at 2230 mm, 358408 at 2890 mm, 358409 at 3550 mm.`；并列点 `(3211.6, -71040.1)` → `Walls 357458 at 1000 mm, 357503 at 1000 mm are equally far from the placement point. Name one with hostElementId.`，对称点 `(5211.6, -71040.1)` 的候选顺序相反；非墙宿主 357428 → `Host element 357428 is a 标高, not a wall. A hosted family needs a wall.`；`rotation_deg = 90` → `A one-level hosted family takes its orientation from its host wall, so rotation_deg must be 0; use flip_facing to turn the family around.`；半径外落空 `(30000, -70040.1)`、半径 20000 在这个模型里命中了另一面墙：`{ mode: "nearest", distanceMm: 4788.4 }`、`id 361719`、包围盒 `[24546.6, -70640.1, 0]`–`[25526.6, -69440.1, 2700]`，与 2026 的验收模型布局不同，所以「层里没有墙」那条拒绝在 2020 上由半径 1 的用例覆盖。
同一轮的 2020 表面：`revit_create_floor` 的四点轮廓加 `3F` 的 `dry_run` 回报 `rolledBack: true`，即 `Document.Create.NewFloor` 分支可用；`revit_links_status` 的 3 个 CAD 链接回报 `status: "NotFound"`，图像状态分支在 2020 下不报错；`revit_export` 的 PDF 回报 `PDF export needs Revit 2021 or later; this workstation runs Revit 2020. Use the dwg or ifc format.`；`revit_element_details` 正常读出 33 个参数，说明 `ForgeTypeId`/`UnitType` 兼容层在 2020 下生效。
全部用例都是 `dry_run`，模型文件始终 23,449,600 字节、mtime `2026-09-28 21:04:22`；这一轮会话里 `activeDocument.isModified` 为 `false`，关闭 Revit 前没有保存。2020 上尚未做真机验证的工具有 `revit_create_grid`、`revit_create_column`、`revit_load_family_file`、`revit_place_family`，它们只有构建证据，本页不写成已验证。

!!! note "历史记录，不是本次新增验证"
    本页保留英文原文的日期、构建与真机检查范围。翻译工作没有执行新的 Revit 验证，也不将构建通过等同于真机行为已验证。
