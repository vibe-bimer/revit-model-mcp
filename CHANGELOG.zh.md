# 变更日志（中文要点）

!!! note "中文版"
    本页是中文要点；逐条明细以英文 [CHANGELOG.md](CHANGELOG.md) 为准（由 release-please 自动生成，请勿手改）。切换右上角语言可看英文原文。

## 0.9.0

- **一份新模型连续出多份**：`revit_rebuild_model_ids` 支持 `copies`（1–50），每份落在互不重叠的 ID 区间，源模型始终只读。
- **批量更稳**：份与份之间自动清理，粘贴被 Revit 拒绝时自动沿用新模型已有类型重做一次；只有重试也失败才退回逐元素兜底，并在结果里标 `idMappingVerified=false`。
- **提速**：10 份副本从 571 s（每份粘贴两遍）降到 165 s（16.5 s/份），见 [重建性能](rebuild-performance.md)。
- **弹窗**：新增 `REVIT_MCP_ANSWER_DIALOGS`，无人值守实例可自动应答弹窗。
- **文档站**：中英双语的生成式功能文档，工具元数据从 MCP 服务器导出，CI 校验生成物是否同步。

## 0.8.1

- 修复 ID 重建与清单导出在 Revit 2020 上的兼容问题（`DisplayUnitType`/`UnitType` 路径）。
- 安装脚本与签名流程改进。

## 0.8.0

- 新增 **`revit_rebuild_model_ids`**：把三维视图里可选中的构件重建为全新 ID 的副本。
- 新增 **`revit_reset_element_ids`**：同文档内换 ID（只对无宿主、无依赖的构件有效）。
- 新增 **`revit_export_element_ids`**：导出构件 ID 清单到 xlsx（按类别/族/类型排序）。

## 0.7.0 及更早

- 关系查询（标高的房间、组内构件、嵌套族、视图样板依赖）、共享坐标、参数填充率检查。
- 动作工具形成完整闭环：`select`/`show`/`isolate`/`move`/`place_family`/`create_wall`/`create_floor`/`set_phase`/`merge_phases`/`set_parameter`/`delete`/`batch`，支持 `dry_run` 与一次撤销。
- 双门禁写入模型、回环优先的传输、心跳与插件日志。
