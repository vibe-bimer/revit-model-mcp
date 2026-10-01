# Revit Model MCP — 人工端到端测试计划

完整的人工验证清单。目标：在每个受支持的 Revit 版本上，从全新安装开始，经过真机模型读取及受门禁保护的动作，覆盖**每一个工具**和**每一种安装／传输路径**。

按计划安排执行。逐项勾选 `[ ]`。每个已勾选项目都记录：**结果**（通过／失败）、**证据**（journal 行、截图、工具 JSON、耗时）和**备注**。每个失败项都应附复现步骤并创建 GitHub Issue。

> 抽查参考模型：**Snowdon Towers Sample Architectural.rvt**（随 Revit 提供）。下文引用的值采集于 2026-09-15、Revit 2024.3，仅供历史对比，不保证其他模型或发布版本相同。先用 `revit_list_catalog` 发现名称，再通过 `revit_document_info` + `revit_aggregate_elements` 采集当前模型的基线。

!!! note "计划覆盖，不是验证证据"
    本清单覆盖当前 **33 个工具：19 个读取 + 14 个需显式启用的动作**，支持 **Revit 2020 和 2022–2027**，不支持 Revit 2021。将被测发布版本的 `tools/list` 与[读取契约](tools.md)、[动作契约](actions.md)及[功能总览](features/index.md)核对。本次文档更新没有执行任何真机 Revit 调用、勾选检查项或新增工作站证据；已记录的运行见[验证证据](validation.md)。下文 2026-09-15 的客户端问题均为历史复测项，不代表当前兼容性保证。

---

<a id="0-test-environments-matrix"></a>
## 0. 测试环境（矩阵）

理想情况下使用**两台机器**：

- **M1 — 较干净的 Windows 工作站**：全新或很少使用的 Windows，已安装目标 Revit 版本，已安装并登录 Claude Desktop。这一轮用于回答“真实用户能否通过安装器顺利用起来”。
- **M2 — 远程客户端（macOS / Linux）**：在 Mac 上使用 Claude Desktop / Claude Code，通过远程（SSH 隧道）传输访问 Windows 工作站中的 Revit。

| 字段 | M1 | M2 |
| --- | --- | --- |
| 操作系统／构建版本 | | |
| Revit 版本 | | |
| Python + uv 版本 | | |
| Claude Desktop 版本 | | |
| Claude Code（`claude --version`） | | |
| 被测发布版本（插件／服务器／mcpb） | | |

记录被测版本的精确发布标签（例如 `v0.5.0`），并确认三类产物的版本一致：`.msi`／插件 ZIP、PyPI 上的 `revit-model-mcp` 和 `.mcpb`。

---

<a id="1-add-in-installation-fresh-per-revit-version"></a>
## 1. 插件安装（全新安装，逐 Revit 版本）

在 **Revit 关闭**时执行。对已安装的每个受支持 Revit 年份（2020 / 2022 / 2023 / 2024 / 2025 / 2026 / 2027）重复本节全部步骤，不包括 2021。

- [ ] **1.1 MSI — SingleUser**：运行 `RevitModelMcp-<ver>-SingleUser.msi`。安装器无错误完成。
- [ ] **1.2 MSI — MultiUser**：在独立用户配置／机器上运行 `RevitModelMcp-<ver>-MultiUser.msi`。安装完成；所有用户都能看到插件。
- [ ] **1.3 克隆脚本**：在克隆目录中执行 `./install.ps1 -Source Release`。安装完成。
- [ ] **1.4 清单存在**：`%APPDATA%\Autodesk\Revit\Addins\<year>\RevitModelMcp.addin` 存在，并指向一个实际存在的 `RevitModelMcp.dll`。
- [ ] **1.5 DLL 版本**：已安装的 `RevitModelMcp.dll` 与发布版本一致。
- [ ] **1.6 来源证明**：安装前，按照文档 `security/#verify-downloads` 验证发布资产的构建来源证明（build-provenance attestation）。
- [ ] **1.7 在 Revit 中加载**：启动 Revit，接受“unsigned add-in”信任对话框（**Always Load**），打开模型。Journal（`%LOCALAPPDATA%\Autodesk\Revit\Autodesk Revit <year>\Journals\journal.*.txt`）应显示 `API_SUCCESS ... Starting External Application: Revit Model MCP ... Assembly Version: <ver>` 和事件注册。MCP DLL 不应出现致命 `API_ERROR`（当引用版本**低于**已安装 Revit 构建时，无害的“assembly version conflict”警告可以接受）。
- [ ] **1.8 卸载**：MSI 卸载干净移除清单（没有孤立文件，下次启动 Revit 没有加载错误）。

