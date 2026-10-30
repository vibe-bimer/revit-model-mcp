# 创建墙

`revit_create_wall`

<p class="facts"><span><b>分组</b> CAD 与 MEP</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

在指定标高上创建直墙，XY 端点与高度用毫米；不给墙类型时取第一个基本类型。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `end_mm` | 是 | — | array |  |
| `height_mm` | 否 | 3000 | number |  |
| `level` | 是 | — | string |  |
| `start_mm` | 是 | — | array |  |
| `wall_type` | 是 | — | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Create a straight wall on a named level. XY endpoints and height are in mm; a null wall_type uses the first basic type.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
