---
description: "本仓库自研 8 个工具的移植状态：1 个已接到新版底座，7 个仍在待移植队列。"
---

# 自研工具的移植状态

本仓库自己设计的工具一共 8 个，其中 1 个已经接到新版底座上，7 个还在待移植队列里。这些工具都不改变基座的行为，只通过 fork 注册表追加命令。

| 工具数 | 基座与自研的区分 | 移植状态 |
| --- | --- | --- |
| [设置视图光照](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | 自研（本仓库） | <span class="state ok">已移植</span> |
| [创建标高](#revit-create-level)<br>`revit_create_level` | 自研（本仓库） | <span class="state no">待移植</span> |
| [创建楼板](#revit-create-floor)<br>`revit_create_floor` | 自研（本仓库） | <span class="state no">待移植</span> |
| [设置阶段](#revit-set-phase)<br>`revit_set_phase` | 自研（本仓库） | <span class="state no">待移植</span> |
| [合并阶段](#revit-merge-phases)<br>`revit_merge_phases` | 自研（本仓库） | <span class="state no">待移植</span> |
| [导出构件 ID 台账](#revit-export-element-ids)<br>`revit_export_element_ids` | 自研（本仓库） | <span class="state no">待移植</span> |
| [重置构件 ID](#revit-reset-element-ids)<br>`revit_reset_element_ids` | 自研（本仓库） | <span class="state no">待移植</span> |
| [重建模型 ID](#revit-rebuild-model-ids)<br>`revit_rebuild_model_ids` | 自研（本仓库） | <span class="state no">待移植</span> |

已移植表示分支上能列出并执行；待移植表示实现已在本地版本里，但分支上还没有对应命令。

## 创建标高 {#revit-create-level}

`revit_create_level` — 已有本地实现（含 dry_run 与验证块），待按新契约重映射到 fork 注册表。

## 创建楼板 {#revit-create-floor}

`revit_create_floor` — 已有本地实现，待重映射。

## 设置阶段 {#revit-set-phase}

`revit_set_phase` — 已有本地实现；Revit 阶段不能创建或改名，只能写入既有阶段。

## 合并阶段 {#revit-merge-phases}

`revit_merge_phases` — 已有本地实现；该命令不进批量步骤词表。

## 导出构件 ID 台账 {#revit-export-element-ids}

`revit_export_element_ids` — 已有本地实现，输出 xlsx 台账，含系统成员与连接器读取。

## 重置构件 ID {#revit-reset-element-ids}

`revit_reset_element_ids` — 已有本地实现，可排练（dry_run 报出代价），每构件独立子事务。

## 重建模型 ID {#revit-rebuild-model-ids}

`revit_rebuild_model_ids` — 已有本地实现（约一千行），支持模板、副本与重名策略；是最后一个移植项，工作量约等于前五项之和。

---

[返回目录](index.md)
