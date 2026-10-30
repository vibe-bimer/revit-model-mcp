# 连接检查

`revit_ping`

<p class="facts"><span><b>分组</b> 连接与实例</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

不读模型，仅检查与 Revit 的连接；没有活动文档时也返回 `data="pong"`。

## 参数 {#parameters}

此工具没有额外业务参数，使用下列通用参数即可。

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |
| `timeout_seconds` | 否 | 120 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Check the connection to Revit without reading the model. Returns data="pong", even when no document is active. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
