# 安全政策

<a id="reporting"></a>
## 报告漏洞

本仓库已启用私密漏洞报告。
请通过 [GitHub 私密报告表单](https://github.com/sharafutdinovdi/revit-model-mcp/security/advisories/new)，或发送邮件到 [sharafutdinov.di.dev@outlook.com](mailto:sharafutdinov.di.dev@outlook.com) 报告漏洞。
包含受影响版本和复现步骤。
不要附带凭据或机密模型数据。
尚未披露的漏洞不得发布到公开 Issue 或 Discussions。

<a id="security-boundaries"></a>
## 安全边界

文件通道使用操作系统权限。
仅允许受信任用户访问通道目录。
响应可能包含模型路径和参数值。
参见[服务器隐私设置](server/README.md#responses-and-privacy)。

HTTP 默认绑定到回环地址，除 `/health` 外，每条路由都使用每用户令牌认证。
健康检查会暴露文档名称、Revit 版本、进程 ID 和工作站只读状态。
保护 `%LOCALAPPDATA%\RevitModelMcp\settings.json`，远程访问使用加密隧道。
监听器没有内置 TLS。
动作需要工作站门禁；Python 服务器还要求显式的注册标志。
绑定设置参见[传输](docs/transport.md)，门禁参见[动作（主动启用）](README.md#actions-opt-in)。

<a id="supported-versions"></a>
## 版本范围

0.x 发布为预览版本；报告问题时请针对最新发布版本或 main。
