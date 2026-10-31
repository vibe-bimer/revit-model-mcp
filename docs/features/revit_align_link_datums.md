---
description: "把宿主轴网与标高对齐到已链接模型，dry_run 可预览回滚"
---

# 对齐链接基准

`revit_align_link_datums`

<p class="facts"><span><b>分组</b> 链接与协同</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

把宿主轴网与标高对齐到已链接模型，dry_run 可预览回滚

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_align_link_datums.md)

## 可复制提示词 {#prompts}

```text
把当前模型的轴网和标高对齐到已链接模型 'StructureLink.rvt'，公差 5 毫米。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `link` | 是 | — | `string` | 要对齐的链接名称 |
| `create_missing` | 否 | `true` | `boolean` | 缺失的宿主基准是否自动创建 |
| `create_plan_views` | 否 | `false` | `boolean` | 是否同时创建平面视图 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `grid_type` | 否 | `null` | `string / null` | 对齐所用的轴网类型名称 |
| `include_pinned` | 否 | `false` | `boolean` | 是否包含已固定的链接 |
| `kinds` | 否 | `null` | `array<string> / null` | 要对齐的基准类型列表：`grids` 或 `levels` |
| `level_offset_mm` | 否 | `0` | `number` | 标高对齐的高程偏移量（单位 mm） |
| `level_type` | 否 | `null` | `string / null` | 对齐所用的标高类型名称 |
| `name_map` | 否 | `null` | `object / null` | 链接基准名到宿主基准名的映射表 |
| `plan_view_type` | 否 | `null` | `string / null` | 新建平面视图所用的视图族类型名称 |
| `prefix` | 否 | `""` | `string` | 匹配到的轴网与标高名称所加前缀 |
| `reuse_matching` | 否 | `true` | `boolean` | 是否复用已有的基准点匹配 |
| `suffix` | 否 | `""` | `string` | 新建宿主基准名称添加的后缀 |
| `tolerance_mm` | 否 | `0.5` | `number` | 轴网与标高对齐的容差（单位 mm） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `timeout_seconds` | 否 | `600` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

</div>

## 功能说明与返回结果 {#contract}

将主体的轴网和标高对齐到已载入的链接，可以选择创建缺失的轴网和标高，并提供回滚预览。

本工具不建立监视关系。

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
