# revit_rebuild_model_ids

<p class="facts"><b>分组</b> 批量与 ID　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.8.0</p>

整模型换新 ID：把三维视图可选中的构件重建为一份或多份新模型

!!! note "说明"
    源模型只读；2020 实测每份 899 构件、ID 零重叠

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `destination_path` ✔ | — | string |
| `copies` | `1` | integer |
| `dry_run` | `false` | boolean |
| `duplicate_names` | `"override"` | string |
| `overwrite` | `false` | boolean |
| `remove_template_levels` | `true` | boolean |
| `seed` | `0` | integer |
| `template_path` | — | any |
| `view` | — | any |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change. |

## 提示词

```text
把当前三维视图里能选中的构件重建到 E:\out\copy-{n}.rvt，出 10 份，每份 ID 都不要重复
```

```text
先彩排一次重建，告诉我多少个构件、新 ID 范围，先不要写文件
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state part">仅构建</span> | 源模型只读；2020 实测每份 899 构件、ID 零重叠 |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
