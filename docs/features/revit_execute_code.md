---
description: "在 Revit 线程编译运行 C#，自动模式下自管一个事务与撤销记录"
---

# 执行 C# 代码

`revit_execute_code`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

在 Revit 线程编译运行 C#，自动模式下自管一个事务与撤销记录

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_execute_code.md)

## 可复制提示词 {#prompts}

```text
跑一段 C#，把当前视图里所有墙的注释参数改成 Review
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `code` | 是 | — | `string` | 要编译并运行的 C# 代码正文 |
| `confirm_token` | 否 | `null` | `string / null` | 首次调用返回、用于第二次确认调用的令牌 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `transaction` | 否 | `"auto"` | `string` | 事务模式，`auto` 或 `none` |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `timeout_seconds` | 否 | `600` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

在 Revit 线程上针对活动的 Revit API 编译并运行 C# 代码。

接受一个方法体，或一个带 `Execute(ScriptContext ctx)` 的 `public static Script` 类。

`auto` 模式独占一个事务和一个撤销条目；`transaction="none"` 默认被拒绝。

需要先调用一次以获得 `confirm_token`，该次调用不运行任何代码；`dry_run` 不需要 `confirm_token`，并强制使用 `transaction="auto"`。

当等待时间预算耗尽时，长操作可能返回 `status=running` 和 `jobId`；此时模型可能已经被修改，`revit_jobs` 会返回其结果。

重新提交会重复执行该操作。

如果有多个 Revit 实例正在运行，必须提供 `document`；否则任意实例都可能响应。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
