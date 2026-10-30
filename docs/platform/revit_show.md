# 显示构件

`revit_show`

<p class="facts"><span><b>分组</b> 视图、图纸与明细表</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

在 Revit 中显示构件并可同时选中，必要时打开标高平面或三维视图。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `element_ids` | 是 | — | array | 要处理的构件 Revit ID 列表。 |
| `select` | 否 | True | boolean |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Display elements in Revit, optionally selecting them; opens a level plan or 3D view when needed.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
