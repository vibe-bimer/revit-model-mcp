#!/usr/bin/env python3
"""Generate the platform catalog: the integration branch's 80 tools, split by origin.

The released tool pages under docs/features come from tools.json, which is dumped from the
released server. This module documents the other catalog: the tool surface of branch
integration/upstream-1.0, which is not released. Its snapshot lives in
tools/site/content/platform-tools.json and is refreshed by --dump-platform in
generate_features.py against the worktree on that branch.

Every tool is labelled by origin, because the point of this section is to keep the upstream
base ("基座") apart from the tools this fork owns ("自研"):
  upstream  a tool that came with the upstream base.
  fork      a tool this fork designed; only the grafted ones exist on the branch yet.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "tools/site/content"
PLATFORM_JSON = CONTENT / "platform-tools.json"
TOOLS_JSON = CONTENT / "tools.json"
PAGES = ROOT / "docs/platform"
NAV_START = "  # >>> platform-nav"
NAV_END = "  # <<< platform-nav"

BRANCH = "integration/upstream-1.0"

GROUP_LABELS = {
    "zh": {
        "core": "连接与实例",
        "read": "查询与统计",
        "actions": "编辑原语",
        "documents": "文档生命周期",
        "views-sheets": "视图、图纸与明细表",
        "family": "族",
        "links": "链接与基准",
        "cad-mep": "CAD 与 MEP",
        "export": "导出与登记",
        "batch": "批处理与报告",
        "code": "C# 逃生口",
    },
    "en": {
        "core": "Connection and instances",
        "read": "Query and totals",
        "actions": "Editing primitives",
        "documents": "Document lifecycle",
        "views-sheets": "Views, sheets and schedules",
        "family": "Families",
        "links": "Links and datums",
        "cad-mep": "CAD and MEP",
        "export": "Export and registers",
        "batch": "Batch and reports",
        "code": "C# escape hatch",
    },
}

# Chinese page content for every tool on the integration branch. The English page uses the
# tool's own description, which is the authoritative text the server ships.
ZH = {
    "revit_change_type": (
        "更改构件类型",
        "把构件换成同一族内的兼容类型，重名类型按族解析；`dry_run` 会回滚。",
    ),
    "revit_copy": (
        "复制构件",
        "沿模型轴按毫米偏移创建 1 到 100 份连续副本；`dry_run` 会回滚。",
    ),
    "revit_delete": (
        "删除构件",
        "删除构件及其 Revit 依赖，计数包含依赖对象；连同依赖超过 500 个构件时需要确认令牌。",
    ),
    "revit_mirror": (
        "镜像构件",
        "沿穿过给定点的模型 X 或 Y 平行线镜像，`copy` 保留原件；组成员、固定、宿主与受约束构件会跳过并报告。",
    ),
    "revit_move": (
        "移动构件",
        "按 `dx_mm`、`dy_mm`、`dz_mm` 沿模型轴移动构件；`dry_run` 回滚并返回验证块。",
    ),
    "revit_rotate": (
        "旋转构件",
        "绕穿过 `center_mm` 的竖轴旋转，或不给点时按组合包围盒中心旋转。",
    ),
    "revit_run_actions": (
        "批量执行动作",
        "在一次撤销内执行最多 50 个动作，首个失败时整体回滚；`dry_run` 回滚并返回验证块。",
    ),
    "revit_set_parameter": (
        "设置参数",
        "写入一个实例或类型参数，可用参数 ID、共享参数 GUID 或本地化名称定位；长度用毫米、面积用平方米。",
    ),
    "revit_update_parameters": (
        "批量更新参数",
        "对符合同一查询条件的构件更新同一个参数，组成员跳到 `skipped.inGroup` 而不中断调用。",
    ),
    "revit_batch_cancel": (
        "取消批量收集",
        "持久化取消标记，尚未开始的模型不再运行；已开始的模型走完当前步骤。",
    ),
    "revit_batch_fetch": (
        "取回批量快照",
        "把已完成的快照下载为新的本地文件，不覆盖已有文件。",
    ),
    "revit_batch_start": (
        "开始批量收集",
        "对本地、UNC 或 RSN 模型启动持久化的只读批量运行；`open_timeout_minutes` 是单个模型的打开时限。",
    ),
    "revit_batch_status": (
        "批量收集状态",
        "在发起客户端退出后仍可读取运行与模型状态。",
    ),
    "revit_build_report": (
        "生成快照报告",
        "不连接 Revit，直接从快照生成本地 Excel 报告。",
    ),
    "revit_process_models": (
        "批处理模型",
        "在同一会话中逐个打开模型，执行步骤与 C# 代码、导出、按需保存后关闭；就地保存和代码需要确认令牌。",
    ),
    "revit_create_mep_run": (
        "创建 MEP 管线",
        "按模型毫米坐标点创建相连的风管、水管、桥架或线管段；缺失的 Z 取标高加该类默认偏移。",
    ),
    "revit_create_wall": (
        "创建墙",
        "在指定标高上创建直墙，XY 端点与高度用毫米；不给墙类型时取第一个基本类型。",
    ),
    "revit_link_cad": (
        "链接 CAD",
        "在 Revit 工作站把 DWG 链接或导入平面视图，返回 CAD 图层与范围。",
    ),
    "revit_walls_from_cad": (
        "从 CAD 建墙",
        "桥接洞口、配对平行 CAD 线并在一次撤销内连接基本墙；Revit 拒绝的连接会列出原因。",
    ),
    "revit_execute_code": (
        "执行 C# 代码",
        "在 Revit 线程上编译并运行 C#，可直接调用 Revit API；写入模型需要先取得确认令牌。",
    ),
    "revit_cancel_job": (
        "取消动作任务",
        "请求取消某个 `jobId`；批处理在下一个模型前停止，已经完成的改动保留。",
    ),
    "revit_document_info": (
        "文档信息",
        "读取活动模型的文件名、Revit 版本、标高（毫米）、面积方案、工作集与视图数量。",
    ),
    "revit_documents": (
        "文档列表",
        "列出一个 Revit 进程中打开的所有文档，包含后台文档；链接文档需显式开启。",
    ),
    "revit_jobs": (
        "任务列表",
        "列出最近任务，或等待某个动作任务的结果；结果在工作站保留 24 小时。",
    ),
    "revit_list_instances": (
        "实例列表",
        "列出 Revit 进程及其文档名、路径、版本、进程号与插件响应状态；忙碌进程仍会列出。",
    ),
    "revit_ping": (
        "连接检查",
        '不读模型，仅检查与 Revit 的连接；没有活动文档时也返回 `data="pong"`。',
    ),
    "revit_ui_state": (
        "界面状态",
        "读取活动文档、打开的视图、当前选择集与打开的文档列表。",
    ),
    "revit_undo_last": (
        "撤销上一个动作",
        "通过 Revit 自身的撤销命令撤销上一次 MCP 动作；条件不满足时结果带拒绝原因。",
    ),
    "revit_activate_document": (
        "激活文档",
        "按标题或路径引用激活一个已经打开的文档。",
    ),
    "revit_close_document": (
        "关闭文档",
        "关闭后台文档；需要先调用一次取得确认令牌，首次调用不改变任何内容。",
    ),
    "revit_new_document": (
        "新建文档",
        "在 Revit 工作站上用样板创建项目或族文件。",
    ),
    "revit_open_document": (
        "打开文档",
        "打开本地、UNC 或 RSN 模型；中心模型默认以分离方式打开，云路径不支持。",
    ),
    "revit_save_document": (
        "保存文档",
        "保存文档；需要先取得确认令牌，首次调用不改变任何内容。",
    ),
    "revit_sync_document": (
        "同步文档",
        "把工作共享文档与中心文件同步；需要先取得确认令牌。",
    ),
    "revit_export": (
        "导出模型文件",
        "在 Revit 工作站导出 PDF、DWG、IFC 或明细表 CSV；`dry_run` 只返回计划生成的文件名。",
    ),
    "revit_export_nwc": (
        "导出 NWC",
        "在 Revit 工作站导出 Navisworks NWC，需要安装导出器；`settings_xml` 应用导出器参数。",
    ),
    "revit_issue_register": (
        "生成问题登记表",
        "生成本地 xlsx 问题登记表，含构件快照与审阅文档；已有同名输出文件时拒绝执行。",
    ),
    "revit_nwc_settings_check": (
        "检查 NWC 设置",
        "只解析 Navisworks 导出器 XML，不执行导出。",
    ),
    "revit_edit_families": (
        "编辑族",
        "就地编辑已打开的族，或对指定项目族逐个执行一个加载循环；`dry_run` 回滚全部改动。",
    ),
    "revit_family_audit": (
        "审核族",
        "审核已打开的族或指定项目族的参数使用情况，不保存也不加载改动；通配项目模式最多取 200 个族。",
    ),
    "revit_load_family": (
        "载入族",
        "在一次撤销内载入工作站的 .rfa 文件；已有同名族默认跳过。",
    ),
    "revit_place_families": (
        "批量放置族",
        "载入可选族并在同一事务、同一次撤销内放置多个实例。",
    ),
    "revit_place_family": (
        "放置族",
        "在指定标高上放置已载入的非宿主族；`family` 可以是名称或 `Family: Type`。",
    ),
    "revit_align_link_datums": (
        "对齐链接基准",
        "把主体的轴网与标高对齐到已载入的链接，可选创建与回滚预览，但不建立监视关系。",
    ),
    "revit_compare_link_datums": (
        "比较链接基准",
        "把主体的轴网与标高和一个已载入的 Revit 链接比较，不改动模型。",
    ),
    "revit_remove_links": (
        "移除链接",
        "删除选定的链接类型及其全部实例；`dry_run` 只预览，Revit 中无法撤销。",
    ),
    "revit_aggregate_elements": (
        "聚合统计",
        "按一到两个字段汇总符合条件的构件，可选求和与平均；长度用毫米、面积用平方米、体积用立方米。",
    ),
    "revit_element_details": (
        "构件详情",
        "按 Revit ID 读取构件的参数与几何，含类型参数与相关警告；几何用模型毫米。",
    ),
    "revit_links_status": (
        "链接状态",
        "读取 RVT、CAD 与图片链接状态；每类最多 100 条，汇总计数覆盖全部链接。",
    ),
    "revit_list_catalog": (
        "目录列表",
        "列出某一类目录：类目、族类型、标高、面积方案、视图、工作集、阶段或参数；默认上限 200 条。",
    ),
    "revit_list_relations": (
        "关系列表",
        "读取模型对象的归属或依赖关系，如标高与房间、面积方案与构件、视图样板与从属视图、组与嵌套族。",
    ),
    "revit_list_warnings": (
        "警告列表",
        "按描述文本分组列出模型警告；指定文本并开启 `include_elements` 可展开该组的构件。",
    ),
    "revit_model_health": (
        "模型健康检查",
        "读取项目元数据、文件大小、计数、单位与十类最常见警告；`output_path` 另写 xlsx 报告。",
    ),
    "revit_model_snapshot": (
        "模型快照",
        "读取 schema 版本 1 的项目快照，供批量审计使用；关闭的工作集会让结果不完整。",
    ),
    "revit_parameter_fill_check": (
        "参数填充检查",
        "按参数与类目统计已填、空值与缺失数量，并给出空值和缺失构件的示例 ID。",
    ),
    "revit_query_elements": (
        "查询构件",
        "分页读取符合条件的构件行，长度用毫米、面积用平方米、体积用立方米；`hasMore` 表示还有下一页。",
    ),
    "revit_schedule_data": (
        "读取明细表数据",
        "读取明细表显示的表头与单元格文本，支持分页。",
    ),
    "revit_shared_coordinates": (
        "共享坐标",
        "读取项目与测量坐标：基点、测量点、活动场地、项目位置与链接偏移，单位毫米与度。",
    ),
    "revit_activate_view": (
        "激活视图",
        "激活一个非样板视图，可缩放适配、保持当前缩放或框选指定构件。",
    ),
    "revit_apply_view_template": (
        "应用视图样板",
        "把匹配的视图样板应用到一个或多个视图。",
    ),
    "revit_capture_elements": (
        "截取构件画面",
        "渲染带高亮的 PNG，标记 1 到 500 个构件作为问题证据，临时视图在结束后回滚。",
    ),
    "revit_close_views": (
        "关闭视图",
        "关闭活动文档中已打开的界面视图。",
    ),
    "revit_create_schedule": (
        "创建明细表",
        "按给定字段顺序为一个类目创建明细表，字段用 Revit 界面名称；`filters`、`sort` 与分组控制行列。",
    ),
    "revit_create_sheet": (
        "创建图纸",
        "用第一个已载入的标题栏或指定标题栏创建图纸。",
    ),
    "revit_create_view": (
        "创建视图",
        "创建平面、剖面、三维或绘图视图；无边界三维视图显示整个模型。",
    ),
    "revit_duplicate_view": (
        "复制视图",
        "复制视图，可选带详图复制或创建为从属视图。",
    ),
    "revit_export_view": (
        "导出视图为 PNG",
        "把选定视图导出为 MCP 客户端上的 PNG 文件，不改变活动视图与模型。",
    ),
    "revit_isolate": (
        "隔离构件",
        "在活动视图中临时隔离指定构件 ID；空列表即取消隔离。",
    ),
    "revit_list_views": (
        "视图列表",
        "列出非样板视图的 ID、名称、类型、标高、比例与样板。",
    ),
    "revit_override_graphics": (
        "高亮构件",
        "在选定模型视图中给构件上色；`reset` 恢复本 Revit 会话中保存的替代。",
    ),
    "revit_place_views_on_sheet": (
        "在图纸上布置视图",
        "把视图与明细表放到图纸上，坐标用图纸毫米。",
    ),
    "revit_select": (
        "选择构件",
        "在 Revit 中选择指定构件 ID 以便查看；空列表即清除选择。",
    ),
    "revit_set_view_lighting": (
        "设置视图光照",
        "设置一个视图的阴影、太阳位置、地平面、背景与渲染光照方案；响应给出改动前后的读数与变化项清单。",
    ),
    "revit_set_view_visibility": (
        "设置视图可见性",
        "在一个视图中更改类目、工作集与过滤器可见性；`dry_run` 只预览。",
    ),
    "revit_show": (
        "显示构件",
        "在 Revit 中显示构件并可同时选中，必要时打开标高平面或三维视图。",
    ),
    "revit_tag_elements": (
        "标注构件",
        "在视图中按类目名称或构件 ID 标注构件，两者只能选一个；已标注构件默认跳过。",
    ),
    "revit_view_elements": (
        "视图构件",
        "分页读取选定视图中的构件，含 ID、类目、族、类型、标高与长度面积体积。",
    ),
    "revit_view_info": (
        "视图信息",
        "查看一个视图的样板、显示设置、类目、工作集、过滤器与链接。",
    ),
    "revit_view_summary": (
        "视图摘要",
        "读取选定视图的构件类目与数量。",
    ),
    "revit_view_warnings": (
        "视图警告",
        "读取涉及选定视图中构件的警告；警告也可能涉及视图之外的其他构件。",
    ),
}

# Tools this fork owns. Only the grafted ones exist on the integration branch.
FORK_TOOLS = {
    "revit_set_view_lighting": {
        "status": "grafted",
        "zh": "设置视图光照",
        "en": "Set view lighting",
        "zh_note": "已通过 fork 注册表接上七个兜底钩子，Python 工具注册与单元测试通过；C# 编译与真机验证仍在 Windows CI 与工作站上。",
        "en_note": "Attached through the fork registry and the seven fallback hooks; the Python tool and its unit tests pass. C# compilation and live validation still happen on Windows CI and the workstation.",
    },
    "revit_create_level": {
        "status": "pending",
        "zh": "创建标高",
        "en": "Create level",
        "zh_note": "已有本地实现（含 dry_run 与验证块），待按新契约重映射到 fork 注册表。",
        "en_note": "The local implementation exists with dry_run and a verification block; it still has to be remapped onto the fork registry.",
    },
    "revit_create_floor": {
        "status": "pending",
        "zh": "创建楼板",
        "en": "Create floor",
        "zh_note": "已有本地实现，待重映射。",
        "en_note": "The local implementation exists; it still has to be remapped.",
    },
    "revit_set_phase": {
        "status": "pending",
        "zh": "设置阶段",
        "en": "Set phase",
        "zh_note": "已有本地实现；Revit 阶段不能创建或改名，只能写入既有阶段。",
        "en_note": "The local implementation exists; Revit cannot create or rename phases, so it only assigns existing ones.",
    },
    "revit_merge_phases": {
        "status": "pending",
        "zh": "合并阶段",
        "en": "Merge phases",
        "zh_note": "已有本地实现；该命令不进批量步骤词表。",
        "en_note": "The local implementation exists; the command is excluded from the batch step vocabulary.",
    },
    "revit_export_element_ids": {
        "status": "pending",
        "zh": "导出元素 ID 台账",
        "en": "Export element ID register",
        "zh_note": "已有本地实现，输出 xlsx 台账，含系统成员与连接器读取。",
        "en_note": "The local implementation writes an xlsx register and reads system members and connectors.",
    },
    "revit_reset_element_ids": {
        "status": "pending",
        "zh": "重置元素 ID",
        "en": "Reset element IDs",
        "zh_note": "已有本地实现，可排练（dry_run 报出代价），每元素独立子事务。",
        "en_note": "The local implementation is rehearsable, reports the cost in dry_run, and commits each element in its own subtransaction.",
    },
    "revit_rebuild_model_ids": {
        "status": "pending",
        "zh": "重建模型 ID",
        "en": "Rebuild model IDs",
        "zh_note": "已有本地实现（约一千行），支持模板、副本与重名策略；是最后一个移植项，工作量约等于前五项之和。",
        "en_note": "The local implementation is about a thousand lines and supports templates, copies and duplicate-name policies; it is the last item to migrate and roughly equals the first five together.",
    },
}

LABELS = {
    "zh": {
        "title": "新版基座工具目录",
        "intro": "这一节记录集成分支上的工具面，与「功能」一节的现有版本分开。分支上的工具尚未发布，其中七个自研工具还没移植，所以目录不是可交付清单，而是移植进度表。",
        "catalogs": "两套工具面",
        "catalogs_intro": "现有版本是已经发布的 0.9.0，集成分支是以上游一零版为底座的新线。两者的工具数量与清单都不同，不能混用。",
        "current": "现有版本",
        "platform": "集成分支",
        "released": "已发布",
        "unreleased": "未发布",
        "branch": "分支",
        "base": "底座提交",
        "origin": "基座与自研的区分",
        "origin_intro": "每个工具在页面上都带来源标记：基座表示随上游底座而来，自研表示本仓库自己设计。自研工具在分支上只移植了光照一项。",
        "base_origin": "基座（上游）",
        "fork_origin": "自研（本仓库）",
        "grafted": "已移植",
        "pending": "待移植",
        "groups": "分组统计",
        "group": "分组",
        "tools": "工具数",
        "read": "读取",
        "action": "动作",
        "all": "合计",
        "catalog": "逐项文档",
        "status": "状态说明",
        "status_body": "集成分支的工具已在 Python 注册表里注册，参数与描述直接来自注册表；C# 侧尚未在本机编译，真机也未验证。把这里的条目当成契约与进度，而不是「已可用」。",
        "fork_page": "自研工具的移植状态",
        "spec": "集成规格与决策记录",
        "kind": "类型",
        "include_release": "当前版本是否已有",
        "yes": "有",
        "no": "没有",
        "parameters": "参数",
        "common": "通用参数",
        "name": "参数",
        "required": "必填",
        "default": "默认值",
        "type": "类型",
        "meaning": "说明",
        "no_specific": "此工具没有额外业务参数，使用下列通用参数即可。",
        "behavior": "功能说明（注册表原文）",
        "behavior_note": "以下保留工具在注册表中声明的英文原文，作为契约来源。",
        "notes": "使用提示",
        "back": "返回目录",
        "group_index": "按分组浏览",
        "fork_status": "移植状态",
        "count_line": "共 {total} 个工具：基座 {base} 个，自研 {fork} 个；读取 {read} 个，动作 {action} 个。",
    },
    "en": {
        "title": "Platform tool catalog",
        "intro": "This section records the tool surface of the integration branch, kept apart from the released catalog under Features. The branch is unreleased and seven fork tools are still missing from it, so the catalog is a migration scoreboard, not a delivery list.",
        "catalogs": "Two catalogs",
        "catalogs_intro": "The current release is 0.9.0. The integration branch is the new line built on the upstream 1.0 base. Their tool counts and names differ, so they are not interchangeable.",
        "current": "Current release",
        "platform": "Integration branch",
        "released": "Released",
        "unreleased": "Unreleased",
        "branch": "Branch",
        "base": "Base commit",
        "origin": "Base and fork tools",
        "origin_intro": "Every page carries an origin marker: base means the tool came with the upstream base, fork means this repository designed it. Only one fork tool is grafted so far.",
        "base_origin": "Base (upstream)",
        "fork_origin": "Fork (this repository)",
        "grafted": "Grafted",
        "pending": "Pending",
        "groups": "Tools per group",
        "group": "Group",
        "tools": "Tools",
        "read": "Read",
        "action": "Action",
        "all": "Total",
        "catalog": "Per-tool documentation",
        "status": "What the status means",
        "status_body": "Every tool here is registered in the Python registry, and its parameters and description come from that registry. The C# side has not been compiled locally and nothing has been validated on a live workstation. Read these pages as contracts and progress, not as <q>available now</q>.",
        "fork_page": "Fork tool migration status",
        "spec": "Integration specification and decision records",
        "kind": "Kind",
        "include_release": "In the current release",
        "yes": "Yes",
        "no": "No",
        "parameters": "Parameters",
        "common": "Common parameters",
        "name": "Parameter",
        "required": "Required",
        "default": "Default",
        "type": "Type",
        "meaning": "Meaning",
        "no_specific": "No additional business parameters; use the common parameters below.",
        "behavior": "Behavior (registry text)",
        "behavior_note": "The tool's own English declaration from the registry is preserved below as the contract of record.",
        "notes": "Usage notes",
        "back": "Back to the catalog",
        "group_index": "Browse by group",
        "fork_status": "Migration status",
        "count_line": "{total} tools: {base} base and {fork} fork; {read} read and {action} action.",
    },
}

COMMON_PARAMETERS = {
    "document",
    "timeout_seconds",
    "pickup_timeout_seconds",
    "process_id",
}

PARAM_MEANINGS = {
    "zh": {
        "document": "打开多个模型时，用标题或路径指定目标文档。",
        "dry_run": "只排练：执行后回滚，返回同样的验证块。",
        "element_ids": "要处理的构件 Revit ID 列表。",
        "view": "视图的准确名称或十进制视图 ID。",
        "limit": "返回条数上限。",
        "offset": "分页起始位置。",
        "confirm_token": "首次调用返回的确认令牌，用于确认破坏性操作。",
        "process_id": "目标 Revit 进程号。",
        "timeout_seconds": "本次调用的等待上限（秒）。",
    },
    "en": {},
}


def snapshot() -> dict:
    return json.loads(PLATFORM_JSON.read_text(encoding="utf-8"))


def audit(platform: list[dict], payload: dict) -> None:
    """Fail closed so a stale or half-edited snapshot cannot publish a wrong catalog."""
    declared = payload.get("count")
    if declared != len(platform):
        raise SystemExit(
            f"platform-tools.json declares {declared} tools but holds {len(platform)}"
        )
    names = [tool["name"] for tool in platform]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise SystemExit(f"Duplicate platform tools: {duplicates}")
    unknown = sorted({tool["toolset"] for tool in platform} - set(GROUP_LABELS["zh"]))
    if unknown:
        raise SystemExit(f"Unknown platform toolsets: {unknown}")
    missing = sorted(set(names) - set(ZH))
    if missing:
        raise SystemExit(f"Missing Chinese page text for: {missing}")
    extra = sorted(set(ZH) - set(names))
    if extra:
        raise SystemExit(f"Chinese page text without a tool: {extra}")
    grafted = {name for name, item in FORK_TOOLS.items() if item["status"] == "grafted"}
    absent = sorted(grafted - set(names))
    if absent:
        raise SystemExit(f"Grafted fork tools missing from the snapshot: {absent}")


def load_platform() -> tuple[list[dict], list[dict]]:
    """Return (platform tools, released tools)."""
    payload = snapshot()
    platform = payload["tools"]
    audit(platform, payload)
    released = json.loads(TOOLS_JSON.read_text(encoding="utf-8"))
    return platform, released


def origin_of(name: str) -> str:
    return "fork" if name in FORK_TOOLS else "base"


def fork_state(name: str) -> str:
    return FORK_TOOLS.get(name, {}).get("status", "")


def counts(tools: list[dict]) -> dict:
    read = sum(1 for t in tools if t["readOnly"])
    fork = sum(1 for t in tools if origin_of(t["name"]) == "fork")
    return {
        "total": len(tools),
        "read": read,
        "action": len(tools) - read,
        "base": len(tools) - fork,
        "fork": fork,
    }


def badge(origin: str, name: str, lang: str) -> str:
    """Origin marker for a table cell; the same label goes into a plain fact span."""
    labels = LABELS[lang]
    if origin == "base":
        return f'<span class="state part">{labels["base_origin"]}</span>'
    state = fork_state(name)
    style = "ok" if state == "grafted" else "no"
    text = labels["grafted"] if state == "grafted" else labels["pending"]
    return f'<span class="state ok">{labels["fork_origin"]}</span> <span class="state {style}">{text}</span>'


def origin_text(origin: str, name: str, lang: str) -> str:
    """The same marker as plain text, for the fact strip where nesting spans would double up."""
    labels = LABELS[lang]
    if origin == "base":
        return labels["base_origin"]
    state = fork_state(name)
    return (
        f"{labels['fork_origin']} · "
        f"{labels['grafted'] if state == 'grafted' else labels['pending']}"
    )


def sort_key(tool: dict) -> tuple[int, str]:
    order = list(GROUP_LABELS["zh"])
    return order.index(tool["toolset"]), tool["name"]


def parameter_rows(tool: dict, common: bool, lang: str) -> list[str]:
    rows = []
    for name, spec in tool["inputSchema"].get("properties", {}).items():
        if (name in COMMON_PARAMETERS) != common:
            continue
        required = "是" if lang == "zh" else "Yes"
        if name not in tool["inputSchema"].get("required", []):
            required = "否" if lang == "zh" else "No"
        default = spec.get("default", "")
        kind = spec.get("type") or ("any" if "anyOf" in spec else "")
        meaning = (
            (PARAM_MEANINGS["zh"].get(name) if lang == "zh" else "")
            or spec.get("description", "")
            or ""
        )
        meaning = " ".join(str(meaning).split())
        rows.append(
            f"| `{name}` | {required} | {default if default != '' else '—'} | {kind} | {meaning} |"
        )
    return rows


def table_heading(lang: str) -> list[str]:
    labels = LABELS[lang]
    return [
        f"| {labels['name']} | {labels['required']} | {labels['default']} | {labels['type']} | {labels['meaning']} |",
        "| --- | :--: | --- | --- | --- |",
    ]


def tool_page(tool: dict, released_names: set[str], lang: str) -> str:
    labels = LABELS[lang]
    name = tool["name"]
    origin = origin_of(name)
    if lang == "zh":
        title, summary = ZH[name]
    else:
        title, summary = tool["title"] or name, " ".join(tool["description"].split())
    facts = [
        f"<b>{labels['group']}</b> {GROUP_LABELS[lang][tool['toolset']]}",
        f"<b>{labels['kind']}</b> {labels['read'] if tool['readOnly'] else labels['action']}",
        f"<b>{labels['origin']}</b> {origin_text(origin, name, lang)}",
        f"<b>{labels['include_release']}</b> {labels['yes'] if name in released_names else labels['no']}",
    ]
    out = [
        f"# {title}",
        "",
        f"`{name}`",
        "",
        '<p class="facts">'
        + "".join(f"<span>{fact}</span>" for fact in facts)
        + "</p>",
        "",
    ]
    if origin == "fork":
        note = FORK_TOOLS[name][f"{lang}_note"]
        out += [f'!!! note "{labels["notes"]}"', f"    {note}", ""]
    if lang == "zh":
        out += [summary, ""]
    out += [f"## {labels['parameters']} {{#parameters}}", ""]
    rows = parameter_rows(tool, False, lang)
    out += (table_heading(lang) + rows) if rows else [labels["no_specific"]]
    common = parameter_rows(tool, True, lang)
    if common:
        out += (
            ["", f"### {labels['common']} {{#common-parameters}}", ""]
            + table_heading(lang)
            + common
        )
    out += ["", f"## {labels['behavior']} {{#behavior}}", ""]
    if lang == "zh":
        out += [labels["behavior_note"], ""]
    description = "\n".join(
        line.strip() for line in tool["description"].strip().splitlines()
    )
    out += ["```text", description, "```", ""]
    out += [
        "---",
        "",
        f"[{labels['back']}](index.md) · [{labels['fork_page']}](fork-tools.md)",
        "",
    ]
    return "\n".join(out)


def index_page(tools: list[dict], released: list[dict], lang: str) -> str:
    labels = LABELS[lang]
    numbers = counts(tools)
    groups = {}
    for tool in sorted(tools, key=sort_key):
        groups.setdefault(tool["toolset"], []).append(tool)
    out = [
        f"# {labels['title']}",
        "",
        labels["intro"],
        "",
        labels["count_line"].format(**numbers),
        "",
        f"## {labels['catalogs']} {{#catalogs}}",
        "",
        labels["catalogs_intro"],
        "",
        f"| | {labels['current']} | {labels['platform']} |",
        "| --- | --- | --- |",
        f"| {labels['tools']} | {len(released)} | {len(tools)} |",
        f"| {labels['read']} | {sum(1 for t in released if t['annotations'].get('readOnlyHint'))} | {numbers['read']} |",
        f"| {labels['action']} | {sum(1 for t in released if not t['annotations'].get('readOnlyHint'))} | {numbers['action']} |",
        f"| {labels['released']} | {labels['released']} | {labels['unreleased']} |",
        f"| {labels['branch']} | main | `{BRANCH}` |",
        "",
        f"## {labels['origin']} {{#origin}}",
        "",
        labels["origin_intro"],
        "",
        f"| {labels['group']} | {labels['base_origin']} | {labels['fork_origin']} |",
        "| --- | --- | --- |",
    ]
    for key, members in groups.items():
        base = sum(1 for t in members if origin_of(t["name"]) == "base")
        fork = len(members) - base
        out.append(f"| {GROUP_LABELS[lang][key]} | {base} | {fork} |")
    totals = {t["name"] for t in tools}
    out += [
        f"| **{labels['all']}** | **{numbers['base']}** | **{numbers['fork']}** |",
        "",
        f"[{labels['fork_page']}](fork-tools.md) · [{labels['spec']}](https://github.com/vibe-bimer/revit-model-mcp/issues/27)",
        "",
        f"## {labels['groups']} {{#groups}}",
        "",
        f"| {labels['group']} | {labels['tools']} | {labels['read']} | {labels['action']} |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key, members in groups.items():
        read = sum(1 for t in members if t["readOnly"])
        out.append(
            f"| [{GROUP_LABELS[lang][key]}](#group-{key}) | {len(members)} | {read} | {len(members) - read} |"
        )
    out.append("")
    for key, members in groups.items():
        out += [
            f"## {GROUP_LABELS[lang][key]} {{#group-{key}}}",
            "",
            f"| {labels['tools']} | {labels['kind']} | {labels['origin']} |",
            "| --- | --- | --- |",
        ]
        for tool in members:
            name = tool["name"]
            title = ZH[name][0] if lang == "zh" else (tool["title"] or name)
            out.append(
                f"| [{title}]({name}.md)<br>`{name}` | "
                f"{labels['read'] if tool['readOnly'] else labels['action']} | {badge(origin_of(name), name, lang)} |"
            )
        out.append("")
    out += [f"## {labels['status']} {{#status}}", "", labels["status_body"], ""]
    assert totals
    return "\n".join(out)


def fork_page(tools: list[dict], lang: str) -> str:
    labels = LABELS[lang]
    names = {tool["name"]: tool for tool in tools}
    grafted = sum(1 for item in FORK_TOOLS.values() if item["status"] == "grafted")
    if lang == "zh":
        title = "自研工具的移植状态"
        intro = (
            f"本仓库自己设计的工具一共 {len(FORK_TOOLS)} 个，其中 {grafted} 个已经接到新版底座上，"
            f"{len(FORK_TOOLS) - grafted} 个还在待移植队列里。这些工具都不改变基座的行为，只通过 fork 注册表追加命令。"
        )
        legend = "已移植表示分支上能列出并执行；待移植表示实现已在本地版本里，但分支上还没有对应命令。"
    else:
        title = "Fork tool migration status"
        intro = (
            f"This repository owns {len(FORK_TOOLS)} tools. {grafted} is attached to the new base and "
            f"{len(FORK_TOOLS) - grafted} are still queued. None of them change base behaviour; they append commands through the fork registry."
        )
        legend = "Grafted means the branch lists and runs it. Pending means the implementation exists in the local version but the branch has no command yet."
    out = [
        f"# {title}",
        "",
        intro,
        "",
        f"| {labels['tools']} | {labels['origin']} | {labels['fork_status']} |",
        "| --- | --- | --- |",
    ]
    for name, item in FORK_TOOLS.items():
        state = labels["grafted"] if item["status"] == "grafted" else labels["pending"]
        style = "ok" if item["status"] == "grafted" else "no"
        page = f"[{item[lang]}]({name}.md)" if name in names else item[lang]
        out.append(
            f"| {page}<br>`{name}` | {labels['fork_origin']} | "
            f'<span class="state {style}">{state}</span> |'
        )
    out += ["", legend, ""]
    for name, item in FORK_TOOLS.items():
        if name in names:
            continue
        out += [
            f"## {item[lang]} {{#{name.replace('_', '-')}}}",
            "",
            f"`{name}` — {item[f'{lang}_note']}",
            "",
        ]
    out += ["---", "", f"[{labels['back']}](index.md)", ""]
    return "\n".join(out)


def nav_block(tools: list[dict]) -> str:
    groups = {}
    for tool in sorted(tools, key=sort_key):
        groups.setdefault(tool["toolset"], []).append(tool)
    lines = [NAV_START, "  - 新版基座:", "      - platform/index.md"]
    lines.append("      - 自研工具的移植状态: platform/fork-tools.md")
    for key, members in groups.items():
        lines.append(f"      - {GROUP_LABELS['zh'][key]}:")
        lines.extend(f"          - platform/{t['name']}.md" for t in members)
    lines.append(NAV_END)
    return "\n".join(lines)


def generate() -> dict[Path, str]:
    tools, released = load_platform()
    released_names = {tool["name"] for tool in released}
    files: dict[Path, str] = {}
    for lang, suffix in (("zh", ""), ("en", ".en")):
        files[PAGES / f"index{suffix}.md"] = index_page(tools, released, lang)
        files[PAGES / f"fork-tools{suffix}.md"] = fork_page(tools, lang)
        for tool in tools:
            files[PAGES / f"{tool['name']}{suffix}.md"] = tool_page(
                tool, released_names, lang
            )
    return files
