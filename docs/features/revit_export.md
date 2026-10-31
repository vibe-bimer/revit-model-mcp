---
description: "导出 PDF、DWG、IFC 或明细表 CSV，dry_run 返回计划文件名"
---

# 导出模型文件

`revit_export`

<p class="facts"><span><b>分组</b> 导出与检验</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

导出 PDF、DWG、IFC 或明细表 CSV，dry_run 返回计划文件名

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_export.md)

## 可复制提示词 {#prompts}

```text
把视图 'A-101' 导出成 PDF 到 'C:\Out'，先用 dry_run 看计划文件名。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `format` | 是 | — | `string` | 导出格式：`pdf` 或 `dwg` 或 `ifc` 或 `csv` |
| `all_sheets` | 否 | `false` | `boolean` | 是否导出全部图纸 |
| `confirm_token` | 否 | `null` | `string / null` | 首次调用返回、供第二次确认调用的令牌 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `options` | 否 | `null` | `object / null` | 按导出格式区分的选项 |
| `output_dir` | 否 | `null` | `string / null` | 导出文件的输出目录 |
| `overwrite` | 否 | `false` | `boolean` | 目标文件已存在时覆盖 |
| `sheet_set` | 否 | `null` | `string / null` | 要导出的图集名称 |
| `sheets` | 否 | `null` | `array<string / integer> / null` | 要导出的图纸名称或 ID 列表 |
| `views` | 否 | `null` | `array<string / integer> / null` | 要导出的视图列表 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `timeout_seconds` | 否 | `1800` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

在 Revit 工作站上导出 PDF、DWG、IFC 或明细表 CSV 文件；`dry_run` 返回计划生成的文件名。

替换已有文件（`overwrite=true`）需要先调用一次取得 `confirm_token`。

长时间操作在等待预算耗尽时可能返回 `status=running` 和 `jobId`；此时模型可能已经被更改，`revit_jobs` 会返回其结果。重新提交会重复该操作。

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
