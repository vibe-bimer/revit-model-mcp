# revit_rebuild_model_ids

<p class="facts"><b>分组</b> 批量与 ID　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.8.0</p>

整模型换新 ID：把三维视图可选中的构件重建为一份或多份新模型

!!! note "说明"
    源模型只读；2020 实测每份 899 构件、ID 零重叠

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `destination_path` ✔ | — | 新模型路径（.rvt）；含 {n} 时按份编号（string） |
| `copies` | `1` | 一份新模型连续出多少份（1–50），每份 ID 区间互不重叠（integer） |
| `dry_run` | `false` | 彩排：复制并给出映射后回滚，不写文件（boolean） |
| `duplicate_names` | `"override"` | 重名处理：override 保留源类型、reuse 沿用新模型版本（批量默认）、rename 旧回退路径（string） |
| `overwrite` | `false` | 目标文件已存在时覆盖（boolean） |
| `remove_template_levels` | `true` | 复制后删掉样板自带标高（默认删）（boolean） |
| `seed` | `0` | 先把 ID 推进 N 个再复制，用于预留互不重叠的号段（integer） |
| `template_path` | — | 起始样板文件（.rte/.rvt）路径；缺省用公制样板（any） |
| `view` | — | 视图名称（或视图 ID）（any） |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

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
