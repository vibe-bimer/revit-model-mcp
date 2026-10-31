---
description: "生成带构件快照的问题登记表 .xlsx，已存在的文件不覆盖"
---

# 问题登记表

`revit_issue_register`

<p class="facts"><span><b>分组</b> 导出与检验</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

生成带构件快照的问题登记表 .xlsx，已存在的文件不覆盖

[同名集成分支页面](../platform/revit_issue_register.md)

## 可复制提示词 {#prompts}

```text
把这 8 个问题整理成一份问题登记表 .xlsx
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `issues` | 是 | — | `array<object>` | 问题条目列表，含标题、类别、发现与严重级别 |
| `output_path` | 是 | — | `string` | 新的 `.xlsx` 问题登记表路径，在运行本服务器的机器上解析；已有文件会被拒绝 |
| `project` | 是 | — | `object` | 项目元数据对象 |
| `pixel_size` | 否 | `900` | `integer` | 输出图片长边像素（1–4000） |
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

写入一份新的本地 `.xlsx` 问题登记表，包含构件快照和评审文档。

接受 1 到 60 个问题；在 210 秒预算内最多捕获 25 张快照（按严重程度选取），失败的快照会写入单元格备注。

快照需要本地或 SSH 传输。

已存在的输出文件会被拒绝。

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
