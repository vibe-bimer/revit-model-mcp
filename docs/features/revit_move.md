# revit_move

<p class="facts"><b>分组</b> 编辑　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.1.0</p>

按模型轴平移构件（mm）

!!! note "说明"
    支持 dry_run

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `dx_mm` ✔ | — | Move elements when adjusting their position; dx_mm, dy_mm and dz_mm are offsets in millimetres on model axes.（number） |
| `dy_mm` ✔ | — | Move elements when adjusting their position; dx_mm, dy_mm and dz_mm are offsets in millimetres on model axes.（number） |
| `element_ids` ✔ | — | 要移动的构件 ID（array） |
| `dry_run` | `false` | dry_run executes and rolls back, returning the same verification block without changing the model.（boolean） |
| `dz_mm` | `0` | Move elements when adjusting their position; dx_mm, dy_mm and dz_mm are offsets in millimetres on model axes.（number） |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## 提示词

```text
把这 3 个构件沿 X 移动 500 mm，先彩排
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
