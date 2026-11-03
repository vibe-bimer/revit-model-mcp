---
description: "从工作站载入一个族文件：整族，或只载入指定类型"
---

# 载入族文件

`revit_load_family_file`

<p class="facts"><span><b>分组</b> 族</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.10.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span><span><b>来源</b> 自研（本仓库）</span></p>

从工作站载入一个族文件：整族，或只载入指定类型

!!! warning "动作工具默认允许，只读需显式开启"
    动作默认允许；机器策略 `ReadOnly`、工作站 `read-only` 文件或 `REVIT_MCP_READ_ONLY=1` 三者任一打开即拒绝动作（全新安装的机器策略默认只读）。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    总是带族载入选项，不会弹出 Revit 自己的对话框；已有族复用，参数值默认不覆盖；路径不存在时报最近匹配。底座另有批量的 `revit_load_family`（收 `paths` 列表），本工具是单文件、可只取一个类型

## 可复制提示词 {#prompts}

```text
把 C:\lib\M_Door.rfa 载进来
```

```text
只载入 M_Door.rfa 里 0900 x 2100 这个类型
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `path` | 是 | — | `string` | 工作站上族文件的绝对路径（.rfa） |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `overwrite_parameters` | 否 | `false` | `boolean` | 用族里的值覆盖项目已有类型的参数值，默认不覆盖 |
| `type_name` | 否 | `null` | `string / null` | 只载入该类型；为空时载入整族 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

从工作站载入一个族文件：整族，或只载入 `type_name` 指定的那一个类型。
载入总是带族载入选项，所以不会弹出 Revit 自己的对话框；同名族已在项目里时复用它，且默认不覆盖既有的参数值——只有 `overwrite_parameters=true` 才用族里的值覆盖。
响应在 `fork` 块回报 `state`（`new` 或 `existing`）、`familyName` 与 `familyTypes`（每个类型的 `id` 与 `name`）。路径不存在时拒绝，并列出同目录下最接近的三个文件名。
`dry_run` 会执行操作后回滚，在不改变模型的情况下返回相同的验证数据块。
同时打开多个模型时，传入 `document` 以指定目标模型；未知或有歧义的引用会被拒绝。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
