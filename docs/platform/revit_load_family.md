# 载入族

`revit_load_family`

<p class="facts"><span><b>分组</b> 族</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

在一次撤销内载入工作站的 .rfa 文件；已有同名族默认跳过。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `overwrite` | 否 | False | boolean |  |
| `overwrite_parameter_values` | 否 | False | boolean |  |
| `paths` | 是 | — | array |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `timeout_seconds` | 否 | 600 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Load workstation .rfa files in one undo entry. Existing families are skipped unless overwrite is true.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
