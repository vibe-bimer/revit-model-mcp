---
description: "在指定标高上放置已载入的非宿主族；`family` 可以是名称或 `Family: Type`。"
---

# 放置族

`revit_place_family`

<p class="facts"><span><b>分组</b> 族</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

在指定标高上放置已载入的非宿主族；`family` 可以是名称或 `Family: Type`。

[同名发布版页面](../features/revit_place_family.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 0.9.0 一致。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `family` | 是 | — | string |  |
| `level` | 是 | — | string |  |
| `rotation_deg` | 否 | `0` | number |  |
| `type_name` | 是 | — | any |  |
| `x_mm` | 是 | — | number |  |
| `y_mm` | 是 | — | number |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Place a loaded unhosted family on a named level. family is a name or Family: Type; a null type_name uses the embedded or first type. XY is in mm, rotation in degrees.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
