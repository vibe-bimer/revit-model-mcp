---
description: "改单个视图的类别、工作集与过滤器可见性，dry_run 可预览"
---

# 设置视图可见性

`revit_set_view_visibility`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

改单个视图的类别、工作集与过滤器可见性，dry_run 可预览

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_set_view_visibility.md)

## 可复制提示词 {#prompts}

```text
在平面视图 'A-101' 里隐藏 OST_StructuralColumns 类别，先用 dry_run 预览。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | 是 | — | `string` | 视图名称（或视图 ID） |
| `category_classes` | 否 | `null` | `object / null` | 按类别子类名控制的可见性 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `filters` | 否 | `null` | `array<object> / null` | 视图可见性过滤条件 |
| `hide_categories` | 否 | `null` | `array<string / integer> / null` | 要隐藏的类别名称或 ID 列表 |
| `hide_categories_by_type` | 否 | `null` | `array<string> / null` | 按类型名称隐藏的类别列表 |
| `show_categories` | 否 | `null` | `array<string / integer> / null` | 要在视图中显示的类别列表 |
| `template_mode` | 否 | `null` | `string / null` | 可见性模板的应用模式 |
| `worksets` | 否 | `null` | `object / null` | 工作集可见性，含 `hide_mask` 与 `show_mask` 列表 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

在一个视图中修改类别、工作集和过滤器的可见性；`dry_run` 只做预览。

类别可以接受 Revit 界面名称、BuiltInCategory 名称（`OST_StructuralColumns`）、英文名称或 ID。

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
