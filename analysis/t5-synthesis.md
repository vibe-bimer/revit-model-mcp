# t5 汇总核验报告：Revit Model MCP 项目分析与五个问题的直接答案

- 分析对象：`/home/roky/revit-mcp`（上游 `sharafutdinovdi/revit-model-mcp`）
- 代码基线：HEAD `dacdafd`（2026-09-18），Python 包版本 `server/pyproject.toml:7 = 0.5.0`
- 汇总人：lead-synthesizer（t5），交叉核验 t1（架构）、t2（使用）、t3（版本）、t4（功能）
- 核验规则：凡标【核验】的结论，均由汇总结论人**独立在 HEAD 代码上复现**，不依赖上游分析者的转述；t1/t2/t4 的结论凡与代码不符，以代码为准并在 §7 记录。

---

## 0. 五个问题的直接答案

| # | 问题 | 一句话答案 |
|---|---|---|
| 1 | 怎么用 | Windows 上装 Revit 插件（MSI/`install.ps1`/按年 ZIP，三选一，装时关 Revit）+ 在 MCP 客户端机器上装 Python 服务（`uvx revit-model-mcp`）+ 客户端配 `REVIT_MCP_HOST`；调 `revit_ping` 得到 `pong` 即成功。写操作再开两道闸门。 |
| 2 | Revit 版本限制 | 当前支持 **Revit 2022–2027**，按年份分别编译（`Debug/Release.R22`…`R27`），逐年分发资产；**代码隐含下限是 2022**（配置矩阵 + `install.ps1` 白名单 + 只使用 2022+ API）。仅 2026 有实机读写验证，2024 有安装脚本验证，其余只有编译证据。 |
| 3 | 迁移到 Revit 2020 | **可行、无硬阻碍，但不是配置开关，属于中等移植工程**（t3 已用真实编译实验量化）。工具链与 NuGet（Nice3point SDK 6.2.3 接受 R20→net47，RevitAPI/Toolkit/Extensions 均有 2020 版）不构成阻碍，`build/` 打包层也已支持 2020；真正成本是 ①`install.ps1` 年份白名单与 csproj/sln/CI 年份矩阵 ②**实测 R20 编译 41 个错误、10 个文件、9 类 API**，主要是 `ForgeTypeId`/`SpecTypeId`/`UnitTypeId`/`GetDataType` 等 2021/2022 才有的单位与规格 API，需补 `DisplayUnitType`/`UnitType` 旧分支 ③Core 必须先加 `net472`、Addin 需显式覆盖 `net472` TFM ④2020 实机验证（RVT 不向后兼容，需 2020 期模型）。t3 估算约 2–3.5 人日（含实机冒烟），长期成本是永久多一条旧 API 分支。 |
| 4 | 现有功能 | 27 个 MCP 工具：默认 **18 个只读**（探活、文档、实例、目录、查询/聚合、视图与 PNG 导出、元素几何、告警、关系）＋`REVIT_MCP_ALLOW_WRITE=1` 时增加 **9 个写入/交互**（select/show/isolate/move/place_family/create_wall/set_parameter/delete/batch）。写操作受双重闸门与“恰好一个 Revit 实例”约束，且**永不保存模型**。 |
| 5 | 扩展能力 | 四条清晰扩展路径：**新增只读工具**（Python/Core/Addin/文档测试共 8 处）、**新增写入工具**（追加 7 处并复核双重门与 dry_run/verification 契约）、**新增传输**（实现 Python `RemoteHost` 5 方法 + `list_revit_instances`，插件侧复用 `ControlChannel.TrySubmit` 单任务语义）、**新增 Revit 版本**（条件编译机制 `REVIT20XX_OR_GREATER` 已就绪，已有 11 处使用）。缺口侧最值得补的是保存/同步/工作共享、视图与图纸创建、族与参数定义、DWG/IFC 交换、几何谓词过滤。 |

---

## 1. 项目是什么：四组件、两条链路

```
MCP 客户端 ──stdio(永远)──> Python MCP 服务 ──┬─ local: powershell.exe（Windows 本机）
                                              ├─ ssh:<alias>: Windows PowerShell over SSH
                                              └─ http(s)://host:port: 插件内置 HttpListener + Bearer
                                                     └─ 两路都汇入插件的 ExternalEvent（Revit API 线程）
```

| 组件 | 位置 | 职责 |
|---|---|---|
| Python MCP 服务 | `server/revit_model_mcp/` | 建 `MCPServer`（`server.py:217`）、注册 18 个只读工具（`:273-723`）与 9 个动作（`actions.py:register_actions`）、`mcp.run(transport="stdio")`（`server.py:780`） |
| 传输宿主 | `ssh_host.py`（local/ssh）、`http_host.py`（HTTP） | `server.py:28-37` 由 `REVIT_MCP_HOST` 选择，非法值启动即 `ValueError` |
| 通道序列化 | `revit_channel.py` | `asyncio.Lock` 单进程内串行（`:327,340`），生成 `correlationId` 并做响应归属 |
| C# 插件 | `src/RevitModelMcp.Addin/` | `Application.cs` ExternalApplication → ExternalEvent + 10s 兜底计时器 + 心跳；`Control/ControlChannel.cs` 在 Revit API 线程执行；`Capture/` 读取器；`Output/` 导出 |
| C# Core | `src/RevitModelMcp.Core/` | **不引用 Revit API**（`RevitModelMcp.Core.csproj` 无 Revit 包，TFM `net48;net8.0`），承载命令解析、契约模型、序列化、单位、格式化 —— 因此 Core 单测可在 macOS/Linux 跑 |

