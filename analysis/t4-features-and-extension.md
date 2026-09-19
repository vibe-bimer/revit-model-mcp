# t4 功能盘点与扩展能力分析（features-analyst）

分析对象：`/home/roky/revit-mcp`，HEAD `dacdafd`（2026-09-18），包版本 `server/pyproject.toml:7 = 0.5.0`
证据规则：每条结论标注 `文件:行`。凡属推断均显式写「推断」。

---

## 1. 结论摘要

1. 项目对外暴露 **两套 MCP 工具集**：默认 **18 个只读工具**（`server/tests/test_server.py:18-37` 的 `EXPECTED_TOOLS`）与可选 **9 个写入/交互工具**（`server/tests/test_actions.py:17-27` 的 `ACTION_TOOLS`），合计 27 个。只读工具在未启用写入时始终注册；写入工具只有 `REVIT_MCP_ALLOW_WRITE=1` 时才会出现在 `list_tools` 中（`server/revit_model_mcp/actions.py:121-123`）。
2. 写入由**双重门**控制：Python 进程环境变量 + Revit 工作站上的 `%LOCALAPPDATA%\RevitModelMcp\allow-write` 文件；HTTP 路径下缺门直接返回 403（`src/.../Control/ActionCommandExecutor.cs:17,35,158`；`src/.../Control/HttpChannel.cs:254`）。
3. 只读能力覆盖：连接探活、文档元数据、目录发现、通用元素查询/聚合、视图列表/摘要/元素/告警/PNG 导出、元素详情（含几何）、模型级质量巡检（health/links/shared coordinates/parameter fill）、关系查询、实例发现。**不含**：保存、同步/工作共享、创建或修改视图/图纸、载入族、创建参数定义、DWG/IFC 导入导出、房间/面积创建、明细表编辑、撤销/重做。
4. 写入能力覆盖：选择/显示/隔离、移动、放置族、建墙、设置参数、删除，以及 `revit_batch`（≤50 步、单个撤销项 `revit_batch`、首个失败全批回滚、解析期全量校验）；5 个变更类工具支持 `dry_run`（执行后回滚并返回同一 `verification` 结构）。
5. 扩展点清晰且分层：**新增只读工具**要同时改 Python（job 构造+工具注册）、Core（命令枚举/解析/响应模型/序列化）、Addin（读者+分发）、文档与测试；**新增写入工具**还要同步 `ACTION_COMMANDS`、批处理字段表、`ActionJobParser`、`ActionCommandExecutor`、`ActionMutations`、`ActionVerifier`；**新增传输**只需在 Python 侧实现 `RemoteHost` 协议（5 个方法）与 `list_revit_instances`，在插件侧复用 `ControlChannel.TrySubmit` 单任务约束；**新增 Revit 版本**已有现成的条件编译机制 `REVIT20XX_OR_GREATER`（11 处使用）。
6. 发现三处**文档与代码不同步**（roadmap/architecture 的「已知缺口」已被 HEAD 修复），以及一处**安装脚本硬编码版本白名单会拒绝 2020**（`install.ps1:172`），对迁移评估有直接影响，详见 §6。

---

## 2. 只读工具清单（18）

公共参数：除 `revit_export_view`、`revit_list_instances` 外都接受 `timeout_seconds=120`、`pickup_timeout_seconds=300`、`document=null`（`docs/tools.md:7`；`server/revit_model_mcp/server.py:60-73`）。
所有只读工具都带 `readOnlyHint=true, destructiveHint=false, idempotentHint=true`（`server.py:59`），标题在 `addressed_tool` 映射中登记（`server.py:248-267`）。

