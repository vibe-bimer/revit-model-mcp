# 创建楼板

`revit_create_floor`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.2.0</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

按闭合轮廓建楼板（至少 3 个顶点，mm）

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    2020 走 Document.Create.NewFloor，2022+ 走 Floor.Create

## 可复制提示词 {#prompts}

```text
用这四个点在 2F 建一块楼板
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `floor_type` | 是 | — | `string / null` | 楼板类型名称；必传参数，可传 null 使用第一个楼板类型 |
| `level` | 是 | — | `string` | 标高名称（用 revit_list_catalog 查到的本地化名称） |
| `points_mm` | 是 | — | `array<array<number>>` | 至少 3 个模型 XY 顶点，每个顶点为 [x,y]（mm）；自动闭合轮廓 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

## 功能说明与返回结果 {#contract}

根据闭合边界，在指定标高上创建楼板，用于布局。
`points_mm` 是模型 XY 坐标系中的多边形顶点，单位为毫米（至少 3 个顶点；边界会自动闭合）；`floor_type` 为 `null` 时选择第一个楼板类型。
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
