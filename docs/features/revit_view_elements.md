---
description: "分页读取视图中的构件（可按类别过滤）"
---

# 视图构件明细

`revit_view_elements`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.2.0</span><span><b>版本</b> 已发布 0.9.0</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

分页读取视图中的构件（可按类别过滤）

[同名集成分支页面](../platform/revit_view_elements.md)

## 可复制提示词 {#prompts}

```text
把三维视图里的构件列表给我，每页 200 条
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | 是 | — | `string` | 视图名称（或视图 ID） |
| `categories` | 否 | `null` | `array<string> / null` | 只列出这些类别的构件 |
| `limit` | 否 | `100` | `integer` | 每页条数 |
| `offset` | 否 | `0` | `integer` | 从第几条开始（配合 limit 分页） |
| `process_id` | 否 | `null` | `integer / null` | 目标 Revit 进程 ID（在多个运行实例中选定） |

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

读取指定视图中的一页构件数据。

返回的数据包含 `elements`、`total`、`offset`、`limit` 和 `hasMore`；每行包含 ID、类别、族、类型、标高，以及可获取的测量值，单位为 mm、m2 和 m3。
没有匹配项，或偏移量超出结果范围时，返回 `elements=[]`；当 `hasMore=true` 时，增加 `offset` 继续读取。
计数和查找类别优先使用 `revit_view_summary`；使用本工具读取单个构件的数据行，使用 `revit_element_details` 读取全部参数。
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
