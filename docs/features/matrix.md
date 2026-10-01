# 版本支持矩阵

<p class="facts">✅ 已实测　🟡 仅构建</p>

## 读取工具（19）

| 工具 | 2020 | 2026 | 其它年份 | 备注 |
| --- | :--: | :--: | :--: | --- |
| [revit_ping](revit_ping.md) | ✅ | ✅ | 🟡 | 检查连接与插件版本 |
| [revit_document_info](revit_document_info.md) | ✅ | ✅ | 🟡 | 当前文档概要：文件名、Revit 版本、标高、面积方案、工作集、视图数 |
| [revit_model_health](revit_model_health.md) | ✅ | ✅ | 🟡 | 交付前体检：文件大小、各类计数、单位设置、数量最多的警告 |
| [revit_links_status](revit_links_status.md) | ✅ | ✅ | 🟡 | RVT / CAD / 图片链接的状态、路径与实例数 |
| [revit_shared_coordinates](revit_shared_coordinates.md) | ✅ | ✅ | 🟡 | 项目基点、测量点、场地与链接的位移（mm）/旋转（°） |
| [revit_parameter_fill_check](revit_parameter_fill_check.md) | ✅ | ✅ | 🟡 | 参数的填充率：有值 / 空 / 缺失，并给出抽样 ID |
| [revit_list_catalog](revit_list_catalog.md) | ✅ | ✅ | 🟡 | 查询与过滤都用这些名字 |
| [revit_aggregate_elements](revit_aggregate_elements.md) | ✅ | ✅ | 🟡 | 回答“有多少”的首选，比逐条取明细快得多 |
| [revit_query_elements](revit_query_elements.md) | ✅ | ✅ | 🟡 | 按类别/族/类型/标高/视图/工作集/参数过滤，分页读取构件明细 |
| [revit_list_views](revit_list_views.md) | ✅ | ✅ | 🟡 | 列出视图，可按视图类型与名称过滤 |
| [revit_view_summary](revit_view_summary.md) | ✅ | ✅ | 🟡 | 视图元数据 + 类别计数（各有多少、多少种类型） |
| [revit_export_view](revit_export_view.md) | ✅ | ✅ | 🟡 | 把视图导出成 PNG 图片（1–4000 像素） |
| [revit_export_element_ids](revit_export_element_ids.md) | ✅ | ✅ | 🟡 | 文件写到 Revit 工作站上 |
| [revit_view_elements](revit_view_elements.md) | ✅ | ✅ | 🟡 | 分页读取视图中的构件（可按类别过滤） |
| [revit_element_details](revit_element_details.md) | ✅ | ✅ | 🟡 | 房间还会返回面积、体积与边界 |
| [revit_view_warnings](revit_view_warnings.md) | ✅ | ✅ | 🟡 | 只读该视图相关元素的警告 |
| [revit_list_warnings](revit_list_warnings.md) | ✅ | ✅ | 🟡 | 全模型警告按文本分组，可展开受影响构件 |
| [revit_list_relations](revit_list_relations.md) | ✅ | ✅ | 🟡 | 关系查询：标高的房间、面积方案成员、组内构件、嵌套族、视图样板依赖 |
| [revit_list_instances](revit_list_instances.md) | ✅ | ✅ | 🟡 | 列出在跑的 Revit 实例及其打开的文档 |

## 动作工具（14）

| 工具 | 2020 | 2026 | 其它年份 | 备注 |
| --- | :--: | :--: | :--: | --- |
| [revit_select](revit_select.md) | ✅ | ✅ | 🟡 | 不改模型 |
| [revit_show](revit_show.md) | ✅ | ✅ | 🟡 | 不改模型 |
| [revit_isolate](revit_isolate.md) | ✅ | ✅ | 🟡 | 临时效果，不写模型 |
| [revit_move](revit_move.md) | ✅ | ✅ | 🟡 | 支持 dry_run |
| [revit_place_family](revit_place_family.md) | ✅ | 🟡 | 🟡 | 2026 未真机验证 |
| [revit_create_wall](revit_create_wall.md) | ✅ | ✅ | 🟡 | 按两点建直墙（mm，指定标高、墙类型、高度） |
| [revit_create_floor](revit_create_floor.md) | ✅ | 🟡 | 🟡 | 2020 走 Document.Create.NewFloor，2022+ 走 Floor.Create |
| [revit_set_phase](revit_set_phase.md) | ✅ | 🟡 | 🟡 | 阶段顺序检查的 API 只在 2022+ ，2020 走兜底 |
| [revit_merge_phases](revit_merge_phases.md) | ✅ | 🟡 | 🟡 | 不可放进 batch |
| [revit_set_parameter](revit_set_parameter.md) | ✅ | ✅ | 🟡 | 支持 dry_run |
| [revit_delete](revit_delete.md) | ✅ | ✅ | 🟡 | 支持 dry_run |
| [revit_reset_element_ids](revit_reset_element_ids.md) | ✅ | 🟡 | 🟡 | 覆盖率有限：机电 27/1089、建筑 373/954、结构 0% |
| [revit_rebuild_model_ids](revit_rebuild_model_ids.md) | ✅ | 🟡 | 🟡 | 源模型只读；2020 实测每份 899 构件、ID 零重叠 |
| [revit_batch](revit_batch.md) | ✅ | ✅ | 🟡 | 首步失败整体回滚 |
