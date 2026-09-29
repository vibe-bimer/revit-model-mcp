# 重建副本（`revit_rebuild_model_ids`）性能分析与提速规划

测量日期 2026-09-29。测量版本 `0.8.1-phases`（在 `src/RevitModelMcp.Addin/Control/ModelRebuild.cs` 里加了分阶段计时 `PhaseLog`）。

- 工作站：`DESKTOP-64UMIOR`，Intel Xeon W-2235 6 核 / 12 线程，63.7 GB RAM；C: 34 GB / D: 307 GB / E: 615 GB 可用。
- Revit 2020 RTM（RevitAPI 20.0.0.377），单会话常驻内存约 1.76 GB private、0.8 GB working set、约 5,000 handles。
- 源模型 `E:\revitmcp-test\建筑结构.rvt`（899 个三维视图可选构件、6 个标高、954 个登记构件）。
- 目标：默认公制样板新建项目（`Application.NewProjectDocument(UnitSystem.Metric)`）。

## 1. 一次副本的时间构成（实测，毫秒）

`PhaseLog` 的分阶段结果（结果 notes 与插件日志同时输出）：

| 阶段 | seed 0 | seed 8000 | 说明 |
| --- | ---: | ---: | --- |
| `new-project` | 1,494–1,608 | 1,273–1,585 | 从默认公制样板新建项目 |
| `seed` | 0 | 24,643–24,872 | 逐个 `Level.Create` + `level.Name=…`，约 **2.86 ms/个** |
| `reserve` | 476–648 | 1,603–1,682 | 把样板里 210–238 个同名构件改名，避免粘贴时弹「重复类型」 |
| `copy-call` | 21,485–22,203 | 22,099–22,857 | 一次跨文档 `ElementTransformUtils.CopyElements` 复制 899 个构件，约 **24 ms/个** |
| `remove-seed` | 0 | 2,431–2,494 | 逐个 `Document.Delete`，约 0.31 ms/个 |
| `remove-template-levels` | 14–30 | 25–32 | 删掉样板自带的标高 |
| `mapping` | 18–76 | 18–49 | 生成 旧ID→新ID 映射表（899 条） |
| `view` | 218–316 | 258–287 | 补一个三维视图，让副本打开就有视图 |
| **`cleanup`** | **29,107–30,038** | **29,428–29,452** | **`RemoveRenamedTemplateElements`：把改名过的样板构件再删掉，占 52%** |
| `save` | 2,334–2,522 | 2,488–2,494 | `Document.SaveAs`（7 MB 文件，含 `.0001/.0002` 备份） |
| **合计** | **55,886–57,200** | **84,837–85,701** | 与任务 `elapsedMs` 一致（差值=入队/回传开销） |

要点：

1. **`cleanup` 是最大单项（约 29.5 s，52%）**，而且它是纯粹为「重命名样板构件」这一绕行方案擦屁股的工作。
2. `copy-call` 是真正的复制成本（约 21.8 s，39%），Revit 的跨文档粘贴就是这个速度（24 ms/构件）。
3. `save` 只要 2.4 s，**不是**瓶颈；`SaveAsOptions.MaximumBackups`/`Compact` 没有可观的收益。
4. `seed` 是线性的：`seed=8000` 多花约 25 s（2.86 ms/个），是唯一随参数增长的阶段。
5. 映射表、视图、新建项目合计不到 2 s，可以忽略。

## 2. 「变慢」的真相：两种完全不同的慢

**(a) 稳态成本高，但不退化。** 同一个 Revit 会话里连续跑 5 次 seed 0 实跑：55.8 / 57.0 / 56.6 / 57.7 / 56.4 s，每个阶段都平稳，内存稳定在 1.76 GB private、约 5,000 handles。也就是说**没有"跑几次就越来越慢"的稳态衰减**。

**(b) 会话被拖垮：`cleanup` 阶段撞上 Revit 内部错误。** 同一会话连续跑 `seed=8000` 实跑时，第 3 次超过客户端 120 s 等待上限。插件日志显示 `cleanup` 阶段在刷：