**需要关注的回归（此前发现过）**：插件必须引用固定为 `<year>.0.0.0`（≤ 已安装构建）的 `RevitAPI/RevitAPIUI` 和 `System.Diagnostics.DiagnosticSource 8.x`，否则会加载失败。逐版本确认。

---

<a id="2-server-client-wiring-every-documented-method"></a>
## 2. 服务器与客户端接线（每一种已记录的方法）

<a id="21-local-server-via-uvx-windows-workstation"></a>
### 2.1 通过 `uvx` 运行本地服务器（Windows 工作站）

- [ ] `uvx revit-model-mcp` 首次运行时能够从 PyPI 解析并安装包（记录包数量 + 耗时）。
- [ ] 服务器启动，并在 `initialize` 中报告 `serverInfo: { name: "Revit Model Reader", version: "<ver>" }`。
- [ ] 禁用动作时，`tools/list` 恰好返回 **19 个读取工具**（第 3 节）；以 `REVIT_MCP_ALLOW_WRITE=1` 重启服务器后返回 **33 个工具：19 个读取 + 14 个动作**（第 4 节）。动作虽已列出，是否可执行仍由工作站门禁决定。

<a id="22-claude-code-registration-claude-mcp-add"></a>
### 2.2 注册到 Claude Code（`claude mcp add`）

- [ ] `claude mcp add revit-model-mcp -s user -e REVIT_MCP_HOST=local -e REVIT_MCP_REDACT_PATHS=1 -- uvx revit-model-mcp` 写入 `~/.claude.json`。
- [ ] `claude mcp list` 显示 `revit-model-mcp: ... ✓ Connected`。
- [ ] `claude -p "what model is open in Revit?"`（无界面模式）返回真实模型数据（将 stdout 保存到文件——直接使用原始管道可能丢失无界面模式的输出）。
- [ ] **应用内本地 Agent**：在 Claude Desktop 的 Code 界面中选择 **“Local”** 标记，询问 Revit 问题 → Agent 调用 `mcp__revit-model-mcp__*`，并使用真实数据回答。

<a id="23-claude-desktop-mcpb-one-click-install-known-broken-re-verify"></a>
### 2.3 Claude Desktop `.mcpb` 一键安装（历史问题，需复测）

- [ ] 在 Windows 上双击 `revit-model-mcp-<ver>.mcpb` 会**在 Claude Desktop 中**打开（文件关联）。*2026-09-15：失败——Windows 显示“choose an app”，Claude 没有注册为 `.mcpb` 处理程序。确认是否已修复，或记录正确安装入口（Settings → Extensions/Connectors → install from file）。*
- [ ] 通过 Claude Desktop 的 **Settings → Extensions/Connectors → 安装 `.mcpb`**；配置表单能够设置 `REVIT_MCP_HOST`（local / remote）、路径脱敏、动作和 HTTP 令牌，而无需编辑 JSON。
- [ ] 安装后连接器出现，其工具能在**可以访问本地 stdio 服务器的界面**中使用。

<a id="24-manual-claude_desktop_configjson-surface-limitation-re-verify"></a>
### 2.4 手工配置 `claude_desktop_config.json`（历史界面问题，需复测）

- [ ] 写入文档所述的 `mcpServers` 块，然后重启 Claude Desktop。
- [ ] 确认当前安装的客户端版本中哪些界面读取该配置。*2026-09-15 历史观察：应用的**云端聊天**无法访问本地 stdio MCP（“doesn't reach this cloud session”）。分别复测云端聊天与本地 Agent，记录实际访问能力及当前配置要求，不把旧限制当作当前保证。*

<a id="25-remote-workstation-m2-m1"></a>
### 2.5 远程工作站（M2 → M1）

- [ ] 从 Mac / Linux 客户端，按照文档 `transport/` 配置远程工作站（SSH 隧道连接到工作站的回环端点）。
- [ ] 客户端 `revit_ping` 成功访问远程 Revit；读取工具返回真实数据。

