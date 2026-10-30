---
description: "打开本地、UNC 或 RSN 模型；中心模型默认以分离方式打开，云路径不支持。"
---

# 打开文档

`revit_open_document`

<p class="facts"><span><b>分组</b> 文档生命周期</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

打开本地、UNC 或 RSN 模型；中心模型默认以分离方式打开，云路径不支持。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `activate` | 否 | `false` | boolean |  |
| `audit` | 否 | `false` | boolean |  |
| `mode` | 否 | `"detached"` | string |  |
| `path` | 是 | — | string |  |
| `worksets` | 否 | `"all"` | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Open a local, UNC or RSN model. Central models open detached by default. Cloud paths are unsupported. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
