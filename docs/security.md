<a id="security"></a>

# 安全

数据处理、保留规则和联系方式见[隐私政策](privacy.md)。

模型 API 默认只读。
除非启用 `REVIT_MCP_ALLOW_WRITE=1`，否则不会注册动作工具；执行动作还要求存在[动作](actions.md)中说明的工作站门禁文件。
默认能力包括连通性检查、文档和实例信息、目录、元素查询和聚合、视图及其中的元素、元素参数、警告、关系、PNG 视图导出，以及模型健康、链接、共享坐标和参数填写检查这四个协调检查工具。
[命令执行器](../src/RevitModelMcp.Addin/Control/ReadCommandExecutor.cs)和读取器不开启 Revit 事务，也不提供元素创建、删除、参数设置或模型保存操作。
视图导出调用 `Document.ExportImage` 并写入图像文件。
通道任务、响应、心跳和诊断日志也会在模型之外写入文件。

`REVIT_MCP_REDACT_PATHS=1` 或 `--redact-paths` 将响应的 `documentPath` 和每个 `path` 字段缩减为文件名，包括链接和图像路径。
这涵盖嵌套结果和实例列表。
模型名称、参数值、错误文本、通道文件以及导出图像的 `localPath` 值仍然可见。

HTTP 默认绑定到 `127.0.0.1:53110`。
每个用户的 `settings.json` 中会生成一个 32 字节随机 Bearer 令牌；文件受保护的 NTFS ACL 只授予当前用户访问权限。
令牌永远不会写入日志。
除 `/health` 外，所有 HTTP 路由都要求令牌；健康检查会暴露活动文档名称和进程信息。
没有内置 TLS：远程访问应通过隧道或 TLS 代理。
在 Revit 环境中设置 `REVIT_MCP_HTTP_ENABLED=0`，或在设置中设置 `httpEnabled=false`，可以彻底禁用监听器。
通过任何传输方式进行的 MCP 动作调用都需要两道门禁。
直接通过 HTTP 提交的动作任务要求 Bearer 令牌和工作站门禁；Python 注册开关不适用于直接调用方。

SSH 模式不存储凭据。
认证和路由使用本地 OpenSSH 配置和代理。
默认的多路复用套接字目录在 macOS 和 Linux 上的权限为 `0700`。
Windows 文件通道依赖账户的文件系统权限。
参见[传输](transport.md)和[安全问题报告](../SECURITY.md)。

<a id="verify-downloads"></a>

## 校验下载

发布资产附带 GitHub 构建来源证明（provenance attestation）。
下载资产后，使用 GitHub CLI 校验：

```sh
gh attestation verify RevitModelMcp-<version>-SingleUser.msi --owner sharafutdinovdi
```

成功时命令以退出码 0 结束，并报告已验证的证明。
检查仓库是否为 `sharafutdinovdi/revit-model-mcp`，签名工作流是否为 `.github/workflows/release.yml`，以及源码提交是否与预期发布标签匹配。
若要显式限制仓库和工作流：

```sh
gh attestation verify RevitModelMcp-<version>-SingleUser.msi \
  --repo sharafutdinovdi/revit-model-mcp \
  --signer-workflow sharafutdinovdi/revit-model-mcp/.github/workflows/release.yml
```

同一命令也可以将 MSI 文件名替换为按年份发布的 ZIP、wheel、源码发行包、`.mcpb` 或 `SHA256SUMS.txt`。
证明将下载文件的摘要绑定到本仓库的构建工作流和一个源码提交。
它不证明程序安全，也不覆盖 uv 随后下载的包。
MSI 和可执行文件未使用 Authenticode 签名；Windows 仍可能显示未知发布者警告。
扩展包没有 MCPB 证书签名。
来源证明适用于启用该功能后构建的发布版本；旧发布不会追溯补充证明。
