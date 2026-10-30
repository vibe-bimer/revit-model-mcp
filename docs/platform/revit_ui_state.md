---
description: "读取活动文档、打开的视图、当前选择集与打开的文档列表。"
---

# 界面状态

`revit_ui_state`

<p class="facts"><span><b>分组</b> 连接与实例</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

读取活动文档、打开的视图、当前选择集与打开的文档列表。

## 参数 {#parameters}

此工具没有额外业务参数，使用下列通用参数即可。

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Read the active document, open views, selection and open documents. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
