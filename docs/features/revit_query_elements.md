# revit_query_elements

<p class="facts"><b>分组</b> 查询与统计　<b>类型</b> 读取（只读）　<b>起始版本</b> 0.1.0</p>

按类别/族/类型/标高/视图/工作集/参数过滤，分页读取构件明细

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `area_scheme` | — | Exact area-scheme name from the area-schemes catalog, matched case-insensitively. Default null applies no scheme filter; selecting a scheme restricts results to its areas and combines with the other filters.（any） |
| `categories` | — | 类别过滤（可多个，取并集）（any） |
| `family` | — | 族名过滤（any） |
| `fields` | — | 要返回的字段；缺省返回常用字段（any） |
| `include_geometry` | `false` | 是否返回位置、包围盒与所在房间中心（模型 mm）（boolean） |
| `level` | — | 标高过滤（any） |
| `limit` | `100` | 每页条数（配合 offset 分页）（integer） |
| `offset` | `0` | 从第几条开始（配合 limit 分页）（integer） |
| `parameter_filters` | — | 参数过滤条件（equals / contains / greater / less / empty / not-empty / exists）（any） |
| `phase` | — | 阶段过滤（any） |
| `sort_direction` | `"asc"` | 排序方向：asc / desc（string） |
| `sort_field` | `"id"` | 排序字段（默认按构件 ID）（string） |
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
列出 2F 上所有没填防火等级的门，给出 ID
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