---

<a id="3-read-tools-full-coverage-18"></a>
<a id="3-read-tools-full-coverage-19"></a>
## 3. 读取工具 — 完整覆盖（19）

在工作站上打开模型。通用模型查询应**先调用 `revit_list_catalog`，再调用 `revit_aggregate_elements`，只有需要逐条数据时才调用 `revit_query_elements`**。先用 `revit_list_instances` 发现进程，再选取唯一的 `document` 子串。记录每个 JSON 结果并抽查值。读取响应通常包含 `success: true`；`revit_list_instances` 则直接返回进程记录列表，没有匹配项时为 `[]`。两个导出工具会写文件，但不修改模型。

| # | 工具 | 如何调用（自然语言提示或直接调用） | 预期／抽查 | [ ] |
| --- | --- | --- | --- | --- |
| 1 | `revit_ping` | “能连接到 Revit 吗？” | `data="pong"`，无活动文档时也可返回；响应方元数据 | [ ] |
| 2 | `revit_document_info` | “打开了什么模型，有哪些标高、面积方案和工作集？” | 文件名、Revit 版本、带 `elevationMm` 的标高、面积方案、工作集和 `viewCount`；`isWorkshared`。Snowdon 历史面积数量：Gross Building 14、Rentable 87。房间数量另用聚合查询 | [ ] |
| 3 | `revit_model_health` | “给我模型健康摘要” | 项目信息、文件大小、计数、单位和主要警告；不可用指标为 null，`skipped` 中说明原因 | [ ] |
| 4 | `revit_links_status` | “列出 RVT、CAD 和图像链接及其状态” | 摘要及 `rvtLinks`、`cadLinks`、`images`；空列表有效；检查逐项错误和列表 100 项上限 | [ ] |
| 5 | `revit_shared_coordinates` | “共享坐标和测量点是什么？” | 基点／测量点、活动场地、项目位置和链接偏移；单位 mm、度 | [ ] |
| 6 | `revit_parameter_fill_check` | 使用目录中的类别及参数名称 | 已填写／空值／缺失计数、实例／类型归属、ID 样本；数值零算已填写 | [ ] |
| 7 | `revit_list_catalog` | 测试 `categories`、`family-types`、`levels`、`area-schemes`、`views`、`worksets`、`phases`、`parameters` | 名称、ID 及各节计数／类型；精确本地化参数名称 | [ ] |
| 8 | `revit_aggregate_elements` | “有多少门和窗？”；`group_by=["category"]` | `matchedElements`、分组计数及可选数值合计／单位；Snowdon 历史值：Doors 142、Windows 106 | [ ] |
| 9 | `revit_query_elements` | 最大房间：字段 `name`、`level`、`area`，`sort_field="area"`、`sort_direction="desc"` | 分页记录和单位；Snowdon 历史值：Parking Garage、标高 Parking、957.6 m²；请求时包含房间几何 | [ ] |
| 10 | `revit_list_views` | “列出非模板视图” | ID／名称、类型、标高、比例、模板、`total`、`processed`；测试类型／名称过滤 | [ ] |
| 11 | `revit_view_summary` | 传第 10 项返回的精确视图名或视图 ID | 头部元数据、类别计数和 `differentTypes`；没有默认使用活动视图的行为 | [ ] |
| 12 | `revit_export_view` | 导出已发现的 3D／平面视图 | PNG、客户端 `localPath`、大小、视图元数据；打开图像确认渲染，活动视图不变 | [ ] |
| 13 | `revit_view_elements` | 对第 10 项发现的视图分页读取 | ID、类别／族／类型／标高、测量值和 `hasMore` | [ ] |
| 14 | `revit_element_details` | 查看第 9 或 13 项中的 ID | 实例／类型参数、相关警告、可用几何；房间包含面积、体积、边界和 `roomCenterMm` | [ ] |
| 15 | `revit_view_warnings` | 传已发现的视图 | 涉及视图内元素的警告；`presentOnView` 区分受影响但位于视图外的元素 | [ ] |
| 16 | `revit_list_warnings` | 先列分组，再传返回的 `warning_text` 和 `include_elements=true` | `totalWarnings`、分组计数、受影响 ID；空分组有效 | [ ] |
| 17 | `revit_list_relations` | `level-rooms`、`area-scheme-elements`、`view-template-dependents` 用 `source_name`；`group-elements`、`nested-family` 用 `source_id` | `relation`、`source`、相关元素记录；不提供任意宿主／被承载关系图。名称来自目录，ID 来自元素查询 | [ ] |
| 18 | `revit_list_instances` | “有哪些 Revit 进程及活动文档？”；再用 `document` 过滤 | `documentName`、`documentPath`、`revitVersion`、`pluginVersion`、`processId`、`pluginResponding` 的列表；不是族／类型实例。Local／SSH 回退记录可能文档为空且 `pluginResponding=false`；HTTP 只列已连接进程 | [ ] |
| 19 | `revit_export_element_ids` | 用默认／自定义 `fields`，将已绘制构件 ID 清单导出到新的工作站 `.xlsx` 路径 | `path`、`fileName`、`sheetName`、列名、行数／总数／类别数、`truncated`、大小；按类别／族／类型排序。默认列：类别、族、类型、标高、构件ID、名称、工作集。ID 不变；MEP 管线标高可能为空 | [ ] |

