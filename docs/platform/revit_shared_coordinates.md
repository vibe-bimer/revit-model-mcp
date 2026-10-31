---
description: "读取项目与测量坐标：基点、测量点、活动场地、项目位置与链接偏移，单位毫米与度。"
---

# 共享坐标

`revit_shared_coordinates`

<p class="facts"><span><b>分组</b> 查询与统计</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 1.0.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

读取项目与测量坐标：基点、测量点、活动场地、项目位置与链接偏移，单位毫米与度。

[同名发布版页面](../features/revit_shared_coordinates.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 1.0.0 一致。

## 参数 {#parameters}

此工具没有额外业务参数，使用下列通用参数即可。

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
Read project and survey coordinates: base and survey points, active site, project locations and link offsets (mm, degrees). Lists are capped at 100 with total counts. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
