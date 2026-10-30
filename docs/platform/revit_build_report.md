---
description: "不连接 Revit，直接从快照生成本地 Excel 报告。"
---

# 生成快照报告

`revit_build_report`

<p class="facts"><span><b>分组</b> 批处理与报告</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

不连接 Revit，直接从快照生成本地 Excel 报告。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `findings` | 否 | `null` | any | Optional findings with model, severity, rule, element_ids (or elementIds), and recommendation. |
| `output_path` | 是 | — | string | New .xlsx file path, resolved on the machine running this server; existing files are never replaced. |
| `previous_dir` | 否 | `null` | any | Optional directory of earlier snapshots matched by model title for the Changes sheet. |
| `snapshots_dir` | 是 | — | string | Directory of schema-version-1 JSON snapshots on the MCP client machine. |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Build a local Excel report from snapshots without contacting Revit.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
