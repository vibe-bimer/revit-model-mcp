# revit_create_floor

<p class="facts"><b>分组</b> 编辑　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.2.0</p>

按闭合轮廓建楼板（至少 3 个顶点，mm）

!!! note "说明"
    2020 走 Document.Create.NewFloor，2022+ 走 Floor.Create

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `floor_type` ✔ | — | points_mm are model XY polygon vertices in millimetres (at least 3; the boundary closes automatically); null floor_type chooses the first floor type.（any） |
| `level` ✔ | — | Create a floor from a closed boundary for layout on a named level.（string） |
| `points_mm` ✔ | — | points_mm are model XY polygon vertices in millimetres (at least 3; the boundary closes automatically); null floor_type chooses the first floor type.（array） |
| `dry_run` | `false` | dry_run executes and rolls back, returning the same verification block without changing the model.（boolean） |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## 提示词

```text
用这四个点在 2F 建一块楼板
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state part">仅构建</span> | 2020 走 Document.Create.NewFloor，2022+ 走 Floor.Create |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
