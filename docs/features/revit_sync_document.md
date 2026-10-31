---
description: "将工作共享文档与中心文件同步；首次调用不改动任何内容，需用返回的 confirm_token 再确认"
---

# 同步文档

`revit_sync_document`

<p class="facts"><span><b>分组</b> 文档与进程</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

将工作共享文档与中心文件同步；首次调用不改动任何内容，需用返回的 confirm_token 再确认

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_sync_document.md)

## 可复制提示词 {#prompts}

```text
把当前工作共享文档同步到中心文件，备注“更新门窗标注”。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `comment` | 是 | — | `string` | 同步提交时附带的说明 |
| `compact` | 否 | `false` | `boolean` | 同步时是否压缩中央模型 |
| `confirm_token` | 否 | `null` | `string / null` | 首次调用返回的令牌，用于第二次确认调用 |
| `process_id` | 否 | `null` | `integer / null` | 在多个运行实例中选定的目标 Revit 进程 |
| `relinquish` | 否 | `"all"` | `string / object` | 要放弃所有权的用户，`all` 表示全部用户 |
| `save_local_after` | 否 | `true` | `boolean` | 同步后是否保存本地副本 |
| `save_local_before` | 否 | `true` | `boolean` | 同步前是否先保存本地副本 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 是 | — | `string` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

将工作共享文档与中心模型同步。

需要先调用一次以获得 `confirm_token`，该次调用不改变任何内容。

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
