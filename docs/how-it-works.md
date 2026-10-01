<a id="how-it-works"></a>

# 工作原理

Python 服务器运行在 MCP 客户端所在的机器上，通过 stdio 与客户端通信。
插件运行在 Windows 上的 Revit 进程内，通过 ExternalEvent 读取活动文档。
远程客户端可以使用带 Bearer 令牌的 HTTP，或 SSH 文件通道。

<a id="compatibility"></a>

## 兼容性

插件以每个受支持年份中最低的稳定 Revit API 构建版本为目标，以兼容该年份的所有补丁版本。

<a id="first-call"></a>

## 首次调用

1. Revit 加载 `RevitModelMcp.addin`，并启动文件监视器、心跳和可选的 HTTP 监听器。
2. MCP 客户端调用 `revit_ping`；服务器构造 `{"command":"ping"}`。
3. HTTP 将任务放入内存队列；local 或 SSH 模式将任务发布为 Windows 通道目录中的 `trigger.txt`。
4. ExternalEvent 在 Revit API 线程上调用共用的命令处理器。
5. 处理器返回 `success:true` 和 `data:"pong"`；服务器通过 MCP 交付 JSON 结果。

通道目录默认为 `%LOCALAPPDATA%\RevitModelMcp`，而非 `%LOCALAPPDATA%\RevitDevLoader`。
插件通过其清单直接加载，不需要单独的加载器。
[数据格式](feed-format.md)说明了路径和响应字段。

<a id="read-only-and-actions"></a>

## 只读工具与动作工具

默认工具读取模型数据，或将视图导出为 PNG。
导出和诊断会在 Revit 模型之外写入文件。
只有 Python 进程启动时启用 `REVIT_MCP_ALLOW_WRITE=1`，动作工具才会出现在 MCP 中。
插件执行任何动作还要求存在 `%LOCALAPPDATA%\RevitModelMcp\allow-write`。
删除该门禁文件即可禁用动作执行，无需重启 Revit。
MCP 环境变量门禁控制工具注册；直接通过 HTTP 调用时则检查令牌和工作站门禁。

选择和导航使用 UI 调用。
模型修改和临时隔离分别在独立事务中执行。
`revit_batch` 使用 `TransactionGroup` 将各步骤的事务组织在一起：成功时形成一个撤销记录，失败或批量试运行时回滚整个事务组。
成功时会消除并报告警告；未解决的错误会导致动作回滚。
动作处理会尝试覆盖 TaskDialog 对话框，并报告其消息。
这些工具不会保存模型。

<a id="routing-and-waiting"></a>

## 路由与等待

HTTP 默认使用 `127.0.0.1:53110`；Bearer 令牌存储在每个用户自己的 `settings.json` 中。
每个 HTTP 端点属于一个 Revit 进程。
通过隧道可以连接远程客户端，同时让监听器继续绑定回环地址。
局域网和 Tailscale 路由见[传输配置](transport.md)。

local 和 SSH 模式以运行 Revit 的账户执行 Windows PowerShell。
每个文件通道请求都携带唯一的 `correlationId`；服务器通过该 ID 匹配响应文件名和响应内容。响应先写入临时文件，再以原子替换方式发布。
每个文件通道目录只运行一个服务器进程；有多个 Revit 实例时，使用具有区分度的 `document` 筛选条件。
HTTP 根据任务 ID 轮询，完成后的结果保留十分钟。
超时不会取消已接受的任务，尤其不会取消动作。

[架构](architecture.md)说明了调度和失败行为。
[服务器参考](../server/README.md)列出了环境设置。

<a id="model-naming-defaults"></a>

## 模型命名默认规则

查询和目录查找接受活动文档中的名称。
快照和视图转储采用以下通用默认规则：

| 数据 | 默认规则 |
| --- | --- |
| 视图转储的配置参数 | 名称以 `Project_` 开头，不区分大小写；实例值优先于类型值 |
| 视图转储的测量值 | `Length`、`Thickness`、`Area` 和 `Volume`，不区分大小写；长度以毫米、面积以平方米、体积以立方米报告 |
| 快照区域 | 族名称包含 `Region` 的族实例，不区分大小写 |
| 区域备注 | 名为 `Comment 1` 和 `Comment 2` 的参数 |
| 注释参数 | 内置 `Mark`，以及名为 `Segment`、`Number` 和 `Zone Code` 的参数 |
| 幕墙嵌板参数 | 上述注释参数，加上 `NameOverride` |
| 视图计数 | 名称以区分大小写的 `Coordination_` 或 `Construction_` 为前缀的非模板视图 |
| 剖面前缀标签 | 区分大小写的开头文本 `Coordination` 或 `Construction`；其他名称均标记为 `other` |

缺失的注释、幕墙嵌板和配置参数值会被省略；缺失的区域备注为 null。
快照提供 `regions`、`regionCount`、区域的 `comment1` 和 `comment2`、模型计数 `totalRegions`、`coordinationViews` 和 `constructionViews`，以及嵌板统计 `panelsWithSegment` 和 `panelsWithNumber`。
模型名称和本地化类别标签按其在 Revit 中存储的内容原样返回。
