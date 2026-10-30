---
description: "渲染带高亮的 PNG，标记 1 到 500 个构件作为问题证据，临时视图在结束后回滚。"
---

# 截取构件画面

`revit_capture_elements`

<p class="facts"><span><b>分组</b> 视图、图纸与明细表</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

渲染带高亮的 PNG，标记 1 到 500 个构件作为问题证据，临时视图在结束后回滚。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `element_ids` | 是 | — | array | 要处理的构件 Revit ID 列表。 |
| `mode` | 否 | `"3d"` | string |  |
| `output_path` | 否 | `null` | any | New PNG path, resolved on the machine running this server; an existing file is an error. Default null downloads to a temporary directory and returns localPath. |
| `padding_mm` | 否 | `1500` | number |  |
| `pixel_size` | 否 | `1600` | integer | PNG size in pixels along the fitted dimension, 32 to 4000 (default 1600); Revit rejects smaller images. |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Render a highlighted PNG that marks 1 to 500 elements, for issue evidence. Supports 3d or plan mode over local or SSH transport. The temporary view is rolled back. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
