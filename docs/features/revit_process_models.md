---
description: "在交互会话中逐个打开模型执行步骤和 C# 代码并按需导出保存；原地保存与代码需 confirm_token 确认"
---

# 批量处理模型

`revit_process_models`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

在交互会话中逐个打开模型执行步骤和 C# 代码并按需导出保存；原地保存与代码需 confirm_token 确认

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_process_models.md)

## 可复制提示词 {#prompts}

```text
批量打开 D:/models 下的模型，导出 PNG 并另存为新文件，不要原地保存。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `code` | 否 | `null` | `any / null` | 要在每个模型中运行的 C# 代码，含事务方式 |
| `confirm_token` | 否 | `null` | `string / null` | 首次调用返回的令牌，用于第二次确认调用 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `exports` | 否 | `null` | `array<any> / null` | 对每个模型执行的导出请求列表 |
| `folder` | 否 | `null` | `string / null` | 要处理的模型文件夹 |
| `open` | 否 | `null` | `any / null` | 打开每个模型的方式，含模式与工作集设置 |
| `paths` | 否 | `null` | `array<string> / null` | 要处理的模型路径列表 |
| `pattern` | 否 | `"*.rvt"` | `string` | 文件名匹配模式，以 `.rvt` 结尾 |
| `process_id` | 否 | `null` | `integer / null` | 在多个运行实例中选定的目标 Revit 进程 ID |
| `recursive` | 否 | `false` | `boolean` | 是否递归处理文件夹中的子目录 |
| `save` | 否 | `null` | `any / null` | 保存设置，模式为 `none`、`output_dir` 或 `in_place` |
| `steps` | 否 | `null` | `array<any> / null` | 1–50 个动作步骤；任一步首次失败都整体回滚 |
| `stop_on_error` | 否 | `false` | `boolean` | 遇到错误时是否停止处理 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `timeout_seconds` | 否 | `14400` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

在交互会话中逐个打开模型，执行步骤和 C# 代码，按需导出、另存并关闭。

原地保存和执行代码需要预览响应中的 `confirm_token`。
`dry_run` 会强制 `code.transaction="auto"`，并在 `warnings` 中报告这一覆盖。

当等待预算耗尽时，长时间操作可能返回 `status=running` 和 `jobId`；此时模型可能已经被修改，`revit_jobs` 会返回其结果。重新提交会重复该操作。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
