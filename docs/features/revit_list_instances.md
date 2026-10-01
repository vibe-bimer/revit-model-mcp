# revit_list_instances

<p class="facts"><b>分组</b> 连接与文档　<b>类型</b> 读取（只读）　<b>起始版本</b> 0.6.0</p>

列出在跑的 Revit 实例及其打开的文档

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |

??? note "通用参数"
    |  参数 | 默认 | 说明 |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |

## 提示词

```text
现在有几个 Revit 实例？各自打开什么模型？
```

## 年份支持

| 年份 | 状态 | 备注 |
| --- | --- | --- |
| 2020 | <span class="state ok">已实测</span> |  |
| 2026 | <span class="state ok">已实测</span> |  |
| 其它年份 | <span class="state part">仅构建</span> | 2022–2025 / 2027 |

---

[全部工具](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
