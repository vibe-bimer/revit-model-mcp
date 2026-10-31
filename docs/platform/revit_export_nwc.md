---
description: "在 Revit 工作站导出 Navisworks NWC，需要安装导出器；`settings_xml` 应用导出器参数。"
---

# 导出 NWC

`revit_export_nwc`

<p class="facts"><span><b>分组</b> 导出与登记</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

在 Revit 工作站导出 Navisworks NWC，需要安装导出器；`settings_xml` 应用导出器参数。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `confirm_token` | 否 | `null` | any | 首次调用返回的确认令牌，用于确认破坏性操作。 |
| `convert_element_properties` | 否 | `null` | any | （集成分支契约未提供说明） |
| `convert_lights` | 否 | `null` | any | （集成分支契约未提供说明） |
| `convert_linked_cad_formats` | 否 | `null` | any | （集成分支契约未提供说明） |
| `coordinates` | 否 | `null` | any | （集成分支契约未提供说明） |
| `divide_file_into_levels` | 否 | `null` | any | （集成分支契约未提供说明） |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `element_ids` | 否 | `null` | any | 要处理的构件 Revit ID 列表。 |
| `export_element_ids` | 否 | `null` | any | （集成分支契约未提供说明） |
| `export_links` | 否 | `null` | any | （集成分支契约未提供说明） |
| `export_parts` | 否 | `null` | any | （集成分支契约未提供说明） |
| `export_room_as_attribute` | 否 | `null` | any | （集成分支契约未提供说明） |
| `export_room_geometry` | 否 | `null` | any | （集成分支契约未提供说明） |
| `export_urls` | 否 | `null` | any | （集成分支契约未提供说明） |
| `faceting_factor` | 否 | `null` | any | （集成分支契约未提供说明） |
| `find_missing_materials` | 否 | `null` | any | （集成分支契约未提供说明） |
| `overwrite` | 否 | `false` | boolean | （集成分支契约未提供说明） |
| `parameters` | 否 | `null` | any | （集成分支契约未提供说明） |
| `path` | 是 | — | string | （集成分支契约未提供说明） |
| `scope` | 否 | `null` | any | （集成分支契约未提供说明） |
| `settings_xml` | 否 | `null` | any | （集成分支契约未提供说明） |
| `view` | 否 | `null` | any | 视图的准确名称或十进制视图 ID。 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `timeout_seconds` | 否 | `1800` | integer | 本次调用的等待上限（秒）。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Export NWC on the Revit workstation; needs the Navisworks exporter. settings_xml applies exporter XML values, explicit arguments take precedence. Replacing an existing file (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
