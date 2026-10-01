# revit_select

<p class="facts"><b>分组</b> 选中与显示　<b>类型</b> 动作（会改模型）　<b>起始版本</b> 0.1.0</p>

在 Revit 里选中指定构件（空列表=清除选择）

!!! note "说明"
    不改模型

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `element_ids` ✔ | — | 要选中的构件 ID；传空列表清除选择（array） |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## 提示词

```text
选中 ID 为 123456 的构件
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
