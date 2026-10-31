---
description: "沿过 point_mm 的 X 或 Y 平行线镜像；dry_run 回滚，copy 保留原图元"
---

# 镜像图元

`revit_mirror`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

沿过 point_mm 的 X 或 Y 平行线镜像；dry_run 回滚，copy 保留原图元

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_mirror.md)

## 可复制提示词 {#prompts}

```text
把选中的三面外墙沿过 (0, 0) 的 Y 轴平行线镜像，并保留原件
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `axis` | 是 | — | `string` | 镜像所沿的模型轴向：`x` 或 `y` |
| `element_ids` | 是 | — | `array<integer>` | 构件 ID 列表（无单位的 Revit ID） |
| `point_mm` | 是 | — | `array<number>` | 镜像参考点坐标列表（单位 mm） |
| `copy` | 否 | `true` | `boolean` | 是否保留原构件 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

沿穿过 `point_mm` 的模型 X 或 Y 方向平行线做镜像；`copy` 保留原构件。

`dry_run` 会回滚。

组成员、已固定、基于宿主和受约束的构件分别记录在 `skipped.inGroup`、`skipped.pinned`、`skipped.hosted` 和 `skipped.constrained` 中，并且不会被修改；如果所有构件都是组成员，调用会被拒绝。

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
