---
description: "把已完成的快照下载为新的本地文件，不覆盖已有文件。"
---

# 取回批量快照

`revit_batch_fetch`

<p class="facts"><span><b>分组</b> 批处理与报告</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 1.0.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

把已完成的快照下载为新的本地文件，不覆盖已有文件。

[同名发布版页面](../features/revit_batch_fetch.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 1.0.0 一致。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} |
| --- | :--: | --- | --- |
| `output_dir` | 是 | — | string |
| `run_id` | 是 | — | string |

</div>

集成分支契约未提供参数说明。

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Download completed snapshots to new local files without overwriting.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
