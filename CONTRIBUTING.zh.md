# 参与贡献

错误报告和功能请求请使用 [Issue 表单](https://github.com/sharafutdinovdi/revit-model-mcp/issues/new/choose)。
错误报告应包含 Revit 年份、插件版本、安装方法、传输方式、复现步骤和已脱敏日志。
对于可见故障，请在表单的截图字段附上对话框或功能区截图。
使用和安装问题请前往 [Discussions](https://github.com/sharafutdinovdi/revit-model-mcp/discussions)。

贡献者须遵守[行为准则](https://github.com/sharafutdinovdi/.github/blob/main/CODE_OF_CONDUCT.md)。

<a id="pull-requests"></a>
## 拉取请求

1. 进行大型变更前先创建 Issue，并就预期行为达成一致。
2. Fork 仓库，克隆 fork，并从 `main` 创建聚焦的分支，例如 `git switch -c fix/http-timeout`。
3. 完成修改，并运行下述相关检查。
4. 提交和 PR 标题使用 Conventional Commits，例如 `fix(server): handle connection timeouts` 或 `feat(addin): expose view metadata`。
5. 推送分支并向 `main` 创建 PR；填写摘要、关联 Issue 和检查清单。
6. 任何 UI 或功能区变更，都要将截图／录像拖放到 PR 的验证部分，或从剪贴板粘贴图像。
7. 从附件和日志中移除凭据、私有模型名称及路径。

PR 清单涵盖受支持的 Revit 构建、测试、文档、截图和秘密信息。
在验证部分写明命令、结果及受影响的 Revit 年份；不适用的检查项也要明确说明。
代码和公开 API 描述使用英文。

`main` 要求通过 PR 合并，并要求分支为最新且所有必需检查通过。
不存在一概要求审批的规则。
[CODEOWNERS](.github/CODEOWNERS) 中的路径需要所有者审核：

- `src/` 下的插件和 Core 源码，但项目依赖清单除外。
- `server/revit_model_mcp/` 下的 Python 运行时代码。
- `build/install/` 下的安装器代码和根目录安装脚本。
- Release、release-please、WinGet 和 Dependabot 自动合并工作流。
- CODEOWNERS、安全政策和许可证。

没有指定所有者的文档、测试、其他 CI 工作流和依赖清单，可在必需检查通过后合并。
Dependabot 的补丁和次版本更新启用 squash 自动合并；必需检查及任何所有者审核仍然适用。
主版本更新会添加 `needs-review` 标签，并等待维护者处理。
`build/install/` 下的 NuGet 清单及发布工作流更新仍需所有者审核。
所有合并均使用 squash，并采用 PR 标题和正文，保持线性历史。

<a id="automated-checks"></a>
## 自动检查

CI 构建 Revit 2020、2022、2026 和 2027 插件，运行 Core 和 Python 测试，构建并冒烟测试两种 MSI 安装范围，并校验 Python 包。
PR 检查校验 Conventional Commit 标题，用 `actionlint` 检查所有工作流文件，按照 `.editorconfig` 检查 C# 格式，并用 Ruff 检查 Python lint 与格式。
CodeQL 在 PR、推送到 `main` 和每周计划中分析 C# 与 Python。
PR 检查成功后，会发布并更新一条评论，包含插件产物链接和已构建的 Revit 年份。
下载产物需要登录 GitHub，产物在 90 天后过期。
共享的 `community.yml` 工作流添加路径标签、欢迎贡献者，并处理长期无活动的 Issue 和 PR。
共享的 `dependabot-auto-merge.yml` 工作流负责依赖更新审核与自动合并。
PR 检查调用共享的 `check-failure-comment.yml` 工作流，为同仓库、非 Dependabot 的 PR 维护一条失败评论，其中包含复现命令。
这些工作流维护于 [sharafutdinovdi/.github](https://github.com/sharafutdinovdi/.github#caller-workflows)。
路径标签自动添加；`enhancement`、`bug`、`docs` 和 `dependencies` 用于对生成的发布说明分组。

<a id="local-checks"></a>
## 本地检查

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)、Python 3.11+、`global.json` 选定的 .NET SDK，并将 actionlint 1.7.12 加入 PATH。
从仓库根目录运行：

```sh
uv tool install pre-commit
pre-commit install
pre-commit run --all-files
```

钩子应用 Ruff 0.16.7 修复和格式化、验证 C# 格式、检查工作流，并检查文件结尾、空白、YAML 和 JSON。
C# 钩子设置 `Configuration=Debug.R26` 和 `DeployAddin=false`，在 C# 文件变更时运行一次。
完整解决方案的格式检查需要 Windows；macOS 和 Linux 贡献者可运行 `SKIP=dotnet-format pre-commit run --all-files`，并以 Windows PR 检查作为 C# 格式的依据。
再次提交前，审核钩子修改并将其暂存。

<a id="build-and-test"></a>
## 构建与测试

在 Windows 上，从全新克隆的仓库根目录运行，使用 `global.json` 选定的 .NET SDK：

```powershell
foreach ($year in '20', '22', '23', '24', '25', '26', '27') {
    dotnet build src/RevitModelMcp.Addin -c "Release.R$year" -p:DeployAddin=false
    if ($LASTEXITCODE -ne 0) { throw "R$year build failed" }
}
dotnet test --project tests/RevitModelMcp.Core.Tests/RevitModelMcp.Core.Tests.csproj
$env:Configuration = 'Debug.R26'
$env:DeployAddin = 'false'
dotnet format RevitModelMcp.sln --verify-no-changes --verbosity minimal
```

`DeployAddin=false` 防止部署到本地 Revit 安装。
Core 测试不需要正在运行的 Revit 实例。
测试运行器为 Microsoft.Testing.Platform；按示例使用 `--project`。
七个 Release 构建覆盖 `Release.R20` 和 `Release.R22` 至 `Release.R27`：Revit 2020 和 2022–2027，不支持 Revit 2021。
要应用格式化，请设置相同环境变量并运行 `dotnet format RevitModelMcp.sln`。

在 Windows、macOS 或 Linux 上，使用 Python 3.11+ 和 uv 运行 Python 测试及包构建：

```sh
cd server
uv run --with pytest pytest -q
uvx ruff==0.16.7 check .
uvx ruff==0.16.7 format --check .
uv build
uvx twine check dist/*
```

传输测试使用模拟操作和本地伪 HTTP 服务器。
这些测试不需要 Windows 工作站。
凭据和模型文件不得进入提交，测试夹具应脱敏。
运行 `uvx ruff==0.16.7 check --fix .` 和 `uvx ruff==0.16.7 format .`，应用 Python lint 修复和格式化。
修改工作流后，从仓库根目录运行 `actionlint` 1.7.12。

<a id="documentation-site"></a>
## 文档站点

文档站使用 MkDocs Material，并包含仓库和服务器的 README。
从仓库根目录预览：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r docs/requirements.txt
.venv/bin/mkdocs serve
```

Windows 上使用 `.venv\Scripts\python.exe` 和 `.venv\Scripts\mkdocs.exe`。
打开 `http://127.0.0.1:8000/revit-model-mcp/`。
提交 PR 前，在已激活环境中运行 `mkdocs build --strict`。

中英文文档必须同步维护。工具页面和导航根据当前 MCP 注册表快照 [`tools.json`](https://github.com/sharafutdinovdi/revit-model-mcp/blob/main/tools/site/content/tools.json)、[`capabilities.yaml`](https://github.com/sharafutdinovdi/revit-model-mcp/blob/main/tools/site/content/capabilities.yaml) 中经审核的双语标题、摘要、提示词和参数含义，以及 [`contracts.yaml`](https://github.com/sharafutdinovdi/revit-model-mcp/blob/main/tools/site/content/contracts.yaml) 中完整的中文工具描述生成。工具描述、签名、schema 或注册发生变化后，激活文档环境，并用 `python -m pip install -e server` 使服务器可导入，然后更新快照：

```sh
python tools/site/generate_features.py --dump
```

审核并更新功能条目的两种语言，包括每个受影响参数的含义。在契约条目中翻译每份完整的已变更描述，并将 `source` 更新为当前 UTF-8 工具描述的精确 SHA-256；不得仅刷新哈希而不审核译文。不手工修改生成页面，也不把注册表导出宣称为真机实测。然后从仓库根目录重新生成并执行以下检查：

```sh
python tools/site/generate_features.py --write
python tools/site/generate_features.py --verify-registry --check
python -m unittest discover -s tools/site -p 'test_*.py'
mkdocs build --strict
python tools/site/check_site.py --site-dir site
```

这些检查涵盖注册表新鲜度、经审核译文的完整性、生成页面漂移、双语导航、内部链接及锚点。源码变化后，在译文更新、生成页面同步且全部检查通过之前，必须阻止站点发布。

<a id="test-coverage"></a>
## 测试覆盖

Python 测试覆盖任务构造、传输失败、下载、动作校验，以及启用／禁用两种标志状态下的 MCP stdio 注册。
多线程伪 HTTP 服务器覆盖健康检查、认证、忙碌响应、任务轮询和 PNG 下载。
Core 测试覆盖解析、序列化、格式化、单位和查询处理。
这些测试不需要真实 Revit 模型。

自动测试不能验证真机 Revit 行为；参见[验证证据](docs/validation.md)。

<a id="release-ritual"></a>
## 发布流程

1. 使用 Conventional Commit 标题合并 PR。
2. release-please 维护 `chore(main): release X.Y.Z` PR，包含生成的变更日志条目和版本更新。
3. 维护者检查发布 PR，并在必需检查通过后合并。
4. 检查 Release please 工作流、两份 MSI 资产、七份按年份分开的 ZIP、wheel、源码发行包和 `SHA256SUMS.txt`。
5. 对稳定发布检查 PyPI、MCP Registry 和 WinGet 任务结果；若未配置 WinGet 提交，则下载清单。

release-please 拥有 [CHANGELOG.md](CHANGELOG.md)、`server/pyproject.toml` 中的版本，以及 `server/server.json` 中的两个版本。
清单从 `0.3.0` 开始；`server/pyproject.toml` 仍是构建检查所使用的包版本。
simple 策略跳过不存在的默认 `version.txt`；不维护单独版本文件。
1.0 之前，`feat` 和破坏性变更提升次版本，`fix` 提升补丁版本。
可见的文档和依赖变更也可能产生补丁发布。
`bump-patch-for-minor-pre-major` 选项为 false，以保留功能变更的次版本提升。

合并发布 PR 会创建 `vX.Y.Z` 和带生成说明的 GitHub Release。
工作流直接调用已有构建和发布流水线；由 `GITHUB_TOKEN` 创建的标签不会触发标签推送工作流。
流水线追加 Install 部分，重试时只替换该部分。
手工推送标签也会运行流水线；若尚无 Release，则使用 GitHub 自动生成的说明。
标签版本必须与 `server/pyproject.toml` 一致。

使用 `GITHUB_TOKEN` 创建或更新的发布 PR，需要获准后才能运行 pull request 工作流。
维护者在发布 PR 中选择 **Approve workflows to run**，然后再等待必需检查。
参见 [GitHub 工作流触发规则](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow#triggering-a-workflow-from-a-workflow)。
仓库 Actions 设置必须允许 GitHub Actions 创建拉取请求。

<a id="release-assets"></a>
## 发布资产

CI 上传可安装的 R20、R22、R26 和 R27 目录布局，以及 `installers` 产物。
它会解包两种 MSI、拒绝包含 Revit API 程序集，并检查每个已构建年份的安装和卸载。
release-please 工作流或手工推送的 `v<version>` 标签会触发全部七个插件构建和 Core／服务器测试。
标签版本必须匹配 `server/pyproject.toml`。
GitHub Release 包含七份按年份分开的 ZIP、单用户和多用户 MSI、Python wheel 和源码发行包，以及覆盖所有资产的 `SHA256SUMS.txt`。
在对应 Revit 实例关闭时，将各年份 ZIP 解压到 `%APPDATA%\Autodesk\Revit\Addins\20<yy>`。
压缩包根目录包含 `RevitModelMcp.addin` 和 `RevitModelMcp` 程序集目录。

发布工作流将 `Build__Version` 设置为标签版本后调用 WixSharp 流水线。
CI 使用 `0.0.0-ci`。
在 Windows 上构建所需年份后，本地也可以使用同一打包命令：

```powershell
$env:Build__Version = '0.2.0'
dotnet run --project build -- pack --no-build
```

`pack --no-build` 打包现有的 `src/RevitModelMcp.Addin/bin/Release.R*` 目录，不清理也不重新编译。
发布打包使用全新检出，以免混入过期配置。
该模块安装 WiX 7、接受其 EULA、安装匹配的 UI 扩展，并将 MSI 写入 `output/`。
单用户安装使用 `%APPDATA%\Autodesk\Revit\Addins\<year>`。
多用户安装在 2026 及以前使用 `%ProgramData%\Autodesk\Revit\Addins\<year>`，2027 使用 `%ProgramFiles%\Autodesk\Revit\Addins\2027`。

稳定发布通过 `pypi` 环境中的 GitHub OIDC，将 wheel 和源码发行包发布到 PyPI。
待配置的发布者信息列于 `.github/workflows/release.yml` 的 `pypi` 任务上方。
PyPI 失败不会阻止 GitHub Release。
PyPI 成功后，工作流更新 `server/server.json` 中的两个版本，并通过 GitHub OIDC 发布到官方 MCP Registry。
Registry 发布采用尽力而为策略，其响应出现在任务日志中。
包含 `-` 的预发布标签跳过 PyPI、MCP Registry 和 WinGet 发布。

发布工作流在发布 GitHub Release 后调用 `.github/workflows/winget.yml`。
`release-please.yml` 为新标签调度 `release.yml`（顶层运行，PyPI 可信发布要求如此）；`release.yml` 再调用 `winget.yml`。同一流水线也可以从 Actions 页手工启动，使用已有标签重新发布资产。
调用任务授予 `id-token: write`；PyPI 任务保留 `pypi` 环境，两种发布者均保留 OIDC 权限。
WinGet 也支持手工发布的 Release 和带稳定发布标签的 `workflow_dispatch`。
它生成并验证 `Sharafutdinov.RevitModelMcp` 的清单，并上传 `winget-manifests` 产物。
提交需要可选的仓库秘密 `WINGET_TOKEN`，即具有 `public_repo` 范围的经典 PAT。
没有令牌时，仍会运行生成和产物上传。
在 Windows 上，`build/winget/New-WingetManifests.ps1 -Version 0.2.0 -ReleaseTag v0.2.0 -OutputDir artifacts/winget` 下载 MSI 并读取哈希和产品代码。
`-SkipDownload` 使用 `output/` 中已有的匹配 MSI。

贡献内容采用 [MIT 许可证](LICENSE)。
