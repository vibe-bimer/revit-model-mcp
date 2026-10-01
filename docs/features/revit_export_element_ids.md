# 导出构件 ID 清单

`revit_export_element_ids`

<p class="facts"><span><b>分组</b> 导出与检验</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.8.0</span></p>

把模型中已绘制构件的 ID 清单写成 Excel（类别/族/类型/标高/构件ID/名称/工作集）

!!! note "使用提示"
    文件写到 Revit 工作站上

## 可复制提示词 {#prompts}

```text
把模型中已绘制构件的 ID 清单导出成 Excel，按类别、族、类型排序
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `fields` | 否 | `null` | `array<string> / null` | 要写进表格的列；缺省为 类别/族/类型/标高/构件ID/名称/工作集 |
| `save_to` | 否 | `null` | `string / null` | 工作站上的 xlsx 绝对路径；文件已存在会报错 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `pickup_timeout_seconds` | 否 | `300` | `integer` | local / SSH 等待插件拾取任务的预算（正整数秒，默认 300）；HTTP 忽略。拾取超时后待处理任务仍可能执行 |
| `timeout_seconds` | 否 | `120` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

将已绘制构件的标识清单写入 Revit 工作站上的 xlsx 文件。

返回的数据包含 `path`、`fileName`、`sheetName`、`columns`、`rowCount`、`totalCandidates`、`truncated`、`sizeBytes` 和 `categoryCounts`。
数据行先按类别、再按族、最后按类型排序；默认列为“类别、族、类型、标高、构件ID、名称、工作集”，`fields` 可将这些列替换为内置字段或参数名称。
“构件ID”列记录 Revit 构件 ID，API 无法为构件指定这个 ID；本工具只列出标识，绝不会修改它们。
没有所属标高的构件，其标高列保持为空；大多数 MEP 管道和风管管段属于这种情况。
默认 `null` 会在工作站上写入 `Documents\RevitModelMcp\Exports\构件ID清单_<model>_<timestamp>.xlsx`；如果 `save_to` 指定的文件已存在则报错；超过 50,000 行时设置 `truncated=true`。
导出仅在模型外写入一个文件，绝不会写入模型；文档不存在、读取失败或超时都会报错。

如果有多个 Revit 实例正在运行，必须提供 `document`；否则任意实例都可能响应。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
