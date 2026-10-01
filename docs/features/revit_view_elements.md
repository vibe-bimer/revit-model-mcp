# revit_view_elements

<p class="facts"><b>分组</b> 视图与截图　<b>类型</b> 读取（只读）　<b>起始版本</b> 0.2.0</p>

分页读取视图中的构件（可按类别过滤）

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `view` ✔ | — | Required exact, case-sensitive non-template view name from revit_list_views, or its Revit view ID as a decimal string; no default. An exact name takes precedence over interpreting a numeric string as an ID.（string） |
| `categories` | — | any |
| `limit` | `100` | integer |
| `offset` | `0` | integer |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |
    | `pickup_timeout_seconds` | `300` | Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later.（integer） |
    | `timeout_seconds` | `120` | Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits.（integer） |

## 提示词

```text
把三维视图里的构件列表给我，每页 200 条
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
