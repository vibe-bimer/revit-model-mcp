---
description: "在视图里按类别或构件 ID 加标记，房间标记需平面视图"
---

# 标注构件

`revit_tag_elements`

<p class="facts"><span><b>分组</b> 选中与显示</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 选择 / 视图状态</span></p>

在视图里按类别或构件 ID 加标记，房间标记需平面视图

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_tag_elements.md)

## 可复制提示词 {#prompts}

```text
给 1F 平面上所有门加上标记
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | 是 | — | `string / integer` | 视图名称（或视图 ID） |
| `categories` | 否 | `null` | `array<string> / null` | 类别名称列表（取并集） |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `element_ids` | 否 | `null` | `array<integer> / null` | 构件 ID 列表（无单位的 Revit ID） |
| `leader` | 否 | `false` | `boolean` | 是否添加引线 |
| `max_elements` | 否 | `5000` | `integer` | 本次最多标注的构件数量 |
| `orientation` | 否 | `"horizontal"` | `string` | 标签文字方向：`horizontal` 或 `vertical` |
| `skip_tagged` | 否 | `true` | `boolean` | 是否跳过已标注的构件 |
| `tag_type` | 否 | `null` | `string / null` | 要使用的标记类型 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

在视图中为构件添加标记，输入按类别名称或按构件 ID 选择，两者必须且只能选择其一。

在 `createdElementIds` 中返回已创建的标记 ID；已标记的构件会被跳过，除非 `skip_tagged` 为 `false`；无法标记的输入列在 `skipped` 中。

`tag_type` 可匹配标记类型名称、族名称或 `Family: Type`；其他情况使用默认标记类型。

房间标记需要平面视图。

`dry_run` 会回滚，并返回将会创建的标记。

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