**文件通道生命周期**【核验，逐跳读码确认】：
1. Python 生成 `correlationId = uuid4().hex`，注入 job 载荷（`revit_channel.py:346-347`），临时文件名 `mcp_<correlationId>.tmp`（`:348`）；
2. `prepare_job` 用 PowerShell 先 `WriteAllBytes` 到临时文件，再 `[IO.File]::Move` 到 `trigger.txt`，Move 失败且目标已存在则判 `channelBusy`（`ssh_host.py:86-95`）——**发布本身是原子的**；
3. 插件端文件监视器/计时器请求 ExternalEvent（`Application.cs:38-47`）；
4. `ControlChannel` 按 `targetDocument`/`targetProcessId` 认领并删除 trigger（`ControlChannel.cs:308-328` → `JobTargetMatcher.TryClaim`）；
5. 响应原子落盘：先写 `<path>.<guid>.tmp`，再 `File.Replace`（目标已存在）或 `File.Move`（不存在），`IOException/UnauthorizedAccessException` 最多重试 10 次，`finally` 清理临时文件（`CommandResponseJsonSerializer.cs:75-105`）；文件名含 `correlationId`（`:34-41`）；
6. 客户端按 `correlationId` 过滤响应：`correlationId` 不属于 {空, 自己} 的响应对当前 job 无效，被加入 `known_responses` 并继续等待（`revit_channel.py:388-399`）；
7. `finish_job` 读回并清理（`ssh_host.py:258-303`）。

**HTTP 链路**：`HttpChannel.cs:50-68` 绑定回环 `:53110`；`/health` 免鉴权、其余需 Bearer（常量时间比较）；`POST /jobs` 限 1 MiB、`timeout` 0–600s；结果保留 10 分钟。HTTP 与文件通道共享“单作业”不变量（`ControlChannel.cs:25-37` `TrySubmit`）。

---

## 2. 问题一：使用方法

### 2.1 两个部件必须分别安装

| 部件 | 运行位置 | 前置条件 |
|---|---|---|
| Revit 插件 | Windows + Revit 2022–2027 | 安装时 Revit 必须关闭；装后重启 Revit 并打开模型 |
| Python MCP 服务 | MCP 客户端机器 | `uv` 在 PATH，Python ≥3.11（由 uv 处理） |

### 2.2 最短可用路径（Windows 本机）

```powershell
# 1) 工作站：装插件（Revit 已关闭）
.\install.ps1 -Source Release          # 或双击 RevitModelMcp-<ver>-SingleUser.msi
# 2) 启动 Revit 并打开模型
```
```sh
# 3) 客户端机器：注册 MCP 服务
claude mcp add revit-model-mcp -e REVIT_MCP_HOST=local -e REVIT_MCP_REDACT_PATHS=1 -- uvx revit-model-mcp
```
```text
# 4) 验证：调用 revit_ping，期望 success:true / data:"pong"（README.md:79）
```

**关键澄清（t2 提出，t1 与代码一致，本报告保留）**：MCP 客户端 ↔ Python 服务**永远是 stdio**（`server.py:780`）。`local`/`ssh:<alias>`/`http(s)://` 描述的是 **Python 服务 ↔ Revit 插件** 这一段。项目**不提供** SSE / Streamable HTTP；若要给远端 MCP 客户端一个网络端点，需自备 stdio→HTTP 代理。

### 2.3 远端客户端（macOS/Linux）

Mac/Linux 上 `REVIT_MCP_HOST=local` 不可用（会报 `Could not start the transport executable...`）。四种方案：

| 方案 | 客户端配置 | 安全性 |
|---|---|---|
| 同 LAN HTTP | `REVIT_MCP_HOST=http://revit-host:53110` | token 与模型数据明文，不推荐 |
| Tailscale | `http://100.x.y.z:53110` | 好，需 IT 一次性准备 |
| SSH 端口转发 | `ssh -N -L 53110:127.0.0.1:53110` + `http://127.0.0.1:53110` | 最稳妥 |
| SSH 文件通道 | `REVIT_MCP_HOST=ssh:revit-host` | 无 token，靠 Windows 文件权限 |

### 2.4 启用写操作（可选，两道闸门）

1. 客户端进程 `REVIT_MCP_ALLOW_WRITE=1`（接受 `1/true/yes/on`，`actions.py:99-109`；**未开则 9 个写入工具根本不注册**，`actions.py:120-123`）；
2. 工作站存在 `%LOCALAPPDATA%\RevitModelMcp\allow-write` 文件（缺失时返回 `actions disabled on the workstation`；删除即失效，无需重启 Revit）。

写操作额外约束：要求**恰好 1 个** Revit 实例（`actions.py:125-131`）；`dry_run=true` 执行后回滚并返回 `verification`；`revit_batch` 1–50 步、合并为单个撤销项 `revit_batch`、首个失败整批回滚、解析期全量校验；**动作不会保存模型**；超时**不代表动作未执行**，重试前应先查模型。

### 2.5 配置项速查（详见 t2 §10）