| # | 工具 | 类别 | 命令 / 后端 | 关键参数 | 证据 |
|---|---|---|---|---|---|
| 1 | `revit_ping` | 连接 | `ping` | — | `server.py:274-284` |
| 2 | `revit_document_info` | 文档 | `document-info` | — | `server.py:288-302` |
| 3 | `revit_list_instances` | 文档/实例 | 无 job；心跳或 `/health` | `document` | `server.py:725-740` |
| 4 | `revit_list_catalog` | 目录发现 | `list-catalog` | `section`（8 段：categories, family-types, levels, area-schemes, views, worksets, phases, parameters） | `server.py:432-448`；`Capture/CatalogReader.cs:10-21` |
| 5 | `revit_query_elements` | 查询 | `query-elements` | 9 个过滤器 + `fields/offset/limit/sort_field/sort_direction/include_geometry` | `server.py:498-548` |
| 6 | `revit_aggregate_elements` | 聚合 | `aggregate-elements` | `group_by`(1–2 字段) + `sum_field` + 9 个过滤器 | `server.py:452-494`；`universal_jobs.py:58-93` |
| 7 | `revit_list_views` | 视图 | `list-views` | `view_type`, `name_contains` | `server.py:552-571` |
| 8 | `revit_view_summary` | 视图 | `view-summary` | `view` | `server.py:575-589` |
| 9 | `revit_view_elements` | 视图 | `view-elements` | `view`, `categories`, `offset`, `limit` | `server.py:615-636` |
| 10 | `revit_view_warnings` | 告警 | `view-warnings` | `view` | `server.py:660-675` |
| 11 | `revit_export_view` | 视图/图像 | `export-view`（PNG） | `view`, `pixel_size`(1–4000), `save_to` | `server.py:593-611`；`revit_channel.py:98-107` |
| 12 | `revit_element_details` | 几何 | `element-details` | `element_id` | `server.py:640-656` |
| 13 | `revit_list_warnings` | 质量 | `list-warnings` | `warning_text`, `include_elements` | `server.py:679-698` |
| 14 | `revit_list_relations` | 关系 | `list-relations` | `relation` + `source_id`/`source_name`（5 种：level-rooms, group-elements, nested-family, area-scheme-elements, view-template-dependents） | `server.py:702-722`；`Capture/RelationReader.cs:14-19` |
| 15 | `revit_model_health` | 质量巡检 | `model-health` | — | `server.py:306-323` |
| 16 | `revit_links_status` | 文档/链接 | `links-status` | — | `server.py:327-344` |
| 17 | `revit_shared_coordinates` | 文档/坐标 | `shared-coordinates` | — | `server.py:348-364` |
| 18 | `revit_parameter_fill_check` | 质量巡检 | `parameter-fill-check` | `categories`(1–20), `parameters`(1–30), `level/workset/view`, `sample_limit`(1–100), `include_types` | `server.py:368-428` |

分类聚合（按业务能力）：**连接/实例 3**（1–3）、**目录/查询/聚合 3**（4–6）、**视图与图像 5**（7–11）、**几何 1**（12）、**告警/质量巡检 5**（13、15–18）、**关系 1**（14）。

### 2.1 查询能力的具体边界（扩展时最容易碰到的约束）

- 系统内置字段白名单仅 10 个：`id, category, family, type, name, level, workset, phase, areaScheme, hasWarnings`（`Capture/ElementFieldReader.cs:9-13`）。
- 其余字段名按「本地化参数名」走 `LookupParameter(name)` 语义（只取首个同名匹配，不支持 GUID/BuiltInParameter 选择；`docs/tools.md:37`；`Capture/QueryParameterResolver.cs:19-51`）。
- 参数过滤操作符：`equals, contains, greater, less, empty, not-empty, exists`（`server.py:102-108`；`Capture/QueryFilterBuilder.cs:149-193`）。
- 单位约定：长度 mm、面积 m2、体积 m3，坐标 mm 保留 1 位小数（`docs/tools.md:41,50`；`Core/Units/UnitConverter.cs`）。
- `group_by` 只允许 1–2 个字段（`universal_jobs.py:87-90`）。

---

## 3. 写入/交互工具清单（9，opt-in）

定义位置 `server/revit_model_mcp/actions.py:168-323`，注解按工具区分 `destructiveHint`/`idempotentHint`（`actions.py:156-166`）。

| 工具 | 子类 | 参数 | 是否可 `dry_run` | 是否可入 `revit_batch` |
|---|---|---|---|---|
| `revit_select` | UI 交互（不产生事务） | `element_ids`（空数组=清空选择） | 否 | 是 |
| `revit_show` | UI 交互 | `element_ids`, `select=true` | 否 | **否**（`ActionJobParser.cs:43` 排除 show/batch） |
| `revit_isolate` | UI 交互（临时隔离） | `element_ids`, `reset=false` | 否 | 是 |
| `revit_move` | 模型变更 | `element_ids`, `dx_mm`, `dy_mm`, `dz_mm=0` | 是 | 是 |
| `revit_place_family` | 模型变更 | `family`, `type_name`, `x_mm`, `y_mm`, `level`, `rotation_deg=0` | 是 | 是 |
| `revit_create_wall` | 模型变更 | `start_mm`, `end_mm`, `level`, `wall_type`, `height_mm=3000` | 是 | 是 |
| `revit_set_parameter` | 模型变更 | `element_id`, `parameter`, `value` | 是 | 是 |
| `revit_delete` | 模型变更（级联依赖） | `element_ids` | 是 | 是 |
| `revit_batch` | 编排 | `steps`(1–50), `dry_run=false` | 是（整批回滚） | — |

