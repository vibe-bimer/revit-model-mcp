# Revit Model MCP

<p class="facts"><span><b>插件 / MCP 版本 0.9.0</b></span><span>Revit <b>2020 / 2022–2027</b></span><span>19 个读取 + 16 个动作，共 35 个工具</span></p>

面向 Revit 技术人员的功能手册：查参数与几何、统计构件、检查模型、导出清单、编辑构件，以及复制模型并换新 ID。默认只读，动作需要双门禁。**Revit 年份**与**插件发布版本**是两种不同的版本；实测覆盖以支持矩阵为准。

## 选择查阅入口 {#entry-points}

<div class="grid cards" markdown>

- **确认 Revit 年份支持**

    [Revit 2020](features/v2020.md) · [Revit 2026](features/v2026.md) · [支持矩阵](features/matrix.md)

- **查某个功能和参数**

    [功能总览](features/index.md)：按场景分类，每项都有用途、参数、返回结果与限制。

- **复制提示词使用**

    [提示词库](features/prompts.md)：按功能分组，复制后替换模型、标高、构件 ID 和文件路径。

- **安装并连接 MCP**

    [安装与配置](server.md) · [传输与接入](transport.md) · [动作门禁](actions.md#gates)

</div>

## 三步上手 {#get-started}

1. 在 Windows Revit 工作站安装插件，在 AI 客户端配置 MCP 服务器；具体步骤见[安装与配置](server.md)。
2. 先做只读查询，例如 `统计 1F 上各种墙类型各有多少个`。过滤名称应先从模型目录获取。
3. 需要动作时再打开双门禁。修改前优先使用支持该参数的工具做 `dry_run`；超时后先核对模型，不要盲目重试。

## 常用提示词 {#common-prompts}

| 场景 | 提示词 |
| --- | --- |
| 统计 | `统计 1F 上各种墙类型各有多少个` |
| 检查 | `做一次交付前体检：文件大小、各类数量、单位设置、最多的警告` |
| 导出 | `把模型中已绘制构件的 ID 清单导出成 Excel，按类别、族、类型排序` |
| 移动 | `把 ID 为 123456 的构件沿 X 移动 500 mm，先彩排` |
| 新模型 ID | `把当前三维视图里能选中的构件重建到 E:\out\copy-{n}.rvt，出 10 份，逐份检查构件数量和 ID 映射` |

## 进一步查阅 {#further-reading}

<a id="tools"></a>
<a id="actions-opt-in"></a>

- 功能用法：[功能总览](features/index.md) · [提示词库](features/prompts.md)
- 跨工具契约：[读取契约](tools.md) · [动作契约](actions.md)
- 项目信息：[更新记录](changelog.md) · [隐私说明](privacy.md)

右上角切换中文 / English 和浅色 / 深色；同一页面切换语言后保留对应内容。
