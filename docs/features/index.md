# 功能总览

<p class="facts">19 个读取 + 14 个动作，共 33 个工具</p>

## 按版本进入

| 年份 | 状态 |
| --- | --- |
| [Revit 2020](v2020.md) | <span class="state ok">已实测</span> |
| [Revit 2026](v2026.md) | <span class="state ok">已实测</span> <span class="state part">仅构建</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建</span> |

## 全部工具

### 连接与文档（3）

| 工具 | 一句话 | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_ping](revit_ping.md) | 检查连接与插件版本 | ✅ | ✅ |
| [revit_document_info](revit_document_info.md) | 当前文档概要：文件名、Revit 版本、标高、面积方案、工作集、视图数 | ✅ | ✅ |
| [revit_list_instances](revit_list_instances.md) | 列出在跑的 Revit 实例及其打开的文档 | ✅ | ✅ |

### 查询与统计（5）

| 工具 | 一句话 | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_list_catalog](revit_list_catalog.md) | 查可用名字：类别、族类型、标高、面积方案、视图、工作集、阶段、参数 | ✅ | ✅ |
| [revit_aggregate_elements](revit_aggregate_elements.md) | 按 1–2 个字段分组统计数量，可附加求和与平均（mm / m² / m³） | ✅ | ✅ |
| [revit_query_elements](revit_query_elements.md) | 按类别/族/类型/标高/视图/工作集/参数过滤，分页读取构件明细 | ✅ | ✅ |
| [revit_element_details](revit_element_details.md) | 单个构件的实例参数、类型参数与几何（mm） | ✅ | ✅ |
| [revit_list_relations](revit_list_relations.md) | 关系查询：标高的房间、面积方案成员、组内构件、嵌套族、视图样板依赖 | ✅ | ✅ |

### 视图与截图（5）

| 工具 | 一句话 | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_list_views](revit_list_views.md) | 列出视图，可按视图类型与名称过滤 | ✅ | ✅ |
| [revit_view_summary](revit_view_summary.md) | 视图元数据 + 类别计数（各有多少、多少种类型） | ✅ | ✅ |
| [revit_export_view](revit_export_view.md) | 把视图导出成 PNG 图片（1–4000 像素） | ✅ | ✅ |
| [revit_view_elements](revit_view_elements.md) | 分页读取视图中的构件（可按类别过滤） | ✅ | ✅ |
| [revit_view_warnings](revit_view_warnings.md) | 只读该视图相关元素的警告 | ✅ | ✅ |

### 导出与检验（6）

| 工具 | 一句话 | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_model_health](revit_model_health.md) | 交付前体检：文件大小、各类计数、单位设置、数量最多的警告 | ✅ | ✅ |
| [revit_links_status](revit_links_status.md) | RVT / CAD / 图片链接的状态、路径与实例数 | ✅ | ✅ |
| [revit_shared_coordinates](revit_shared_coordinates.md) | 项目基点、测量点、场地与链接的位移（mm）/旋转（°） | ✅ | ✅ |
| [revit_parameter_fill_check](revit_parameter_fill_check.md) | 参数的填充率：有值 / 空 / 缺失，并给出抽样 ID | ✅ | ✅ |
| [revit_export_element_ids](revit_export_element_ids.md) | 把可见构件的 ID 清单写成 Excel（类别/族/类型/标高/构件ID/名称/工作集） | ✅ | ✅ |
| [revit_list_warnings](revit_list_warnings.md) | 全模型警告按文本分组，可展开受影响构件 | ✅ | ✅ |

### 选中与显示（3）

| 工具 | 一句话 | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_select](revit_select.md) | 在 Revit 里选中指定构件（空列表=清除选择） | ✅ | ✅ |
| [revit_show](revit_show.md) | 在视图里定位/高亮构件，必要时打开对应视图 | ✅ | ✅ |
| [revit_isolate](revit_isolate.md) | 临时隔离显示（reset=true 恢复） | ✅ | ✅ |

### 编辑（6）

| 工具 | 一句话 | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_move](revit_move.md) | 按模型轴平移构件（mm） | ✅ | ✅ |
| [revit_place_family](revit_place_family.md) | 在指定标高放置已载入的族实例，可绕 Z 旋转 | ✅ | 🟡 |
| [revit_create_wall](revit_create_wall.md) | 按两点建直墙（mm，指定标高、墙类型、高度） | ✅ | ✅ |
| [revit_create_floor](revit_create_floor.md) | 按闭合轮廓建楼板（至少 3 个顶点，mm） | ✅ | 🟡 |
| [revit_set_parameter](revit_set_parameter.md) | 按参数名写值（长度 mm、面积 m²，其余按内部单位） | ✅ | ✅ |
| [revit_delete](revit_delete.md) | 删除构件及其依赖 | ✅ | ✅ |

### 阶段（2）

| 工具 | 一句话 | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_set_phase](revit_set_phase.md) | 赋创建阶段 / 拆除阶段（空串清除，null 不变） | ✅ | 🟡 |
| [revit_merge_phases](revit_merge_phases.md) | 把一个阶段的引用并入另一个阶段并删除空阶段 | ✅ | 🟡 |

### 批量与 ID（3）

| 工具 | 一句话 | 2020 | 2026 |
| --- | --- | :--: | :--: |
| [revit_reset_element_ids](revit_reset_element_ids.md) | 同文档内换 ID：只对无宿主、无依赖的独立构件有效 | ✅ | 🟡 |
| [revit_rebuild_model_ids](revit_rebuild_model_ids.md) | 整模型换新 ID：把三维视图可选中的构件重建为一份或多份新模型 | ✅ | 🟡 |
| [revit_batch](revit_batch.md) | 1–50 步动作合并成一次撤销（revit_batch） | ✅ | ✅ |

!!! warning "写入门禁：客户端 REVIT_MCP_ALLOW_WRITE=1 + 工作站 allow-write 文件，且只有一个 Revit 实例"
