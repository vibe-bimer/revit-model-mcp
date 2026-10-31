---
description: "载入可选族并在同一事务、同一次撤销内放置多个实例。"
---

# 批量放置族

`revit_place_families`

<p class="facts"><span><b>分组</b> 族</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 1.0.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

载入可选族并在同一事务、同一次撤销内放置多个实例。

[同名发布版页面](../features/revit_place_families.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 1.0.0 一致。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `at_rooms` | 否 | `null` | any | （集成分支契约未提供说明） |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `load` | 否 | `null` | any | （集成分支契约未提供说明） |
| `placements` | 否 | `null` | any | （集成分支契约未提供说明） |
| `stop_on_error` | 否 | `true` | boolean | （集成分支契约未提供说明） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `timeout_seconds` | 否 | `600` | integer | 本次调用的等待上限（秒）。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Load optional families and place instances in one transaction and undo entry.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
