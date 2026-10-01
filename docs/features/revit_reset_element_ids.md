# revit_reset_element_ids

<p class="facts"><b>分组</b> 批量与 ID　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.8.0</p>

同文档内换 ID：只对无宿主、无依赖的独立构件有效

!!! note "说明"
    覆盖率有限：机电 27/1089、建筑 373/954、结构 0%

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `element_ids` ✔ | — | 要换 ID 的构件；有宿主、有依赖、成组或属于 MEP 系统的会被拒绝（array） |
| `dry_run` | `false` | 彩排：替换后回滚，先跑一次看哪些构件不合格（boolean） |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## 提示词

```text
给选中的这 27 个独立构件换新 ID
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state part">仅构建</span> | 覆盖率有限：机电 27/1089、建筑 373/954、结构 0% |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
