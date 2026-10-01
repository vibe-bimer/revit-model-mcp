# 导出视图图片

`revit_export_view`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.3.0</span></p>

把视图导出成 PNG 图片（1–4000 像素）

## 可复制提示词 {#prompts}

```text
把 1F 平面导出成 PNG，宽度 2000 像素
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `view` | 是 | — | `string` | 视图名称（或视图 ID） |
| `pixel_size` | 否 | `1600` | `integer` | 输出图片长边像素（1–4000） |
| `save_to` | 否 | `null` | `string / null` | MCP 客户端机器上的新 PNG 文件路径，不是 Revit 工作站路径；文件已存在会报错 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

当数字无法解释几何形状时，将指定视图导出为 PNG。

返回的数据包含 MCP 客户端上的 `localPath`、图像宽度／高度（单位为像素）、`sizeBytes` 和视图元数据，不包含 base64。
导出不会改变活动视图，也不会写入模型；可用于检查轮廓、区域和房间边界。
文档不存在、视图未知或不受支持、目标文件已存在、未生成 PNG 或下载失败都会报错。
使用默认的 120 秒响应等待预算和 300 秒任务领取等待预算；超时会报错，不返回部分数据。

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
