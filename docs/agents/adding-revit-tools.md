# 新增 Revit 工具

给这个仓库加读取工具、动作工具，或接入新的 Revit API 时，从头到尾照这份清单走。

!!! note "中文版"
    本页是中文说明；英文原文见本页的 English 版本（右上角切换），两者以英文为准。

## 步骤 0：先查本地 API 库

仓库里的 `revit-corpus/` 是一份本地 Revit 2026 API 参考（28,796 篇 CHM 文档 + FTS5 索引）。它是可选的、机器本地数据：目录不存在就跳过这步，改用官方文档。

```sh
python3 revit-corpus/scripts/corpus_query.py overloads Floor.Create     # 所有重载页
python3 revit-corpus/scripts/corpus_query.py members FilteredElementCollector -k method
python3 revit-corpus/scripts/corpus_query.py 'Floor' -k class --show
```

也可以用 `revit-docs` 连接器（`revit_docs_symbol` / `revit_docs_search` / `revit_docs_read`）——`revit_docs_symbol` 直接吃带点的名字，FTS 引号它自己处理。

**读全文，不要只看签名**：重载、参数、返回值、异常与 remarks 都可能决定实现方式。例：`FilteredElementCollector` 至少要有一个过滤器，且优先用原生过滤器而不是 LINQ。

## 读取工具清单（8 个同步点）

1. **Python 任务构造**：在 `server/revit_model_mcp/revit_channel.py` 加一个 `ReadJob` 类方法（参考 `list_views`）；通用过滤语义放进 `universal_jobs.py`。
2. **MCP 注册**：在 `server.py` 加 `@addressed_tool` 函数，写清描述与参数默认值。
3. **Core 解析**：在 `src/RevitModelMcp.Core` 加对应的任务/结果契约（不引用 Revit API，可在 Linux 上单测）。
4. **插件执行**：在 `src/RevitModelMcp.Addin/Control` 实现，经 `ExternalEvent` 在 Revit 主线程执行。
5. **测试**：Core 单测 + Python 测试各补一例，覆盖正常与边界。
6. **文档**：更新 `docs/tools.md`（中文索引会自动生成）与工具契约。
7. **一致性检查**：`docs/tools.md` 与 `bundle/manifest.json` 的工具名必须一致（CI 会校验）。
8. **真机验证**：至少在一个年份上实跑，把证据写进 `docs/validation.md`。

## 动作工具清单（额外 7 点）

1. 必须同时受 `REVIT_MCP_ALLOW_WRITE=1` 与工作站 `allow-write` 文件两道门禁约束，**不得放宽默认值**。
2. 支持 `dry_run`：执行后回滚，返回同样的 `verification` 块。
3. 返回 `verification`（改动前/后对照），不得把超时或失败伪装成成功。
4. 在 `ActionJobParser` 里登记动作名与参数范围（如 `copies` 上限）。
5. 明确是否可以放进 `revit_batch`（一次撤销），不可以的要写进 `docs/actions.md`。
6. 要求"恰好一个 Revit 实例"的场景要显式检查，避免改错模型。
7. 更新 `docs/actions.md`（中文索引自动生成）与工具页内容源。

## 构建与部署

```powershell
foreach ($year in '20','22','23','24','25','26','27') {
    dotnet build src/RevitModelMcp.Addin -c "Release.R$year" -p:DeployAddin=false
}
dotnet test --project tests/RevitModelMcp.Core.Tests/RevitModelMcp.Core.Tests.csproj
```

Revit 2020 走 `DisplayUnitType`/`UnitType`/`Document.Create.NewFloor`，2022+ 走 `ForgeTypeId`/`Floor.Create`；兼容层在 `src/RevitModelMcp.Addin/Compatibility/`。

## 已知 API 限制与年份差异

- 元素 ID 不可写、不可指定，只能通过"复制 + 删除"让 Revit 重新分配。
- 删除会级联：有依赖、有宿主、成组或属于 MEP 系统的构件要单独处理。
- 阶段 API 只在 2022+ 暴露；2020 走顺序检查兜底。
- 列表型结果要分页（`offset`/`limit`），并如实返回 `hasMore`。
