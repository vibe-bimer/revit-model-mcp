# revit_create_wall

<p class="facts"><b>分组</b> 编辑　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.2.0</p>

按两点建直墙（mm，指定标高、墙类型、高度）

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `end_mm` ✔ | — | array |
| `level` ✔ | — | string |
| `start_mm` ✔ | — | array |
| `wall_type` ✔ | — | any |
| `dry_run` | `false` | boolean |
| `height_mm` | `3000` | number |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change. |

## 提示词

```text
在 1F 从 (0,0) 到 (6000,0) 建一道 200mm 墙
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
