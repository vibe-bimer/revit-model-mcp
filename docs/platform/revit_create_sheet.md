# 创建图纸

`revit_create_sheet`

<p class="facts"><span><b>分组</b> 视图、图纸与明细表</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

用第一个已载入的标题栏或指定标题栏创建图纸。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `name` | 是 | — | string |  |
| `number` | 是 | — | string |  |
| `title_block` | 否 | None | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Create a sheet with the first loaded or a named title block.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