批处理动作白名单：`move, place-family, create-wall, set-parameter, delete, select, isolate`；嵌套 batch 与 `show` 被拒绝（`src/RevitModelMcp.Core/Control/ActionJobParser.cs:8,43`）。每步独立事务，整体 `TransactionGroup` 合并为单个撤销项 `revit_batch`（`docs/actions.md:130`）。失败即整批回滚，全部已尝试步骤标记 `rolledBack:true`（`docs/actions.md:77`）。

`verification` 结构按动作给出模型事实：move→包围盒前后、set-parameter→参数值与 instance/type 归属、create→元素元数据、delete→请求与依赖 ID 及存活检查（`docs/feed-format.md:228-238`）。

---

## 4. 读写边界、安全门与执行语义

| 约束 | 内容 | 证据 |
|---|---|---|
| 注册门 | `REVIT_MCP_ALLOW_WRITE` 必须为 1/true/yes/on，否则 9 个写入工具根本不注册 | `actions.py:99-109,121-123` |
| 工作站门 | 每次动作检查 `%LOCALAPPDATA%\RevitModelMcp\allow-write` 是否存在；缺失时返回 `actions disabled on the workstation`；删文件立即生效、无需重启 Revit | `ActionCommandExecutor.cs:17,35,158`；`docs/actions.md:106-115` |
| HTTP 门 | 动作类 HTTP 请求在工作站门缺失时返回 **403**；非动作请求仍可读 | `HttpChannel.cs:254` |
| 单实例约束 | 写入前调用 `list_revit_instances`，**必须恰好 1 个**实例，否则 `ToolError("Actions require exactly one running Revit instance.")` | `actions.py:125-131` |
| 多实例寻址（只读） | 只读支持 `document=` 子串寻址（映射为 `targetDocument`），可跨实例；写入的 `document` 走 `targetDocument` 且**不得回退到活动文档** | `server.py:209-215`；`revit_channel.py:259-265`；`docs/actions.md:12-22` |
| 不保存模型 | 任何动作都不保存文档；无保存/同步工具 | `docs/actions.md:134` |
| 超时语义 | 默认响应 120 s、取件 300 s；插件内部快速读命令 60 s 上限（超出返回 `partial:true`）；超时后动作可能已执行，需先检查模型 | `revit_channel.py:15-16`；`ReadCommandExecutor.cs:13`；`docs/tools.md:38`；`revit_channel.py:412-420` |
| 单任务串行 | 插件同一时刻只接受一个 job；`ControlChannel.TrySubmit` 在忙/存在 `trigger.txt` 时拒绝（HTTP 409） | `ControlChannel.cs:25-37`；`docs/transport.md:97` |
| 响应关联与原子发布 | job 载荷带 `correlationId`，响应文件名与体也带该 ID；响应写盘用临时文件 + `File.Replace/Move` 重试 10 次 | `revit_channel.py:346-347`；`Core/Serialization/CommandResponseJsonSerializer.cs:40-41,75-105` |
| 路径脱敏 | `REVIT_MCP_REDACT_PATHS=1` 或 `--redact-paths` 把 `documentPath` 与嵌套 `path` 降为文件名（本地 `localPath` 不受影响） | `server.py:44-56`；`docs/transport.md:285-291` |
| 目标文档解析 | 动作的 `targetDocument` 不唯一/不存在时，**整批在解析阶段中止**，不执行任何步骤 | `docs/actions.md:15-18` |

---

## 5. 扩展点与推荐步骤

### 5.1 新增「只读工具」（job-based）

需要同时落地的 8 处：

