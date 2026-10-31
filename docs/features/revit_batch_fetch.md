---
description: "把已完成的快照下载为新的本地文件，不覆盖已有文件"
---

# 获取批量快照

`revit_batch_fetch`

<p class="facts"><span><b>分组</b> 批量作业</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

把已完成的快照下载为新的本地文件，不覆盖已有文件

[同名集成分支页面](../platform/revit_batch_fetch.md)

## 可复制提示词 {#prompts}

```text
把批次 'run-2026-10-31' 的快照下载到 'C:\Snapshots'，别覆盖已有文件。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `output_dir` | 是 | — | `string` | 快照下载到的本地目录 |
| `run_id` | 是 | — | `string` | 批量采集运行的 `run_id` 标识 |

</div>

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

将已完成的快照下载为新的本地文件，写入 `output_dir`，不覆盖已有文件。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
