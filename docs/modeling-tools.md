# 建模工具规格：首批

本页是 wayfinder 地图[建筑/结构基础建模工具：首批规格地图](https://github.com/vibe-bimer/revit-model-mcp/issues/8)的交付物。

!!! warning "这是规格，不是已实现功能"
    本页描述的工具**尚未实现**。它把首批 7 个工具的契约、2020/2026 API 落法与验证方式定死，供实现票直接照做。实现进度以 [CHANGELOG](changelog.md) 与[验证证据](validation.md)为准。

<a id="scope"></a>
## 范围与批次

| 批次 | 内容 |
| --- | --- |
| **首批（本页）** | `create_level`、`create_grid`、`load_family_file`、`place_hosted_family`、`create_column`、`create_beam`、`copy_elements` |
| 第二批 | 房间、构件类型复制、开洞、材质、墙连接 |
| 第三批 | 屋顶、楼梯、栏杆、幕墙、标注、视图与图纸；天花只做 2026 |

目标是「从项目模板出发，建起一层可用的建筑/结构骨架」。结构专业**只做几何构件**，不碰结构分析模型、荷载、边界条件与钢筋。

<a id="conventions"></a>
## 通用约定

这些沿用仓库现状，不是新决定：

- 长度单位为毫米，模型坐标为 XY；长度参数以 mm 进出。
- 标高与类型按**名称精确解析**；`type_name`、`wall_type` 这类参数是**可传 `null` 的必填参数**。
- 每个动作都接受通用参数 `document=null`，并支持 `dry_run=false`；试运行执行后回滚，返回同形 `verification`。
- 创建类动作的成功响应含 `verification.after = { id, category, family, type, level, boundingBoxMinMm, boundingBoxMaxMm }`，试运行时追加 `wouldCreate: true`。
- 所有首批工具都可进入 `revit_run_actions`（单次撤销、最多 50 步）。
- 只读门禁（机器策略 `ReadOnly`、工作站 `read-only` 文件、`REVIT_MCP_READ_ONLY=1`）与「动作不得保存模型」不因新工具放宽；旧的两道 `allow-write` 门禁已随 1.0 底座移除。

<a id="batch-one"></a>
## 首批工具

<a id="create-level"></a>
### `revit_create_level`

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `name` | 是 | — | `string` | 标高名称 |
| `elevation_mm` | 是 | — | `number` | 高程（mm） |
| `create_view` | 否 | `false` | `boolean` | 同时创建对应的楼层平面视图 |

- 创建：`Level.Create(Document, 高程)`。
- **重名即拒绝**，错误里给出已有标高的名称与高程。判定口径与仓库现有 `FindLevel` 一致：`BuiltInParameter.DATUM_TEXT` 精确匹配。
- `create_view=true` 时用 `ViewPlan.Create`，视图类型**按 `ViewFamilyType.ViewFamily == ViewFamily.FloorPlan` 解析，不按名字**——模板里的视图类型名在 2020/2026 语料中都查不到，按名字找必然脆。
- 改名、改高程、按间距复制到上层**不属于首批**。

<a id="create-grid"></a>
### `revit_create_grid`

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `label` | 是 | — | `string` | 轴号 |
| `start_mm` / `end_mm` | 是 | — | `array<number>` | 起点、终点 `[x, y]` |
| `mid_mm` | 否 | `null` | `array<number>` | 给定时按三点定弧，走 `Grid.Create(Document, Arc)` |

- 直线走 `Grid.Create(Document, Line)`；曲线必须落在水平面上，否则拒绝并说明原因。输入只有 `[x, y]`，Z 恒为 0，因此「非水平面」在实现里表现为共线三点（定不出弧）与重合端点，两者都在 `Validate` 里拒绝并说明原因。
- 轴号写入 `Grid.Name`；重名即拒绝。
- **不暴露范围与标头**：那些 API 都在 `DatumPlane` 上，分 `Model` / `ViewSpecific` 两种语义且需要指定视图，属于第二批。

<a id="load-family"></a>
### `revit_load_family_file`

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `path` | 是 | — | `string` | **Revit 工作站**上的族文件绝对路径 |
| `type_name` | 否 | `null` | `string` | 只载入该类型（`LoadFamilySymbol`）；为空时载入整族（`LoadFamily`） |
| `overwrite_parameters` | 否 | `false` | `boolean` | 是否用族里的值覆盖项目已有类型的参数值 |

- **名字的由来**：底座自带的 `revit_load_family` 收的是 `paths` 列表、一次载入多个族文件，语义是批量；本节定的是单文件、可只取一个类型，所以落成独立命令 `load-family-file`，两者并存而不是互相顶掉。
- **总是**传入 `IFamilyLoadOptions`，且 `OnFamilyFound` 与 `OnSharedFamilyFound` 两个回调都实现。不传时 Revit 会用默认处理器并弹出**模态对话框**，无人值守必然卡死——这是本工具必须接受该接口的唯一理由。
- 默认语义：继续载入，但**不覆盖**既有参数值；同名族已存在时复用项目里的版本。
- 响应在 `fork` 块回报 `state: "new" | "existing"`、`familyName` 与 `familyTypes: [{ id, name }]`（fork 自己的结果块，见 adr/0005）。
- `path` 不存在时拒绝，并列出同目录下最接近的三个文件名；路径规则与上游文件动作一致（绝对路径、不许穿越、不接云端路径）。

<a id="place-hosted-family"></a>
### `revit_place_hosted_family`

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `family` / `type_name` | 是 / 否 | — / `null` | `string / null` | 已载入的族与类型 |
| `x_mm` / `y_mm` | 是 | — | `number` | 放置定位点 |
| `host_element_id` | 否 | `null` | `integer` | 显式宿主（墙）ID |
| `host_search_radius_mm` | 否 | `2000` | `number` | 未给宿主时的就近搜索半径 |
| `level` | 否 | `null` | `string / null` | 放置标高；为空时取最近标高 |
| `rotation_deg` | 否 | `0` | `number` | 必须为 `0`：宿主族的方向由宿主墙决定，要翻面用 `flip_facing` |
| `sill_height_mm` | 否 | `null` | `number` | 窗台高（`INSTANCE_SILL_HEIGHT_PARAM`） |
| `flip_facing` | 否 | `null` | `boolean` | 需要时调用 `flipFacing()` |

宿主解析有两条路：

1. **显式 `host_element_id`**：校验构件存在、是 `Wall`，且符号的 `Family.FamilyPlacementType == OneLevelBasedHosted`。Revit 自己不校验宿主，失败也没有文档化的异常类型，这一层必须由工具做。
2. **就近找墙**：候选只有**放置标高这一层**的墙——标高由 `level` 给出，为空时取定位点高程最近者；墙的层高区间按 `WALL_BASE_CONSTRAINT` 与 `WALL_HEIGHT_TYPE`（未连接高度时用自身高度）判定。每层各画一遍墙的模型里，上下层墙在平面上完全重合，不先按层筛掉就永远并列，所以标高先于宿主解析。把定位点投影到候选墙的定位线上，取水平距离最小者；要求距离不超过 `host_search_radius_mm`，且投影参数落在 0..1（点确实落在这段墙上）。**找不到、超出半径、或同层最近距离并列**，一律拒绝并列出候选 `{ id, distanceMm }`，让调用者显式指定；半径先判、并列后判，因为一次落在半径外的搜索不该报并列。

响应回报 `hostResolution: { mode: "explicit" | "nearest", hostId, distanceMm }`，因此试运行也能看清它会挂到哪面墙上。

宿主族的方向、手向都由宿主墙决定，`rotation_deg` 因此只接受 `0`——转一个宿主实例在 API 里要么被忽略、要么变成沿着墙移动，所以非零角度会被拒绝并说明改用 `flip_facing`。

现有的 `revit_place_family`（非宿主、基于标高）**保留原名不动**，两者并存。

<a id="create-column"></a>
### `revit_create_column`

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `family` / `type_name` | 是 / 否 | — / `null` | `string / null` | 已载入的结构柱族与类型 |
| `level` | 是 | — | `string` | 底部标高 |
| `x_mm` / `y_mm` | 是 | — | `number` | 定位点 |
| `top_level` | 否 | `null` | `string / null` | 顶部标高 |
| `height_mm` | 否 | `null` | `number` | 未给 `top_level` 时按高度推算（默认 3000） |
| `base_offset_mm` / `top_offset_mm` | 否 | `0` | `number` | 顶底偏移 |
| `rotation_deg` | 否 | `0` | `number` | 绕 Z 轴旋转 |

- 创建：`document.Create.NewFamilyInstance(point, symbol, level, StructuralType.Column)`。这一处在两个年份只有**声明类型**不同（2020 在 `Creation.Document`，2026 在 `ItemFactoryBase`），`document.Create.*` 的调用点两边都编译，**不需要 `#if`**。
- 顶底标高由工具**内部直接写** `FAMILY_BASE_LEVEL_PARAM` / `FAMILY_TOP_LEVEL_PARAM` 与两个偏移参数。这些是 ElementId 值，而现有的 `revit_set_parameter` 明确拒绝 ElementId 参数，所以只能在这里设。
- **不做附着**：`ColumnAttachment` 的合法目标是楼板、屋顶、天花、梁、支撑——**标高不是合法目标**，「附着到顶标高」在 API 上不成立。
- 实现口径：柱顶不另设「高度」参数——不给 `top_level` 时顶部标高仍写底部标高，顶部偏移写 `base_offset_mm + height_mm`，于是柱顶高程等于「底部标高 + 底部偏移 + 高度」。旋转走 `LocationPoint.Rotate`，轴是一条穿过放置点的竖直线（`Line.CreateBound`），因为该方法收的是 `Line` 而不是向量。`verification.after` 报 id、类别、族、类型、底部标高与包围盒。

<a id="create-beam"></a>
### `revit_create_beam`

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `family` / `type_name` | 是 / 否 | — / `null` | `string / null` | 已载入的结构框架族与类型 |
| `level` | 是 | — | `string` | 参照标高 |
| `start_mm` / `end_mm` | 是 | — | `array<number>` | 轴线两端 `[x, y]` |
| `structural_usage` | 否 | `null` | `string / null` | 结构用途，写入 `FamilyInstance.StructuralUsage` |
| `z_offset_mm` | 否 | `0` | `number` | 垂直偏移 |

- 走「曲线 + 标高」路线：`NewFamilyInstance(Curve, FamilySymbol, Level, StructuralType.Beam)`，两个年份都在，直接给轴线与参照标高。
- **不用工作平面路线**：`NewFamilyInstance(Reference, Line, FamilySymbol)` 需要一个面引用，MCP 调用者拿不到。
- **端点不做吸附**：Revit 没有程序化吸附 API，`StructuralFramingUtils.SetEndReference` 只对已经连接的端有效。坐标由调用者给。
- `z_offset_mm` 落在 **`STRUCTURAL_BEAM_END0_ELEVATION` / `END1_ELEVATION`（起点/终点标高偏移）**：2026 真机上把两者写成同一个值，梁的包围盒从 `z=-600..0` 抬到 `0..600`，读回报出 `zOffsetParam:"起点标高偏移"`。
- **`INSTANCE_ELEVATION_PARAM`（显示名「相对标高的偏移」）在这个族上是空壳**：写入成功、读回一致，包围盒与轴线都不动，参数表里也看不到这个值。
- 因此判「写进去了」只看包围盒是否按偏移抬升（容差 1e-6 英尺），不看参数读回；参数不抬升就还原原值、换下一组，两组都不抬升时 `ElementTransformUtils.MoveElement` 移动构件，移动也不抬升就抛错——`z_offset_mm` 没落上的梁不允许当成放置在标高上。

<a id="copy-elements"></a>
### `revit_copy_elements`

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `element_ids` | 是 | — | `array<integer>` | 要复制的构件 |
| `target_level` | 否 | `null` | `string / null` | 目标标高；给了就按标高差求 `dz` |
| `dz_mm` / `dx_mm` / `dy_mm` | 否 | `0` | `number` | 直接给偏移 |
| `dry_run` | 否 | `false` | `boolean` | 试运行 |

- 走**唯一会重宿主**的那条重载：`ElementTransformUtils.CopyElements(Document, ids, Document, Transform, CopyPasteOptions)`。`(Document, ids, XYZ)` 那条的文档明确写着「不做重宿主」，用它会把门窗从宿主上摘下来。
- **必须**设置 `CopyPasteOptions.SetDuplicateTypeNamesHandler(...)`（是方法，不是属性）。不设时 Revit 会弹模态对话框问「只复制新类型还是取消」，无人值守直接卡死；默认返回 `DuplicateTypeAction.UseDestinationTypes`。
- 跨标高时 `Transform` 取纯平移；没有哪个重载接受「目标标高」参数，标高差必须由调用者算。
- **宿主族构件的宿主必须在 `element_ids` 里**，否则整批拒绝并点名。Revit 文档化的后果是「找不到新宿主时该构件会在粘贴完成时被删除」——静默丢构件比拒绝更糟。
- **失败粒度是逐构件报告**：复制不销毁任何东西，没必要像 `revit_reset_element_ids` 那样整批拒绝。每个构件给 `old → new` 或失败原因。
- `CopyElements` 只返回新 ID 集合，**不保证顺序、不给映射**。按「类别 + 类型 + 位置」校验配对，无法精确配对时明确标 `idMappingVerified: false`。

<a id="verification"></a>
## 验证矩阵与完成定义

每个首批工具在 **2020 与 2026 两个年份**各跑三条用例：

1. 成功路径（真实写入，核对 `verification.after`）。
2. `dry_run` 回滚（返回同形 `verification` 且 `wouldCreate: true`）。
3. 一条错误路径（标高重名、宿主非法、族文件不存在）。

外加两条全局断言：`dry_run` 之后 `revit_document_info.isModified` 必须仍为 `false`（证明回滚真的发生）；真实写入之后，测试模型**文件**的 mtime 必须不变——动作不保存模型，所以文档在内存里会变脏（`isModified=true`），这是正常的，不是失败。

| 年份 | 测试模型 |
| --- | --- |
| 2020 | `E:\revitmcp-test\建筑结构.rvt` |
| 2026 | `E:\revitmcp-test\mcp-verify-2026.rvt`（由该模型升级另存而来，保留 52 个视图） |

**完成定义**：首批 7 个工具在两年份都真机实测通过才算完成——这是**批次门槛**，不是每个 PR 的门槛。证据按仓库既有约定落[验证证据](validation.md)与 `validation-assets` 分支；某工具在 2026 过不了，就记已知限制并在[版本支持矩阵](features/matrix.md)标「仅构建」，不允许用构建通过冒充完成。

<a id="later-batches"></a>
## 第二、三批

- **第二批**：房间 → 构件类型复制（含复合结构改层）→ 开洞 → 材质 → 墙连接。
- **第三批**：屋顶 → 楼梯 → 栏杆 → 幕墙 → 标注 → 视图与图纸。

这两批的 API 入口在 2020 与 2026 **完全一致**，不需要年份分叉。

<a id="known-limits"></a>
## 已确定的事实与限制

下面这些已经查清，不必再查一遍：

- **Revit 2020 没有天花创建路径**：已安装的 `RevitAPI.dll`（20.0.0.377）里 `Ceiling` 类的公开声明成员为 0，全汇编没有任何返回 `Ceiling` 的方法、也没有接受 `CeilingType` 的方法；`Ceiling.Create` 直到 2026 才出现。2020 侧只能**读取**天花、或复制一个已存在的天花。
- **墙的「附着到楼板 / 顶部」在两个年份都没有 API 入口**，只有 `WALL_TOP_IS_ATTACHED` / `WALL_BOTTOM_IS_ATTACHED` 参数。
- **没有程序化吸附 API**；`ObjectSnapTypes` 只服务交互式拾取。
- **`revit_set_parameter` 拒绝 ElementId 参数**，所以标高类参数的写入必须由专门工具内部完成。
- **`Room.IsEnclosed` 在两个年份都不存在**；房间封闭性只能用 `Room.IsPointInRoom` / `ClosedShell` 判断。
- **2026 工作站的族库不完整**：`RVT 2026\Libraries` 只有 446 个 `.rfa`（结构预制与路径分析），没有门窗柱梁；`RVT 2020\Libraries` 有 4,514 个，中文库门窗柱梁齐全。在 2026 上验证 `load_family_file` 要用 2020 库的族文件（族向后兼容）或模型里已载入的族。
- **`CloseMainWindow()` 在该工作站上对 Revit 2020 与 2026 都不生效**；强杀前必须先确认 `isModified=false`，之后再清掉 `%LOCALAPPDATA%\RevitModelMcp\instance_*.json` 心跳。
- **「仅几何构件」的边界**：语料既不能证实也不能证伪 Revit 会不会在建结构构件时顺带生成分析构件。契约只保证这些工具不调用任何分析 API；是否产生分析构件由项目设置决定，验证时把 `IsStructuralAnalysisEnabled` 当作环境事实记录。
