# 功能总览

19 个读取 + 15 个动作，共 34 个工具

## 按 Revit 年份查阅 {#by-version}

| Revit 年份 | 验证状态 |
| --- | --- |
| [Revit 2020](v2020.md) | 读取 19/19、动作 15/15 已实测；其余仅构建 |
| [Revit 2026](v2026.md) | 读取 18/19、动作 8/15 已实测；其余仅构建 |
| 2022–2025 / 2027 | 仅构建，未实测 |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

## 全部功能 {#all-features}

### 连接与文档 (3) {#group-connection}

| 工具 | 用途 |
| --- | --- |
| [检查连接](revit_ping.md)<br>`revit_ping` | 检查连接与插件版本 |
| [文档概要](revit_document_info.md)<br>`revit_document_info` | 当前文档概要：文件名、Revit 版本、标高、面积方案、工作集、视图数 |
| [Revit 实例列表](revit_list_instances.md)<br>`revit_list_instances` | 列出在跑的 Revit 实例及其打开的文档 |

### 查询与统计 (5) {#group-query}

| 工具 | 用途 |
| --- | --- |
| [名称目录](revit_list_catalog.md)<br>`revit_list_catalog` | 查可用名字：类别、族类型、标高、面积方案、视图、工作集、阶段、参数 |
| [分组统计](revit_aggregate_elements.md)<br>`revit_aggregate_elements` | 按 1–2 个字段分组统计数量，可附加求和与平均（mm / m² / m³） |
| [构件查询](revit_query_elements.md)<br>`revit_query_elements` | 按类别/族/类型/标高/视图/工作集/参数过滤，分页读取构件明细 |
| [构件参数与几何](revit_element_details.md)<br>`revit_element_details` | 单个构件的实例参数、类型参数与几何（mm） |
| [构件关系](revit_list_relations.md)<br>`revit_list_relations` | 关系查询：标高的房间、面积方案成员、组内构件、嵌套族、视图样板依赖 |

### 视图与截图 (6) {#group-views}

| 工具 | 用途 |
| --- | --- |
| [视图目录](revit_list_views.md)<br>`revit_list_views` | 列出视图，可按视图类型与名称过滤 |
| [视图统计](revit_view_summary.md)<br>`revit_view_summary` | 视图元数据 + 类别计数（各有多少、多少种类型） |
| [导出视图图片](revit_export_view.md)<br>`revit_export_view` | 把视图导出成 PNG 图片（1–4000 像素） |
| [视图构件明细](revit_view_elements.md)<br>`revit_view_elements` | 分页读取视图中的构件（可按类别过滤） |
| [视图相关警告](revit_view_warnings.md)<br>`revit_view_warnings` | 只读该视图相关元素的警告 |
| [设置视图光照](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | 设置视图的阴影、太阳位置与强度、地面平面、背景和渲染光源方案 |

### 导出与检验 (6) {#group-export}

| 工具 | 用途 |
| --- | --- |
| [模型检查](revit_model_health.md)<br>`revit_model_health` | 交付前体检：文件大小、各类计数、单位设置、数量最多的警告 |
| [链接状态](revit_links_status.md)<br>`revit_links_status` | RVT / CAD / 图片链接的状态、路径与实例数 |
| [共享坐标](revit_shared_coordinates.md)<br>`revit_shared_coordinates` | 项目基点、测量点、场地与链接的位移（mm）/旋转（°） |
| [参数填充检查](revit_parameter_fill_check.md)<br>`revit_parameter_fill_check` | 参数的填充率：有值 / 空 / 缺失，并给出抽样 ID |
| [导出构件 ID 清单](revit_export_element_ids.md)<br>`revit_export_element_ids` | 把模型中已绘制构件的 ID 清单写成 Excel（类别/族/类型/标高/构件ID/名称/工作集） |
| [模型警告](revit_list_warnings.md)<br>`revit_list_warnings` | 全模型警告按文本分组，可展开受影响构件 |

### 选中与显示 (3) {#group-display}

| 工具 | 用途 |
| --- | --- |
| [选择构件](revit_select.md)<br>`revit_select` | 在 Revit 里选中指定构件（空列表=清除选择） |
| [定位显示构件](revit_show.md)<br>`revit_show` | 在视图里定位/高亮构件，必要时打开对应视图 |
| [临时隔离显示](revit_isolate.md)<br>`revit_isolate` | 临时隔离显示（reset=true 恢复） |

### 编辑 (6) {#group-edit}

| 工具 | 用途 |
| --- | --- |
| [移动构件](revit_move.md)<br>`revit_move` | 按模型轴平移构件（mm） |
| [放置非宿主族](revit_place_family.md)<br>`revit_place_family` | 在指定标高放置已载入的非宿主族实例，可绕 Z 旋转 |
| [创建直墙](revit_create_wall.md)<br>`revit_create_wall` | 按两点建直墙（mm，指定标高、墙类型、高度） |
| [创建楼板](revit_create_floor.md)<br>`revit_create_floor` | 按闭合轮廓建楼板（至少 3 个顶点，mm） |
| [修改参数](revit_set_parameter.md)<br>`revit_set_parameter` | 按参数名写值（长度 mm、面积 m²，其余按内部单位） |
| [删除构件](revit_delete.md)<br>`revit_delete` | 删除构件及其依赖 |

### 阶段 (2) {#group-phases}

| 工具 | 用途 |
| --- | --- |
| [设置构件阶段](revit_set_phase.md)<br>`revit_set_phase` | 赋创建阶段 / 拆除阶段（空串清除，null 不变） |
| [合并项目阶段](revit_merge_phases.md)<br>`revit_merge_phases` | 把一个阶段的引用并入另一个阶段并删除空阶段 |

### 批量与 ID (3) {#group-ids}

| 工具 | 用途 |
| --- | --- |
| [同文档替换 ID](revit_reset_element_ids.md)<br>`revit_reset_element_ids` | 同文档内换 ID：只对无宿主、无依赖的独立构件有效 |
| [新模型重建 ID](revit_rebuild_model_ids.md)<br>`revit_rebuild_model_ids` | 整模型换新 ID：把三维视图可选中的构件重建为一份或多份新模型 |
| [批量动作](revit_batch.md)<br>`revit_batch` | 1–50 步动作合并成一次撤销（revit_batch） |

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。
