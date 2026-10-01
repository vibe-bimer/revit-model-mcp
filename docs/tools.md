# 读取工具（19）

<p class="facts">完整契约见英文页 <a href="../tools.en.md">tools.en.md</a>　逐工具的中文说明见 <a href="features/index.md">功能总览</a></p>

| 工具 | 一句话 | 参数个数 | 起始版本 |
| --- | --- | :--: | --- |
| `revit_ping` | [检查连接与插件版本](features/revit_ping.md) | 3 | 0.1.0 |
| `revit_document_info` | [当前文档概要：文件名、Revit 版本、标高、面积方案、工作集、视图数](features/revit_document_info.md) | 3 | 0.1.0 |
| `revit_model_health` | [交付前体检：文件大小、各类计数、单位设置、数量最多的警告](features/revit_model_health.md) | 3 | 0.5.0 |
| `revit_links_status` | [RVT / CAD / 图片链接的状态、路径与实例数](features/revit_links_status.md) | 3 | 0.5.0 |
| `revit_shared_coordinates` | [项目基点、测量点、场地与链接的位移（mm）/旋转（°）](features/revit_shared_coordinates.md) | 3 | 0.6.0 |
| `revit_parameter_fill_check` | [参数的填充率：有值 / 空 / 缺失，并给出抽样 ID](features/revit_parameter_fill_check.md) | 10 | 0.6.0 |
| `revit_list_catalog` | [查可用名字：类别、族类型、标高、面积方案、视图、工作集、阶段、参数](features/revit_list_catalog.md) | 4 | 0.1.0 |
| `revit_aggregate_elements` | [按 1–2 个字段分组统计数量，可附加求和与平均（mm / m² / m³）](features/revit_aggregate_elements.md) | 14 | 0.1.0 |
| `revit_query_elements` | [按类别/族/类型/标高/视图/工作集/参数过滤，分页读取构件明细](features/revit_query_elements.md) | 18 | 0.1.0 |
| `revit_list_views` | [列出视图，可按视图类型与名称过滤](features/revit_list_views.md) | 5 | 0.1.0 |
| `revit_view_summary` | [视图元数据 + 类别计数（各有多少、多少种类型）](features/revit_view_summary.md) | 4 | 0.1.0 |
| `revit_export_view` | [把视图导出成 PNG 图片（1–4000 像素）](features/revit_export_view.md) | 4 | 0.3.0 |
| `revit_export_element_ids` | [把可见构件的 ID 清单写成 Excel（类别/族/类型/标高/构件ID/名称/工作集）](features/revit_export_element_ids.md) | 5 | 0.8.0 |
| `revit_view_elements` | [分页读取视图中的构件（可按类别过滤）](features/revit_view_elements.md) | 7 | 0.2.0 |
| `revit_element_details` | [单个构件的实例参数、类型参数与几何（mm）](features/revit_element_details.md) | 4 | 0.1.0 |
| `revit_view_warnings` | [只读该视图相关元素的警告](features/revit_view_warnings.md) | 4 | 0.4.0 |
| `revit_list_warnings` | [全模型警告按文本分组，可展开受影响构件](features/revit_list_warnings.md) | 5 | 0.4.0 |
| `revit_list_relations` | [关系查询：标高的房间、面积方案成员、组内构件、嵌套族、视图样板依赖](features/revit_list_relations.md) | 6 | 0.7.0 |
| `revit_list_instances` | [列出在跑的 Revit 实例及其打开的文档](features/revit_list_instances.md) | 1 | 0.6.0 |
