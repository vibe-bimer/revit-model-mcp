---
description: "在 Revit 工作站把 DWG 链接或导入平面视图，返回 CAD 图层与范围。"
---

# 链接 CAD

`revit_link_cad`

<p class="facts"><span><b>分组</b> CAD 与 MEP</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 1.0.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

在 Revit 工作站把 DWG 链接或导入平面视图，返回 CAD 图层与范围。

[同名发布版页面](../features/revit_link_cad.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 1.0.0 一致。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `layers` | 否 | `null` | any | （集成分支契约未提供说明） |
| `level` | 否 | `null` | any | （集成分支契约未提供说明） |
| `link` | 否 | `true` | boolean | （集成分支契约未提供说明） |
| `origin` | 否 | `"internal"` | string | （集成分支契约未提供说明） |
| `path` | 是 | — | string | （集成分支契约未提供说明） |
| `units` | 否 | `"auto"` | string | （集成分支契约未提供说明） |
| `view` | 否 | `null` | any | 视图的准确名称或十进制视图 ID。 |

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
Link or import a DWG into a plan view on the Revit workstation. Returns CAD layers and extents in mm.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
