---
description: "把视图导出成 PNG 图片（1–4000 像素）"
---

# 导出视图图片

`revit_export_view`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.3.0</span><span><b>版本</b> 已发布 0.9.0</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

把视图导出成 PNG 图片（1–4000 像素）

[同名集成分支页面](../platform/revit_export_view.md)

## 可复制提示词 {#prompts}

```text
把 1F 平面导出成 PNG，宽度 2000 像素
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | 是 | — | `string` | 视图名称（或视图 ID） |
| `output_path` | 否 | `null` | `string / null` | 新的 PNG 文件路径，在运行本服务器的机器上解析；文件已存在时报错。默认为 `null` 时下载到临时目录并返回 `localPath` |
| `pixel_size` | 否 | `1600` | `integer` | 输出图片长边像素（1–4000） |
| `process_id` | 否 | `null` | `integer / null` | 多个运行实例中选定的目标 Revit 进程 |

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

当数字无法解释几何形状时，将指定视图导出为 PNG。

返回的数据包含 MCP 客户端上的 `localPath`、图像宽度／高度（单位为像素）、`sizeBytes` 和视图元数据，不包含 base64。
导出不会改变活动视图，也不会写入模型；可用于检查轮廓、区域和房间边界。
文档不存在、视图未知或不受支持、目标文件已存在、未生成 PNG 或下载失败都会报错。
使用默认的 120 秒响应等待预算和 300 秒任务拾取等待预算；超时会报错，不返回部分数据。

如果有多个 Revit 实例正在运行，必须提供 `document`；否则任意实例都可能响应。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state ok">已实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
