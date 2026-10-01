# revit_aggregate_elements

<p class="facts"><b>分组</b> 查询与统计　<b>类型</b> 读取（只读）　<b>起始版本</b> 0.1.0</p>

按 1–2 个字段分组统计数量，可附加求和与平均（mm / m² / m³）

!!! note "说明"
    回答“有多少”的首选，比逐条取明细快得多

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `group_by` ✔ | — | 1–2 个分组字段（category/family/type/level 或参数名）（array） |
| `area_scheme` | — | Exact area-scheme name from the area-schemes catalog, matched case-insensitively. Default null applies no scheme filter; selecting a scheme restricts results to its areas and combines with the other filters.（any） |
| `categories` | — | 类别过滤（可多个，取并集）（any） |
| `family` | — | 族名过滤（any） |
| `level` | — | 标高名称（用 revit_list_catalog 查到的本地化名称）（any） |
| `parameter_filters` | — | 参数过滤条件（equals/contains/greater/less/empty/not-empty/exists）（any） |
| `phase` | — | 阶段过滤（any） |
| `sum_field` | — | 需要求和的数值字段或参数名，附带 sum/average（any） |
| `type_name` | — | 类型名称（与族一起定位）（any） |
| `view` | — | 视图名称（或视图 ID）（any） |
| `workset` | — | 工作集过滤（any） |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |
    | `pickup_timeout_seconds` | `300` | Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later.（integer） |
    | `timeout_seconds` | `120` | Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits.（integer） |

## 提示词

```text
统计 1F 上各种墙类型各有多少个
```

```text
按标高统计门的数量和总宽度
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
