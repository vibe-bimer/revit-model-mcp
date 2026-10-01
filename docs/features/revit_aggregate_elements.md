# revit_aggregate_elements

<p class="facts"><b>分组</b> 查询与统计　<b>类型</b> 读取（只读）　<b>起始版本</b> 0.1.0</p>

按 1–2 个字段分组统计数量，可附加求和与平均（mm / m² / m³）

!!! note "说明"
    回答“有多少”的首选，比逐条取明细快得多

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `group_by` ✔ | — | array — Required list of one or two distinct system fields (e.g. category, family, type, level) or exact localized parameter names from the catalog; no default. Each combination produces a count, with numeric totals added by sum_field. |
| `area_scheme` | — | any — Exact area-scheme name from the area-schemes catalog, matched case-insensitively. Default null applies no scheme filter; selecting a scheme restricts results to its areas and combines with the other filters. |
| `categories` | — | any |
| `family` | — | any |
| `level` | — | any |
| `parameter_filters` | — | any — AND-combined objects with an exact localized parameter name in parameter, an operator (equals, contains, greater, less, empty, not-empty, exists), and value for comparisons; default null applies no parameter filters. Numeric values use mm, m2, m3 or other document display units; contains requires text, and empty/not-empty/exists need no value. |
| `phase` | — | any |
| `sum_field` | — | any — Numeric system field or exact localized parameter name to sum and average within each group. Default null omits numeric aggregation; lengths use mm, areas m2, volumes m3, and other quantities use the returned unit. |
| `type_name` | — | any — Exact type name to match, case-insensitively, combined with the other model filters. Default null applies no type filter; discover names with the family-types catalog. |
| `view` | — | any — Exact non-template view name from the views catalog, matched case-insensitively, to restrict the element collector. Default null searches the document without a view filter; combines with the other model filters. |
| `workset` | — | any |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted. |
    | `pickup_timeout_seconds` | `300` | integer — Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later. |
    | `timeout_seconds` | `120` | integer — Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits. |

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
