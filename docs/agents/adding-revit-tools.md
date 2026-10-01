# 新增 Revit 工具

本页说明如何为本仓库新增读取工具、动作工具，或接入新的 Revit API。编写代码前，请从头到尾完成本页的流程。

!!! note "原文的历史范围"
    本页完整翻译英文指南。原文中的语料库覆盖范围、工作站部署记录及“下一项动作工具”示例反映该指南记录时的状态，不代表新增的真机验证证据；发布前仍须逐年核实 API 和模型行为。

<a id="step-0-verify-the-api-in-the-local-corpus"></a>
## 步骤 0：在本地语料库中核实 API

本地 Revit 2026 API 参考位于 `revit-corpus/`（28,796 篇 CHM 文档，带 FTS5 索引）。这是可选的机器本地数据：如果目录不存在，直接跳过本步骤，改查官方文档，无须专门提示目录缺失。

在仓库根目录使用命令行查询：

```sh
python3 revit-corpus/scripts/corpus_query.py overloads Floor.Create   # 每个重载的文档页
python3 revit-corpus/scripts/corpus_query.py members FilteredElementCollector -k method
python3 revit-corpus/scripts/corpus_query.py 'Floor' -k class --show
```

也可以通过 `revit-docs` MCP 连接器查询（`revit_docs_symbol`、`revit_docs_search`、`revit_docs_read`）。`revit_docs_symbol` 接受不加引号的点分符号名，并代为处理 FTS 引号。

请阅读完整文档，而不只是签名：重载、参数、返回值、异常和备注都很重要。例如，`FilteredElementCollector` 至少需要一个过滤器，并应优先使用原生过滤器而非 LINQ。

<a id="read-tool-checklist-8-sync-points"></a>
## 读取工具清单（8 个同步点）

基于任务的读取工具需要同时修改通道的两端：

1. **Python 任务构造**：在 `server/revit_model_mcp/revit_channel.py` 中新增 `ReadJob` 类方法（参考 `list_views`）；共享过滤语义放入 `universal_jobs.py`。
2. **MCP 注册**：在 `server.py` 中新增 `@addressed_tool` 函数，并在标题映射中增加对应条目。遗漏条目会触发 `KeyError`；标题最多 40 个字符（由测试强制检查）。
3. **Core 契约**：扩展 `ControlJobKind` 和 `Core/Control/ControlJobParser.cs` 中的 `FromContract` 分支（通用查询使用 `UniversalJobParser.cs`）。
4. **Core 模型**：在 `Core/Models/ReadCommandModels.cs` 中新增响应数据类型。
5. **插件读取器**：在 `src/RevitModelMcp.Addin/Capture/` 下新增读取器。Revit API 引用只能出现在 Addin 项目中，不能出现在 Core 中。
6. **插件分发**：在 `Control/ReadCommandExecutor.cs` 中新增分支。
7. **长任务**：如果单次 ExternalEvent 可能超过 60 s，请采用 `ViewElementsSession.cs` 中的分页会话模式，并在 `ControlChannel.ProcessJob` 中注册会话。
8. **文档与测试**：更新 `docs/tools.md`、`README.md`、`docs/feed-format.md`；更新 `server/tests/test_server.py` 中的 `EXPECTED_TOOLS` 和 `EXPECTED_PARAMETERS`；在 `tests/RevitModelMcp.Core.Tests/` 下补充解析器测试。

新增读取工具必须保持 `readOnlyHint=true`，不得放宽默认只读行为。

<a id="action-tool-checklist-7-additional-points"></a>
## 动作工具清单（额外 7 点）

动作工具扩展读取通道，必须遵循相同的约束：

1. `server/revit_model_mcp/actions.py`：新增 `@action` 函数和标题条目；将允许批处理的参数加入 `_BATCH_FIELDS`。
2. `revit_channel.py`：将命令加入 `ACTION_COMMANDS`，以保持正确的超时与错误语义。
3. `Core/Control/ActionJobParser.cs`：更新 `IsAction`、参数校验和 `ActionJobContract` 字段。
4. `Addin/Control/ActionCommandExecutor.cs`：增加分发分支和事务策略（试运行回滚、警告处理、对话框抑制）。
5. `Addin/Control/ActionMutations.cs`：实现变更本身。显式转换单位（输入为 mm，内部为英尺），并拒绝只读目标。
6. `Addin/Control/ActionVerifier.cs`：记录变更前后的事实；在 `docs/feed-format.md` 中说明响应结构。
7. **文档与测试**：更新 `docs/actions.md`、`README.md`、`server/tests/test_actions.py`。

