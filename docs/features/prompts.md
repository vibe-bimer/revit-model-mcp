# 提示词库

19 个读取 + 15 个动作，共 34 个工具

客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

## 连接与文档 {#group-connection}

### [检查连接](revit_ping.md)

`revit_ping` — 检查连接与插件版本

```text
看看 Revit 插件在不在线
```

### [文档概要](revit_document_info.md)

`revit_document_info` — 当前文档概要：文件名、Revit 版本、标高、面积方案、工作集、视图数

```text
当前打开的是哪个模型？有哪些标高？
```

### [Revit 实例列表](revit_list_instances.md)

`revit_list_instances` — 列出在跑的 Revit 实例及其打开的文档

```text
现在有几个 Revit 实例？各自打开什么模型？
```

## 查询与统计 {#group-query}

### [名称目录](revit_list_catalog.md)

`revit_list_catalog` — 查可用名字：类别、族类型、标高、面积方案、视图、工作集、阶段、参数

```text
列出这个模型里所有可用的参数名
```

### [分组统计](revit_aggregate_elements.md)

`revit_aggregate_elements` — 按 1–2 个字段分组统计数量，可附加求和与平均（mm / m² / m³）

```text
统计 1F 上各种墙类型各有多少个
```

```text
按标高统计门的数量和总宽度
```

### [构件查询](revit_query_elements.md)

`revit_query_elements` — 按类别/族/类型/标高/视图/工作集/参数过滤，分页读取构件明细

```text
列出 2F 上所有没填防火等级的门，给出 ID
```

### [构件参数与几何](revit_element_details.md)

`revit_element_details` — 单个构件的实例参数、类型参数与几何（mm）

```text
把 ID 357640 的构件参数和几何都读出来
```

### [构件关系](revit_list_relations.md)

`revit_list_relations` — 关系查询：标高的房间、面积方案成员、组内构件、嵌套族、视图样板依赖

```text
1F 标高上都有哪些房间？
```

## 视图与截图 {#group-views}

### [视图目录](revit_list_views.md)

`revit_list_views` — 列出视图，可按视图类型与名称过滤

```text
列出所有平面视图
```

### [视图统计](revit_view_summary.md)

`revit_view_summary` — 视图元数据 + 类别计数（各有多少、多少种类型）

```text
三维视图里各类构件分别有多少个？
```

### [导出视图图片](revit_export_view.md)

`revit_export_view` — 把视图导出成 PNG 图片（1–4000 像素）

```text
把 1F 平面导出成 PNG，宽度 2000 像素
```

### [视图构件明细](revit_view_elements.md)

`revit_view_elements` — 分页读取视图中的构件（可按类别过滤）

```text
把三维视图里的构件列表给我，每页 200 条
```

### [视图相关警告](revit_view_warnings.md)

`revit_view_warnings` — 只读该视图相关元素的警告

```text
这个视图里有哪些警告？
```

### [设置视图光照](revit_set_view_lighting.md)

`revit_set_view_lighting` — 设置视图的阴影、太阳位置与强度、地面平面、背景和渲染光源方案

```text
把三维视图的阴影打开，阴影浓度 60，背景换成天空，渲染光源用室外阳光
```

```text
把 {3D} 的太阳设成 2026-06-21 15:00，阳光强度 80，先彩排一次
```

```text
用光照模式把太阳固定在方位角 135°、高度角 45°，并打开标高 01 的地面平面
```

## 导出与检验 {#group-export}

### [模型检查](revit_model_health.md)

`revit_model_health` — 交付前体检：文件大小、各类计数、单位设置、数量最多的警告

```text
做一次交付前体检：文件大小、各类数量、单位设置、最多的警告
```

### [链接状态](revit_links_status.md)

`revit_links_status` — RVT / CAD / 图片链接的状态、路径与实例数

```text
检查所有链接是否正常
```

### [共享坐标](revit_shared_coordinates.md)

`revit_shared_coordinates` — 项目基点、测量点、场地与链接的位移（mm）/旋转（°）

