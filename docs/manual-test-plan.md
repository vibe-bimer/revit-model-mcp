# 人工测试计划（中文摘要）

!!! note "中文摘要"
    本页为中文摘要；把右上角语言切到 English 可看完整说明。

要点：按"读取 → 动作（dry_run → 真跑）→ 导出 → 重建 ID"的顺序人工过一遍；每个动作先 `dry_run` 看 `verification`，再真跑并在 Revit 里核对结果；写操作需要客户端 `REVIT_MCP_ALLOW_WRITE=1` 与工作站 `allow-write` 文件，且只允许一个 Revit 实例。
