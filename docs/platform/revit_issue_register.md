---
description: "生成本地 xlsx 问题登记表，含构件快照与审阅文档；已有同名输出文件时拒绝执行。"
---

# 生成问题登记表

`revit_issue_register`

<p class="facts"><span><b>分组</b> 导出与登记</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

生成本地 xlsx 问题登记表，含构件快照与审阅文档；已有同名输出文件时拒绝执行。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `issues` | 是 | — | array |  |
| `output_path` | 是 | — | string | New .xlsx issue register path, resolved on the machine running this server; existing files are refused. |
| `pixel_size` | 否 | `900` | integer | PNG size in pixels along the fitted dimension, 32 to 4000 (default 1600); Revit rejects smaller images. |
| `project` | 是 | — | object |  |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Write a new local .xlsx issue register with element snapshots and review documents. Takes 1 to 60 issues; captures at most 25 snapshots (by severity) within a 210-second budget, and failed snapshots become cell notes. Snapshots need local or SSH transport. Existing output files are refused. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
