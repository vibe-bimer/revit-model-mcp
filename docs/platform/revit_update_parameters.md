---
description: "对符合同一查询条件的构件更新同一个参数，组成员跳到 `skipped.inGroup` 而不中断调用。"
---

# 批量更新参数

`revit_update_parameters`

<p class="facts"><span><b>分组</b> 编辑原语</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

对符合同一查询条件的构件更新同一个参数，组成员跳到 `skipped.inGroup` 而不中断调用。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `filters` | 是 | — |  | （集成分支契约未提供说明） |
| `include_type_parameters` | 否 | `false` | boolean | （集成分支契约未提供说明） |
| `max_elements` | 否 | `5000` | integer | （集成分支契约未提供说明） |
| `parameter` | 是 | — | string | （集成分支契约未提供说明） |
| `parameter_id` | 否 | `null` | any | （集成分支契约未提供说明） |
| `value` | 是 | — | any | （集成分支契约未提供说明） |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Update a parameter on elements matching the same filters as revit_query_elements. Group members are reported in skipped.inGroup instead of failing the call; dry_run predicts this.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
