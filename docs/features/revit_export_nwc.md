---
description: "在 Revit 工作站导出 NWC，需装 Navisworks 导出器；覆盖已有文件需确认令牌"
---

# 导出 Navisworks NWC

`revit_export_nwc`

<p class="facts"><span><b>分组</b> 导出与检验</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

在 Revit 工作站导出 NWC，需装 Navisworks 导出器；覆盖已有文件需确认令牌

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_export_nwc.md)

## 可复制提示词 {#prompts}

```text
把当前视图导出成 NWC 到 D:\\output\\塔楼.nwc，文件已存在就覆盖
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `path` | 是 | — | `string` | 导出的 `.nwc` 文件路径 |
| `confirm_token` | 否 | `null` | `string / null` | 首次调用返回、用于第二次确认调用的令牌 |
| `convert_element_properties` | 否 | `null` | `boolean / null` | 是否把构件属性转换为 NWC 属性 |
| `convert_lights` | 否 | `null` | `boolean / null` | 是否把灯具转换为 `.nwc` 几何 |
| `convert_linked_cad_formats` | 否 | `null` | `boolean / null` | 是否在导出时转换链接的 CAD 格式 |
| `coordinates` | 否 | `null` | `string / null` | 导出使用的坐标系 |
| `divide_file_into_levels` | 否 | `null` | `boolean / null` | 是否按标高拆分导出文件 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `element_ids` | 否 | `null` | `array<integer> / null` | 构件 ID 列表（无单位的 Revit ID） |
| `export_element_ids` | 否 | `null` | `boolean / null` | 是否在 `.nwc` 中导出构件 ID |
| `export_links` | 否 | `null` | `boolean / null` | 是否随文件导出链接模型 |
| `export_parts` | 否 | `null` | `boolean / null` | 要导出的模型部件 |
| `export_room_as_attribute` | 否 | `null` | `boolean / null` | 是否把房间导出为属性 |
| `export_room_geometry` | 否 | `null` | `boolean / null` | 是否在 `.nwc` 中导出房间几何 |
| `export_urls` | 否 | `null` | `boolean / null` | 是否随文件导出 URL |
| `faceting_factor` | 否 | `null` | `number / null` | 导出面片细分因子 |
| `find_missing_materials` | 否 | `null` | `boolean / null` | 是否查找缺失的材质 |
| `overwrite` | 否 | `false` | `boolean` | 目标文件已存在时覆盖 |
| `parameters` | 否 | `null` | `string / null` | 要统计的参数名列表 |
| `scope` | 否 | `null` | `string / null` | 导出范围：`model`、`view` 或 `selection` |
| `settings_xml` | 否 | `null` | `string / null` | 导出设置文件路径 |
| `view` | 否 | `null` | `string / integer / null` | 视图名称（或视图 ID） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `timeout_seconds` | 否 | `1800` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

在 Revit 工作站上导出 NWC，需要安装 Navisworks 导出器。`settings_xml` 应用导出器的 XML 取值，显式传入的参数优先。

覆盖已有文件（`overwrite=true`）需要先调用一次取得 `confirm_token`。

耗时较长的动作在等待预算用尽时可能返回 `status=running` 和 `jobId`；此时模型可能已经被修改，`revit_jobs` 会返回它的结果。重新提交会重复该动作。

如果有多个 Revit 实例正在运行，必须提供 `document`；否则任意实例都可能响应。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
