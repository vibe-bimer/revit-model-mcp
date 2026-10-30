# 目录列表

`revit_list_catalog`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

列出某一类目录：类目、族类型、标高、面积方案、视图、工作集、阶段或参数；默认上限 200 条。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `limit` | 否 | 200 | integer | 返回条数上限。 |
| `name_contains` | 否 | None | any | Case-insensitive substring of the view name. |
| `section` | 是 | — | string |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | 120 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
List catalog names for one section: categories, family-types, levels, area-schemes, views, worksets, phases or parameters. name_contains filters names case-insensitively; limit bounds results (default 200, maximum 2000). Returns total before the limit and hasMore. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
