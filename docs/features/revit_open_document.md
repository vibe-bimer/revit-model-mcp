---
description: "在工作站打开本地、UNC 或 RSN 模型，中央模型默认分离打开"
---

# 打开模型

`revit_open_document`

<p class="facts"><span><b>分组</b> 文档与进程</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

在工作站打开本地、UNC 或 RSN 模型，中央模型默认分离打开

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_open_document.md)

## 可复制提示词 {#prompts}

```text
帮我打开中央模型 'Tower.rvt'，用分离模式打开。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `path` | 是 | — | `string` | 要打开的模型文件路径 |
| `activate` | 否 | `false` | `boolean` | 打开后是否激活该文档 |
| `audit` | 否 | `false` | `boolean` | 是否在打开后审计模型 |
| `mode` | 否 | `"detached"` | `string` | 打开方式：`detached`、`detached_discard_worksets`、`local_copy` 或 `read_only_local` |
| `process_id` | 否 | `null` | `integer / null` | 目标 Revit 进程 ID（在多个运行实例中选定） |
| `worksets` | 否 | `"all"` | `string / object` | 工作集处理：`all`、`none` 或打开与关闭列表 |

</div>

## 功能说明与返回结果 {#contract}

打开本地、UNC 或 RSN 模型；中心模型默认以分离方式打开，不支持云路径。

长时间操作在等待预算耗尽时可能返回 `status=running` 和 `jobId`；此时模型可能已经被更改，`revit_jobs` 会返回其结果。重新提交会重复该操作。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state part">仅构建，未实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