- [ ] **3.19 开启路径脱敏**：设置 `REVIT_MCP_REDACT_PATHS=1` 后，路径字段被脱敏，但名称、参数值、错误、通道文件和导出的 `localPath` 仍可见。
- [ ] **3.20 关闭路径脱敏**：设置 `REVIT_MCP_REDACT_PATHS=0` 后显示完整路径。
- [ ] **3.21 查询边界**：`hasMore=true` 时继续分页；检查无匹配、偏移超出结果、无效字段／过滤条件、不存在的 ID／视图。缺少文档、读取失败、超时属于错误，不是完整结果。工具声明承诺不返回部分数据，但当前文件通道可能返回终态 `success:false`、`partial:true` 数据：记录此例外，不得算作完整证据；完整结果必须满足 `success:true` 且 `partial:false`（或无该字段）。等待超时不取消任务。房间数量按标高聚合；面积合计按标高分组并选定面积方案。
- [ ] **3.22 关系**：覆盖全部五种支持的关系、空成员关系、无效／缺失／类型错误的源对象；不得推断不支持的宿主关系。
- [ ] **3.23 导出安全**：检查自定义／默认字段、工作簿列和数量、已有目标文件被拒绝、工作站 `.xlsx` 与客户端 PNG 路径差异；有适当模型时检查超过 50,000 行的工作簿截断标志。确认两个导出均不修改模型元素或赋 ID。

---

<a id="4-action-tools-gated-writes-9"></a>
<a id="4-action-tools-gated-actions-14"></a>
## 4. 动作工具 — 受门禁保护的动作（15）

动作需要**同时满足两道门禁**：`REVIT_MCP_ALLOW_WRITE=1` **以及**工作站上的 allow-write 文件。直接 HTTP 调用者还需要 Bearer 令牌。本节只描述另行授权的人工测试，不是文档维护时执行的动作。使用一次性模型副本和独立输出路径，先备份、记录基线；真实修改前获得所有者许可。

连接必须恰好发现一个 Revit 进程。`document` 用于选择该进程内已打开的模型；多个文档打开时必填。未知或歧义目标会在任何修改前被拒绝。`revit_select`、`revit_show`、`revit_isolate` 还要求目标文档处于活动状态。

**安全语义因工具而异**：选择、显示／导航使用 UI 调用，不需要模型事务；隔离改变临时视图状态，没有 `dry_run`。下表九个普通模型编辑工具支持事务式 `dry_run=true`：执行、验证预期结果，再回滚。批处理支持事务组回滚。换 ID 是独立的不可逆替换流程：必须先 dry run；任一元素不合格时阻止整组选中项的真实执行。重建 ID 写入新模型文件，不修改源模型；其 dry run 执行复制但不保存文件。

!!! warning "报错不等于回滚"
    `verification.error` 可能在 **COMMIT（提交）后**发生：编辑已经完成，但提交后的重读失败。传输或接单超时不会取消待执行任务，任务可能稍后执行。重试前检查目标模型、ID 及输出文件，不能宣称每个失败响应都保证模型不变。

- [ ] **4.0 枚举**：启用服务器动作标志后，`tools/list` 恰好包含下列 **15 个具名动作**和 19 个读取（共 34 个）。保存 schema；不存在独立的“按名称打开视图”或 undo 工具。