1. **Python job 构造**：在 `server/revit_model_mcp/revit_channel.py` 的 `ReadJob` 上加 classmethod（如 `list_views` 模式，`revit_channel.py:81-254`）；若复用通用过滤语义，在 `universal_jobs.py:96-126` 增加 payload 构造函数。
2. **MCP 工具注册**：`server/revit_model_mcp/server.py` 加 `@addressed_tool` 函数，**并登记标题映射**（`server.py:248-267`）。漏登记会直接 `KeyError`；标题必须 ≤40 字符（测试断言 `test_server.py:152-153`）。
3. **Core 合同**：`Core/Control/ControlJobParser.cs` 的 `ControlJobKind` 枚举（`:8-31`）与 `FromContract` switch（`:155-176`）加分支（通用查询类走 `Core/Control/UniversalJobParser.cs`）。
4. **Core 模型/序列化**：在 `Core/Models/ReadCommandModels.cs` 增加响应 data 类型；`Core/Serialization/CommandResponseJsonSerializer.cs` 复用。
5. **Addin 读者**：在 `src/RevitModelMcp.Addin/Capture/` 新增 reader（Revit API 只能出现在 Addin 项目；Core 不引用 Revit API，`docs/architecture.md:10`）。
6. **Addin 分发**：`Control/ReadCommandExecutor.cs:41-135` 的 switch 加 case。
7. **长任务**：若单次 ExternalEvent 内可能超过 60 s，参照 `Control/ViewElementsSession.cs` / `Control/ViewDumpSession.cs` 的「会话 + 分页 ExternalEvent」模式，并在 `ControlChannel.ProcessJob`（`ControlChannel.cs:185-199`）注册会话类型。
8. **文档与测试**：`docs/tools.md`、`README.md#tools`、`docs/feed-format.md`；Python `server/tests/test_server.py` 的 `EXPECTED_TOOLS`（`:18-37`）与 `EXPECTED_PARAMETERS`（`:39-133`）；C# `tests/RevitModelMcp.Core.Tests/Control/ControlJobParserTests.cs` 与 `UniversalJobParserTests.cs`。

> 约束：新工具不得放宽只读默认值；`list_tools` 的只读断言在 `server/tests/test_server.py:150-157` 强制 `readOnlyHint=true`。

### 5.2 新增「写入工具」

在 §5.1 的通道基础上追加：

1. `server/revit_model_mcp/actions.py`：加 `@action` 函数 + 标题映射（`actions.py:144-155`）；若需可入批处理，加入 `_BATCH_FIELDS`（`actions.py:33-69`）。
2. `server/revit_model_mcp/revit_channel.py`：加入 `ACTION_COMMANDS` frozenset（`:20-32`），否则超时提示会误判为读命令（`:412-420`）且错误响应语义不同（`:507-509`）。
3. `Core/Control/ActionJobParser.cs`：`IsAction`（`:8`）、参数校验与 `ActionJobContract` 字段（`:50-95`）。
4. `Addin/Control/ActionCommandExecutor.cs`：执行分发开关（`:213-231`）与事务策略（dry_run 回滚、警告消解、TaskDialog 抑制）。
5. `Addin/Control/ActionMutations.cs`：实际变更实现（注意单位换算与 `IsReadOnly` 校验，`:60-84`）。
6. `Addin/Control/ActionVerifier.cs`：before/after 事实（`:13-47`），并在 `docs/feed-format.md:228-238` 补契约。
7. 文档：`docs/actions.md`、`README.md`；测试：`server/tests/test_actions.py`。

**硬性约束**：保持双重门；`ElementId` 上限在 Revit 2022–2023 为 2,147,483,647（`docs/actions.md:10`）；`place_family` 走「基于标高、非结构」重载，宿主/面/自适应族会报错（`docs/actions.md:121`）；`set_parameter` 不支持 ElementId 与只读参数，类型参数编辑影响全部实例（`docs/actions.md:123-125`）。

### 5.3 新增/扩展传输

- Python 侧：实现 `RemoteHost` 协议 5 个方法 `prepare_job / wait_until_trigger_is_gone / wait_for_new_response / finish_job / delete_files`（`revit_channel.py:300-321`）+ `list_revit_instances`，并在 `server.py:28-37` 的 `create_host` 与 `REVIT_MCP_HOST` 中接线（现有实现：`http_host.py:26-210`、`ssh_host.py:48-305`）。
- 插件侧：新监听器复用 `ControlChannel.TrySubmit` 保持「单任务」语义（HTTP 参考 `HttpChannel.cs:98-166`，路由为 `/health`、`POST /jobs`、`GET /jobs/{id}`、`GET /views/{name}/image`）。
- 安全约束：默认回环优先；HTTP 无内建 TLS（需 SSH 隧道/Tailscale/TLS 反代）；请求体上限 1 MiB；`/health` 不鉴权；其余需 Bearer；拒绝重定向以保护 token（`docs/transport.md:75-101`）。