| 变量 | 作用端 | 默认 | 说明 |
|---|---|---|---|
| `REVIT_MCP_HOST` | 服务 | `local` | `local` / `ssh:<alias>` / `http(s)://`；`--host` 覆盖 |
| `REVIT_MCP_TOKEN` | 服务 | 空 | HTTP bearer token |
| `REVIT_MCP_ALLOW_WRITE` | 服务 | 未设 | 仅真值时注册 9 个动作工具 |
| `REVIT_MCP_REDACT_PATHS` | 服务 | 未设 | 把 `documentPath` 与嵌套 `path` 降为文件名 |
| `REVIT_MCP_CHANNEL_DIR` | 服务+Revit | `%LOCALAPPDATA%\RevitModelMcp` | 必须两侧一致，且**不**改 settings.json / allow-write / 日志位置 |
| `REVIT_MCP_SSH_MUX` / `_SSH_OPTIONS` | 服务 | 启用 / 空 | local 模式忽略 |
| `REVIT_MCP_HTTP_ENABLED/_BIND/_PORT/_TOKEN` | Revit | `1`/`127.0.0.1`/`53110`/自动 | 只覆盖不写回，改后需重启 Revit |

超时默认（`revit_channel.py:15-16`）：取件 300s、响应 120s；插件内快速读命令 60s 上限，超出返回 `partial:true`。

---

## 3. 问题二：Revit 版本限制

### 3.1 当前矩阵【核验】

| 位置 | 内容 |
|---|---|
| `src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj:15-16` | `Debug.R22…R27`、`Release.R22…R27` —— 配置矩阵本身就是硬性支持范围 |
| `install.ps1:2,33,117,170-172` | 文档字符串“2022-2027”；探测循环固定 `2022..2027`；白名单正则 `^202[2-7]$`，**不在范围内直接抛错** |
| `README.md:137-144` | 2022–2024 → .NET Framework 4.8；2025–2026 → .NET 8；2027 → .NET 10 |
| `Nice3point.Revit.Sdk/6.2.3` props | `RevitVersion ≥2019 → net47`、`≥2021 → net48`、`≥2025 → net8.0-windows7.0`、`≥2027 → net10.0-windows7.0`（本地 NuGet 缓存实测） |
| `docs/validation.md:9-14` | 2026 有实机读+写；2024 有安装脚本+本地构建；2022/2023/2025/2027 仅 CI 编译证据 |

> 勘误：`RevitModelMcp.sln` 只列了 `R22–R26`（t1 观察），但 `csproj:15-16` 与 CI/release 工作流覆盖到 `R27`——以 csproj 与流水线为准，R27 确实受支持。这是解决方案文件的滞后，不影响能力结论。

### 3.2 三个层次的“限制”

1. **构建/分发层（硬约束）**：每个 Revit 年份单独编译、单独打包（`*.zip` 6 个年份、MSI 两个安装范围），安装脚本按年份写 `.addin`。想要某年份必须为该年份产出资产。
2. **API 层（软约束，以条件编译管理）**：代码使用 `REVIT2023_OR_GREATER`/`REVIT2024_OR_GREATER` 共 **11 处**（`QueryFilterBuilder.cs:325,334,343,352,361`、`ReadCommandExecutor.cs:304`、`ActionCommandExecutor.cs:248`、`QueryParameterResolver.cs:198`、`RelationReader.cs:104`、`RevitValueReader.cs:11`、`ElementQueryReader.cs:87`），由 SDK 的 `GenerateRevitCompatibleDefineConstants` 自动生成。**最低基线是 2022**：现有分支只区分 2023/2024 及以上，2022 是分支的“否则”侧。
3. **验证层（事实约束）**：`docs/validation.md:20` 明确 2022–2025 与 2027 **没有实机读写验证**；CI 编译不等于运行可用。

---

## 4. 问题三：迁移到 Revit 2020 的可行性

（本节与 t3（compatibility-analyst）交叉核验；核验项标注【核验】。）

### 4.1 结论

**可行，无硬阻碍，但不是开关。**阻碍不在“拿不到 API/包”，而在“代码按 2022+ 的 API 代际写成，且脚本/CI 把年份写死”。t3 已用**真实编译实验**量化了工作量，本节采用其实测结果并以本报告的口径复核。

| 维度 | 结论 |
|---|---|
| 可行性 | ✅ 可行（工具链与 NuGet 层无阻碍；`build/` 打包层已能处理 R20） |
| 主要成本 | 新增一层“pre-2022 单位/规格 API 兼容层”：**实测 R20 编译产生 41 个错误（39 个体内 API 成员 + 2 个 `ForgeTypeId` 类型声明），分布于 10 个文件，归为 9 类 API** |
| 关联改动 | Core 加 `net472` 目标、csproj/sln 加 R20 配置、`install.ps1`/CI/文档年份列表扩展 |
| 工时估算（t3） | 兼容层 1–1.5 人日；构建+CI+脚本+文档 0.5–1 人日；回归与实机冒烟 0.5–1 人日（需 Revit 2020 环境） |
| 长期成本 | 永久多一条旧 API 分支（Core 单测覆盖不到，只能靠编译矩阵 + 实机冒烟）；Revit 2020 已 EOL，无官方 CI 环境 |
| 若不为 2020 | 升级到 2021 **并不省事**（`GetDataType`/`IsMeasurableSpec` 同为 2022 才有），维持 2022 下限最省成本 |

### 4.2 工具链与依赖：不构成阻碍【核验 / t3 实测】

