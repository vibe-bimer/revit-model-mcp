# 取消动作任务

`revit_cancel_job`

<p class="facts"><span><b>分组</b> 连接与实例</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

请求取消某个 `jobId`；批处理在下一个模型前停止，已经完成的改动保留。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `job_id` | 是 | — | string |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Request cancellation of an action jobId. Process-models stops before the next model and marks unstarted models cancelled; a single running Revit operation finishes, and completed changes stay committed.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
