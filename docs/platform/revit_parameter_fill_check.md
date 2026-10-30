# 参数填充检查

`revit_parameter_fill_check`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

按参数与类目统计已填、空值与缺失数量，并给出空值和缺失构件的示例 ID。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `categories` | 是 | — | array | Category names (1 to 20) from the categories catalog; matches any listed category. |
| `include_types` | 否 | True | boolean |  |
| `level` | 否 | None | any |  |
| `parameters` | 是 | — | array | Exact localized parameter names (1 to 30); names that do not match count as missing. |
| `sample_limit` | 否 | 20 | integer | Maximum sampled element IDs per empty and missing list, 1 to 100 (default 20); counts always cover all elements. |
| `view` | 否 | None | any | 视图的准确名称或十进制视图 ID。 |
| `workset` | 否 | None | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | 120 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs. Numeric zero counts as filled. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
