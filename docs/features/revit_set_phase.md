# 设置构件阶段

`revit_set_phase`

<p class="facts"><span><b>分组</b> 阶段</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.3.0</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

赋创建阶段 / 拆除阶段（空串清除，null 不变）

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    阶段顺序检查的 API 只在 2022+ ，2020 走兜底

## 可复制提示词 {#prompts}

```text
把这些构件标成在“现有”阶段拆除
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `created_phase` | 是 | — | `string / null` | 创建阶段名；空串清除、null 不变 |
| `demolished_phase` | 是 | — | `string / null` | 拆除阶段名；空串清除该标记、null 不变 |
| `element_ids` | 是 | — | `array<integer>` | 要改阶段的构件 ID |
| `dry_run` | 否 | `false` | `boolean` | 彩排：执行后回滚，返回同样的校验块，不写模型 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

## 功能说明与返回结果 {#contract}

按准确的阶段名称，指定构件的创建阶段或拆除阶段。

每个阶段参数可以是 `revit_list_catalog(section="phases")` 返回的阶段名称，也可以是用于清除该指定的空字符串，或用于保持不变的 `null`；至少一个参数必须非 `null`。
创建操作的 API 无法新增阶段；请先在 Revit 界面中创建新阶段。
例如，`demolished_phase="现有"` 将构件标记为在该阶段拆除；`demolished_phase=""` 则清除拆除阶段。
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
