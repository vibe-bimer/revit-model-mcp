# 移动构件

`revit_move`

<p class="facts"><span><b>分组</b> 编辑原语</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

按 `dx_mm`、`dy_mm`、`dz_mm` 沿模型轴移动构件；`dry_run` 回滚并返回验证块。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `dx_mm` | 是 | — | number |  |
| `dy_mm` | 是 | — | number |  |
| `dz_mm` | 否 | 0 | number |  |
| `element_ids` | 是 | — | array | 要处理的构件 Revit ID 列表。 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Move elements by dx_mm, dy_mm and dz_mm on model axes. dry_run rolls back and returns the verification block. Group members, pinned, hosted and constrained elements are reported in skipped.inGroup, skipped.pinned, skipped.hosted and skipped.constrained and are not changed; the call is refused if every element is a group member.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
