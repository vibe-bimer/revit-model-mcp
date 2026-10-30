# 聚合统计

`revit_aggregate_elements`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

按一到两个字段汇总符合条件的构件，可选求和与平均；长度用毫米、面积用平方米、体积用立方米。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `area_scheme` | 否 | None | any | Exact area-scheme name, case-insensitive. |
| `categories` | 否 | None | any |  |
| `family` | 否 | None | any |  |
| `group_by` | 是 | — | array | One or two distinct fields (e.g. category, family, type, level) or exact localized parameter names. |
| `level` | 否 | None | any |  |
| `parameter_filters` | 否 | None | any | AND-combined filters: parameter (exact localized name), operator (equals, contains, greater, less, empty, not-empty, exists) and value. Numbers use mm, m2, m3 or display units. |
| `phase` | 否 | None | any |  |
| `sum_field` | 否 | None | any | Numeric field or parameter name to sum and average per group; lengths in mm, areas m2, volumes m3. |
| `type_name` | 否 | None | any | Exact type name, case-insensitive. |
| `view` | 否 | None | any | 视图的准确名称或十进制视图 ID。 |
| `workset` | 否 | None | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | 120 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Summarize matching elements by one or two fields, with optional sum and average. Lengths use mm, areas m2, volumes m3. For area totals, group by level and select the area scheme. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
