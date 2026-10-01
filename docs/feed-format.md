# 文件通道格式（中文摘要）

!!! note "中文摘要"
    本页为中文摘要；把右上角语言切到 English 可看完整说明。

要点：HTTP 通道未启用时，插件与客户端通过 `%LOCALAPPDATA%\RevitModelMcp` 下的文件交换数据——`trigger.txt` 通知有新任务，`response_*.json` 回传结果；文件名里带命令名与关联 ID，结果默认 10 分钟后过期并被清理。要长期运行或并发调用，建议改用 HTTP 通道。

## 响应文件 <a id="command-responses"></a>

本节是英文页对应小节的锚点，便于英文页面内的交叉链接在中文界面同样可用。
