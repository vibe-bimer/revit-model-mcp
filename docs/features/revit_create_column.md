---
description: "在指定标高的点上放一根结构柱，柱顶给标高或给高度（mm）"
---

# 创建柱

`revit_create_column`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.10.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span><span><b>来源</b> 自研（本仓库）</span></p>

在指定标高的点上放一根结构柱，柱顶给标高或给高度（mm）

!!! warning "动作工具默认允许，只读需显式开启"
    动作默认允许；机器策略 `ReadOnly`、工作站 `read-only` 文件或 `REVIT_MCP_READ_ONLY=1` 三者任一打开即拒绝动作（全新安装的机器策略默认只读）。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    顶底标高与偏移由工具自己写（set_parameter 拒绝 ElementId 参数）；不做附着，柱顶只能给标高或高度

## 可复制提示词 {#prompts}

```text
在 1F 的 (3000,4500) 放一根 600x600 的混凝土柱，柱顶到 3F
```

```text
在 1F 原点放一根柱，高 4200
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `family` | 是 | — | `string` | 柱族名，必须已在项目里（先用 revit_load_family_file 载入） |
| `level` | 是 | — | `string` | 底部标高名 |
| `x_mm` | 是 | — | `number` | 放置点 X 坐标（mm，模型坐标） |
| `y_mm` | 是 | — | `number` | 放置点 Y 坐标（mm，模型坐标） |
| `base_offset_mm` | 否 | `0` | `number` | 底部偏移（mm），默认 0 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `height_mm` | 否 | `null` | `number / null` | 未给 top_level 时的柱高（mm，相对底部偏移），缺省 3000 |
| `rotation_deg` | 否 | `0` | `number` | 绕竖轴旋转角度（度），默认 0 |
| `top_level` | 否 | `null` | `string / null` | 顶部标高名；给出时忽略 height_mm |
| `top_offset_mm` | 否 | `0` | `number` | 顶部偏移（mm，相对顶部标高），默认 0 |
| `type_name` | 否 | `null` | `string / null` | 族类型名；留空用族的第一个类型 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

在 `level` 上的点 `x_mm`、`y_mm` 处放一根 `family`（可指定 `type_name`）的结构柱。
柱顶有两种给法：给 `top_level` 时柱顶落在那个标高上；不给 `top_level` 时用 `height_mm` 从底部偏移往上量（两者都不给按 3000 mm）。顶底标高、底部偏移与顶部偏移都由工具自己写入，因为这些是 ElementId 类型的参数，通用的 revit_set_parameter 出于安全考虑拒绝设置它们。
不做附着：柱顶不是「附着到某个构件」，而是一个标高或一段高度。柱族必须已经在项目里，`type_name` 不存在时会列出该族现有的类型。
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
