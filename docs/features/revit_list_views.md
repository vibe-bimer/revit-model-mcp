# 视图目录

`revit_list_views`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.1.0</span></p>

列出视图，可按视图类型与名称过滤

## 可复制提示词 {#prompts}

```text
列出所有平面视图
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `name_contains` | 否 | `null` | `string / null` | 按名称子串过滤 |
| `view_type` | 否 | `null` | `string / null` | 视图类型（如 FloorPlan、ThreeD） |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `pickup_timeout_seconds` | 否 | `300` | `integer` | local / SSH 等待插件拾取任务的预算（正整数秒，默认 300）；HTTP 忽略。拾取超时后待处理任务仍可能执行 |
| `timeout_seconds` | 否 | `120` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

在分析视图前查找非模板视图。

返回的数据包含 `views`；每个视图包含 `id`、`name`、`type`、`level`、`scale` 和 `template`，并提供已扫描非模板视图的 `total` 和 `processed` 计数。
没有视图匹配筛选条件时返回 `views=[]`。
在请求构件分页数据前，将返回的视图名称传给 `revit_view_summary`。
文档不存在、读取失败或超时都会报错；不返回部分数据。

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