| 项 | 结论 |
|---|---|
| `Nice3point.Revit.Sdk` | 项目用 `6.2.3`。该 SDK 是**版本无关的工具链**（版本号是工具链版本，不是 Revit 年份），其 props 由配置名推导 `RevitVersion`，**仅解析失败（`-1`）才报错，无年份白名单**。2020 落在 `net47`。网上“SDK 没有 2020 版本”是误读（NuGet 上 12 个版本都是 6.x 工具链版本）。 |
| `Nice3point.Revit.Api.RevitAPI` / `RevitAPIUI` | NuGet 实测存在 `2020.2.11`、`2020.2.60`，`[2020.0.0,2021.0.0)` 可还原（报 NU1603 近似匹配，与现有年份同现象） |
| `Nice3point.Revit.Toolkit` | NuGet 实测有 2020.0.0 … 2020.4.0 等 37 个版本 |
| `Nice3point.Revit.Extensions` | NuGet 实测有 2020.0.0 … 2020.5.4 等 46 个版本 |
| R22 对照构建 | t3 先用 `-c Release.R22` 构建成功，证明实验方法有效，再跑 `Release.R20` |
| Python 侧 | 完全不受影响（只与通道协议交互） |
| `build/` 打包层 | `TryParseVersion` 支持 R20→2020、`RevitPlatform(int.Parse(...))` 支持 2020、MSI 目标目录对 2020 走 `%ProgramData%\...\Addins\2020`（正确）—— **打包层基本无需改** |
| 唯一的“硬编码年份” | `install.ps1` 的 `2022..2027` 与 `^202[2-7]$` |

> 关键机制补充（t3 实测）：`GenerateCompatibleDefineConstants` 只对 **`Configurations` 中列出的年份** 生成 `REVIT{Y}_OR_GREATER`。因此 **`Configurations` 必须显式加入 R20**，否则 `REVIT2022_OR_GREATER` 之类的常量根本不会生成，兼容层无从书写。这是最容易漏的一步。

### 4.3 真正的工作量与风险点（以实测错误为准）

| # | 类别 | 位置 | 说明 |
|---|---|---|---|
| 1 | **年份白名单（必改）** | `install.ps1:2,8,33,117,170-172` | `^202[2-7]$` 直接拒绝 2020；探测循环 `2022..2027` 也要改 |
| 2 | **配置矩阵 + TFM** | `RevitModelMcp.Addin.csproj:15-16` | 增加 `Debug.R20`/`Release.R20`（同时解决 §4.2 的 OR_GREATER 生成问题）；并**显式覆盖 TFM 为 `net472`**（SDK 默认给 2020 的 `net47` 档会让 `Polyfill 11.0.1` 缺少 `ToHashSet`，多出 5 处错误：`ReadCommandReader.cs:208,272`、`ViewDumpSession.cs:46`、`ViewElementsSession.cs:249`、`ViewImageExporter.cs:32`；`net472` 由 BCL 原生提供，实测错误清零） |
| 3 | **Core 目标框架** | `src/RevitModelMcp.Core/RevitModelMcp.Core.csproj:6`（`net48;net8.0`） + `:10-11` Configurations | **必须先加 `net472`**，否则 restore 直接 `NU1201`（net47/net472 的 add-in 无法引用 net48 的 Core）。实测加 `net472` 后 R22/net48 仍构建成功 |
| 4 | 解决方案配置 | `RevitModelMcp.sln` | 增加 `Debug.R20`/`Release.R20` 两个 BuildType 与项目映射（`build/Modules/ResolveConfigurationsModule.cs` 从 sln 读 `Release.R*`）。**顺带补上既缺的 R27 配置**（csproj 与 release 工作流按项目路径直接构建 R27，所以此前未暴露） |
| 5 | **API 兼容层（主要工作量）** | 实测 41 个错误 / 10 个文件 / 9 类 API | 见下表 §4.3.1 |
| 6 | CI/发布 | `ci.yml`（72-77 构建步、109 `manifests.Count`、110/199 年份循环、122/149 安装路径数组、209-223 artifact）、`release.yml`（51/55/88/208、MSI 断言 6→7）、`codeql.yml:43`、`artifact-comment.yml:40`、`community.yml:53`、`winget.yml:126` | 年份数组、构建任务、年份目录数量断言、发行说明“2022-2027” |
| 7 | 文档/元数据 | `README.md:15,139-145`、`docs/transport.md:325,343`、`docs/validation.md:9,14,20`、`docs/actions.md:10`（ElementId 32 位上限应由“2022–2023”改为“2020–2023”）、`docs/manual-test-plan.md:33,142-147`、`docs/roadmap.md:20`、`CONTRIBUTING.md`、`build/winget/**/locale.en-US.yaml.template:14` | Python 服务端 / bundle 与 Revit 版本无耦合，无需改 |
| 8 | **实机验证（不可省）** | `docs/validation.md` | 需 Revit 2020 环境 + **2020 期模型**（RVT 不向后兼容，2024 的 Snowdon Towers 样本无法在 2020 打开）；CI 编译通过 ≠ 可用 |

#### 4.3.1 实测 R20 编译错误分布与替代方案（t3，本报告复核）

**缺失的 API 与替代**：

