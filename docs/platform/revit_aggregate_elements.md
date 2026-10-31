---
description: "按一到两个字段汇总符合条件的构件，可选求和与平均；长度用毫米、面积用平方米、体积用立方米。"
---

# 聚合统计

`revit_aggregate_elements`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 1.0.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

按一到两个字段汇总符合条件的构件，可选求和与平均；长度用毫米、面积用平方米、体积用立方米。

[同名发布版页面](../features/revit_aggregate_elements.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 1.0.0 一致。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `area_scheme` | 否 | `null` | any | Exact area-scheme name, case-insensitive. |
| `categories` | 否 | `null` | any | （集成分支契约未提供说明） |
| `family` | 否 | `null` | any | （集成分支契约未提供说明） |
| `group_by` | 是 | — | array | One or two distinct fields (e.g. category, family, type, level) or exact localized parameter names. |
| `level` | 否 | `null` | any | （集成分支契约未提供说明） |
| `parameter_filters` | 否 | `null` | any | AND-combined filters: parameter (exact localized name), operator (equals, contains, greater, less, empty, not-empty, exists) and value. Numbers use mm, m2, m3 or display units. |
| `phase` | 否 | `null` | any | （集成分支契约未提供说明） |
| `sum_field` | 否 | `null` | any | Numeric field or parameter name to sum and average per group; lengths in mm, areas m2, volumes m3. |
| `type_name` | 否 | `null` | any | Exact type name, case-insensitive. |
| `view` | 否 | `null` | any | 视图的准确名称或十进制视图 ID。 |
| `workset` | 否 | `null` | any | （集成分支契约未提供说明） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | `120` | integer | 本次调用的等待上限（秒）。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Summarize matching elements by one or two fields, with optional sum and average. Lengths use mm, areas m2, volumes m3. For area totals, group by level and select the area scheme. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
