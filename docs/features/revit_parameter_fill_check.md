# 参数填充检查

`revit_parameter_fill_check`

<p class="facts"><span><b>分组</b> 导出与检验</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.6.0</span></p>

参数的填充率：有值 / 空 / 缺失，并给出抽样 ID

## 可复制提示词 {#prompts}

```text
检查墙的防火等级填充率，给出空值的构件 ID
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `categories` | 是 | — | `array<string>` | 类别名称列表（取并集） |
| `parameters` | 是 | — | `array<string>` | 要统计的参数名列表 |
| `include_types` | 否 | `true` | `boolean` | 实例上找不到参数时，是否回退到类型参数（默认 true）；不是把类型元素额外计数 |
| `level` | 否 | `null` | `string / null` | 只统计该标高上的构件 |
| `sample_limit` | 否 | `20` | `integer` | 每个参数最多返回多少个抽样 ID |
| `view` | 否 | `null` | `string / null` | 视图名称（或视图 ID） |
| `workset` | 否 | `null` | `string / null` | 只统计该工作集里的构件 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |
| `pickup_timeout_seconds` | 否 | `300` | `integer` | local / SSH 等待插件拾取任务的预算（正整数秒，默认 300）；HTTP 忽略。拾取超时后待处理任务仍可能执行 |
| `timeout_seconds` | 否 | `120` | `integer` | 拾取任务后的结果等待预算（正整数秒，默认 120）；HTTP 使用它作为响应预算，不能覆盖插件内部执行上限。超时不代表待处理动作已取消 |

## 功能说明与返回结果 {#contract}

!!! note "使用提示"
    以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。

在导出或交付前统计参数的已填写、空值和缺失情况。

返回的数据包含检查范围、按参数和类别划分的数量统计、参数属于实例还是类型的信息、存储类型，以及空值／缺失参数的构件 ID 样本。
没有匹配构件时，计数为 0，样本为空；不存在的参数计为缺失，数值 0 计为已填写。
文档不存在、检查范围无效或超时都会报错；不返回部分数据。

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
