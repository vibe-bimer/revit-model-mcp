# 导出 NWC

`revit_export_nwc`

<p class="facts"><span><b>分组</b> 导出与登记</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

在 Revit 工作站导出 Navisworks NWC，需要安装导出器；`settings_xml` 应用导出器参数。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `confirm_token` | 否 | None | any | 首次调用返回的确认令牌，用于确认破坏性操作。 |
| `convert_element_properties` | 否 | None | any |  |
| `convert_lights` | 否 | None | any |  |
| `convert_linked_cad_formats` | 否 | None | any |  |
| `coordinates` | 否 | None | any |  |
| `divide_file_into_levels` | 否 | None | any |  |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `element_ids` | 否 | None | any | 要处理的构件 Revit ID 列表。 |
| `export_element_ids` | 否 | None | any |  |
| `export_links` | 否 | None | any |  |
| `export_parts` | 否 | None | any |  |
| `export_room_as_attribute` | 否 | None | any |  |
| `export_room_geometry` | 否 | None | any |  |
| `export_urls` | 否 | None | any |  |
| `faceting_factor` | 否 | None | any |  |
| `find_missing_materials` | 否 | None | any |  |
| `overwrite` | 否 | False | boolean |  |
| `parameters` | 否 | None | any |  |
| `path` | 是 | — | string |  |
| `scope` | 否 | None | any |  |
| `settings_xml` | 否 | None | any |  |
| `view` | 否 | None | any | 视图的准确名称或十进制视图 ID。 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `timeout_seconds` | 否 | 1800 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Export NWC on the Revit workstation; needs the Navisworks exporter. settings_xml applies exporter XML values, explicit arguments take precedence. Replacing an existing file (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
