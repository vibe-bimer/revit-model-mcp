# 导出视图为 PNG

`revit_export_view`

<p class="facts"><span><b>分组</b> 视图、图纸与明细表</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

把选定视图导出为 MCP 客户端上的 PNG 文件，不改变活动视图与模型。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `output_path` | 否 | None | any | New PNG path, resolved on the machine running this server; an existing file is an error. Default null downloads to a temporary directory and returns localPath. |
| `pixel_size` | 否 | 1600 | integer | PNG size in pixels along the fitted dimension, 32 to 4000 (default 1600); Revit rejects smaller images. |
| `view` | 是 | — | string | 视图的准确名称或十进制视图 ID。 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Export a selected view to a PNG file on the MCP client. Does not change the active view or the model. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
