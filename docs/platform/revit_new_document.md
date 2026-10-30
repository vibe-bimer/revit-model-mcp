# 新建文档

`revit_new_document`

<p class="facts"><span><b>分组</b> 文档生命周期</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

在 Revit 工作站上用样板创建项目或族文件。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `activate` | 否 | True | boolean |  |
| `kind` | 否 | project | string |  |
| `name` | 否 | None | any |  |
| `save_as` | 否 | None | any |  |
| `template` | 否 | None | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `process_id` | 否 | None | any | 目标 Revit 进程号。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Create a project or family from a template on the Revit workstation.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
