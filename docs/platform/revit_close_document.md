# 关闭文档

`revit_close_document`

<p class="facts"><span><b>分组</b> 文档生命周期</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

关闭后台文档；需要先调用一次取得确认令牌，首次调用不改变任何内容。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `confirm_token` | 否 | None | any | 首次调用返回的确认令牌，用于确认破坏性操作。 |
| `save` | 否 | False | boolean |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 是 | — | string | 打开多个模型时，用标题或路径指定目标文档。 |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Close a background document. Needs confirm_token from a first call, which changes nothing.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
