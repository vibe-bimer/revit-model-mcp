# 关系列表

`revit_list_relations`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

读取模型对象的归属或依赖关系，如标高与房间、面积方案与构件、视图样板与从属视图、组与嵌套族。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `relation` | 是 | — | string |  |
| `source_id` | 否 | None | any | Revit ID of the source group (group-elements) or family instance (nested-family). |
| `source_name` | 否 | None | any | Source name, case-insensitive: a level (level-rooms), area scheme (area-scheme-elements) or view template (view-template-dependents). |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | 120 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Read model object membership or dependencies. relation is level-rooms, area-scheme-elements or view-template-dependents (with source_name), or group-elements or nested-family (with source_id). A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
