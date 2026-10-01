# Revit 实例列表

`revit_list_instances`

<p class="facts"><span><b>分组</b> 连接与文档</span><span><b>类型</b> 读取（只读）</span><span><b>起始版本</b> 0.6.0</span></p>

列出在跑的 Revit 实例及其打开的文档

## 可复制提示词 {#prompts}

```text
现在有几个 Revit 实例？各自打开什么模型？
```

## 参数 {#parameters}

此工具没有额外业务参数，使用下列通用参数即可。

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

## 功能说明与返回结果 {#contract}

列出 Revit 进程及其活动文档。

返回一个记录列表，每条记录包含 `documentName`、`documentPath`、`revitVersion`、`pluginVersion`、`processId` 和 `pluginResponding`；没有匹配实例时返回 `[]`。
`pluginVersion` 标识加载项的构建版本，例如 `0.6.0+68febc5d`；由旧版加载项写入的心跳中，此字段为空。
本地和 SSH 模式使用加载项心跳，并在需要时回退到进程检测；回退记录中的文档为空，且 `pluginResponding=false`。
HTTP 模式只报告其连接的进程；传输失败会报错。
在为其他工具选择唯一的文档子串前，先使用本工具。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state ok">已实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
