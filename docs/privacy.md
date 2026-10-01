<a id="privacy-policy"></a>

# 隐私政策

生效日期：2026 年 9 月 14 日。
本政策的变更记录在仓库历史中。

<a id="data-collection"></a>

## 数据收集

Revit Model MCP 读取配置的工作站上在 Revit 中打开的模型，并返回 MCP 客户端请求的信息。
请求的数据可能包括模型名称、路径、元素参数、几何、警告和导出的视图图像。
两道写入门禁都启用时，可选动作可以修改模型。
项目不包含分析统计、遥测或崩溃报告功能。
运行时网络连接用于访问配置的 Revit 工作站，采用 HTTP 或 SSH，并可能经过用户配置的代理或隧道。
扩展包启动器在安装或更新时，使用 uvx 从 PyPI 及其包托管服务下载程序包和依赖。
预发布扩展包从 GitHub Releases 下载程序包的 wheel。
这些包下载不会发送 Revit 模型数据。

<a id="usage-and-storage"></a>

## 使用与存储

响应针对所请求的操作返回给 MCP 客户端。
local 和 SSH 文件通道在 Windows 工作站的 `%LOCALAPPDATA%\RevitModelMcp` 下写入请求、响应和导出的 PNG 文件。
`REVIT_MCP_CHANNEL_DIR` 可以覆盖通道目录。
设置和工作站写入门禁仍保留在默认目录。
HTTP 将已完成任务的响应保存在内存中，直到过期；导出图像也使用工作站通道目录。
下载的 PNG 文件写入 `save_to` 指定的客户端路径，或客户端临时目录下新建的 `revit-view-*` 目录。

`REVIT_MCP_REDACT_PATHS=1` 会从响应的 `documentPath` 和嵌套 `path` 字段中移除目录部分。
扩展包默认启用此设置。
模型名称、参数值、错误和导出图像的 `localPath` 值仍然可见。
脱敏作用于 Python 向外返回的响应，而非工作站文件或插件日志。
布尔设置还接受 `true/false`、`yes/no` 和 `on/off`，不区分大小写，并忽略首尾空白；`1/0` 仍是规范写法。

<a id="third-party-sharing"></a>

## 与第三方共享

本项目不向维护者或分析统计服务发送模型数据。
所选 MCP 客户端会接收请求的响应，并可能按其自身政策处理或保留这些响应。
Claude Desktop 受 [Anthropic 隐私政策](https://www.anthropic.com/legal/privacy)约束。
其他 MCP 客户端有各自的隐私政策。
用户配置的远程主机、代理和隧道都是所选传输路由的一部分。

<a id="data-retention"></a>

## 数据保留

[传输契约](transport.md)规定，已完成的 HTTP 结果在十分钟后过期。
插件每分钟检查一次过期情况，并尝试删除相关 HTTP 图像产物。
Revit 进程退出时，内存中的结果也会消失。
文件通道在处理过程中消耗触发文件，并在取回结果时尝试移除响应文件和原始 PNG 导出文件。
待处理文件，以及操作中断或清理失败后残留的文件，可能继续保留在磁盘上；这些文件没有按时间自动过期的机制。
下载到客户端的 PNG 文件没有由本项目管理的过期机制。

插件日志存储在 Windows“文档”文件夹的 `RevitModelMcp\Logs` 下；无法使用该位置时，回退到 `%TEMP%\RevitModelMcp\Logs`。
日志达到 10 MiB 时轮转，启动时的清理保留最近修改的 14 个日志文件。
这是文件数量限制，不是以天数计算的保留期。
即使已启用 Python 响应脱敏，日志仍可能包含模型名称、路径和异常详情。
Python 诊断信息发送到 MCP 客户端的日志流；保留规则由该客户端控制。

若要移除项目数据，先关闭 Revit 和 MCP 服务器，卸载插件和桌面扩展，再移除 `%LOCALAPPDATA%\RevitModelMcp`。
还应移除任何自定义通道目录、上述日志目录和客户端上下载的 PNG 文件。
仅卸载软件会保留本地设置。
客户端对话、客户端日志和包缓存需要通过客户端或包管理器另行删除。

<a id="contact"></a>

## 联系方式

隐私问题可以发送至 [sharafutdinov.di.dev@outlook.com](mailto:sharafutdinov.di.dev@outlook.com)。
涉及安全的敏感报告可以使用 [GitHub 私密安全公告表单](https://github.com/sharafutdinovdi/revit-model-mcp/security/advisories/new)。
