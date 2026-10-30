---
description: "写入一个实例或类型参数，可用参数 ID、共享参数 GUID 或本地化名称定位；长度用毫米、面积用平方米。"
---

# 设置参数

`revit_set_parameter`

<p class="facts"><span><b>分组</b> 编辑原语</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，但参数不同</span><span><b>本页契约适用于发布版</b> 否</span></p>

写入一个实例或类型参数，可用参数 ID、共享参数 GUID 或本地化名称定位；长度用毫米、面积用平方米。

[同名发布版页面](../features/revit_set_parameter.md)

## 与发布版的契约差异 {#contract-diff}

下表由注册表 inputSchema 自动比较得出，不是手写清单。

- 仅集成分支有参数 parameter_id
- 参数 value 类型：发布版 string / 集成分支 integer|number|string

本页契约适用于集成分支，不适用于发布版 0.9.0；照抄分支参数会在发布版上失败。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `element_id` | 是 | — | integer |  |
| `parameter` | 是 | — | string |  |
| `parameter_id` | 否 | `null` | any |  |
| `value` | 是 | — | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Set one instance or type parameter. parameter_id selects by BuiltInParameter name, shared GUID or ParameterElement ID; otherwise parameter takes a localized UI name, BuiltInParameter name or English alias, and ambiguous matches are refused. Value is a string, integer or number by storage type; lengths in mm, areas in m2. Group members fail with a clear message. dry_run rolls back and returns the verification block.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
