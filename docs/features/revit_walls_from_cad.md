---
description: "按 CAD 线段配对成墙并连接开口，尺寸单位为毫米"
---

# 从 CAD 生成墙体

`revit_walls_from_cad`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

按 CAD 线段配对成墙并连接开口，尺寸单位为毫米

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_walls_from_cad.md)

## 可复制提示词 {#prompts}

```text
用底图 'Level 1' 的 CAD 线生成基本墙体，高 3000 毫米并连接两端。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `cad_id` | 是 | — | `integer` | 导入 CAD 实例的构件 ID |
| `layers` | 是 | — | `array<string>` | 用于建墙的 CAD 图层名称列表 |
| `level` | 是 | — | `string` | 标高名称（用 revit_list_catalog 查到的本地化名称） |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `height_mm` | 否 | `3000` | `number` | 生成墙体的默认高度（单位 mm） |
| `join` | 否 | `true` | `boolean` | 是否在端点处连接生成的墙体 |
| `max_gap_mm` | 否 | `3000` | `number` | CAD 线之间可跨越的最大间隙（单位 mm） |
| `max_thickness_mm` | 否 | `700` | `number` | 识别墙体的最大厚度（单位 mm） |
| `min_length_mm` | 否 | `300` | `number` | 可成墙的最短 CAD 线段长度（单位 mm） |
| `min_thickness_mm` | 否 | `80` | `number` | 生成墙体的最小厚度（单位 mm） |
| `wall_type` | 否 | `null` | `string / null` | 基本墙类型名称；必传参数，可传 null 使用第一个基本墙类型 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `timeout_seconds` | 否 | `600` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

桥接洞口、配对平行的 CAD 线并连接基本墙，合并为一个撤销条目。尺寸单位为 mm。

Revit 拒绝的连接会被略过，并在 `unjoinedEnds` 中连同 `unjoinedReasons` 一起报告；`dry_run` 报告相同的连接数。

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
