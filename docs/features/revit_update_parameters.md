---
description: "按与 revit_query_elements 相同的筛选条件更新图元参数；成组成员记入 skipped，dry_run 可预测结果"
---

# 更新参数

`revit_update_parameters`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 1.0.0</span><span><b>版本</b> 未发布（1.0.0）</span><span><b>集成分支有同名工具</b> 有</span><span><b>本页契约适用于发布版</b> 是</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

按与 revit_query_elements 相同的筛选条件更新图元参数；成组成员记入 skipped，dry_run 可预测结果

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

[同名集成分支页面](../platform/revit_update_parameters.md)

## 可复制提示词 {#prompts}

```text
把一层所有墙的 Comments 参数改成“待检查”，先 dry_run 预览影响范围。
```

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `filters` | 是 | — | `any` | 与 `revit_query_elements` 相同的构件筛选条件 |
| `parameter` | 是 | — | `string` | 参数名（本地化名称） |
| `value` | 是 | — | `string / integer / number` | 要写入的值（长度 mm、面积 m²，其余按内部单位） |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `include_type_parameters` | 否 | `false` | `boolean` | 是否同时更新类型参数 |
| `max_elements` | 否 | `5000` | `integer` | 最多更新的构件数量 |
| `parameter_id` | 否 | `null` | `string / null` | 要更新的参数 ID |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

</div>

## 功能说明与返回结果 {#contract}

更新与 `revit_query_elements` 相同筛选条件匹配的构件上的一个参数。

组成员在 `skipped.inGroup` 中报告，而不是让整个调用失败；`dry_run` 会预先给出这一结果。

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