| API | 2020 | 2021 | 2022 | 2020 侧替代 |
|---|---|---|---|---|
| `ForgeTypeId` / `UnitTypeId` / `SpecTypeId` | ✗ | ✓ | ✓ | `Definition.ParameterType`（2022 移除）+ `UnitType.UT_*` + `Units.GetFormatOptions(UnitType)` / `FormatOptions.DisplayUnits` + `DisplayUnitType.DUT_*` + `UnitUtils.ConvertTo/FromInternalUnits(double, DisplayUnitType)` |
| `Definition.GetDataType()` / `InternalDefinition.GetDataType()` | ✗ | ✗ | ✓ | 同上（7 处：`CatalogReader:178`、`QueryParameterResolver:70,172`、`ViewElementReader:274,352`、`ActionMutations:90,102`） |
| `UnitUtils.IsMeasurableSpec` | ✗ | ✗ | ✓ | `ParameterType`/`UnitType` 判断（`QueryFilterBuilder:133`、`QueryParameterResolver:180`） |
| `Units.GetFormatOptions(ForgeTypeId)` / `FormatOptions.GetUnitTypeId()` | ✗（2020/2021 参数是 `UnitType`） | 部分 | ✓ | 旧重载（`ModelHealthReader:74`、`QueryFilterBuilder:141`） |
| `ElementIdSetFilter` | ✗ | ✓ | ✓ | 在视图收集器结果上按 ID 集合 LINQ 过滤（2020 只有 `FilteredElementCollector.Excluding`，无“包含集合”过滤器）——`ActionCommandExecutor.cs:171` |
| `BasePoint.Clipped` | ✗ | ✓ | ✓ | 2020 无等价属性；代码本身 try/catch 返回 null，可整体 `#if REVIT2021_OR_GREATER` 屏蔽（`SharedCoordinatesReader.cs:60`） |
| `ImageType.Status` | ✗ | ✓ | ✓ | 回退为 `"Other"`（`LinksStatusReader.cs:68`） |

**错误分布（39 个体内错误 / 10 文件 + 2 个类型声明错误）**：`ActionMutations` 9、`ViewElementReader` 8、`QueryFilterBuilder` 8、`ModelHealthReader` 4、`QueryParameterResolver` 3（另加 `:20,177` 两处 `ForgeTypeId` 声明）、`ActionCommandExecutor` 2、`SharedCoordinatesReader` 2、`ActionVerifier` 1、`LinksStatusReader` 1、`CatalogReader` 1。

**已确认无需改动**：现有 `!REVIT2023_OR_GREATER` 分支（3 参 `ParameterFilterRuleFactory.Create*Rule`）在 2020 存在；`>=2027→ProgramFiles` 的安装路径分流对 2020 正确。

> **口径说明**：§4.3-5 的“41 个编译错误”与“源码引用计数 33 行 / 9 文件”（本报告独立 grep：`SpecTypeId.` 16、`UnitTypeId.` 9、`GetDataType` 7、`ForgeTypeId` 3）是两种不同度量——前者是 t3 真机编译产出的**错误数**（含同一成员的多处调用与类型声明错误），后者是源码**引用行数**。两者互相印证同一结论：影响面集中在单位/规格/过滤三类 API，共 10 个 Addin 文件。

### 4.4 建议的迁移顺序

1. **Core 先加 `net472`**（`RevitModelMcp.Core.csproj:6` 与 Configurations），否则 R20 连 restore 都过不了（`NU1201`）；
2. **Addin 加 `Debug.R20;Release.R20` 配置并显式设 `net472` TFM**——这一步同时让 `REVIT20xx_OR_GREATER` 常量得以生成；
3. **写兼容层**，用 `#if REVIT2022_OR_GREATER` 双分支覆盖 §4.3.1 的 7 类缺失 API（单位/规格/过滤为主），把“规格→单位种类→换算”的映射**抽到 Core 用枚举表达**，以便在 net8.0 上单测，避免兼容层只能靠实机验证；
4. **sln 加 R20 配置**（顺带补 R27），让打包模块能枚举到新年份；
5. **修 `install.ps1`** 白名单与探测循环，先用**手工 ZIP** 做最小可用验证，暂不动 MSI/CI；
6. **Revit 2020 真机冒烟**：18 个只读工具（重点是 `revit_list_catalog`、`revit_element_details`、`revit_export_view`、`revit_model_health` 这些最依赖单位/类型 API 的）＋ action 最小集（含 `dry_run`/`verification`）；需要 2020 期模型基线；
7. **最后**接入 CI/打包/文档，并在 `docs/validation.md` 增加 2020 行（定位与现有 R22–R25“仅构建证据”一致：2020 无官方 CI，只能单机 Windows 冒烟）。

### 4.5 迁移风险清单

- **单位/类型 API 代际**是最大项：会影响响应字段语义（`catalog`/`health`/`element-details` 的单位换算链），且旧分支永久存在、Core 单测覆盖不到。
- **TFM 陷阱**：SDK 对 2020 默认给 `net47`，会让 `Polyfill` 缺 `ToHashSet` 并连带 5 处错误；必须显式改 `net472`（= Revit 2020 实际运行时 .NET Framework 4.7.2）。
- **能力降级不可避免**：`BasePoint.Clipped` 在 2020 无等价属性（需屏蔽该字段）；`ElementIdSetFilter` 需改为内存过滤；`ImageType.Status` 回退为 `"Other"`。这些必须在文档中显式声明为“2020 降级项”。
- **Revit 2020 已 EOL**：无官方 CI 环境、无法自动化回归；且 RVT 模型不向后兼容，需要单独采集 2020 期测试模型。
- **不划算的替代**：只升到 2021 不能省下兼容层（`GetDataType`/`IsMeasurableSpec` 同为 2022 才有）；若目标是“更老版本”而非“2020 本身”，需重新评估是否值得。
- 上游是活跃项目（HEAD 距 roadmap 审阅日已过数天且含行为变更 `5a65afc`/`d558ee9`），迁移分支必须固定基线并规划 rebase 成本。

---

## 5. 问题四：现有功能（27 个工具）

### 5.1 只读 18 个（默认注册，`readOnlyHint=true`）

