---
description: "把主体的轴网与标高对齐到已载入的链接，可选创建与回滚预览，但不建立监视关系。"
---

# 对齐链接基准

`revit_align_link_datums`

<p class="facts"><span><b>分组</b> 链接与基准</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

把主体的轴网与标高对齐到已载入的链接，可选创建与回滚预览，但不建立监视关系。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `create_missing` | 否 | `true` | boolean | （集成分支契约未提供说明） |
| `create_plan_views` | 否 | `false` | boolean | （集成分支契约未提供说明） |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `grid_type` | 否 | `null` | any | （集成分支契约未提供说明） |
| `include_pinned` | 否 | `false` | boolean | （集成分支契约未提供说明） |
| `kinds` | 否 | `null` | any | （集成分支契约未提供说明） |
| `level_offset_mm` | 否 | `0` | number | （集成分支契约未提供说明） |
| `level_type` | 否 | `null` | any | （集成分支契约未提供说明） |
| `link` | 是 | — | string | （集成分支契约未提供说明） |
| `name_map` | 否 | `null` | any | （集成分支契约未提供说明） |
| `plan_view_type` | 否 | `null` | any | （集成分支契约未提供说明） |
| `prefix` | 否 | `""` | string | （集成分支契约未提供说明） |
| `reuse_matching` | 否 | `true` | boolean | （集成分支契约未提供说明） |
| `suffix` | 否 | `""` | string | （集成分支契约未提供说明） |
| `tolerance_mm` | 否 | `0.5` | number | （集成分支契约未提供说明） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `timeout_seconds` | 否 | `600` | integer | 本次调用的等待上限（秒）。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Align host grids and levels to a loaded link, with optional creation and rollback preview. Does not create a monitor relationship.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
