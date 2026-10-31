---
description: "项目基点、测量点、场地与链接的位移（mm）/旋转（°）"
---

# 共享坐标

`revit_shared_coordinates`

<p class="facts"><span><b>分组</b> 导出与检验</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.2.0</span><span><b>版本</b> 已发布 0.9.0</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span></p>

项目基点、测量点、场地与链接的位移（mm）/旋转（°）

[同名集成分支页面](../platform/revit_shared_coordinates.md)

## 可复制提示词 {#prompts}

```text
报告项目的共享坐标和链接位移
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `process_id` | 否 | `null` | `integer / null` | 多个运行实例中选定的目标 Revit 进程 |

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

在导出或交付前读取项目坐标和测量坐标。

返回的数据包含项目基点／测量点、活动场地、项目位置，以及链接的偏移量和旋转角；偏移量单位为 mm，旋转角单位为度，均四舍五入到小数点后 1 位。
位置和链接列表各最多返回 100 个条目，不支持分页，同时提供总数；没有链接时 `sharedSiteFromLinks` 为空列表。
没有活动文档、读取失败或超时都会报错；不返回部分数据。

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
