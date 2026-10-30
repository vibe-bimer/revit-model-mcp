---
description: "按参数与类目统计已填、空值与缺失数量，并给出空值和缺失构件的示例 ID。"
---

# 参数填充检查

`revit_parameter_fill_check`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，但参数不同</span><span><b>本页契约适用于发布版</b> 否</span></p>

按参数与类目统计已填、空值与缺失数量，并给出空值和缺失构件的示例 ID。

[同名发布版页面](../features/revit_parameter_fill_check.md)

## 与发布版的契约差异 {#contract-diff}

下表由注册表 inputSchema 自动比较得出，不是手写清单。

- 仅发布版有参数 pickup_timeout_seconds
- 仅集成分支有参数 process_id

本页契约适用于集成分支，不适用于发布版 0.9.0；照抄分支参数会在发布版上失败。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `categories` | 是 | — | array | Category names (1 to 20) from the categories catalog; matches any listed category. |
| `include_types` | 否 | `true` | boolean |  |
| `level` | 否 | `null` | any |  |
| `parameters` | 是 | — | array | Exact localized parameter names (1 to 30); names that do not match count as missing. |
| `sample_limit` | 否 | `20` | integer | Maximum sampled element IDs per empty and missing list, 1 to 100 (default 20); counts always cover all elements. |
| `view` | 否 | `null` | any | 视图的准确名称或十进制视图 ID。 |
| `workset` | 否 | `null` | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | `120` | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs. Numeric zero counts as filled. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
