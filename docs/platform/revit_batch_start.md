# 开始批量收集

`revit_batch_start`

<p class="facts"><span><b>分组</b> 批处理与报告</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

对本地、UNC 或 RSN 模型启动持久化的只读批量运行；`open_timeout_minutes` 是单个模型的打开时限。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `folder` | 否 | None | any |  |
| `open_timeout_minutes` | 否 | None | any |  |
| `parameter_rules` | 否 | None | any |  |
| `paths` | 否 | None | any |  |
| `recursive` | 否 | False | boolean |  |
| `years` | 否 | None | any |  |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Start a persistent, read-only run over local, UNC or RSN models. open_timeout_minutes is the per-model open deadline (default 30, 45 when upgrading in memory).
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
