---
description: "在墙上放门窗：宿主可点名也可就近找墙，回报挂在哪面墙上（mm）"
---

# 放置宿主族

`revit_place_hosted_family`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.10.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span><span><b>来源</b> 自研（本仓库）</span></p>

在墙上放门窗：宿主可点名也可就近找墙，回报挂在哪面墙上（mm）

!!! warning "动作工具默认允许，只读需显式开启"
    动作默认允许；机器策略 `ReadOnly`、工作站 `read-only` 文件或 `REVIT_MCP_READ_ONLY=1` 三者任一打开即拒绝动作（全新安装的机器策略默认只读）。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    就近找墙只在放置标高这一层里找；宿主不是墙、定位点超出 host_search_radius_mm 或最近距离并列时被拒绝并列出候选；非单层宿主族用 revit_place_family；rotation_deg 只能是 0，翻面用 flip_facing；不做附着

## 可复制提示词 {#prompts}

```text
在 1F 的 (3000,0) 挂一扇门，就近找墙
```

```text
把这扇窗挂到 105 号墙上，窗台高 900
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `family` | 是 | — | `string` | 门、窗等单层宿主族名，必须已在项目里（先用 revit_load_family_file 载入） |
| `x_mm` | 是 | — | `number` | 放置点 X 坐标（mm，模型坐标） |
| `y_mm` | 是 | — | `number` | 放置点 Y 坐标（mm，模型坐标） |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `flip_facing` | 否 | `null` | `boolean / null` | true 时调用 flipFacing() 翻转朝向；留空不动 |
| `host_element_id` | 否 | `null` | `integer / null` | 宿主墙的构件 ID；留空则按定位点就近找墙 |
| `host_search_radius_mm` | 否 | `2000` | `number` | 就近找墙时定位点到墙定位线的最大水平距离（mm），默认 2000 |
| `level` | 否 | `null` | `string / null` | 放置标高名；留空取高程离定位点最近的标高（定位点按标高 0 计） |
| `rotation_deg` | 否 | `0` | `number` | 只接受 0：宿主族的方向由宿主墙决定，要翻面用 flip_facing |
| `sill_height_mm` | 否 | `null` | `number / null` | 窗台高度（mm），写入族自己的 INSTANCE_SILL_HEIGHT_PARAM |
| `type_name` | 否 | `null` | `string / null` | 族类型名；留空用族的第一个类型 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

把 `family` 的一个门、窗或其他单层宿主族实例放到 `x_mm`、`y_mm` 上。

宿主要么是 `host_element_id` 点名的墙，要么是定位线落在定位点 `host_search_radius_mm` 之内的最近一面墙；找不到宿主、距离超出半径，或两面墙一样近，都会被拒绝并列出候选，让调用方点名一面。
响应在 `fork.hostResolution` 回报 `{mode, hostId, distanceMm}`，所以试运行也能看出这扇门窗会挂在哪面墙上。
`sill_height_mm` 写入族自己的 INSTANCE_SILL_HEIGHT_PARAM，`flip_facing` 调用 flipFacing()。`rotation_deg` 只接受 0：宿主实例的方向由宿主墙决定，要翻面用 `flip_facing`。
不是单层宿主的族会被拒绝：那种族用 revit_place_family 放置，旋转也在那边做。
不做附着，因为门窗没有可附着的目标。
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