硬性约束：

- 保留两道写入门禁：服务器环境中的 `REVIT_MCP_ALLOW_WRITE=1` 和工作站上的 `allow-write` 文件。不得削弱其中任何一道。
- 变更操作支持 `dry_run`，并返回 `verification` 块。
- 动作不得保存模型。
- Revit 2022–2023 仅接受不超过 2,147,483,647 的元素 ID。
- `place_family` 使用基于标高的非结构重载；有宿主、基于面和自适应族不在支持范围内。
- 超时后，先检查模型再重试；任务可能已经执行。

<a id="worked-example-revit_create_floor"></a>
## 实现示例：`revit_create_floor`

原文将其列为下一项动作工具。Revit 2026 语料库中的事实如下：

- `Floor.Create(Document, IList<CurveLoop>, ElementId floorTypeId, ElementId levelId)` — 核心重载。
- `Floor.Create(Document, IList<CurveLoop>, ElementId, ElementId, Boolean, Line, Double)` — 带坡度的结构变体。

设计说明：

- 接受模型坐标中的 mm 点，用 `Line.CreateBound` 线段构造 `CurveLoop`，并显式闭合边界。
- 通过 `FloorType` 的 `FilteredElementCollector` 按名称解析 `floor_type`（`null` 选择第一个基本楼板类型）；按精确名称解析 `level`。
- 校验器：变更前为空，变更后为新建元素的元数据及包围盒，与 `revit_place_family` 一致。
- 将 `create_floor` 加入 `_BATCH_FIELDS`，使其可以组合进 `revit_batch`。
- 测试矩阵：试运行回滚、真实创建及校验、错误类型名报错、拒绝未闭合边界。

<a id="build-and-deploy"></a>
## 构建与部署

- Linux 上可用以下命令检查编译：
  `dotnet build src/RevitModelMcp.Addin -c Release.R26 -p:DeployAddin=false -p:EnableWindowsTargeting=true`。
  对于 `net8.0-windows` 目标，仅设置 `UseWPF=false` 不够：WindowsDesktop 引用包通过 `EnableWindowsTargeting` 解析。完整构建仍以 Windows PR CI 为准。
- 运行 `dotnet test --project tests/RevitModelMcp.Core.Tests/RevitModelMcp.Core.Tests.csproj` 和 `cd server && uv run --with pytest pytest -q`。
- 在环境中设置 `EnableWindowsTargeting=true` 后，Linux 上也能运行 `dotnet format --verify-no-changes`（按照 AGENTS.md，同时设置 `Configuration=Debug.R26` 和 `DeployAddin=false`）：
  `env 'EnableWindowsTargeting=true' Configuration=Debug.R26 DeployAddin=false dotnet format RevitModelMcp.sln --verify-no-changes --verbosity minimal`。
  可能出现工作区加载警告；退出码为 0 即通过。完整构建矩阵和打包仍以 Windows PR CI 为准。