```
[WRN] A renamed template element could not be removed: ElementId cannot be deleted.\r\nParameter name: elementId
[WRN] A renamed template element could not be removed: An internal error has occurred.
[WRN] A renamed template element could not be removed: A managed exception was thrown by Revit or by one of its external applications.
```

失败的删除非常贵（每次都要走 Revit 的错误处理/回滚），于是 29 s 的 `cleanup` 膨胀到 60 s 以上，任务超时。此前观察到的"部分拷贝"（888/899、墙 289/325、`isolatedCopy=true`、`idMappingVerified=false`、153–183 s）也发生在同一批会话里：一次大 `CopyElements` 被 Revit 拒绝后，工具退回到二分隔离模式（最多 400 个事务），于是又慢又丢构件。

**结论：慢的主因是「改名样板构件 → 复制 → 再删掉改名构件」这条绕行路线，它既贵（29 s/次）又脆（大量删除触发 Revit 内部错误，且失败会在会话里累积）。**

## 3. 提速方案（按收益/风险排序）

### 方案 1：用对话框事件替代改名+删除（预计 55.9 s → 约 26 s，2.1×）

「重复类型」弹窗的语义是"将使用来自粘贴文档中的版本"（`确定`），也就是**保留源模型的类型**——这正是我们想要的。Revit API 提供了在无人值守时替用户点这个按钮的正规手段：

- `UIControlledApplication.DialogBoxShowing` 事件 + `DialogBoxShowingEventArgs.OverrideResult(int)`（2020 与 2026 语料均已确认存在），`DialogBoxShowingEventArgs.DialogId` 可用来只拦这一个对话框。
- 命中「重复类型」时 `OverrideResult(1)`（确定），粘贴照常进行且用源模型的类型。
- 于是 `ReserveDestinationNames`（改名）与 `RemoveRenamedTemplateElements`（29 s 的删除）**都不再需要**：单次副本约 26 s，而且没有大规模删除 → 没有内部错误 → 会话不再被拖垮。
- 保险丝：保留现有的 `SendMessage(BM_CLICK)` 看门狗思路（工作站 `dlgclick.ps1`）作为兜底；用 `duplicateNames=override|rename` 参数保留旧路径，便于回退与对比。

风险：该事件必须真的对粘贴产生的对话框触发（需要在实机上验证一次）；若不触发，退到方案 1b。

**方案 1b（退路）：只改名、不删除。** 保留 `reserve`（0.5 s），删掉 `cleanup`（29 s），代价是副本里留下约 210 个 `__rebuild_type_N (模板)` 命名的样板类型。或者只对真正冲突的名字改名（当前是全量改名）。

### 方案 2：去掉 O(seed) 的烧号（每份省 1.5–27 s）

Revit 的 id 单调递增：实测 `新ID起点 = 2592 + seed` 严格成立，而且一次复制本身就把 id 计数器推进了 1,784。所以：

- **同一个目标文档连续出多份**：复制 → 存盘 → 删掉刚复制进来的构件（连类型）→ 再复制。第 2 份自动从 4376 开始、第 3 份从 6160 开始……**不需要任何 seed**。省掉 `new-project`（1.5 s）、`seed`（2.86 ms×seed）、`remove-seed`（0.31 ms×seed）。
- 9 份 seed 0…8000（步长 1000）现在的总烧号成本约 103 s，加 9 次新建项目约 13 s，合计约 116 s（占 9 份总时长约 20%）。
- 更省的烧号元素：先做微基准（`Level` 现在 2.86 ms/个，`level.Name` 那次改名占一半左右，去掉改名预计省 30–50%）。
- 风险：删 899 个复制进来的构件可能撞上同样的"删不掉"问题（需要验证）；类型残留会让下一份复制再次遇到同名冲突（正好由方案 1 的对话框覆盖兜住）。

### 方案 3：一次任务出多份（`copies=N`）

