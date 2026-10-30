# 高亮构件

`revit_override_graphics`

<p class="facts"><span><b>分组</b> 视图、图纸与明细表</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

在选定模型视图中给构件上色；`reset` 恢复本 Revit 会话中保存的替代。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `color` | 否 | #FF0000 | string |  |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `element_ids` | 是 | — | array | 要处理的构件 Revit ID 列表。 |
| `fill` | 否 | True | boolean |  |
| `halftone_others` | 否 | False | boolean |  |
| `line_weight` | 否 | None | any |  |
| `reset` | 否 | False | boolean |  |
| `transparency` | 否 | 0 | integer |  |
| `views` | 否 | active | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Colour elements in selected model views; reset restores overrides saved in this Revit session.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
