# 传输与接入

!!! note "中文版"
    本页为中文精简版；把右上角语言切到 English 可看完整英文原文。

三种传输方式，按场景选一种即可。

| 方式 | 适用场景 | 关键点 |
| --- | --- | --- |
| **stdio**（默认） | MCP 服务器与客户端在同一台机器 | 客户端直接拉起 `revit-model-mcp` 进程，最简单 |
| **SSH** | 客户端在 Linux/macOS，Revit 在 Windows 工作站 | 服务器跑在客户端侧，通过 SSH 把请求送到工作站的插件通道 |
| **HTTP** | 需要长任务、批量、或多客户端 | 插件在 `127.0.0.1:53110` 监听，Bearer token 鉴权；可直连或用 SSH 端口转发 |

## HTTP 通道要点

- 地址：`http://127.0.0.1:53110`（只监听回环，不对外暴露）；鉴权：`Authorization: Bearer <token>`
- 端口与令牌来自工作站 `%LOCALAPPDATA%\RevitModelMcp\settings.json`，可用环境变量覆盖：
  `REVIT_MCP_HTTP_PORT`、`REVIT_MCP_HTTP_BIND`、`REVIT_MCP_HTTP_ENABLED`、`REVIT_MCP_TOKEN`、`REVIT_MCP_CHANNEL_DIR`
- 常用端点：`POST /jobs`（提交）、`GET /jobs/{id}`（取结果）、`GET /health`（版本与当前文档）
- **长任务**：通道约 120 s 后不再等待，改回 `{jobId}`；此后用 `GET /jobs/{id}` 轮询。任务结果约 10 分钟后过期，请及时取。
- 忙时会返回 **409**（同时只有一个任务），重试即可。
- 无人值守实例（例如并行跑副本的农场实例）可设 `REVIT_MCP_ANSWER_DIALOGS=1`，让它自动应答所有弹窗；交互使用的实例不要开。

## 客户端配置

MCP 服务器通过环境变量选择通道：`REVIT_MCP_HOST`、`REVIT_MCP_TOKEN`（HTTP 模式）、以及写入门禁 `REVIT_MCP_ALLOW_WRITE=1`。模型路径默认做脱敏，需要完整路径时设 `REVIT_MCP_REDACT_PATHS=0`。

## HTTP 配置 <a id="http-configuration"></a>

本节是英文页对应小节的锚点，便于英文页面内的交叉链接在中文界面同样可用。
