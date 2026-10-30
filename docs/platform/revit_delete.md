# 删除构件

`revit_delete`

<p class="facts"><span><b>分组</b> 编辑原语</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，但参数不同</span><span><b>本页契约适用于发布版</b> 否</span></p>

删除构件及其 Revit 依赖，计数包含依赖对象；连同依赖超过 500 个构件时需要确认令牌。

[同名发布版页面](../features/revit_delete.md)

## 与发布版的契约差异 {#contract-diff}

下表由注册表 inputSchema 自动比较得出，不是手写清单。

- 仅集成分支有参数 confirm_token

本页契约适用于集成分支，不适用于发布版 0.9.0；照抄分支参数会在发布版上失败。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `confirm_token` | 否 | None | any | 首次调用返回的确认令牌，用于确认破坏性操作。 |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `element_ids` | 是 | — | array | 要处理的构件 Revit ID 列表。 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Delete elements and their Revit dependencies; the count includes dependents. dry_run returns the count. Above 500 elements including dependents a confirm_token from a first call is needed; revit_run_actions refuses such deletions.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
