---
description: "把主体的轴网与标高和一个已载入的 Revit 链接比较，不改动模型。"
---

# 比较链接基准

`revit_compare_link_datums`

<p class="facts"><span><b>分组</b> 链接与基准</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 1.0.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

把主体的轴网与标高和一个已载入的 Revit 链接比较，不改动模型。

[同名发布版页面](../features/revit_compare_link_datums.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 1.0.0 一致。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} |
| --- | :--: | --- | --- |
| `kinds` | 否 | `null` | any |
| `level_offset_mm` | 否 | `0` | number |
| `link` | 是 | — | string |
| `name_map` | 否 | `null` | any |
| `prefix` | 否 | `""` | string |
| `reuse_matching` | 否 | `true` | boolean |
| `suffix` | 否 | `""` | string |
| `tolerance_mm` | 否 | `0.5` | number |

</div>

集成分支契约未提供参数说明。

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | `120` | integer | 本次调用的等待上限（秒）。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Compare host grids and levels with one loaded Revit link. Changes nothing. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
