---
description: "把工作共享文档与中心文件同步；需要先取得确认令牌。"
---

# 同步文档

`revit_sync_document`

<p class="facts"><span><b>分组</b> 文档生命周期</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

把工作共享文档与中心文件同步；需要先取得确认令牌。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `comment` | 是 | — | string |  |
| `compact` | 否 | `false` | boolean |  |
| `confirm_token` | 否 | `null` | any | 首次调用返回的确认令牌，用于确认破坏性操作。 |
| `relinquish` | 否 | `"all"` | any |  |
| `save_local_after` | 否 | `true` | boolean |  |
| `save_local_before` | 否 | `true` | boolean |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 是 | — | string | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | `null` | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Synchronize a workshared document with central. Needs confirm_token from a first call, which changes nothing.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
