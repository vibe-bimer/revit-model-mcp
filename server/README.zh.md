<a id="revit-model-mcp-server"></a>

# Revit Model MCP 服务器

Python 包通过 MCP stdio 提供 Revit 工具，默认只读。
可选动作要求启用 `REVIT_MCP_ALLOW_WRITE=1`，并存在工作站 `allow-write` 门禁。
它需要 Python 3.11 或更新版本，以及已在 Windows 上的 Revit 中加载的匹配插件。

<a id="install-and-run"></a>

## 安装与运行

首次发布到 PyPI 后，可以使用 uv 运行已发布的包：

```sh
uvx revit-model-mcp
```

向 Claude Code 注册 Windows 本地服务器：

```sh
claude mcp add revit-model-mcp -e REVIT_MCP_HOST=local -- uvx revit-model-mcp
```

对于 macOS 或 Linux 上的客户端：

```sh
claude mcp add revit-model-mcp -e REVIT_MCP_HOST=ssh:revit-host -e REVIT_MCP_REDACT_PATHS=1 -- uvx revit-model-mcp
```

将 `revit-host` 替换为客户端 SSH 配置中的别名。
Windows SSH 会话必须使用与 Revit 相同的账户，或使用显式共享的通道目录。

Windows 上的 Claude Desktop 在 `claude_desktop_config.json` 中使用以下配置项：

```json
{
  "mcpServers": {
    "revit-model-mcp": {
      "command": "uvx",
      "args": ["revit-model-mcp"],
      "env": {
        "REVIT_MCP_HOST": "local",
        "REVIT_MCP_REDACT_PATHS": "1"
      }
    }
  }
}
```

`uvx` 必须位于客户端 PATH 中；也支持使用可执行文件的绝对路径。
远程 Desktop 客户端使用 `REVIT_MCP_HOST=ssh:revit-host`。

开发时，或首次发布到 PyPI 之前，从仓库根目录运行：

```sh
uv run --directory server revit-model-mcp
claude mcp add revit-model-mcp -e REVIT_MCP_HOST=local -- uv run --directory /absolute/path/to/revit-model-mcp/server revit-model-mcp
```

mcp-name: io.github.sharafutdinovdi/revit-model-mcp

<a id="configuration"></a>

## 配置

| 变量 | 默认值 | 行为 |
|---|---|---|
| `REVIT_MCP_HOST` | `local` | 本地 PowerShell、`ssh:<alias>`，或 `http://` / `https://` 插件端点。`--host` 会覆盖它。 |
| `REVIT_MCP_ALLOW_WRITE` | 未设置 | `1` 会在服务器启动时注册 14 个动作工具，包括 `revit_batch`；还需要工作站门禁。布尔设置也接受 `true/false`、`yes/no` 和 `on/off`，不区分大小写并忽略首尾空白。 |
| `REVIT_MCP_TOKEN` | 未设置 | 来自工作站设置的 HTTP Bearer 令牌。`--token` 会覆盖它。 |
| `REVIT_MCP_SSH_MUX` | 启用 | `0` 禁用 OpenSSH 连接多路复用。local 模式忽略 SSH 设置。 |
| `REVIT_MCP_SSH_OPTIONS` | 未设置 | 额外 SSH 参数，按 shell 引号规则解析，在内置选项之后、主机之前追加。例如：`-o ServerAliveInterval=30 -p 2222`。 |
| `REVIT_MCP_ACTIVATE_TASK` | 未设置 | 可选的已有 Windows 计划任务。触发文件 60 秒仍待处理时运行一次。任务必须激活交互式 Revit 窗口。服务器不会创建任何任务。 |
| `REVIT_MCP_CHANNEL_DIR` | Windows 上的 `%LOCALAPPDATA%\RevitModelMcp` | 绝对 Windows 通道路径。在启动 Revit 前，在 Python 服务器环境和 Revit 环境中设置相同值。SSH 模式下，此路径属于远程主机。 |
| `REVIT_MCP_REDACT_PATHS` | 未设置 | `1` 将响应中的每个 `documentPath` 和嵌套 `path` 值替换为文件名。`--redact-paths` 启用相同行为。 |

SSH 模式每次调用都传入 `ControlMaster=auto`、`ControlPath=<dir>/mux-%C` 和 `ControlPersist=600`。
套接字目录使用非空的 `$XDG_RUNTIME_DIR`，否则使用 `/tmp/revit-model-mcp-<uid>/`。
在 macOS 和 Linux 上，该目录会被创建或限制为 `0700` 权限。
保持其绝对路径简短，以满足 Unix 套接字长度限制；`%C` 对连接身份进行哈希。
主连接在最后一个客户端断开后仍可使用 600 秒。
额外选项遵循 OpenSSH“第一个值生效”的规则。
若要自定义多路复用路径或生命周期，设置 `REVIT_MCP_SSH_MUX=0`，并通过 `REVIT_MCP_SSH_OPTIONS` 提供全部三个 `Control*` 选项。
OpenSSH 不支持多路复用的客户端，例如 Windows 原生 OpenSSH，应使用 `REVIT_MCP_SSH_MUX=0`。

`uv run --directory server revit-model-mcp --help` 会打印环境中的主机模式、Windows 通道目录和路径脱敏开关，不会联系 Revit。

服务器在进程启动时读取激活配置。
配置的任务可能还原 Revit 窗口并将其置于前台。
没有任务时，服务器只轮询等待拾取。

<a id="responses-and-privacy"></a>

## 响应与隐私

模型路径出现在响应实例元数据和实例列表中。
脱敏覆盖成功 MCP 结果中的 `documentPath` 和所有嵌套 `path` 字段，包括 `revit_links_status` 返回的 RVT/CAD/图像链接路径。
它保留导出图像的 `localPath` 值，供客户端打开已下载的文件。
它不会脱敏名称、参数值、插件错误文本或存储在通道中的文件。
Revit 模型数据和错误可能保留原始语言。
Python 工具描述和服务器生成的消息使用英语。

<a id="request-behavior"></a>

## 请求行为

HTTP 配置和远程访问命令见[传输](../docs/transport.md#http-configuration)。
HTTP 提交一次，然后在 `timeout_seconds` 范围内根据任务 ID 轮询；拾取超时仅适用于文件传输。
HTTP 导出直接下载 PNG，无需远程 PowerShell。
每个 HTTP 端点代表一个 Revit 进程。

默认文件拾取超时为 300 秒。
拾取后响应超时为 120 秒。
大多数工具接受 `pickup_timeout_seconds` 和 `timeout_seconds`。
`revit_export_view` 使用默认值。
主机上运行多个 Revit 实例时，应提供 `document`。
使用具有区分度的文档标题或文件名。
匹配不区分大小写，接受子串。
待处理任务在拾取超时后仍留在通道中，并可能稍后执行。
每个通道目录只运行一个 MCP 服务器进程。

文件处理和 SSH 行为见[传输](../docs/transport.md)。

<a id="tests"></a>

## 测试

从仓库根目录执行：

```sh
cd server
uv run --with pytest pytest -q
```

测试使用模拟的主机操作，并在没有 Revit 的情况下测试 MCP stdio。

参见[工具参数](../README.md#tools)、[动作参数](../README.md#actions-opt-in)和[响应契约](../docs/feed-format.md#command-responses)。

<a id="license"></a>

## 许可

[MIT](LICENSE)，版权所有 (c) 2026 Dinar Sharafutdinov。
