# 参与贡献

!!! note "中文版"
    本页是中文说明；英文原文见本页的 English 版本（右上角切换）。

<a id="local-checks"></a>
## 本地检查

```sh
uv tool install pre-commit
pre-commit install
pre-commit run --all-files
```

C# 的钩子需要 Windows；在 Linux/macOS 上用 `SKIP=dotnet-format pre-commit run --all-files`，并以 Windows 的 PR CI 结果为准。

## 构建与测试

```powershell
foreach ($year in '20','22','23','24','25','26','27') {
    dotnet build src/RevitModelMcp.Addin -c "Release.R$year" -p:DeployAddin=false
}
dotnet test --project tests/RevitModelMcp.Core.Tests/RevitModelMcp.Core.Tests.csproj
```

```sh
cd server && uv run --with pytest pytest -q
uvx ruff==0.16.7 check . && uvx ruff==0.16.7 format --check .
```

Core 测试不需要 Revit，可在任意平台运行；文档站生成物用 `python tools/site/generate_features.py --check` 校验是否需要重新生成。

## 提交规范

- 用 Conventional Commits（`feat:` / `fix:` / `perf:` / `docs:` / `chore:` …），提交信息用英文。
- 每个行为变更都要有测试，不得删除或弱化已有测试。
- 不要手改 `CHANGELOG.md`、`server/pyproject.toml` 的版本号或 `server/server.json` 的版本字段——这些由 release-please 通过发布 PR 维护。

<a id="release-ritual"></a>
## 发布仪式

1. 合并 release-please 的发布 PR（它会更新 CHANGELOG 与版本号）；
2. release 工作流构建产物并发布，资产包含 7 个年份的插件包、单/多用户 MSI、Python 包与 `SHA256SUMS.txt`；
3. 校验资产与校验和，必要时把 MSI 装到工作站做一次真机验证；
4. 版本号必须与 tag 去掉 `v` 前缀后一致。