| 分类 | 工具 |
|---|---|
| 连接/实例（3） | `revit_ping`、`revit_document_info`、`revit_list_instances` |
| 目录/查询/聚合（3） | `revit_list_catalog`（8 段：categories, family-types, levels, area-schemes, views, worksets, phases, parameters）、`revit_aggregate_elements`、`revit_query_elements` |
| 视图与图像（5） | `revit_list_views`、`revit_view_summary`、`revit_view_elements`、`revit_view_warnings`、`revit_export_view`（PNG） |
| 几何（1） | `revit_element_details` |
| 告警/质量巡检（5） | `revit_list_warnings`、`revit_model_health`、`revit_links_status`、`revit_shared_coordinates`、`revit_parameter_fill_check` |
| 关系（1） | `revit_list_relations`（level-rooms / group-elements / nested-family / area-scheme-elements / view-template-dependents） |

契约由测试固定：`server/tests/test_server.py:18-37`（`EXPECTED_TOOLS`）与 `:39-133`（`EXPECTED_PARAMETERS`）。

查询边界：内置字段白名单仅 10 个（`id, category, family, type, name, level, workset, phase, areaScheme, hasWarnings`，`ElementFieldReader.cs:9-13`）；其它字段按“本地化参数名”走 `LookupParameter`（仅首个同名匹配）；过滤操作符 7 种；单位约定长度 mm、面积 m²、体积 m³。

### 5.2 写入/交互 9 个（`REVIT_MCP_ALLOW_WRITE=1` 才注册）

| 工具 | 子类 | dry_run | 可入 batch |
|---|---|---|---|
| `revit_select` | 交互（无事务） | 否 | 是 |
| `revit_show` | 交互 | 否 | 否 |
| `revit_isolate` | 交互（临时隔离） | 否 | 是 |
| `revit_move` | 模型变更 | 是 | 是 |
| `revit_place_family` | 模型变更 | 是 | 是 |
| `revit_create_wall` | 模型变更 | 是 | 是 |
| `revit_set_parameter` | 模型变更 | 是 | 是 |
| `revit_delete` | 模型变更（级联依赖） | 是 | 是 |
| `revit_batch` | 编排（≤50 步） | 是（整批回滚） | — |

### 5.3 能力缺口（当前**没有**的）

- 文档生命周期：保存、另存、关闭、打开模型、链接管理（仅只读 `links-status`）
- 工作共享：与中心模型同步、签出/借用图元、工作集切换
- 视图/图纸：创建/复制视图、放置视图到图纸、创建/编辑明细表与过滤器、视图模板编辑
- 族与类型：载入 `.rfa`、创建/删除类型与参数定义（共享参数、项目参数）
- 几何写入：除建墙与放族外，无楼板/梁柱/洞口/房间/面积边界，无标注与尺寸
- 数据交换：DWG/IFC/GBXML 导入导出（仅视图 PNG 导出）
- 交互：无撤销/重做工具、无对话框交互
- 查询：无几何谓词过滤（如“相交/在框内”），坐标仅随 `include_geometry` 附带

---

## 6. 问题五：扩展能力

### 6.1 四条扩展路径

**A. 新增只读工具（低风险，8 处同步改动）**
1. `revit_channel.py` 加 `ReadJob` classmethod（参考 `list_views` 模式）或复用 `universal_jobs.py`
2. `server.py` 加 `@addressed_tool` 函数**并登记标题映射**（`server.py:248-267`；漏登记直接 `KeyError`；标题 ≤40 字符）
3. `Core/ControlJobParser.cs` 的 `ControlJobKind` 枚举（`:8-31`）与 `FromContract` switch（`:155-176`）
4. `Core/Models/ReadCommandModels.cs` 增加 data 类型
5. `Addin/Capture/` 新增 reader（Revit API 只能出现在 Addin 项目）
6. `Control/ReadCommandExecutor.cs:41-135` 分发 switch 加 case
7. 长任务（>60s）参照 `ViewElementsSession`/`ViewDumpSession` 的“会话+分页 ExternalEvent”模式，并在 `ControlChannel.ProcessJob` 注册会话类型
8. 文档与测试：`docs/tools.md`、`README.md`、`docs/feed-format.md`、`test_server.py` 的 `EXPECTED_TOOLS/EXPECTED_PARAMETERS`、C# 解析器测试

**B. 新增写入工具（中风险，追加 7 处）**
`actions.py`（`@action` + 标题映射 + 必要时 `_BATCH_FIELDS`）→ `revit_channel.py` 的 `ACTION_COMMANDS` frozenset → `ActionJobParser.cs`（`IsAction`、参数校验、`ActionJobContract`）→ `ActionCommandExecutor.cs`（分发与事务策略）→ `ActionMutations.cs`（实际变更，注意单位换算与 `IsReadOnly`）→ `ActionVerifier.cs`（before/after 事实）→ 文档与测试。**硬性约束：保持双重门，不得放宽只读默认值。**

**C. 新增传输（低–中风险）**
Python 侧实现 `RemoteHost` 协议 5 方法（`prepare_job` / `wait_until_trigger_is_gone` / `wait_for_new_response` / `finish_job` / `delete_files`，`revit_channel.py:300-321`）＋ `list_revit_instances`，接入 `server.py:28-37` 的 `create_host`；插件侧新监听器复用 `ControlChannel.TrySubmit` 保住“单任务”不变量。安全约束：回环优先、无内建 TLS、请求体 1 MiB、`/health` 不鉴权、拒绝重定向。

