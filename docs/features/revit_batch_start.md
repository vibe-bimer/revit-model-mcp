---
description: "对本地、UNC 或 RSN 模型启动持久只读采集"
---

# 启动批量采集

`revit_batch_start`

<p class="facts"><span><b>分组</b> 批量作业</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

对本地、UNC 或 RSN 模型启动持久只读采集

[同名集成分支页面](../platform/revit_batch_start.md)

## 可复制提示词 {#prompts}

```text
扫描 \\fileserver\models 下的所有 RVT 模型并开始批量采集
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `folder` | 否 | `null` | `string / null` | 要扫描的模型目录路径 |
| `open_timeout_minutes` | 否 | `null` | `integer / null` | 每个模型打开的超时上限（单位分钟） |
| `parameter_rules` | 否 | `null` | `array<object> / null` | 快照要包含的类别与参数对列表 |
| `paths` | 否 | `null` | `array<string> / null` | 批量处理的模型文件路径 |
| `recursive` | 否 | `false` | `boolean` | 是否扫描子目录中的模型 |
| `years` | 否 | `null` | `array<integer> / null` | 要采集的 Revit 版本年份列表 |

</div>

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

对本地、UNC 或 RSN 模型启动一次持久化的只读运行。

`open_timeout_minutes` 是每个模型的打开时限（默认 30，在内存中升级时为 45）。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
