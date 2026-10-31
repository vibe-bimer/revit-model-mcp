---
description: "按 mm 点串生成风管、水管、桥架或线管，并连成一段"
---

# 生成管线

`revit_create_mep_run`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

按 mm 点串生成风管、水管、桥架或线管，并连成一段

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_create_mep_run.md)

## 可复制提示词 {#prompts}

```text
在 3F 上从这几个点拉一条 DN100 的水管
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `kind` | 是 | — | `string` | 管线类型：`duct` 或 `pipe` 或 `cable_tray` 或 `conduit` |
| `level` | 是 | — | `string` | 标高名称（用 revit_list_catalog 查到的本地化名称） |
| `points_mm` | 是 | — | `array<array<number>>` | 至少 3 个模型 XY 顶点，每个顶点为 [x,y]（mm）；自动闭合轮廓 |
| `connect_to` | 否 | `null` | `integer / null` | 新建管段要连接的构件 ID |
| `diameter_mm` | 否 | `null` | `number / null` | 管道直径（单位 mm） |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `height_mm` | 否 | `null` | `number / null` | 风管或桥架的截面高度（单位 mm） |
| `offset_mm` | 否 | `null` | `number / null` | 管段相对标高的偏移（单位 mm） |
| `system_type` | 否 | `null` | `string / null` | 管道所属的系统类型 |
| `type_name` | 否 | `null` | `string / null` | 类型名称（与族一起定位） |
| `width_mm` | 否 | `null` | `number / null` | 风管或桥架的截面宽度（单位 mm） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

根据模型中的 mm 点创建相连的风管、管道、电缆桥架或电线管段。

缺少 Z 值时，使用该标高加上该构件种类的默认偏移量。

无法放置的弯头以未连接配对的形式报告。

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
