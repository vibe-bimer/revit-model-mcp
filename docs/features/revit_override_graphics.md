---
description: "在指定视图里给构件着色，reset 可还原本次会话的覆盖"
---

# 着色构件

`revit_override_graphics`

<p class="facts"><span><b>分组</b> 选中与显示</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 选择 / 视图状态</span></p>

在指定视图里给构件着色，reset 可还原本次会话的覆盖

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_override_graphics.md)

## 可复制提示词 {#prompts}

```text
把这几根柱子在 1F 平面涂成红色，其他构件调淡
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `element_ids` | 是 | — | `array<integer>` | 构件 ID 列表（无单位的 Revit ID） |
| `color` | 否 | `"#FF0000"` | `string` | 覆盖颜色的十六进制值，如 `#FF0000` |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `fill` | 否 | `true` | `boolean` | 是否填充覆盖的图形 |
| `halftone_others` | 否 | `false` | `boolean` | 其他构件是否以半色调显示 |
| `line_weight` | 否 | `null` | `integer / null` | 要覆盖的线宽值 |
| `reset` | 否 | `false` | `boolean` | true 时恢复当前视图的临时隐藏 / 隔离；配合空 element_ids 列表使用 |
| `transparency` | 否 | `0` | `integer` | 覆盖颜色的透明度百分比（0-100） |
| `views` | 否 | `"active"` | `string / array<string / integer>` | 要应用覆盖的视图，`active` 表示当前视图 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

在选定的模型视图中为构件着色；`reset` 会恢复保存在本次 Revit 会话中的覆盖设置。

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
