---
description: "创建平面、剖面、三维或详图视图；包围盒坐标为模型毫米"
---

# 创建视图

`revit_create_view`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

创建平面、剖面、三维或详图视图；包围盒坐标为模型毫米

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_create_view.md)

## 可复制提示词 {#prompts}

```text
创建一个名为"三层平面"的楼层平面视图，比例 1:100
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `kind` | 是 | — | `string` | 视图类型：`floor_plan` 或 `ceiling_plan` 或 `structural_plan` 或 `section` 或 `3d` 或 `drafting` |
| `box` | 否 | `null` | `any / null` | 视图裁剪框，含 `min_mm` 与 `max_mm` 模型坐标 |
| `detail_level` | 否 | `null` | `string / null` | 新视图的详细程度 |
| `display_style` | 否 | `null` | `string / null` | 视图显示样式，如 `hidden_line` 或 `shaded` |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `element_ids` | 否 | `null` | `array<integer> / null` | 构件 ID 列表（无单位的 Revit ID） |
| `level` | 否 | `null` | `string / null` | 标高名称（用 revit_list_catalog 查到的本地化名称） |
| `name` | 否 | `null` | `string / null` | 新建视图的名称 |
| `scale` | 否 | `null` | `integer / null` | 新视图的比例 |
| `template` | 否 | `null` | `string / null` | 创建视图时套用的视图模板名称 |
| `view_family_type` | 否 | `null` | `string / null` | 新建视图所用的视图族类型名称 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

创建平面视图、剖面视图、三维视图或绘图视图。无边界的三维视图显示整个模型，采用着色显示和精细详细程度。

范围框坐标使用模型 mm。

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
