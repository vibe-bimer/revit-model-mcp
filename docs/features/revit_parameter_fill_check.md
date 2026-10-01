# revit_parameter_fill_check

<p class="facts"><b>分组</b> 导出与检验　<b>类型</b> 读取（只读）　<b>起始版本</b> 0.6.0</p>

参数的填充率：有值 / 空 / 缺失，并给出抽样 ID

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `categories` ✔ | — | array — Required list of 1-20 category names from the categories catalog; no default. Matches any listed category and combines with level, workset and view filters. |
| `parameters` ✔ | — | array — Required list of 1-30 exact localized parameter names; no default. Each name uses the first LookupParameter match, with type fallback controlled by include_types; missing names are counted as missing. |
| `include_types` | `true` | boolean |
| `level` | — | any |
| `sample_limit` | `20` | integer — Maximum element IDs sampled per parameter for each empty and missing list, an integer from 1 to 100. Default 20 limits samples only; all matching elements contribute to counts. |
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
检查墙的防火等级填充率，给出空值的构件 ID
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
