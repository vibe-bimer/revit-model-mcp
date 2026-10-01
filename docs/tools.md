# 只读工具参考

所有工具都支持本地、SSH 和 HTTP 传输。它们不改变模型；两个导出工具会写入文件。

<a id="transports-and-output-files"></a>
## 传输与输出文件

HTTP 模式下，`revit_export_view` 通过 `/views/{name}/image` 下载 PNG。
`revit_export_element_ids` 在 Revit 工作站写入工作簿，因此 `save_to` 是工作站路径；HTTP 客户端读取返回的 `path`，而不是下载文件。
标识符列保存 Revit 构件 ID，API 不能指定这个 ID：该工具仅列出标识符，从不更改它们。
HTTP 模式下，`revit_list_instances` 报告所连接的 Revit 进程。

<a id="common-arguments-and-tool-catalogue"></a>
## 通用参数与工具目录

除 `revit_export_view` 和 `revit_list_instances` 外，每个只读工具都接受 `timeout_seconds=120`、`pickup_timeout_seconds=300` 和 `document=null`。
超时以正整数秒计；接单超时只适用于本地和 SSH 传输，在 HTTP 模式下忽略。
`revit_export_view` 使用默认的 120 秒响应等待和 300 秒接单等待预算，不提供超时参数。
有多个 Revit 实例运行时，应通过活动文档标题或文件名中唯一的子串指定 `document`；否则任意实例都可能响应。
`revit_list_instances(document=null)` 列出所有实例；文档筛选返回所有匹配实例，而不是从中选择一个。
表中未列出默认值的参数是必填参数。
聚合与查询共用筛选参数 `categories`、`family`、`type_name`、`level`、`view`、`workset`、`phase`、`area_scheme` 和 `parameter_filters`；它们的默认值均为 `null`。

| 工具 | 除通用只读选项外的参数 | 用途 |
| --- | --- | --- |
| `revit_ping` | 无 | 检查连接；返回 `data:"pong"`。 |
| `revit_document_info` | 无 | 读取文档、标高、面积方案和工作集。 |
| `revit_list_catalog` | `section` | 发现可用的类别、族、视图和参数名称。 |
| `revit_aggregate_elements` | `group_by`、`sum_field=null`、共用查询筛选参数 | 按一个或两个字段分组；返回数量，以及可选的合计／平均值。 |
| `revit_query_elements` | 共用查询筛选参数、`fields=null`、`offset=0`、`limit=100`、`sort_field="id"`、`sort_direction="asc"`、`include_geometry=false` | 分页读取匹配构件。 |
| `revit_list_views` | `view_type=null`、`name_contains=null` | 查找活动文档中的视图。 |
| `revit_view_summary` | `view` | 读取视图元数据与各类别数量。 |
| `revit_export_view` | `view`、`pixel_size=1600`、`save_to=null`、`document=null`；无超时参数 | 下载 PNG；`pixel_size` 指图像适配方向的尺寸，范围为 1–4000 像素。 |
| `revit_export_element_ids` | `fields=null`、`save_to=null`、`timeout_seconds=120`、`pickup_timeout_seconds=300`、`document=null` | 将已绘制构件的标识符清单写入 Revit 工作站上的 xlsx 工作簿，按类别、族、类型排序。 |
| `revit_view_elements` | `view`、`categories=null`、`offset=0`、`limit=100` | 分页读取视图中的构件。 |
| `revit_element_details` | `element_id` | 按无单位的 Revit ID 读取实例／类型参数和几何。 |
| `revit_view_warnings` | `view` | 读取涉及视图中构件的警告。 |
| `revit_list_warnings` | `warning_text=null`、`include_elements=false` | 对警告分组，或检查特定警告组。 |
| `revit_list_relations` | `relation`、`source_id=null`、`source_name=null` | 读取成员关系或依赖。 |
| `revit_list_instances` | `document=null`；无超时参数 | 列出端点或心跳信息。 |
| `revit_model_health` | 无 | 交付前读取模型质量统计和高频警告。 |
| `revit_links_status` | 无 | 读取 RVT、CAD 和图像的状态、路径及实例数量。 |
| `revit_shared_coordinates` | 无 | 读取项目基点／测量点、场地和链接变换，单位为 mm 和度。 |
| `revit_parameter_fill_check` | `categories`、`parameters`、`level=null`、`workset=null`、`view=null`、`sample_limit=20`、`include_types=true` | 统计已填、空值和缺失参数；抽样返回无单位的构件 ID。 |

