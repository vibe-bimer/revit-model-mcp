# 打开文档

`revit_open_document`

<p class="facts"><span><b>分组</b> 文档生命周期</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

打开本地、UNC 或 RSN 模型；中心模型默认以分离方式打开，云路径不支持。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `activate` | 否 | False | boolean |  |
| `audit` | 否 | False | boolean |  |
| `mode` | 否 | detached | string |  |
| `path` | 是 | — | string |  |
| `worksets` | 否 | all | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Open a local, UNC or RSN model. Central models open detached by default. Cloud paths are unsupported. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
