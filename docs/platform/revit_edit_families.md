# 编辑族

`revit_edit_families`

<p class="facts"><span><b>分组</b> 族</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

就地编辑已打开的族，或对指定项目族逐个执行一个加载循环；`dry_run` 回滚全部改动。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `families` | 否 | None | any |  |
| `operations` | 是 | — | array |  |
| `overwrite_parameter_values` | 否 | False | boolean |  |
| `stop_on_error` | 否 | True | boolean |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `timeout_seconds` | 否 | 1800 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Edit an open family in place, or named project families (exact names or ["*"]), one load cycle each. A dry run rolls back all changes. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
