# 批量收集状态

`revit_batch_status`

<p class="facts"><span><b>分组</b> 批处理与报告</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

在发起客户端退出后仍可读取运行与模型状态。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `run_id` | 是 | — | string |  |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Read durable run and model status after the initiating client exits.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
