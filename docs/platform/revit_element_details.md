---
description: "按 Revit ID 读取构件的参数与几何，含类型参数与相关警告；几何用模型毫米。"
---

# 构件详情

`revit_element_details`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，但参数不同</span><span><b>本页契约适用于发布版</b> 否</span></p>

按 Revit ID 读取构件的参数与几何，含类型参数与相关警告；几何用模型毫米。

[同名发布版页面](../features/revit_element_details.md)

## 与发布版的契约差异 {#contract-diff}

下表由注册表 inputSchema 自动比较得出，不是手写清单。

- 参数 element_id 约束 minimum：发布版 — / 集成分支 1
- 仅发布版有参数 pickup_timeout_seconds
- 仅集成分支有参数 process_id

本页契约适用于集成分支，不适用于发布版 0.9.0；照抄分支参数会在发布版上失败。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `element_id` | 是 | — | integer | Revit element ID from revit_query_elements or revit_view_elements. |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | 120 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Read parameters and geometry of an element by Revit ID, with its type parameters and related warnings. Geometry is in model mm; roomCenterMm is a point inside the room. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
