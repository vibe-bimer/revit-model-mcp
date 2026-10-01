# 构件参数与几何

`revit_element_details`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.1.0</span></p>

单个构件的实例参数、类型参数与几何（mm）

!!! note "使用提示"
    房间还会返回面积、体积与边界

## 可复制提示词 {#prompts}

```text
把 ID 357640 的构件参数和几何都读出来
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `element_id` | 是 | — | `integer` | 单个构件的 Revit ID |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `pickup_timeout_seconds` | 否 | `300` | `integer` | local / SSH 等待插件拾取任务的预算（正整数秒，默认 300）；HTTP 忽略。拾取超时后待处理任务仍可能执行 |
| `timeout_seconds` | 否 | `120` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

按 Revit ID 读取构件的参数和几何数据。

返回的数据包含 `element`、实例参数、可获取的 `typeElement` 参数，以及相关警告；没有警告时返回空列表。
房间数据包含标高、面积（m2）、体积（m3）和边界（mm）；参数值包含显示值／内部值，以及可获取时的公制单位。
`location` 和 `boundingBox` 使用模型坐标系中的 mm，四舍五入到小数点后 1 位；无法获取的几何数据会省略。
在房间内放置对象时使用 `roomCenterMm`；`boundingBox.centerMm` 可能位于非矩形房间外。
构件或文档不存在、读取失败或超时都会报错；不返回部分数据。

如果有多个 Revit 实例正在运行，必须提供 `document`；否则任意实例都可能响应。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state ok">已实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
