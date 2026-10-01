# Revit Model MCP 服务器

把 Revit 模型的数据通过 Model Context Protocol 提供给 AI 客户端：读取默认只读，写入需要两道门禁。

!!! note "中文版"
    本页是中文说明；英文原文见本页的 English 版本（右上角切换）。

<a id="installation"></a>
## 安装

服务器是个普通 Python 包，装在**客户端**所在的机器上（不是 Revit 工作站）：

```sh
uv tool install revit-model-mcp      # 或：pipx install revit-model-mcp
revit-model-mcp --help
```

Revit 侧安装插件 MSI（`RevitModelMcp-<版本>-SingleUser.msi`），安装后启动 Revit 即加载。

<a id="quick-start"></a>
## 快速接入（stdio）

在客户端（例如 Claude Desktop、Cline 等）注册：

```json
{
  "mcpServers": {
    "revit-model-mcp": {
      "command": "revit-model-mcp",
      "env": { "REVIT_MCP_HOST": "http://127.0.0.1:53110", "REVIT_MCP_TOKEN": "<工作站 settings.json 里的 token>" }
    }
  }
}
```

跨机器时推荐 SSH 通道（服务器跑在客户端侧，通过 SSH 把请求送到工作站的插件通道），需要长任务或批量时用 HTTP 通道并直接给 `REVIT_MCP_HOST`。详见 [传输与接入](../docs/transport.md)。

<a id="actions-opt-in"></a>
## 打开写入（可选）

动作类工具需要**同时**满足两个条件：

1. 客户端环境变量 `REVIT_MCP_ALLOW_WRITE=1`
2. 工作站上存在 `%LOCALAPPDATA%\RevitModelMcp\allow-write` 文件

并且要求**恰好一个** Revit 实例在运行，避免请求落到错误的模型上。不打开时，只有 19 个读取工具可用。

## 工具

共 33 个：19 个读取（查询、统计、视图、导出、体检）+ 14 个动作（选中显示、编辑、阶段、批量、ID 重建）。完整清单见 [功能总览](../docs/features/index.md)，逐个工具的说明与提示词见 [工具手册](../docs/features/index.md)。

## 环境变量

| 变量 | 作用 |
| --- | --- |
| `REVIT_MCP_HOST` | 插件 HTTP 通道地址（默认 `http://127.0.0.1:53110`） |
| `REVIT_MCP_TOKEN` | HTTP 通道的 Bearer token |
| `REVIT_MCP_ALLOW_WRITE` | `1` 时向客户端暴露动作工具 |
| `REVIT_MCP_REDACT_PATHS` | `0` 时返回完整模型路径（默认脱敏） |
| `REVIT_MCP_HTTP_PORT` / `_BIND` / `_ENABLED` | 插件侧 HTTP 通道参数 |
| `REVIT_MCP_CHANNEL_DIR` | 文件通道目录（默认 `%LOCALAPPDATA%\RevitModelMcp`） |
| `REVIT_MCP_ANSWER_DIALOGS` | `1` 时自动应答所有 Revit 弹窗（无人值守实例用） |