### 5.4 支持新 Revit API / 新 Revit 版本

1. **条件编译机制已就绪**：源码已使用 `REVIT2024_OR_GREATER` / `!REVIT2023_OR_GREATER` 等常量，共 11 处（`ReadCommandExecutor.cs:304`、`ActionCommandExecutor.cs:248`、`Capture/QueryFilterBuilder.cs:325,334,343,352,361`、`Capture/QueryParameterResolver.cs:198`、`Capture/RevitValueReader.cs:11`、`Capture/ElementQueryReader.cs:87`、`Capture/RelationReader.cs:104`、`HttpChannel.cs:368`）。这些常量由 `Nice3point.Revit.Sdk` 的 `GenerateRevitCompatibleDefineConstants` 目标根据 `RevitVersion` 自动生成。
2. **版本矩阵改动清单**：`src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj:15-16` 的 `Configurations` 增加 `Debug/Release.Rxx`；SDK 会把两位配置映射为 `20xx` 并选择 TFM（`Nice3point.Revit.Common.props:35-47`，证据取自本机 NuGet 缓存中的 SDK 6.0.0；项目实际引用 `Nice3point.Revit.Sdk/6.2.3`，映射规则需以该版本为准核验。规则：≥2019 → `net47`，≥2021 → `net48`，≥2025 → `net8.0-windows7.0`）；包引用 `Nice3point.Revit.Api.RevitAPI/RevitAPIUI` 与 `Nice3point.Revit.Toolkit`、`Extensions` 需要对应年份版本（`csproj:20-23`）。
3. **CI/发布**：`.github/workflows/ci.yml:73-77` 与 `codeql.yml` 的构建配置、`artifact-comment.yml:40`、`community.yml:53` 的年份列表；`build/Modules/ResolveConfigurationsModule.cs`；MSI/打包在 `build/install/`；`.addin` 清单按年份修补。
4. **安装脚本（重要）**：`install.ps1:33,117,170-172` 把支持范围硬编码为 **2022–2027**（`$selected -notmatch '^202[2-7]$'` 会直接抛错），并且检测循环固定 `2022..2027`。**支持 2020 必须先改这里**。
5. **API 代际差异（推断，需实机验证）**：`SpecTypeId`/`UnitTypeId`/`ForgeTypeId` 派 API 出现在 9 个文件中（`ActionCommandExecutor.cs`、`ActionMutations.cs`、`ActionVerifier.cs`、`Capture/QueryFilterBuilder.cs`、`ModelHealthReader.cs`、`QueryParameterResolver.cs`、`ViewElementReader.cs`、`SharedCoordinatesReader.cs`、`CatalogReader.cs`，共 25 处引用）。这些是 Revit 2021+ 的 ForgeTypeId 体系；2020 需要 `DisplayUnitType` 分支（用同样的 `#if` 机制隔离）。此项与 compatibility-analyst 的结论需交叉核验。
6. **依赖可得性（外部证据）**：NuGet 上存在 `Nice3point.Revit.Api.RevitAPI 2020.2.60`（[nuget.org](https://www.nuget.org/packages/Nice3point.Revit.Api.RevitAPI/2020.2.60)），Nice3point 工具链文档称支持 Revit 2020–2026（[DeepWiki: Getting Started](https://deepwiki.com/Nice3point/RevitToolkit/1.1-getting-started)）。因此 **SDK/包层面不是绝对阻碍**，主要工作量在 API 代际分支、安装/打包年份白名单与实机验证。

### 5.5 推荐实施顺序（按风险从低到高）

1. （低）新增只读工具/查询字段：纯增量，8 步清单，无安全面变化。
2. （低-中）扩展传输：实现 `RemoteHost` 协议，安全默认值不变。
3. （中）新增写入工具：必须复核双重门与 dry_run/verification 契约。
4. （中-高）新增 Revit 版本：csproj/CI/install.ps1/打包 + 条件编译分支 + 各版本实机验证（当前 `docs/roadmap.md:20` 自述「2026-09-12 验证未覆盖 2022–2025、2027 实机」）。
5. （高）批处理策略增强（`roadmap.md:17` 指出的确认令牌与无人值守策略尚不存在）。

---

## 6. 发现：文档与代码不同步（建议 captain 在综合结论中修正）

| # | 文档陈述 | 代码事实 | 影响 |
|---|---|---|---|
| 1 | `docs/architecture.md:39`「The file protocol has no request correlation identifier.」 | 文件通道现已带 `correlationId`：job 载荷注入（`revit_channel.py:346-347`）、响应文件名后缀（`CommandResponseJsonSerializer.cs:40-41`）、客户端按 ID 过滤（`revit_channel.py:390-396`） | 架构描述过时；HEAD 提交 `5a65afc`「correlate responses by job id and publish atomically」已修复 |
| 2 | `docs/roadmap.md:11`「File responses: writes are not atomic, and a polling client can observe incomplete JSON」 | 响应写盘已原子化：临时文件 + `File.Replace/Move` + 10 次重试（`CommandResponseJsonSerializer.cs:75-105`） | 缺口清单过时 |
| 3 | `docs/roadmap.md:10`「jobs lack correlation IDs and interprocess response ownership」 | 同 #1；响应所有权由 correlationId 过滤实现 | 缺口清单过时（「一目录一服务进程」建议仍有效） |
| 4 | `docs/roadmap.md` 审阅日期 2026-09-12，HEAD 为 2026-09-18 | 至少 2 个提交（`5a65afc`、`d558ee9`）改变了缺口状态 | 引用 roadmap 时需声明「审阅日期早于 HEAD」 |

`install.ps1:172` 对 2020 的硬性拒绝（见 §5.4-4）属于**代码约束**而非文档不同步，但对「迁移至 Revit 2020」的答案有决定性影响。

---

## 7. 能力覆盖缺口（可用于回答「有哪些功能 / 能否扩展」）

当前**没有**的常见 BIM 自动化能力（可作为扩展候选池）：

- 文档生命周期：保存、另存、`SaveAs`、关闭、打开模型、链接管理（仅只读 `links-status`）。
- 工作共享：与中心模型同步、签出/借用图元、工作集切换。
- 视图/图纸：创建视图、复制视图、放置视图到图纸、创建/编辑明细表与过滤器、视图模板编辑。
- 族与类型：载入族（`.rfa`）、创建类型/参数定义（共享参数、项目参数）、删除类型。
- 几何写入：除了建墙与放族，无楼板/梁柱/洞口/房间/面积边界创建，无尺寸标注与标注创建。
- 数据交换：DWG/IFC/GBXML 导入导出、图片导出仅限视图 PNG（`export-view`）。
- 交互：无撤销/重做工具（批处理仅在内部使用事务组），无对话框交互（动作执行期只做 TaskDialog 自动抑制）。
- 查询侧：无几何谓词过滤（如「相交/在框内」）、无纯几何查询接口（只有 `include_geometry` 附带坐标）。

---

## 8. 关键证据索引（供交叉核验）

- 工具注册与注释：`server/revit_model_mcp/server.py:217-225,243-270,273-740`
- 动作注册与门：`server/revit_model_mcp/actions.py:99-166`
- 工具名清单（测试即契约）：`server/tests/test_server.py:18-133`、`server/tests/test_actions.py:17-27`
- 通道协议与超时：`server/revit_model_mcp/revit_channel.py:15-32,300-321,329-458,461-525`
- 命令解析（命令即契约）：`src/RevitModelMcp.Core/Control/ControlJobParser.cs:8-31,141-198`
- 读命令分发：`src/RevitModelMcp.Addin/Control/ReadCommandExecutor.cs:13,31-136`
- 单任务与分发：`src/RevitModelMcp.Addin/Control/ControlChannel.cs:25-37,144-200`
- 写入执行/门/事务：`src/RevitModelMcp.Addin/Control/ActionCommandExecutor.cs:17,35,45-231`
- 传输与安全：`docs/transport.md:8-115,213-291`；`src/RevitModelMcp.Addin/Control/HttpChannel.cs:98-166,228,254`
- 协议数据形状：`docs/feed-format.md:25-56,177-263`
- 版本矩阵与条件编译：`src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj:15-23`；`install.ps1:33,117,170-172`；`.github/workflows/ci.yml:73-77`
