# 实例列表

`revit_list_instances`

<p class="facts"><span><b>分组</b> 连接与实例</span><span><b>类型</b> 读取</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 有</span></p>

列出 Revit 进程及其文档名、路径、版本、进程号与插件响应状态；忙碌进程仍会列出。

## 参数 {#parameters}

此工具没有额外业务参数，使用下列通用参数即可。

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
List Revit processes with documentName, documentPath, revitVersion, processId and pluginResponding. Busy or unresponsive processes stay listed with pluginResponding=false. HTTP mode reports only its connected process.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
