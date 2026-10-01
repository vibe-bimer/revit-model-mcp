# revit_set_parameter

<p class="facts"><b>分组</b> 编辑　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.1.0</p>

按参数名写值（长度 mm、面积 m²，其余按内部单位）

!!! note "说明"
    支持 dry_run

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `element_id` ✔ | — | integer |
| `parameter` ✔ | — | string |
| `value` ✔ | — | string |
| `dry_run` | `false` | boolean |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change. |

## 提示词

```text
把这些墙的防火等级改成 2 小时
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
