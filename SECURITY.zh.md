# 安全政策

!!! note "中文版"
    本页是中文说明；英文原文见本页的 English 版本（右上角切换）。

<a id="reporting"></a>
## 报告漏洞

请**不要**用公开 issue 报告安全问题。用 GitHub 的私密漏洞报告（Security → Report a vulnerability）或直接联系维护者，并附上：复现步骤、受影响版本、你的环境（Revit 年份、插件版本、传输方式）。

<a id="supported-versions"></a>
## 支持范围

只对最新发布版本提供安全修复；Revit 2020–2027 的构建都在支持范围内。

## 设计上的安全边界

- 默认只读，写入需两道门禁（客户端环境变量 + 工作站文件）。
- HTTP 通道只监听回环地址，使用 Bearer token 鉴权；跨机建议 SSH 端口转发。
- 不记录令牌，不把模型数据发往任何外部服务。
