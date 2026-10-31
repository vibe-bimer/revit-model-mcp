---
description: "读取当前文档、打开的视图、选择集与所有打开的文档"
---

# 界面状态

`revit_ui_state`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

读取当前文档、打开的视图、选择集与所有打开的文档

[同名集成分支页面](../platform/revit_ui_state.md)

## 可复制提示词 {#prompts}

```text
我现在选中了什么？还开了哪些视图？
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `process_id` | 否 | `null` | `integer / null` | 在多个运行实例中选定的目标 Revit 进程，优先于 `document` |

</div>

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

读取当前文档、打开的视图、选择集以及已打开的文档。

响应包含当前文档、打开的视图、选择集以及已打开的文档。

非空 `skipped` 列表表示结果不完整；`skippedCount` 统计所有被跳过的条目。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
