# 构件关系

`revit_list_relations`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.7.0</span></p>

关系查询：标高的房间、面积方案成员、组内构件、嵌套族、视图样板依赖

## 可复制提示词 {#prompts}

```text
1F 标高上都有哪些房间？
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `relation` | 是 | — | `string` | 关系种类：level-rooms / area-scheme-elements / group-elements / nested-family / view-template-dependents |
| `source_id` | 否 | `null` | `integer / null` | 源对象的 Revit ID（组或族实例） |
| `source_name` | 否 | `null` | `string / null` | 源对象名称（标高、面积方案或视图样板） |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `pickup_timeout_seconds` | 否 | `300` | `integer` | local / SSH 等待插件拾取任务的预算（正整数秒，默认 300）；HTTP 忽略。拾取超时后待处理任务仍可能执行 |
| `timeout_seconds` | 否 | `120` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

读取模型对象的成员关系或依赖关系。

返回的数据包含 `relation`、`source` 和 `elements`；构件条目包含 ID、名称、类别、族和类型；没有相关对象时返回 `elements=[]`。
`relation` 为必填项：`level-rooms`、`area-scheme-elements` 或 `view-template-dependents` 需配合 `source_name`；`group-elements` 或 `nested-family` 需配合 `source_id`。
从 `revit_list_catalog` 获取来源对象名称，从构件查询结果获取 ID。
关系无效、来源对象缺失或错误、文档不存在、读取失败或超时都会报错；不返回部分数据。

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