| # | 动作工具 | 测试及验证 | 清理／安全 | [ ] |
| --- | --- | --- | --- | --- |
| 1 | `revit_select` | 选择已发现的房间／元素 ID；确认高亮和选中数量 `count`；`element_ids=[]` 清空选择 | 恢复原选择；无模型事务、无 `dry_run` | [ ] |
| 2 | `revit_show` | 对已发现 ID 分别使用 `select=true`、`false`；核对 `activeView`、`viewOpened`、选择状态及必要时打开标高平面／3D 视图的导航行为 | 恢复视图／选择；仅 UI，不是按名称打开；无模型事务、无 `dry_run` | [ ] |
| 3 | `revit_isolate` | 在活动视图中临时隔离 ID，再用 `element_ids=[]`、`reset=true`；核对临时隐藏／隔离状态 | 重置视图状态；无 `dry_run`，不是持久几何编辑 | [ ] |
| 4 | `revit_move` | 先 dry run，再按模型轴 `dx_mm`、`dy_mm`、`dz_mm` 移动测试实例；比较前后位置或包围盒 | 反向移动或丢弃测试副本；检查 mm 单位 | [ ] |
| 5 | `revit_place_family` | 先 dry run，再将已加载无宿主族放到目录标高；测试旋转、显式／null `type_name`、`Family: Type`、类型冲突及缺失族建议 | 房间内用 `roomCenterMm`；删除测试实例或丢弃副本 | [ ] |
| 6 | `revit_create_wall` | 先 dry run，再用不同模型 XY 端点、目录标高／类型和正高度创建直墙；核对新 ID／类型／几何 | 删除测试墙或丢弃副本；`wall_type` 必填但可为 null | [ ] |
| 7 | `revit_create_floor` | 先 dry run，再用至少三个模型 XY 顶点建楼板；核对自动闭合边界、ID、类型及标高；拒绝连续重复顶点 | 删除测试楼板或丢弃副本；`floor_type` 必填但可为 null | [ ] |
| 8 | `revit_set_phase` | 先 dry run，再用目录阶段名；测试创建／拆除赋值、`""` 清除及 null 保持不变；检查阶段引用 | 恢复原赋值或丢弃副本；不创建／重命名阶段；两个参数均 null 被拒绝 | [ ] |
| 9 | `revit_merge_phases` | 先 dry run，再将源阶段创建／拆除引用转到目标；核对数量、`sourceDeleted`；仍被引用的阶段可能保留且 `sourceDeleted=false` | 专用一次性副本；源／目标必须不同；不能加入批处理 | [ ] |
| 10 | `revit_set_parameter` | 先 dry run，再改可写参数；核对前后值及实例／类型归属；长度 mm、面积 m²、其他 double 内部单位 | 恢复值或丢弃副本；共享类型修改影响全部实例；只读／ElementId 参数被拒绝 | [ ] |
| 11 | `revit_set_view_lighting` | 先 dry run 读取改动前后读数；再真实设置阴影开关、`shadow_intensity`、`sunlight_intensity`、太阳日期／时间或光照模式方位角／高度角、地面平面与标高、背景与渲染光源方案。核对 `changedSettings` 与 `verification.before/after.lighting`，并用 `revit_export_view` 对比图片；在共享太阳与阴影设置的视图上确认 `shadows` 被拒绝 | 恢复可还原项（阴影、强度、太阳时间、光源方案）；**背景与地面平面标高无法通过 API 清除**，需丢弃副本。`shadows` 关闭后强度设置不再有可见效果 | [ ] |
| 12 | `revit_delete` | 先 dry run，检查包含依赖的 ID，再仅删除已批准的测试元素；核对存活检查和返回数量 | 删除数量含依赖；丢弃副本或经授权使用 Revit UI 撤销 | [ ] |
| 13 | `revit_reset_element_ids` | **必须先 dry run**：检查 `ineligible` 原因和 `idMapping`；合格／不合格混选时真实执行须整组拒绝。对已批准的全合格测试副本，确认旧 ID 消失、新副本及保留的类型／类别 | **不可逆，不依赖撤销。** 拒绝有宿主、属组、有依赖、MEP 曲线／系统成员及不可复制元素。丢弃副本并恢复备份；不原地赋 ID，也不把旧 ID 写入参数 | [ ] |
| 14 | `revit_rebuild_model_ids` | Dry run 有映射但无保存文件。真实执行到新的工作站 `destination_path`；检查 `saved`、源／副本数量、排除项、每个 ID 映射。覆盖视图／模板、`seed`、重名模式、`copies`／`{n}` 路径，逐项检查 `copyResults` | 源模型不变、不保存。未经批准不覆盖；检查所有输出。只复制三维视图可选构件及基准对象，不是完整项目归档；不保留视图／图纸／明细表／注释／阶段／工作集／MEP 系统／未选宿主 | [ ] |
| 15 | `revit_batch` | 先 dry run，再执行 1–50 个已批准步骤；核对预期验证、回滚及选择恢复。真实成功只有一个 `revit_batch` 撤销项；首个执行失败回滚事务组；检查 `committed`、从零计数的 `failedStep` 及各步结果 | 使用一次性副本；后续步骤参数无效须在任何执行前拒绝。允许名称：`move`、`place_family`、`create_wall`、`create_floor`、`set_phase`、`set_parameter`、`set_view_lighting`、`delete`、`select`、`isolate`；不允许 `show`、阶段合并、换 ID／重建 ID 或嵌套批处理 | [ ] |

