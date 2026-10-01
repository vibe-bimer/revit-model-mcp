# 放置非宿主族

`revit_place_family`

<p class="facts"><span><b>分组</b> 编辑</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.2.0</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

在指定标高放置已载入的非宿主族实例，可绕 Z 旋转

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    2026 未真机验证

## 可复制提示词 {#prompts}

```text
用已载入的非宿主家具族，在 1F 的 (3000, 4000) 放置一个实例，先彩排
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `family` | 是 | — | `string` | 族名称 |
| `level` | 是 | — | `string` | 标高名称（用 revit_list_catalog 查到的本地化名称） |
| `type_name` | 是 | — | `string / null` | 类型名称（与族一起定位） |
| `x_mm` | 是 | — | `number` | 模型 X 坐标（mm） |
| `y_mm` | 是 | — | `number` | 模型 Y 坐标（mm） |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |
| `rotation_deg` | 否 | `0` | `number` | 绕 Z 轴旋转角度（°） |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

## 功能说明与返回结果 {#contract}

在指定标高上放置已加载、无需宿主的族，用于布局。

`family` 接受族名称或 `Family: Type` 格式，不区分大小写。
`type_name` 为 `null` 时，使用 `family` 中指定的类型，或第一个类型。类型指定冲突时会拒绝操作。
族不存在时，返回名称相近的族及其类别。
模型 XY 坐标单位为毫米，绕 Z 轴的旋转角单位为度。
在房间内放置对象时使用 `roomCenterMm`。

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
