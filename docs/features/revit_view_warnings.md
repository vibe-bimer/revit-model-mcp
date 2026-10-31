---
description: "只读该视图相关构件的警告"
---

# 视图相关警告

`revit_view_warnings`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.4.0</span><span><b>版本</b> 已发布 0.9.0</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

只读该视图相关构件的警告

[同名集成分支页面](../platform/revit_view_warnings.md)

## 可复制提示词 {#prompts}

```text
这个视图里有哪些警告？
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | 是 | — | `string` | 视图名称（或视图 ID） |
| `process_id` | 否 | `null` | `integer / null` | 在多个运行实例中选定的目标 Revit 进程 ID，优先于 `document` |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `timeout_seconds` | 否 | `120` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

读取涉及指定视图中构件的警告。

返回的数据包含 `view` 和 `warnings`；每条警告包含文本、严重程度，以及带 `presentOnView` 标记的构件 ID；没有相关警告时返回 `warnings=[]`。
一条警告也可能同时涉及视图外的构件。
使用 `revit_view_summary` 检查视图内容，或使用 `revit_list_warnings` 查看整个模型的警告分组。
文档不存在、视图未知或不受支持、读取失败或超时都会报错；不返回部分数据。

如果有多个 Revit 实例正在运行，必须提供 `document`；否则任意实例都可能响应。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state ok">已实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
