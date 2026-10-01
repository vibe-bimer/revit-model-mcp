# revit_list_relations

<p class="facts"><b>分组</b> 查询与统计　<b>类型</b> 读取（只读）　<b>起始版本</b> 0.7.0</p>

关系查询：标高的房间、面积方案成员、组内构件、嵌套族、视图样板依赖

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `relation` ✔ | — | string |
| `source_id` | — | Positive integer Revit ID of the source group for group-elements or family instance for nested-family. Default null is valid for name-based relations; these two ID-based relations require a value.（any） |
| `source_name` | — | Exact, case-insensitive source name: a level for level-rooms, area scheme for area-scheme-elements, or view template for view-template-dependents. Default null is valid for ID-based relations; name-based relations require a value from the catalog.（any） |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |
    | `pickup_timeout_seconds` | `300` | Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later.（integer） |
    | `timeout_seconds` | `120` | Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits.（integer） |

## 提示词

```text
1F 标高上都有哪些房间？
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
