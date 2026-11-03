---
description: "按两点建直线轴网，或给中点走三点定弧（mm）"
---

# 创建轴网

`revit_create_grid`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.10.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span><span><b>来源</b> 自研（本仓库）</span></p>

按两点建直线轴网，或给中点走三点定弧（mm）

!!! warning "动作工具默认允许，只读需显式开启"
    动作默认允许；机器策略 `ReadOnly`、工作站 `read-only` 文件或 `REVIT_MCP_READ_ONLY=1` 三者任一打开即拒绝动作（全新安装的机器策略默认只读）。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    同名轴网被拒绝；曲线固定在水平面上，共线三点建不了弧

## 可复制提示词 {#prompts}

```text
建一条叫 A 的轴线，从 (0,0) 到 (30000,0)
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `end_mm` | 是 | — | `array<number>` | 终点坐标 [x, y]（mm，水平面） |
| `label` | 是 | — | `string` | 轴号，写入 Grid.Name；重名会被拒绝 |
| `start_mm` | 是 | — | `array<number>` | 起点坐标 [x, y]（mm，水平面） |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `mid_mm` | 否 | `null` | `array<number> / null` | 可选弧中点 [x, y]；给出即三点定弧，不得与起终点共线 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

创建一条轴网，用于布局：`start_mm` 到 `end_mm` 的直线，或给出 `mid_mm` 时的三点圆弧。
`label` 是轴号，写入 Grid.Name；已存在同名轴网时会被拒绝，这样后续工具永远不会解析到有歧义的轴网。端点与中点都是模型 XY 坐标系中的 `[x, y]`，单位为毫米；曲线始终位于水平面上，且 `mid_mm` 不得与端点共线（共线三点定不出弧，会被拒绝）。
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
