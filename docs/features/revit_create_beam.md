---
description: "沿给定轴线在标高上放一根结构梁，可写结构用途与竖向偏移（mm）"
---

# 创建梁

`revit_create_beam`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.1.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span><span><b>来源</b> 自研（本仓库）</span></p>

沿给定轴线在标高上放一根结构梁，可写结构用途与竖向偏移（mm）

!!! warning "动作工具默认允许，只读需显式开启"
    动作默认允许；机器策略 `ReadOnly`、工作站 `read-only` 文件或 `REVIT_MCP_READ_ONLY=1` 三者任一打开即拒绝动作（全新安装的机器策略默认只读）。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    走曲线+标高的重载，端点不吸附；竖向偏移写族的标高参数，只有包围盒真的抬升才算写进去，否则改为移动实例，两条路都不成立就报错而不是放在标高上

## 可复制提示词 {#prompts}

```text
在 2F 从 (0,0) 到 (6000,0) 放一根 300x600 的混凝土梁，梁顶降 150
```

```text
在 1F 从 (0,0) 到 (6000,0) 放一根钢梁，结构用途设成 Girder
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `end_mm` | 是 | — | `array<number>` | 轴终点，[x,y]（mm）；与起点重合会被拒绝 |
| `family` | 是 | — | `string` | 族名称 |
| `level` | 是 | — | `string` | 标高名称（用 revit_list_catalog 查到的本地化名称） |
| `start_mm` | 是 | — | `array<number>` | 轴起点，[x,y]（mm）；按给定坐标放，不做吸附 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `structural_usage` | 否 | `null` | `string / null` | 结构用途（Girder / Joist / Purlin / Bearing / Other 等）；缺省沿用族自己的设定 |
| `type_name` | 否 | `null` | `string / null` | 类型名称（与族一起定位） |
| `z_offset_mm` | 否 | `0` | `number` | 相对参考标高的竖向偏移（mm）；落在哪个参数以实例读回为准 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

沿 `start_mm` 到 `end_mm` 的轴线，在 `level` 上放一根 `family`（可指定 `type_name`）的结构梁。
两个端点都是模型 XY 坐标系中的 `[x, y]`，单位为毫米；坐标按给定值放，端点不做吸附——Revit 没有程序化吸附接口，`SetEndReference` 只对模型里已经连接的端有效。放置走曲线与标高的重载，因此标高与轴线都由调用者给定，不需要面引用。
`structural_usage` 写入 FamilyInstance.StructuralUsage，取值是结构用途枚举的名称。`z_offset_mm` 是相对参考标高的竖向偏移：先写族的起点与终点标高偏移，再试实例的标高参数，只有包围盒真的按偏移抬升才算写进去——族可以接受值却把梁留在标高上；参数都不抬升时改为移动实例，移动也不抬升就报错，不把没落的偏移当成已放置。偏移最终落在哪个参数由创建后的读回给出。梁族必须已经在项目里，`type_name` 不存在时会列出该族现有的类型。
`dry_run` 会执行操作后回滚，在不改变模型的情况下返回相同的验证数据块。
同时打开多个模型时，传入 `document` 以指定目标模型；未知或有歧义的引用会被拒绝。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state ok">已实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
