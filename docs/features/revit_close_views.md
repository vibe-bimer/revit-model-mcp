---
description: "关闭当前文档中打开的 UI 视图"
---

# 关闭视图

`revit_close_views`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

关闭当前文档中打开的 UI 视图

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_close_views.md)

## 可复制提示词 {#prompts}

```text
关闭除“L1 平面图”以外的所有打开视图。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `keep_active` | 否 | `true` | `boolean` | 是否保留当前激活的视图 |
| `process_id` | 否 | `null` | `integer / null` | 多个运行实例中选定的目标 Revit 进程 |
| `views` | 否 | `null` | `array<string> / null` | 要关闭的视图名称列表 |

</div>

## 功能说明与返回结果 {#contract}

关闭活动文档中已打开的 UI 视图。

`views` 指定要关闭的视图；省略时关闭除活动视图外的所有打开视图，`keep_active` 为真时保留活动视图。
无法关闭的视图会被拒绝，并在结果中报告原因。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
