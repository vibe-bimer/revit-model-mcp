---
description: "在一个视图中更改类目、工作集与过滤器可见性；`dry_run` 只预览。"
---

# 设置视图可见性

`revit_set_view_visibility`

<p class="facts"><span><b>分组</b> 视图、图纸与明细表</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

在一个视图中更改类目、工作集与过滤器可见性；`dry_run` 只预览。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `category_classes` | 否 | None | any |  |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `filters` | 否 | None | any |  |
| `hide_categories` | 否 | None | any |  |
| `hide_categories_by_type` | 否 | None | any |  |
| `show_categories` | 否 | None | any |  |
| `template_mode` | 否 | None | any |  |
| `view` | 是 | — | string | 视图的准确名称或十进制视图 ID。 |
| `worksets` | 否 | None | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Change category, workset and filter visibility in one view; dry_run previews. Categories accept the Revit UI name, the BuiltInCategory name (OST_StructuralColumns), the English name or an ID.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
