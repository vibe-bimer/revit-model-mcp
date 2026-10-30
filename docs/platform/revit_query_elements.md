# 查询构件

`revit_query_elements`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

分页读取符合条件的构件行，长度用毫米、面积用平方米、体积用立方米；`hasMore` 表示还有下一页。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `area_scheme` | 否 | None | any | Exact area-scheme name, case-insensitive. |
| `categories` | 否 | None | any |  |
| `family` | 否 | None | any |  |
| `fields` | 否 | None | any |  |
| `include_geometry` | 否 | False | boolean | Include location, boundingBox and roomCenterMm in model mm. Default false; true enlarges the response. |
| `level` | 否 | None | any |  |
| `limit` | 否 | 100 | integer | 返回条数上限。 |
| `offset` | 否 | 0 | integer | 分页起始位置。 |
| `parameter_filters` | 否 | None | any | AND-combined filters: parameter (exact localized name), operator (equals, contains, greater, less, empty, not-empty, exists) and value. Numbers use mm, m2, m3 or display units. |
| `phase` | 否 | None | any |  |
| `sort_direction` | 否 | asc | string | asc (default) or desc, case-insensitive. |
| `sort_field` | 否 | id | string | System field (e.g. id, category, level) or exact localized parameter name to sort by; default id. |
| `type_name` | 否 | None | any | Exact type name, case-insensitive. |
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
Read a page of matching element rows. Lengths use mm, areas m2, volumes m3; optional geometry is in model mm. roomCenterMm is a point inside the room, a bounding-box centre can lie outside it. hasMore=true means further pages exist. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
