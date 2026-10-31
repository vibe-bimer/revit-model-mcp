---
description: "在工作站用模板新建项目或族文件"
---

# 新建模型

`revit_new_document`

<p class="facts"><span><b>分组</b> 文档与进程</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

在工作站用模板新建项目或族文件

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_new_document.md)

## 可复制提示词 {#prompts}

```text
用 'Metric Generic Model.rte' 模板新建一个项目，命名为 '塔楼方案'。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `activate` | 否 | `true` | `boolean` | 是否让新文档成为活动文档 |
| `kind` | 否 | `"project"` | `string` | 新文档类型，`project` 或 `family` |
| `name` | 否 | `null` | `string / null` | 新建文档的名称 |
| `process_id` | 否 | `null` | `integer / null` | 目标 Revit 进程 ID（在多个运行实例中选定） |
| `save_as` | 否 | `null` | `string / null` | 新建文档另存到的文件路径 |
| `template` | 否 | `null` | `string / null` | 新文档使用的模板文件 |

</div>

## 功能说明与返回结果 {#contract}

在 Revit 工作站上从样板新建项目或族，`kind` 决定新建项目还是族，`template` 指定所用的样板。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