**D. 新增 Revit 版本（中–高风险）**
条件编译机制已就绪（`REVIT20XX_OR_GREATER` 自动生成，已有 11 处使用）；改动清单见 §4.3；必须实机验证。

### 6.2 推荐实施顺序（风险由低到高）

1. （低）新增只读工具 / 查询字段 —— 纯增量，无安全面变化
2. （低–中）扩展传输 —— 实现 `RemoteHost` 协议，安全默认值不变
3. （中）新增写入工具 —— 必须复核双重门与 `dry_run`/`verification` 契约
4. （中–高）新增 Revit 版本 —— csproj/CI/install.ps1/打包 + 条件编译分支 + 实机验证
5. （高）批处理策略增强 —— `roadmap.md:17` 指出的确认令牌与无人值守策略目前尚不存在

### 6.3 优先级建议（结合能力缺口）

若目标是扩大实用价值，建议顺序：**保存/同步类动作（工作共享）→ 视图/图纸创建 → 族与参数定义 → DWG/IFC 导出 → 几何谓词过滤**。注意保存/同步会突破“动作永不保存”这一当前设计承诺，需要新的安全策略与文档修订，属于破坏性变更。

---

## 7. t1/t2 冲突消解与文档漂移

### 7.1 冲突点：文件通道的关联 ID 与原子性

| 来源 | 陈述 | 判定 |
|---|---|---|
| t1（架构） | 当前实现有 `correlationId`，响应通过临时文件 + `File.Replace/Move` 原子落盘 | ✅ **正确**，已独立核验（§1 步骤 1–5） |
| t2（使用） | “文件通道**无请求关联 ID、响应非原子写入**，客户端可能读到不完整 JSON”（引用 `docs/roadmap.md:10-11`、`docs/architecture.md:39-42`） | ❌ **仅反映过时文档，非当前代码事实** |

**核验证据（独立复现）**：
- `server/revit_model_mcp/revit_channel.py:346-347` 生成并注入 `correlationId`；`:388-399` 按 ID 过滤无关响应；`:465` 解析响应中的 `correlationId`。
- `src/RevitModelMcp.Core/Serialization/CommandResponseJsonSerializer.cs:34-41` 文件名含 `correlationId`；`:80-105` 临时文件 + `File.Replace`/`File.Move` + 最多 10 次重试 + `finally` 清理。
- `git log`：`5a65afc feat(channel): correlate responses by job id and publish atomically (#61)` 正是该修复；HEAD `dacdafd` 在其之后。
- `docs/architecture.md:39` 与 `docs/roadmap.md:10-11` 至今仍写旧状态，**属文档漂移**。

**因此**：这是一项**已修复的缺口**，最终结论按**当前代码**表述；在报告中作为**文档漂移风险**列出（§8-R1），而不是现状限制。

### 7.2 保留的关键澄清（t2，与 t1 一致）

**MCP 客户端 ↔ Python 服务永远是 stdio；`local`/`ssh:`/`http(s)` 只是 Python ↔ 插件通道。** 证据：`server.py:780` `mcp.run(transport="stdio")`；`server.py:30-37` 的 `create_host` 只解析三种宿主。项目不提供 SSE/Streamable HTTP 端点。这是最容易被误解的一点，必须在报告显著位置保留。

### 7.3 其它已确认的文档漂移

| # | 文档 | 现状 |
|---|---|---|
| 1 | `docs/architecture.md:39` “The file protocol has no request correlation identifier.” | 已有 `correlationId` |
| 2 | `docs/roadmap.md:11` “File responses: writes are not atomic…” | 已原子发布（临时文件 + Replace/Move + 10 次重试） |
| 3 | `docs/roadmap.md:10` “jobs lack correlation IDs and interprocess response ownership” | 已有；但“一个通道目录一个服务进程”的建议**仍然有效**（`asyncio.Lock` 只保证进程内串行） |
| 4 | `docs/roadmap.md` 审阅日期 2026-09-12，HEAD 2026-09-18 | 引用 roadmap 缺口清单时必须声明“审阅日期早于 HEAD” |
| 5 | `RevitModelMcp.sln` 只列 `R22–R26` | `csproj:15-16` 与 CI/release 已覆盖 `R27` |

---

## 8. 风险清单（按优先级）

