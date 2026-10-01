# Revit Model MCP

<p class="facts"><b>当前版本 0.9.0</b>　支持 Revit <b>2020–2027</b>　真机实测 <b>2020 / 2026</b>　工具 <b>33 个</b>（19 读取 + 14 动作）</p>

让 AI 客户端直接读、查、改 Revit 模型：构件的参数与几何、视图组成、交付前体检、导出清单、编辑模型，以及**整模型换新 ID**。读取默认只读，写入需要双门禁。

## 从哪里开始

<div class="grid cards" markdown>

- **按版本看功能**
    先确认你的 Revit 年份支持什么：[Revit 2020](features/v2020.md) · [Revit 2026](features/v2026.md) · [版本支持矩阵](features/matrix.md)
- **找某个工具**
    33 个工具按 8 组归类，每个工具一页（用途 · 参数 · 可复制提示词 · 年份支持）：[工具手册](features/index.md)
- **想知道能说什么**
    按场景整理的中文提示词，直接复制：[提示词库](features/prompts.md)
- **要接进来用**
    传输方式与门禁：[传输与接入](transport.md) · [工作原理](how-it-works.md)

</div>

## 三步上手

1. 在 Revit 工作站安装插件（MSI），在 AI 客户端注册 MCP 服务器（stdio / SSH / HTTP 任选）
2. 直接提需求，例如 `统计 1F 上各种墙类型各有多少个`
3. 需要改模型时再打开写入门禁：客户端 `REVIT_MCP_ALLOW_WRITE=1` + 工作站 `%LOCALAPPDATA%\RevitModelMcp\allow-write`，并确保只有一个 Revit 实例

## 常用提示词

| 场景 | 提示词 |
| --- | --- |
| 统计 | `统计 1F 上各种墙类型各有多少个` |
| 体检 | `做一次交付前体检：文件大小、各类数量、单位设置、最多的警告` |
| 导出 | `把三维视图里的构件导出成 Excel，按类别、族、类型排序` |
| 改模型 | `把 ID 为 123456 的构件沿 X 移动 500 mm，先彩排` |
| 换新 ID | `把当前三维视图里能选中的构件重建到 E:\out\copy-{n}.rvt，出 10 份，每份 ID 都不要重复` |

!!! tip "语言与主题"
    右上角可切换**深色/浅色**与**中文/English**。英文首页是项目的 README，其余页面为对应英文原文。

## 项目 README 的对应小节（英文原文）

<a id="actions-opt-in"></a>
<a id="tools"></a>
这些锚点对应仓库 README 的小节；完整内容见英文首页（右上角切 **English**）或仓库根目录的 `README.md`。
