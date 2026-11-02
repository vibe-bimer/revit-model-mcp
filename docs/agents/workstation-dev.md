# 在 Windows 工作站上开发

本页说明在运行 Revit 的那台 Windows 工作站上直接开发本仓库的方法。工作站上跑着 Revit，插件就在同一台机器上，因此构建即部署、调用即本地，不必在开发机和工作站之间搬运文件。

!!! note "适用范围"
    本页描述的是在工作站本机做开发调试的流程。如果开发机与工作站分离，请改用远程通道，命令见[传输配置](../transport.md)。

<a id="the-two-machines"></a>
## 两台机器的分工

| 位置 | 用途 | 通道 |
| --- | --- | --- |
| 开发机（本页不涉及） | 编辑、提交、推送 | 远程 |
| 工作站（本页） | 构建插件、运行 Revit、做真机验收 | 本地通道 |

工作站的仓库路径：`C:\Users\Administrator\revit-model-mcp`。

<a id="toolchain"></a>
## 工具链

工作站已经装好：

- .NET SDK 10.0.401 与 8.0.427（`global.json` 要求 10.0.100，`rollForward: latestMinor` 因此满足）；
- Python 3.14 与 `uv`（`C:\Users\Administrator\.local\bin\uv.exe`）；
- Git、VS Code。

工作站没有 Visual Studio 或 Rider，只有 VS Code。VS Code 装 C# 扩展（`ms-dotnettools.csharp`）后可以断点调试。

<a id="one-time-setup"></a>
## 一次性准备

```powershell
cd $env:USERPROFILE\revit-model-mcp\server
uv sync                      # 安装服务器依赖，版本取自 server/pyproject.toml
```

`uv sync` 会把本仓库以可编辑方式装进环境。**不跑这一步，服务器会认为 add-in 版本是 0.0.0**，所有调用都被拒：

> This server needs a Model MCP add-in of major version 0; the Revit workstation has 1.0.0+…

<a id="the-dev-loop"></a>
## 开发循环

### 1. 关 Revit

插件的 DLL 被 Revit 锁着，构建前必须关掉。

```powershell
# 先确认模型没有未保存的改动
# （在工作站本机用 MCP 客户端调用 revit_ui_state，看 activeDocument.isModified）
Stop-Process -Name Revit -Force
```

`CloseMainWindow()` 会被保存提示挡住，验收之后关 Revit 一律用 `Stop-Process -Force`——前提是模型本来就没被保存过。

### 2. 构建并部署

csproj 里 `DeployAddin` 默认是 `true`，Nice3point SDK 在 Windows 上会把产物直接写进 add-in 目录，所以一条命令就完成了构建与部署：

```powershell
cd $env:USERPROFILE\revit-model-mcp
dotnet build src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj -c Debug.R26 -p:LaunchRevit=false
```

部署目标是 `%APPDATA%\Autodesk\Revit\Addins\2026\RevitModelMcp\`。

首次在新克隆上构建会失败一次：

```
error NETSDK1004: ... Assets file ... not found. Run a NuGet package restore
```

这是因为构建末尾的 `PinMergedRevitApiReferences` 目标会用 `dotnet run --no-restore` 调 `build/RevitApiReferencePin`，而那个子项目还没还原。**先单独还原一次即可**：

```powershell
dotnet restore build/RevitApiReferencePin/RevitApiReferencePin.csproj
```

之后 `dotnet build` 就不会再失败。

年份换 `Debug.R22`／`Debug.R27` 同理，部署目录里的年份跟着变。本仓库的 csproj 只有 R22–R27 配置，没有 R20。

### 3. 签名

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $env:USERPROFILE\sign-addin.ps1
```

证书是 `CN=RevitModelMcp Dev`。脚本对每个年份目录里的 `RevitModelMcp.dll` 重新签名，输出形如 `2026: RevitModelMcp.dll signed`。**每次部署新构建后都要重签一次**。

### 4. 起 Revit

SSH 进来的命令跑在 Windows session 0，`Start-Process Revit.exe` 起不来（进程立刻退出）。交互会话在 session 1，用计划任务启动：

```powershell
schtasks /Run /TN RevitMcpLaunchVerify
```

这个任务跑 `C:\Users\Administrator\startrevit.ps1`，打开 `E:\revitmcp-test\mcp-verify-2026.rvt`。约 75–90 秒后 Revit 起来。

仓库里另有 `RevitMcpLaunch` 任务，它打开的是另一个大项目模型，验收时不要用。

### 5. 用本地通道调用

```powershell
cd $env:USERPROFILE\revit-model-mcp\server
$env:REVIT_MCP_HOST = 'local'
uv run python -m revit_model_mcp.server
```

