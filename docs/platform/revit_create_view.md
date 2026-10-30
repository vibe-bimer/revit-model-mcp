---
description: "创建平面、剖面、三维或绘图视图；无边界三维视图显示整个模型。"
---

# 创建视图

`revit_create_view`

<p class="facts"><span><b>分组</b> 视图、图纸与明细表</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

创建平面、剖面、三维或绘图视图；无边界三维视图显示整个模型。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `box` | 否 | `null` | any |  |
| `detail_level` | 否 | `null` | any |  |
| `display_style` | 否 | `null` | any |  |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `element_ids` | 否 | `null` | any | 要处理的构件 Revit ID 列表。 |
| `kind` | 是 | — | string |  |
| `level` | 否 | `null` | any |  |
| `name` | 否 | `null` | any |  |
| `scale` | 否 | `null` | any |  |
| `template` | 否 | `null` | any |  |
| `view_family_type` | 否 | `null` | any |  |

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
Create a plan, section, 3D or drafting view. Unbounded 3D views show the whole model, shaded, fine detail. Box coordinates are model mm.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
