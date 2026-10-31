---
description: "删除所选链接类型及其实例；dry_run 预览，删除后 Revit 内不可撤销"
---

# 移除链接

`revit_remove_links`

<p class="facts"><span><b>分组</b> 链接与协同</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

删除所选链接类型及其实例；dry_run 预览，删除后 Revit 内不可撤销

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_remove_links.md)

## 可复制提示词 {#prompts}

```text
先用 dry_run 预览，然后删除当前文档里的所有 Revit 链接
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `links` | 是 | — | `array<string / integer> / string` | 要删除的链接名称或 ID 列表，或 `*` 表示全部 |
| `confirm_token` | 否 | `null` | `string / null` | 首次调用返回的令牌，用于第二次确认调用 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `include_imported_cad` | 否 | `false` | `boolean` | 是否一并移除导入的 CAD 实例 |
| `kinds` | 否 | `null` | `array<string> / null` | 要移除的链接类别 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

删除选定的链接类型及其全部实例；`dry_run` 只做预览。该操作在 Revit 中无法撤销。

需要先调用一次取得 `confirm_token`，首次调用不改变任何内容。

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