`REVIT_MCP_HOST=local` 让服务器用本机 PowerShell 写同一个通道目录 `%LOCALAPPDATA%\RevitModelMcp\`，没有 SSH 往返。实测 `revit_ping` 约 0.4 秒、`revit_list_catalog` 约 0.04 秒。

<a id="debugging"></a>
## 下断点

`Fork*` 层的动作代码都在静态方法里，断点很好下：

- `src/RevitModelMcp.Addin/Fork/ForkColumns.cs` — `Apply`／`Validate`／`Read`；
- `src/RevitModelMcp.Addin/Fork/ForkGrids.cs`、`ForkFamilies.cs` — 同构；
- `src/RevitModelMcp.Addin/Fork/ForkActions.cs` — 三个 switch，决定命令分派到哪个 Fork 类。

在 VS Code 里打开「运行和调试」，选「附加到进程」，附加 `Revit.exe`，再触发一次 MCP 调用就会停在断点上。

在没有 IDE 的情况下，只能靠响应 JSON 反推——例如用 `verification.after` 的 `boundingBoxMinMm`／`boundingBoxMaxMm` 判断旋转和偏移是否生效。

<a id="gates"></a>
## 门禁

Windows 上有些门禁的表现和开发机不同：

- **C# 格式化钩子会真的执行**。`pre-commit` 的 `dotnet format` 钩子在非 Windows 上只打印提示并跳过，在 Windows 上会实际改文件。第一次跑可能会冒出一批格式改动，提交前先看一遍 diff。
- **行尾**。仓库有 `.editorconfig` 和 Git 的 CRLF 设置，不要改 `core.autocrlf`。
- **PowerShell 脚本编码**。含中文的 `.ps1` 必须是 UTF-8 with BOM，否则 PowerShell 按 GBK 解析并报「字符串缺少终止符」。
- **命令输出编码**。SSH 回来的 PowerShell 输出是 GBK，管道里用 `iconv -f GBK -t UTF-8` 转一下再读。

完整的门禁清单：

```powershell
cd $env:USERPROFILE\revit-model-mcp
dotnet test --project tests/RevitModelMcp.Core.Tests/RevitModelMcp.Core.Tests.csproj
cd server; uv run --with pytest pytest -q
cd ..; uvx ruff==0.16.10 check .; uvx ruff==0.16.10 format --check .
pre-commit run --all-files
python build/check_fork_budget.py
```

<a id="the-fork-bound"></a>
## fork 层的边界

新增动作工具必须走 fork 层：`src/RevitModelMcp.Core/Fork/`、`src/RevitModelMcp.Addin/Fork/`、`server/revit_model_mcp/fork_actions.py`。

`build/check_fork_budget.py` 会把改动过的文件分成三类：hook（9 个分派文件，共 80 行预算）、read（`build/fork.json` 的 `reads` 表里逐个列出并附理由）、fork（路径前缀匹配）。**任何不在这三类的文件都会被判为 unowned 而让门禁失败**——上游的 `ActionMutations.cs` 就在这一类之外，所以不能改它。

工具注册后 `ForkRegistry.IsAction` 自动生效，`ActionJobParser.cs` 不需要为 fork 命令写任何校验分支——校验写在各自的 `Fork*.cs` 的 `Validate` 里。

<a id="verification"></a>
## 真机验收

验收记录写进 `docs/validation.md` 与 `docs/validation.en.md`，格式照 `revit_create_level` 那一段。每个动作至少覆盖：

1. `dry_run` 回滚后 `isModified` 仍为 `false`，回滚掉的构件 id 用 `revit_element_details` 查不到；
2. 真实写入后 `verification.after` 里有 id、类别、类型与包围盒；
3. 错误路径有明确的拒绝理由；
4. 写入之后模型文件的**大小与 mtime 都不变**——动作不保存模型。

`revit_ui_state` 的 `activeDocument.isModified` 是判断模型状态的入口。

模型里未必有需要的族。真机验收常用的族文件：

- 柱：`C:\ProgramData\Autodesk\RVT 2020\Libraries\China\结构\柱\混凝土\混凝土 - 正方形 - 柱.rfa`；
- 门：`C:\ProgramData\Autodesk\RVT 2020\Libraries\China\建筑\门\其它\入口门厅.rfa`。

2026 的中文族库只有「结构预制」「路径分析」两个目录，结构柱族只在 2020 库里。

<a id="year-limits"></a>
## 年份限制

本仓库的 csproj 只有 R22–R27 配置。`Release.R20` 会 restore 失败，所以 **2020 年份的真机验收在这个仓库内做不了**——validation 文档要如实写「2020 无记录」，不要假装做过。工作站上装了 2020 版 Revit，但插件没有 2020 的构建配置。
