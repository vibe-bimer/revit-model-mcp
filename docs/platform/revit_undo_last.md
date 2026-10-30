---
description: "通过 Revit 自身的撤销命令撤销上一次 MCP 动作；条件不满足时结果带拒绝原因。"
---

# 撤销上一个动作

`revit_undo_last`

<p class="facts"><span><b>分组</b> 连接与实例</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

通过 Revit 自身的撤销命令撤销上一次 MCP 动作；条件不满足时结果带拒绝原因。

## 参数 {#parameters}

此工具没有额外业务参数，使用下列通用参数即可。

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Undo the last MCP action through Revit's own undo command. Runs only when the target document is active, no command is pending and Revit's last undo entry is the one this session recorded; otherwise the result carries a refusal reason.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