<a id="coordinator-checks"></a>
## 协调检查

导出或交付前依次调用 `revit_model_health` → `revit_links_status` → `revit_shared_coordinates` → `revit_parameter_fill_check(categories=["Walls","Doors"], parameters=["Mark","Comments"])`。
类别和参数名称使用模型语言；填充检查接受 1–20 个类别、1–30 个参数，抽样上限范围为 1–100。
协调检查的位置和链接列表最多返回 100 项，不分页；位置按名称排序，链接按 ID 排序。
只要报告类型的任一实例符合条件，`pinned` 和 `viewSpecific` 就分别为 true。
参数名通过 `LookupParameter(name)` 解析，使用第一个同名匹配；不支持按 GUID 或 BuiltInParameter 选择。

<a id="filters-units-and-pagination"></a>
## 筛选、单位与分页

进行通用模型查询前先调用 `revit_list_catalog`；数量与分类汇总优先使用 `revit_aggregate_elements`，需要逐个构件记录时才使用 `revit_query_elements`。
偏移量是从零开始的行数；每页上限是正整数行数。只要 `hasMore=true`，就继续推进 offset。
提供公制字段时，长度使用 mm，面积使用 m2，体积使用 m3。
其他数值筛选值遵循文档显示单位；返回的查询值在可用时带有 `unit` 字段。
筛选输入与数值输出的区别见[通道格式](feed-format.md#jobs)。
参数名来自模型语言；筛选前使用 `revit_list_catalog(section="parameters")`。
查询参数筛选以 AND 组合，使用准确的本地化名称。支持 `equals`、`contains`、`greater`、`less`、`empty`、`not-empty` 和 `exists`；`contains` 要求文本，`empty`／`not-empty`／`exists` 不需要 value。
汇总面积时，应按标高分组并指定面积方案。

<a id="export-destinations"></a>
## 导出路径

对于 `revit_export_view`，`save_to` 是 MCP 客户端上的新 PNG 文件路径；默认下载到本地临时目录，返回 `localPath`、图像宽高、`sizeBytes` 和视图元数据，不返回 base64。
对于 `revit_export_element_ids`，`save_to` 是 Revit 工作站上的绝对 `.xlsx` 路径。默认路径为 `Documents\RevitModelMcp\Exports\构件ID清单_<model>_<timestamp>.xlsx`；响应返回 `path`、`fileName`、`sheetName`、`columns`、`rowCount`、`totalCandidates`、`truncated`、`sizeBytes` 和 `categoryCounts`。
两种导出都不覆盖已有目标文件。工作簿最多 50,000 行；候选构件更多时，`truncated=true`。
默认列为 `类别`、`族`、`类型`、`标高`、`构件ID`、`名称`、`工作集`；`fields` 可用内置字段名或参数名替换这些列。
没有标高的构件，其标高列为空，包括大多数 MEP 管道和风管段。
导出视图不会切换活动视图，也不写入模型。

<a id="geometry"></a>
## 几何

`revit_element_details` 在 `data` 中随参数返回几何。
`revit_query_elements(include_geometry=True)` 在返回页面的每个构件中添加相同字段。
该查询开关默认为 `False`；默认查询省略几何。
所有坐标使用模型轴，以毫米计，保留一位小数。

| 字段 | 内容 |
| --- | --- |
| `location` | 点：`type:"point"`、`xMm`、`yMm`、`zMm`。曲线：`type:"curve"`、`startMm`、`endMm`、`lengthMm`。 |
| `boundingBox` | 来自构件模型包围盒的 `minMm`、`maxMm`、`centerMm`，均为 `[x,y,z]` 数组。房间使用自己的包围盒。 |
| `roomCenterMm` | 已放置房间的位置 `[x,y,z]`。在房间内放置物体时使用 `roomCenterMm`。包围盒中心可能位于非矩形房间之外。 |

不可用的几何字段省略。
