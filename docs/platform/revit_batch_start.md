---
description: "对本地、UNC 或 RSN 模型启动持久化的只读批量运行；`open_timeout_minutes` 是单个模型的打开时限。"
---

# 开始批量收集

`revit_batch_start`

<p class="facts"><span><b>分组</b> 批处理与报告</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

对本地、UNC 或 RSN 模型启动持久化的只读批量运行；`open_timeout_minutes` 是单个模型的打开时限。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `folder` | 否 | `null` | any |  |
| `open_timeout_minutes` | 否 | `null` | any |  |
| `parameter_rules` | 否 | `null` | any |  |
| `paths` | 否 | `null` | any |  |
| `recursive` | 否 | `false` | boolean |  |
| `years` | 否 | `null` | any |  |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Start a persistent, read-only run over local, UNC or RSN models. open_timeout_minutes is the per-model open deadline (default 30, 45 when upgrading in memory).
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