- [ ] **4.1 门禁反向测试**：服务器动作标志关闭时，即使有工作站门禁，动作也不在 `tools/list` 中；标志打开但无工作站门禁时，已列出的动作被拒绝。删除工作站门禁无需重启 Revit 即生效。读取仍可使用。
- [ ] **4.2 HTTP 令牌门禁**：不带 Bearer 令牌的直接 HTTP 动作被拒绝；`/health` 无令牌也可使用。
- [ ] **4.3 事务安全**：普通事务编辑及批处理成功 dry run 应报告 `dryRun:true`、`rolledBack:true`；新建 ID 仅为临时值。核对会回滚的执行／提交失败没有部分编辑。另行检查 UI 状态、不可逆 ID 替换及外部文件行为，不套用一概的事务保证。
- [ ] **4.4 模型恢复**：恢复选择／隔离／视图及可逆测试编辑；重跑 `revit_aggregate_elements`，还要比较 ID、参数及阶段引用，而不仅是数量。丢弃换 ID／阶段合并副本并重开备份；仅检查／移除已批准的测试输出文件。
- [ ] **4.5 定位目标**：测试显式 `document`、多个已打开文档、未知／歧义目标及非活动目标的 UI 拒绝。发现多个进程时须拒绝动作，不得任意选择进程。
- [ ] **4.6 批处理边界**：测试 1、50 步，拒绝 0／51 步、未知动作／键及无效后续参数；覆盖单步 `dry_run`、首个失败回滚、单一撤销项和即时单步验证（后续步骤可能再次改变结果）。
- [ ] **4.7 验证与超时恢复**：使用可控测试副本或模拟故障检查提交后 `verification.error` 的处理及待执行任务超时警告。重试前记录实际模型／文件状态；不得从失败响应推断回滚或取消。
- [ ] **4.8 清理路径**：验证清空选择／重置隔离／删除等支持操作，适用时经授权使用 Revit UI 撤销。不虚构 MCP undo 工具，也不以撤销作为换 ID 的恢复路径。

---

<a id="5-transports"></a>
## 5. 传输

- [ ] **5.1 本地**：工作站上设置 `REVIT_MCP_HOST=local`——第 3 节全部通过。
- [ ] **5.2 SSH 隧道**：远程客户端 → 工作站回环地址——M2 上 `revit_ping` + 一个读取工具通过。
- [ ] **5.3 HTTP**：回环地址 + Bearer 令牌——`/health`（无令牌）响应；带认证的读取成功。**待复测历史回归——Issue #44**：此前运行报告端口 53110 的 HTTP 监听器无法绑定。检查当前发布版本及 Issue 状态，不宣称当前仍有此缺陷。
- [ ] **5.4 并发／通道争用**：短时间内连续发出多个**读取**调用。2026-09-15 历史运行中 *7 个并行调用有 4 个失败*，单文件通道报“busy: trigger.txt exists”。复测当前快速／并行读取，记录失败率；仍有争用则创建 Issue。不要并发执行破坏性动作测试。

