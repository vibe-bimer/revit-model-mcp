---
description: "为单个类别按命名字段和顺序创建明细表，支持筛选与排序分组；dry_run 会回滚"
---

# 创建明细表

`revit_create_schedule`

<p class="facts"><span><b>分组</b> 图纸与明细表</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

为单个类别按命名字段和顺序创建明细表，支持筛选与排序分组；dry_run 会回滚

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_create_schedule.md)

## 可复制提示词 {#prompts}

```text
给“门”类别建一个明细表，字段按 Mark、Level、Count 排列，命名为“门窗统计”。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `category` | 是 | — | `string` | 要创建明细表的构件类别名称 |
| `fields` | 是 | — | `array<string>` | 要返回或写入的字段；缺省用该工具的常用字段 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `filters` | 否 | `null` | `array<any> / null` | 明细表筛选条件列表，按字段、运算符和值 |
| `itemized` | 否 | `true` | `boolean` | 是否将相同行逐条列出 |
| `name` | 否 | `null` | `string / null` | 新明细表的名称 |
| `sort` | 否 | `null` | `array<any> / null` | 排序与分组规则列表，含字段与升降序 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

为单个类别按给定顺序和命名字段创建明细表，字段使用 Revit 界面名称，例如 `Mark`、`Level` 或 `Count`。

`filters` 按字段、运算符和值保留行；`sort` 排序，并在设置 `header` 或 `footer` 时对行分组。
长度单位为 mm，面积单位为 m2，体积单位为 m3。
`itemized=false` 会合并完全相同的行。

返回 `viewId` 和解析后的字段；无法识别的名称列在 `skipped` 中。
`dry_run` 会回滚。

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
