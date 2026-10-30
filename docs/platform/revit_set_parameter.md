# 设置参数

`revit_set_parameter`

<p class="facts"><span><b>分组</b> 编辑原语</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

写入一个实例或类型参数，可用参数 ID、共享参数 GUID 或本地化名称定位；长度用毫米、面积用平方米。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `element_id` | 是 | — | integer |  |
| `parameter` | 是 | — | string |  |
| `parameter_id` | 否 | None | any |  |
| `value` | 是 | — | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Set one instance or type parameter. parameter_id selects by BuiltInParameter name, shared GUID or ParameterElement ID; otherwise parameter takes a localized UI name, BuiltInParameter name or English alias, and ambiguous matches are refused. Value is a string, integer or number by storage type; lengths in mm, areas in m2. Group members fail with a clear message. dry_run rolls back and returns the verification block.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
