---
description: "从快照本地生成 Excel 报告，无需连接 Revit"
---

# 生成快照报告

`revit_build_report`

<p class="facts"><span><b>分组</b> 导出与检验</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

从快照本地生成 Excel 报告，无需连接 Revit

[同名集成分支页面](../platform/revit_build_report.md)

## 可复制提示词 {#prompts}

```text
把 snapshots 目录里的快照汇总成一份 Excel 报告
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `output_path` | 是 | — | `string` | 新的 `.xlsx` 文件路径，在运行本服务器的机器上解析；已有文件不会被覆盖 |
| `snapshots_dir` | 是 | — | `string` | 存放 schema 版本 1 JSON 快照的目录，位于 MCP 客户端机器 |
| `findings` | 否 | `null` | `array<object> / null` | 可选的发现项，含 model、severity、rule、`element_ids` 与 recommendation |
| `previous_dir` | 否 | `null` | `string / null` | 用于「变更」工作表比对的早期快照目录，可选 |

</div>

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

不连接 Revit，直接从快照文件读取数据，在本地生成 Excel 报告，不需要 Revit 在运行。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
