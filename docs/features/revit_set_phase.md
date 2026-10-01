# revit_set_phase

<p class="facts"><b>分组</b> 阶段　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.3.0</p>

赋创建阶段 / 拆除阶段（空串清除，null 不变）

!!! note "说明"
    阶段顺序检查的 API 只在 2022+ ，2020 走兜底

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `created_phase` ✔ | — | 创建阶段名；空串清除、null 不变（any） |
| `demolished_phase` ✔ | — | any |
| `element_ids` ✔ | — | 要改阶段的构件 ID（array） |
| `dry_run` | `false` | boolean |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## 提示词

```text
把这些构件标成在“现有”阶段拆除
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state part">仅构建</span> | 阶段顺序检查的 API 只在 2022+ ，2020 走兜底 |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