---

<a id="6-multi-version-revit"></a>
## 6. 多版本 Revit

在每个已安装版本中打开模型，重复**第 3 节的读取冒烟集**（至少包括 ping、document_info、list_catalog、aggregate_elements、list_warnings、export_view）：

- [ ] 6.1 Revit 2022（net48）
- [ ] 6.2 Revit 2023（net48）
- [ ] 6.3 Revit 2024（net48）
- [ ] 6.4 Revit 2025（net8）
- [ ] 6.5 Revit 2026（net8）
- [ ] 6.6 Revit 2027（net10）——若可用
- [ ] 6.7 **同时打开两个实例**：运行 2 个或更多 Revit 版本时，确认读取工具要求 `document`，并正确路由到目标实例（分别带／不带 `document` 调用 `revit_ping`）。`revit_list_instances` 是进程发现例外；发现多个进程时，即使传入 `document`，动作也必须拒绝。
- [ ] 6.8 Revit 2020（net48）
- [ ] 6.9 **支持边界**：确认安装器／构建目标仅覆盖 2020 和 2022–2027；不得将 Revit 2021 列为支持版本。分开记录仅构建与真机实测结果；不可用的版本保留为未测。

---

<a id="7-client-surface-matrix-which-claude-surface-actually-works"></a>
## 7. 客户端界面矩阵（哪个 Claude 界面实际可用）

逐界面记录已安装客户端版本、配置及实际通过／失败。2026-09-15 的观察属于历史记录，应填写当前结果，不据此假定兼容性。区分在客户端本地运行、通过 SSH／HTTP 访问工作站的 stdio 服务器与云端托管连接器。

| 界面 | 能访问本地 stdio MCP？ | 能访问远程 MCP？ | [ ] |
| --- | --- | --- | --- |
| Claude Desktop — **云端聊天**（Chat / Cowork） | 需复测；历史上不可用 | 若已配置，记录连接器及可达性 | [ ] |
| Claude Desktop — **本地 Agent**（Code + “Local”标记） | 复测当前注册 | 若已配置，记录远程工作站设置下的结果 | [ ] |
| 本地 Claude Code CLI（`claude -p`、`claude`） | 复测当前注册 | 若已配置，记录远程工作站设置下的结果 | [ ] |
| 配置了**远程工作站**的 Claude Desktop（M2） | 记录该界面是否在本地启动 stdio | 复测工作站连接及认证 | [ ] |

- [ ] 根据实际通过的配置，为各类用户（Windows 本地／Mac 远程）记录*推荐*设置。

---

<a id="8-known-issue-regression-must-re-test"></a>
## 8. 已知问题回归（必须重新测试）

针对此前故障或意外行为（包括 2026-09-15 客户端观察）进行明确复测。这不是保证当前仍存在的缺陷清单；记录发布／客户端版本和当前结果：

- [ ] **8.1** `.mcpb` 文件关联／在 Claude 中打开（见第 2.3 节）。
- [ ] **8.2** 云端聊天中无法使用本地 stdio MCP（见第 2.4 节）。
- [ ] **8.3** HTTP 监听器绑定 53110 — Issue #44（见第 5.3 节）。
- [ ] **8.4** 并行工具调用时的通道争用（见第 5.4 节）。
- [ ] **8.5** 各版本插件加载时，无害与致命 `API_ERROR`（程序集版本冲突）的区分（见第 1.7 节）。
- [ ] **8.6** 非交互式 shell 的 PATH 中没有 `uvx` / `claude`（使用完整路径）——这是安装文档提示，不是产品缺陷。

---

<a id="9-reporting"></a>
## 9. 报告

为本轮测试生成简短结果表：环境、发布标签、逐节通过／失败数量，以及已创建 Issue 列表。也可录制一段**干净的演示视频**，但必须先布置 UI（见偏好说明）：在 Revit 中打开真实 3D／模型视图（而不只是项目浏览器），调整 Claude 和 Revit 面板大小，让两边都清楚可读，然后开始录屏。录制前请所有者先设置布局。

**发布完成定义**：第 1–7 节至少在 Revit 2024 + 2026（本地）及一次远程（M2）运行中全部通过；第 8 节的所有回归要么通过，要么有已跟踪 Issue；客户端界面矩阵（第 7 节）已写入 README／文档。
