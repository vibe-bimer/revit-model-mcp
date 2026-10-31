---
description: "就地编辑已打开的族或项目族，dry_run 会回滚全部改动"
---

# 编辑族

`revit_edit_families`

<p class="facts"><span><b>分组</b> 族</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

就地编辑已打开的族或项目族，dry_run 会回滚全部改动

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_edit_families.md)

## 可复制提示词 {#prompts}

```text
帮我编辑项目族 'M_Column' 的可见性参数，先用 dry_run 预览。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `operations` | 是 | — | `array<any>` | 族编辑操作列表，含增删参数、清理与赋值 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `families` | 否 | `null` | `array<string> / null` | 要编辑的族文件 |
| `overwrite_parameter_values` | 否 | `false` | `boolean` | 加载族时是否覆盖已有参数值 |
| `stop_on_error` | 否 | `true` | `boolean` | 遇到错误时是否停止编辑 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `timeout_seconds` | 否 | `1800` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

就地编辑已打开的族，或编辑指定名称的项目族（准确名称或 `["*"]`），每个族各经历一次载入循环。

`dry_run` 会回滚全部更改。

长时间操作在等待预算耗尽时可能返回 `status=running` 和 `jobId`；此时模型可能已经被更改，`revit_jobs` 会返回其结果。重新提交会重复该操作。

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
