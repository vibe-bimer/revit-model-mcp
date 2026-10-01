# revit_export_view

<p class="facts"><b>分组</b> 视图与截图　<b>类型</b> 读取（只读）　<b>起始版本</b> 0.3.0</p>

把视图导出成 PNG 图片（1–4000 像素）

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `view` ✔ | — | 视图名称（或视图 ID）（string） |
| `pixel_size` | `1600` | 输出图片长边像素（1–4000）（integer） |
| `save_to` | — | 工作站上的输出路径；文件已存在会报错（any） |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |

## 提示词

```text
把 1F 平面导出成 PNG，宽度 2000 像素
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
