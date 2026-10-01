# revit_place_family

<p class="facts"><b>分组</b> 编辑　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.2.0</p>

在指定标高放置已载入的族实例，可绕 Z 旋转

!!! note "说明"
    2026 未真机验证

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `family` ✔ | — | string |
| `level` ✔ | — | string |
| `type_name` ✔ | — | any |
| `x_mm` ✔ | — | number |
| `y_mm` ✔ | — | number |
| `dry_run` | `false` | boolean |
| `rotation_deg` | `0` | number |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change. |

## 提示词

```text
在 1F 的 (3000, 4000) 放一个 900x2100 的门
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state part">仅构建</span> | 2026 未真机验证 |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
