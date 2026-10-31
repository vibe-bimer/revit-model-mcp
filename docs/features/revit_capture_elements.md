---
description: "生成标记 1–500 个构件的 PNG 截图，临时视图会回滚"
---

# 构件截图

`revit_capture_elements`

<p class="facts"><span><b>分组</b> 选中与显示</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

生成标记 1–500 个构件的 PNG 截图，临时视图会回滚

[同名集成分支页面](../platform/revit_capture_elements.md)

## 可复制提示词 {#prompts}

```text
把 1F 平面上这几根梁高亮截一张图，做问题记录用
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `element_ids` | 是 | — | `array<integer>` | 构件 ID 列表（无单位的 Revit ID） |
| `mode` | 否 | `"3d"` | `string` | 捕捉模式，`3d` 表示三维视图 |
| `output_path` | 否 | `null` | `string / null` | 新的 PNG 输出路径，在运行本服务的机器上解析 |
| `padding_mm` | 否 | `1500` | `number` | 截图构件四周的留白宽度（单位 mm） |
| `pixel_size` | 否 | `1600` | `integer` | 输出图片长边像素（1–4000） |
| `process_id` | 否 | `null` | `integer / null` | 在多个运行实例中选定的目标 Revit 进程，优先于 `document` |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

渲染一张高亮的 `.png` 图像，标记 1 到 500 个构件，用作问题证据。

支持 `3d` 或 `plan` 模式，通过本地或 SSH 传输。

临时视图会被回滚。

非空 `skipped` 列表表示结果不完整；`skippedCount` 统计所有被跳过的条目。

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