| # | 风险 | 严重度 | 说明与建议 |
|---|---|---|---|
| R1 | **文档漂移误导使用者**（`architecture.md:39`、`roadmap.md:10-11` 描述的缺口已修） | 中 | 本次分析已按代码更正；建议上游同步修订文档，否则后续 agent/用户会重复得出“无关联 ID、非原子”的错误结论 |
| R2 | **实机验证覆盖极窄**：仅 Revit 2026 有真实读写验证 | 高 | `docs/validation.md:20`。2022/2023/2025/2027 只有编译证据；迁移/升级判断不能以 CI 绿灯为凭据 |
| R3 | **超时语义易误判**：超时不取消已接受的 job，动作可能已执行 | 高 | `revit_channel.py:412-420`、`docs/architecture.md:75-78`。调用方必须先查模型再决定重试 |
| R4 | **并发即冲突**：插件同一时刻只处理一个 job，并发调用撞 busy | 中 | `ControlChannel.cs:25-37`；实测 7 并发中 4 失败。建议客户端串行化或改用 HTTP 轮询 |
| R5 | **单进程假设**：响应归属由 `correlationId` 保证，但同一通道目录跑多个服务进程仍会互相干扰 | 中 | `asyncio.Lock` 是进程内的；保持“一目录一进程” |
| R6 | 脱敏边界有限：`REVIT_MCP_REDACT_PATHS` 只覆盖 `documentPath` 与嵌套 `path` | 中 | 模型名、参数值、错误文本、通道文件、导出图片 `localPath` 仍可见 |
| R7 | `/health` 免鉴权且泄露文档名与 PID | 低–中 | 回环绑定下影响有限；一旦放通局域网需评估 |
| R8 | 未签名 MSI、HTTP 无内建 TLS | 中 | 用 `gh attestation verify` 校验来源；远端走 SSH 隧道/Tailscale |
| R9 | 写操作设计承诺“永不保存模型”，扩展保存/同步会突破该承诺 | 中 | 扩展规划时必须同步更新安全策略与文档 |
| R10 | 2020 迁移的单位/类型 API 代际分支可能引起能力降级，且 Revit 2020 已 EOL、RVT 不向后兼容 | 中–高 | 见 §4.3.1、§4.5：需永久维护旧分支、`BasePoint.Clipped` 等字段需屏蔽、需单独采集 2020 期模型；无官方 CI 只能人工冒烟 |
| R11 | `Polyfill`/TFM 陷阱：SDK 对 2020 默认 `net47` 会让 `ToHashSet` 缺失并连带 5 处编译错误 | 中（仅 2020 迁移时） | `RevitModelMcp.Addin.csproj` 必须显式覆盖为 `net472`；Core 必须先加 `net472` 目标否则 `NU1201` |

---

## 9. 核验方法与证据索引

### 9.1 本次汇总独立执行的核验

```sh
# 关联 ID 与原子性
grep -n "correlation" server/revit_model_mcp/revit_channel.py      # 346,347,348,375,390,393,409,465
sed -n '80,105p' src/RevitModelMcp.Core/Serialization/CommandResponseJsonSerializer.cs
sed -n '86,96p' server/revit_model_mcp/ssh_host.py                 # WriteAllBytes + File.Move
sed -n '308,328p' src/RevitModelMcp.Addin/Control/ControlChannel.cs
git log --oneline -8                                                # 5a65afc 修复提交

# stdio 澄清
grep -n "mcp.run" server/revit_model_mcp/server.py                  # 780: transport="stdio"
sed -n '28,37p' server/revit_model_mcp/server.py                    # create_host 三宿主

# 版本矩阵与 2020 工作量
sed -n '15,16p' src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj  # Debug/Release.R22…R27
grep -n "202\[2-7\]\|2022\.\.2027" install.ps1                      # 33,117,170-172
grep -rn "SpecTypeId\.\|UnitTypeId\.\|ForgeTypeId\|GetDataType" src --include=*.cs | wc -l   # 33 行 / 9 文件
grep -rn "REVIT20[0-9][0-9]_OR_GREATER" src --include=*.cs | wc -l  # 11
sed -n '41,48p' ~/.nuget/packages/nice3point.revit.sdk/6.2.3/Sdk/Nice3point.Revit.Common.props
# NuGet 2020 可用性（api.nuget.org flatcontainer）
#   revitapi: 2020.2.11, 2020.2.60 | revitapiui: 同上
#   toolkit: 2020.0.0 … 2020.4.0 | extensions: 2020.0.0 … 2020.5.4
```

### 9.2 上游分析产出

- t1：架构与运行链路（team.json 任务输出）
- t2：`/tmp/revit-mcp-analysis/t2-usage.md`（含本机实测证据：`--help`、`--host` 非法值、MCP stdio 探测 18/27 工具、pytest 251 passed）
- t3：Revit 版本与 2020 迁移（compatibility-analyst）——**唯一带真实编译实验的专项**：临时副本 + 仓库固定 SDK 10.0.100，R22 对照构建成功、R20 实测 41 错误；并用 `System.Reflection.Metadata` 比对 RevitAPI 2020.2.60 / 2021.1.50 / 2022.1.80 的成员面
- t4：`analysis/t4-features-and-extension.md`（193 行，逐条文件:行证据）

### 9.3 核验中修正/校准的上游数据

| 上游陈述 | 本报告值 | 原因 |
|---|---|---|
| t4：ForgeTypeId 代 API “9 个文件共 25 处” | 源码引用 **9 个文件 33 行**（按行去重；分项：SpecTypeId 16 / UnitTypeId 9 / GetDataType 7 / ForgeTypeId 3）；真实编译**错误 41 个 / 10 个文件** | t4 口径未含 `ForgeTypeId` 类型名与部分 `GetDataType`；t3 的错误数含类型声明与多次调用，两者是不同度量，已在 §4.3.1 说明 |
| t3：“现有条件编译点 9 文件 12 处” | **11 处** `REVIT20XX_OR_GREATER`（另有 1 处 `NETFRAMEWORK`，故 t3 的 12 处含它） | 统计口径差异：t3 把 `HttpChannel.cs:368` 的 `NETFRAMEWORK` 也计入；本报告把它单列 |
| t1：解决方案仅 R22–R26、无 R27 | **支持 R27**（csproj 与 CI/release 覆盖）；sln 确实缺 R27 配置 | `RevitModelMcp.sln` 配置列表滞后于 csproj/工作流；t3 亦独立发现该缺口，建议随 R20 一并补 |
| t2：文件通道无关联 ID、响应非原子 | **已修复**，按当前代码表述 | t2 引用的是 `docs/architecture.md:39`、`docs/roadmap.md:10-11` 的过时文档（§7.1） |