把 9 份合成一个任务：一次源选择、一次样板打开、一次映射表生成，省掉 9 次 MCP 往返与排队；同时把客户端 120 s 等待与 10 分钟结果过期的限制改成流式进度上报。配合方案 1+2，9 份从约 10 分钟降到约 4 分钟。

### 方案 4：并行（真正的墙钟时间收益）

Revit API 是进程内单线程，一个 Revit 进程同时只能有一个任务；所以并行的唯一形态是**多实例/多机**：

- 现在动作路径有硬约束：`server/revit_model_mcp/actions.py:169` 抛 `Actions require exactly one running Revit instance.`；`server/revit_model_mcp/server.py:220` 已经支持用 `document` 子串在多个实例间选目标，但 HTTP 通道端口 `127.0.0.1:53110` 是写死的 → 多实例需要每实例端口 + 实例选择。
- 容量：单实例 private 约 1.76 GB、working set 约 0.8 GB；6 核/12 线程、63.7 GB RAM → **3–4 个实例很宽裕**（约 7 GB / 3.2 GB）。
- 预期：优化后的 9 份（每份约 26 s）用 4 个实例 ≈ **1 分钟墙钟**；保守按每实例 30–40 s 也算 1.5 分钟以内。串行今天是 10 分钟。
- 配套：一个"副本农场"调度脚本（每实例一个工作目录 + 端口 + 心跳文件），任务级重试，失败实例自动重启。

### 方案 5：不改（负收益/无收益）

- `SaveAsOptions.MaximumBackups=1` / `Compact`：`save` 只占 2.4 s，收益可忽略。
- 减少 `mapping`/`view`/`new-project`：合计不到 2 s。
- 在 Revit 内多线程：API 不允许，不要尝试。

## 4. 分阶段计划

| 阶段 | 内容 | 预期 | 验收 |
| --- | --- | --- | --- |
| P0（0.5 天） | 落地分阶段计时（`PhaseLog`）+ 日志降噪（改名失败每天 1,512 行 / 809 KB，改为聚合计数）；修 `.0001/.0002` 备份残留 | 可观测 | 结果与日志都能看到阶段耗时 |
| P1（0.5–1 天） | 方案 1：`DialogBoxShowing` + `OverrideResult(1)`，默认不再改名/删除；保留 `duplicateNames=rename` 回退 | 55.9 s → ~26 s | 899/899、`idMappingVerified=true`、`isolatedCopy=false`、无弹窗、类型与源一致 |
| P2（1 天） | 方案 3 + 2：`copies=N`（或 `seeds=[…]`）一个任务出多份 + 目标文档复用（免 seed）；客户端改流式进度 | 9 份 ≈ 4 分钟 | 9 份 ID 区间互不重合（或按需重合）、每份 899/899 |
| P3（1–2 天） | 方案 4：多实例（每实例端口 + 工作目录 + 调度脚本），去掉/放宽单实例约束 | 9 份 ≈ 1 分钟墙钟 | 4 实例并发下 9 份全部通过 |
| P4（0.5 天） | 加固：Revit 内部错误重试与退避、会话健康度探测（连续 N 次失败/超时自动重启 Revit）、`idMappingVerified=false` 时明确报错而非静默产出 | 长跑稳定 | 连续 20 份无退化、无部分拷贝 |

长期路线：把「烧号」换成"目标文档复用"后，seed 只作为"需要指定起点"的高级参数保留；`idMappingVerified` 继续作为质量闸门。

## 5. 当前状态

- `PhaseLog` 已实现并实测（本文数据即来自它），但**尚未提交**；`0.8.1-phases` 只部署在工作站上用于测量。
- `seed` 功能（`ModelRebuild.cs`、`ActionJobParser.cs`、`server/revit_model_mcp/actions.py`、`server/tests/test_actions.py`、`tests/RevitModelMcp.Core.Tests/Control/ActionJobParserTests.cs`、`docs/actions.md`）同样未提交、未发布。
- 9 份副本与对照表已交付：`/home/roky/构件ID对照_9份副本.xlsx`（seeds 0…8000，ID 区间 2592–4375 … 10592–12375，每份 899 构件）。
