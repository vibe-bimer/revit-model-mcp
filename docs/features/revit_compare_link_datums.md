---
description: "对比宿主与一个已加载 Revit 链接的轴网和标高（不改动模型）"
---

# 对比链接标高轴网

`revit_compare_link_datums`

<p class="facts"><span><b>分组</b> 链接与协同</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

对比宿主与一个已加载 Revit 链接的轴网和标高（不改动模型）

[同名集成分支页面](../platform/revit_compare_link_datums.md)

## 可复制提示词 {#prompts}

```text
对比一下链接模型“结构参考.rvt”里的轴网和标高与当前项目有哪些差异？
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `link` | 是 | — | `string` | 要比较的已链接 Revit 模型名称 |
| `kinds` | 否 | `null` | `array<string> / null` | 要比较的链接类别 |
| `level_offset_mm` | 否 | `0` | `number` | 比较标高时施加的垂直偏移（单位 mm） |
| `name_map` | 否 | `null` | `object / null` | 宿主名称到链接名称的映射 |
| `prefix` | 否 | `""` | `string` | 用于筛选链接的名称前缀 |
| `process_id` | 否 | `null` | `integer / null` | 多个运行实例中选定的目标 Revit 进程 |
| `reuse_matching` | 否 | `true` | `boolean` | 是否复用已匹配的轴网与标高 |
| `suffix` | 否 | `""` | `string` | 匹配到的轴网与标高名称所加后缀 |
| `tolerance_mm` | 否 | `0.5` | `number` | 比较基准点时的容差（单位 mm） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `timeout_seconds` | 否 | `120` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

将主模型的轴网和标高与一个已加载的 Revit 链接进行比较。

返回轴网和标高的对比结果；不改变任何内容。

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
