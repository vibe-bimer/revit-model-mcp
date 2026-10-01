# 分组统计

`revit_aggregate_elements`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.1.0</span></p>

按 1–2 个字段分组统计数量，可附加求和与平均（mm / m² / m³）

!!! note "使用提示"
    回答“有多少”的首选，比逐条取明细快得多

## 可复制提示词 {#prompts}

```text
统计 1F 上各种墙类型各有多少个
```

```text
按标高统计门的数量和总宽度
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `group_by` | 是 | — | `array<string>` | 1–2 个分组字段（category/family/type/level 或参数名） |
| `area_scheme` | 否 | `null` | `string / null` | 面积方案的精确本地化名称（由 area-schemes 目录获取）；选择后仅查询该方案的面积构件，并与其它过滤条件共同生效 |
| `categories` | 否 | `null` | `array<string> / null` | 类别过滤（可多个，取并集） |
| `family` | 否 | `null` | `string / null` | 族名过滤 |
| `level` | 否 | `null` | `string / null` | 标高名称（用 revit_list_catalog 查到的本地化名称） |
| `parameter_filters` | 否 | `null` | `array<object> / null` | 参数过滤条件（equals/contains/greater/less/empty/not-empty/exists） |
| `phase` | 否 | `null` | `string / null` | 阶段过滤 |
| `sum_field` | 否 | `null` | `string / null` | 需要求和的数值字段或参数名，附带 sum/average |
| `type_name` | 否 | `null` | `string / null` | 类型名称（与族一起定位） |
| `view` | 否 | `null` | `string / null` | 视图名称（或视图 ID） |
| `workset` | 否 | `null` | `string / null` | 工作集过滤 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `pickup_timeout_seconds` | 否 | `300` | `integer` | local / SSH 等待插件拾取任务的预算（正整数秒，默认 300）；HTTP 忽略。拾取超时后待处理任务仍可能执行 |
| `timeout_seconds` | 否 | `120` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

在调用 `revit_list_catalog` 后，按 1 个或 2 个字段汇总匹配的构件。

返回的数据包含 `matchedElements` 和 `groups`；每组包含分组键、`count`，以及可选的 `numericCount`、`sum`、`average` 和 `unit`。
长度使用 mm，面积使用 m2，体积使用 m3；没有数值的分组，其 `sum` 和 `average` 为 `null`。
没有匹配项时返回 `groups=[]`；即使结果为空，无效的字段名或筛选条件名也会报错。
先调用 `revit_list_catalog`；计数和分类汇总优先使用本工具，仅在需要单个构件的数据行时使用 `revit_query_elements`。
汇总面积时，按标高分组，并选择面积方案。
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