- **部署到工作站**：ILRepack 只在 Windows 构建中运行，因此 Linux 构建会生成独立程序集。通过 SSH 将 `RevitModelMcp.dll`、`RevitModelMcp.Core.dll`、`JetBrains.Annotations.dll`、`Nice3point.Revit.Extensions.dll`、`Nice3point.Revit.Toolkit.dll`、`RevitModelMcp.deps.json` 和 `RevitModelMcp.runtimeconfig.json` 复制到 `%APPDATA%\Autodesk\Revit\Addins\2026\RevitModelMcp\`。先备份该目录；Revit 运行时已加载的 DLL 会被锁定，因此只能在 Revit 关闭后部署。
- **每次部署后都为 DLL 签名**。Revit 每次启动都会提示未签名插件，而每次重新构建都会改变文件哈希，因此“Always Load”不会持续生效。记录中的工作站保留一张自签名代码签名证书（`CN=RevitModelMcp Dev`，已加入 LocalMachine 的 TrustedPublisher 和 Root 信任存储）。在 Revit 关闭后通过 SSH 运行辅助脚本：

  ```sh
  ssh revit-host 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Administrator\sign-addin.ps1'
  ```

  一次性证书设置（记录中的工作站已经完成）：
  `New-SelfSignedCertificate -Subject "CN=RevitModelMcp Dev" -Type CodeSigningCert -CertStoreLocation Cert:\CurrentUser\My`，随后将证书加入 LocalMachine 的 TrustedPublisher 和 Root。参见 [Autodesk 关于代码签名窗口反复出现的说明](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/The-code-signing-window-always-appears-when-launching-Revit.html)。
- **远程重启 Revit 时，先正常关闭而非强制终止**：先请求 `CloseMainWindow()`；只有确认模型没有未保存改动后，才退回 `Stop-Process`。`revit_document_info` 会报告 `isModified`；强制终止会丢弃未保存编辑，历史上已经因此丢失过一整个会话的人工阶段操作。通过交互式计划任务 `RevitMcpLaunch`（`schtasks /Run /TN RevitMcpLaunch`）重新启动，让 GUI 出现在控制台会话中。强制终止后，删除 `%LOCALAPPDATA%\RevitModelMcp` 下过期的 `instance_<pid>.json` 心跳，否则动作会报告“exactly one instance”约束违规。
- 只有当 Python 服务器从本克隆运行（`uv run --directory server revit-model-mcp`）而不是从已发布的 `uvx revit-model-mcp` 包运行时，MCP 客户端才能获得新增工具。开发时将连接器指向本克隆。
- **通过 `revit` MCP 连接器进行真机冒烟测试**：先调用 `revit_ping`，再以 `dry_run=true` 调用新工具，最后真实执行、核对 `verification` 并清理。

<a id="revit-2020-builds"></a>
### Revit 2020 构建

`Debug.R20` 和 `Release.R20` 针对 Revit 2020 构建插件。有两项约束：

- `Nice3point.Revit.Api.RevitAPI` 2020 包对应更新后的 Revit 2020，而工作站可能仍运行原始 2020 版本，缺少约九十个成员。将版本特定代码放在 `src/RevitModelMcp.Addin/Compatibility/` 中；使用新的 Revit 2020 调用前，先对照已安装 `RevitAPI.dll` 旁的 `RevitAPI.xml` 核实。`BasePoint.GetProjectBasePoint` 和 `BasePoint.GetSurveyPoint` 访问器就是这样的例子。
- 未签名插件会让 Revit 停在发布者对话框。每次部署后，用 `RevitModelMcp Dev` 证书为已部署的 `RevitModelMcp.dll` 签名，方式与 `sign-addin.ps1` 为其他已安装年份签名相同。

<a id="known-revit-api-limits"></a>
## 已知 Revit API 限制

以下结论已确定，无须重复调查。

- **无法通过 API 创建或重命名阶段。** 不存在 `NewPhase` 或 `Phase.Create`；对 `Document.Phases` 调用 `PhaseArray.Append/Insert` 不会持久化。所有重命名路径都会失败：`BuiltInParameter.PHASE_NAME` 为只读，`Element.Name` 会抛出 `"This element does not support assignment of a user-specified name"`（已在 Revit 2026 真机复现；[2025 年 Autodesk 论坛讨论](https://forums.autodesk.com/t5/revit-api-forum/is-it-possible-to-control-phases-using-the-revit-api/td-p/13631528) 和 [2021 年讨论](https://forums.autodesk.com/t5/revit-api-forum/how-to-create-project-phase-programly/td-p/9722434) 也报告了相同错误）。阶段必须在阶段对话框（Manage > Phases）中创建和命名；应在项目模板中统一阶段集合。
- **可以合并阶段**，这也是 `revit_merge_phases` 的实现方式：重新分配所有 `CreatedPhaseId` 或 `DemolishedPhaseId` 指向源阶段的元素，再删除清空后的阶段。这与 Autodesk 支持在[阶段合并讨论](https://forums.autodesk.com/t5/revit-api-forum/merge-phases/td-p/5594567)中说明的方法一致。
- **可以通过模拟按键驱动阶段对话框，但很脆弱**：提交 `ID_SETTINGS_PHASES` 命令并模拟按键，可以创建和重命名阶段，[Dynamo 论坛示例](https://forum.dynamobim.com/t/creating-phases-renaming-phases/114509)展示了这一点。它需要可见屏幕来校准 Tab 顺序；按键序列出错会让 Revit 被对话框阻塞，绝不可无人值守使用。

<a id="version-caveats"></a>
## 版本注意事项

原文所述语料库仅覆盖 Revit 2026。在语料库中查到成员，不代表它在 2022–2025 或 2027 中可用：检查现有的 `REVIT20XX_OR_GREATER` 条件编译（原文记录 11 处使用），并在 API 不同时添加逐年分支。发布支持声明前，每个受支持年份都必须完成真机模型验证。