```text
报告项目的共享坐标和链接位移
```

### [参数填充检查](revit_parameter_fill_check.md)

`revit_parameter_fill_check` — 参数的填充率：有值 / 空 / 缺失，并给出抽样 ID

```text
检查墙的防火等级填充率，给出空值的构件 ID
```

### [导出构件 ID 清单](revit_export_element_ids.md)

`revit_export_element_ids` — 把模型中已绘制构件的 ID 清单写成 Excel（类别/族/类型/标高/构件ID/名称/工作集）

```text
把模型中已绘制构件的 ID 清单导出成 Excel，按类别、族、类型排序
```

### [模型警告](revit_list_warnings.md)

`revit_list_warnings` — 全模型警告按文本分组，可展开受影响构件

```text
列出数量最多的警告
```

## 选中与显示 {#group-display}

### [选择构件](revit_select.md)

`revit_select` — 在 Revit 里选中指定构件（空列表=清除选择）

```text
选中 ID 为 123456 的构件
```

### [定位显示构件](revit_show.md)

`revit_show` — 在视图里定位/高亮构件，必要时打开对应视图

```text
把这几根柱子显示给我看
```

### [临时隔离显示](revit_isolate.md)

`revit_isolate` — 临时隔离显示（reset=true 恢复）

```text
只显示这一层的窗
```

## 编辑 {#group-edit}

### [移动构件](revit_move.md)

`revit_move` — 按模型轴平移构件（mm）

```text
把这 3 个构件沿 X 移动 500 mm，先彩排
```

### [放置非宿主族](revit_place_family.md)

`revit_place_family` — 在指定标高放置已载入的非宿主族实例，可绕 Z 旋转

```text
用已载入的非宿主家具族，在 1F 的 (3000, 4000) 放置一个实例，先彩排
```

### [创建直墙](revit_create_wall.md)

`revit_create_wall` — 按两点建直墙（mm，指定标高、墙类型、高度）

```text
在 1F 从 (0,0) 到 (6000,0) 建一道 200mm 墙
```

### [创建楼板](revit_create_floor.md)

`revit_create_floor` — 按闭合轮廓建楼板（至少 3 个顶点，mm）

```text
用这四个点在 2F 建一块楼板
```

### [修改参数](revit_set_parameter.md)

`revit_set_parameter` — 按参数名写值（长度 mm、面积 m²，其余按内部单位）

```text
把这些墙的防火等级改成 2 小时
```

### [删除构件](revit_delete.md)

`revit_delete` — 删除构件及其依赖

```text
删掉这两个构件，先彩排
```

## 阶段 {#group-phases}

### [设置构件阶段](revit_set_phase.md)

`revit_set_phase` — 赋创建阶段 / 拆除阶段（空串清除，null 不变）

```text
把这些构件标成在“现有”阶段拆除
```

### [合并项目阶段](revit_merge_phases.md)

`revit_merge_phases` — 把一个阶段的引用并入另一个阶段并删除空阶段

```text
把“阶段 1”合并进“新构造”
```

## 批量与 ID {#group-ids}

### [同文档替换 ID](revit_reset_element_ids.md)

`revit_reset_element_ids` — 同文档内换 ID：只对无宿主、无依赖的独立构件有效

```text
给选中的这 27 个独立构件换新 ID
```

### [新模型重建 ID](revit_rebuild_model_ids.md)

`revit_rebuild_model_ids` — 整模型换新 ID：把三维视图可选中的构件重建为一份或多份新模型

```text
把当前三维视图里能选中的构件重建到 E:\out\copy-{n}.rvt，出 10 份，每份 ID 都不要重复
```

```text
先彩排一次重建，告诉我多少个构件、新 ID 范围，先不要写文件
```

### [批量动作](revit_batch.md)

`revit_batch` — 1–50 步动作合并成一次撤销（revit_batch）

```text
把这 10 个构件一起移动并改参数，做成一次撤销
```

```text
把这一批修改先用 dry_run 演示一遍
```
