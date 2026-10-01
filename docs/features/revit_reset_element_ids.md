# 同文档替换 ID

`revit_reset_element_ids`

<p class="facts"><span><b>分组</b> 批量与 ID</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.8.0</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

同文档内换 ID：只对无宿主、无依赖的独立构件有效

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    先运行 dry_run；有宿主、有依赖、成组或属于 MEP 系统的构件会被拒绝

## 可复制提示词 {#prompts}

```text
给选中的这 27 个独立构件换新 ID
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `element_ids` | 是 | — | `array<integer>` | 要换 ID 的构件；有宿主、有依赖、成组或属于 MEP 系统的会被拒绝 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：替换后回滚，先跑一次看哪些构件不合格 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

## 功能说明与返回结果 {#contract}

用副本替换构件，让 Revit 分配新的构件 ID；API 本身无法指定构件 ID。

返回的数据包含 `count`、`idMapping`（旧 ID 到新 ID 的映射），以及 `ineligible` 中列出的不符合条件构件和各自的原因。
以下情况会拒绝构件：删除它也会删除依赖对象；它依附于宿主（副本不会重新关联宿主）；它属于组；它是 MEP 曲线或 MEP 系统成员（副本不会重新加入网络，且 Revit 会重新修复管线）；或 Revit 报告该构件无法复制。
`dry_run` 会执行操作后回滚，在不改变模型的情况下返回相同的验证数据块；务必先执行试运行，因为这种替换无法撤销。
正式执行时，只要有任何构件不符合条件，就会拒绝整个选择范围，以防依赖构件被意外销毁。
本工具绝不会就地修改构件 ID，也绝不会将旧 ID 写入参数。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
