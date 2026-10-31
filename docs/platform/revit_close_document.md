---
description: "关闭后台文档；需要先调用一次取得确认令牌，首次调用不改变任何内容。"
---

# 关闭文档

`revit_close_document`

<p class="facts"><span><b>分组</b> 文档生命周期</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 1.0.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

关闭后台文档；需要先调用一次取得确认令牌，首次调用不改变任何内容。

[同名发布版页面](../features/revit_close_document.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 1.0.0 一致。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `confirm_token` | 否 | `null` | any | 首次调用返回的确认令牌，用于确认破坏性操作。 |
| `save` | 否 | `false` | boolean | （集成分支契约未提供说明） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 是 | — | string | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Close a background document. Needs confirm_token from a first call, which changes nothing.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
