---
description: "可直接复制的提示词库，每个工具配有示例提示词与用途摘要。"
---

# 提示词库

35 个读取 + 52 个动作，共 87 个工具

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

### [界面状态](revit_ui_state.md)

`revit_ui_state` — 读取当前文档、打开的视图、选择集与所有打开的文档

```text
我现在选中了什么？还开了哪些视图？
```

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

### [查看视图信息](revit_view_info.md)

`revit_view_info` — 查看单个视图的模板、类别、工作集、过滤器与链接

```text
给我看看楼层平面视图 'Level 1' 的类别可见性、工作集和过滤器设置。
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

`revit_view_warnings` — 只读该视图相关构件的警告

```text
这个视图里有哪些警告？
```

### [激活视图](revit_activate_view.md)

`revit_activate_view` — 激活非样板视图，并按需缩放或框选构件

```text
打开 1F 平面并缩放到刚好放得下
```

### [关闭视图](revit_close_views.md)

`revit_close_views` — 关闭当前文档中打开的 UI 视图

```text
关闭除“L1 平面图”以外的所有打开视图。
```

### [设置视图可见性](revit_set_view_visibility.md)

`revit_set_view_visibility` — 改单个视图的类别、工作集与过滤器可见性，dry_run 可预览

```text
在平面视图 'A-101' 里隐藏 OST_StructuralColumns 类别，先用 dry_run 预览。
```

### [创建视图](revit_create_view.md)

`revit_create_view` — 创建平面、剖面、三维或详图视图；包围盒坐标为模型毫米

```text
创建一个名为"三层平面"的楼层平面视图，比例 1:100
```

### [复制视图](revit_duplicate_view.md)

`revit_duplicate_view` — 复制视图，可带详图，也可作为从属视图

```text
把 1F 平面复制一份带详图的副本
```

### [应用视图样板](revit_apply_view_template.md)

`revit_apply_view_template` — 将匹配的视图样板应用到一个或多个视图

```text
把“MEP 出图”视图样板应用到所有暖通平面视图。
```

### <span class="state part">自研</span> [设置视图光照](revit_set_view_lighting.md)

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

### [检查 NWC 导出设置](revit_nwc_settings_check.md)

`revit_nwc_settings_check` — 解析工作站上的 NWC 导出设置 XML，不实际导出

```text
帮我看看 Revit 工作站上 NWC 导出设置 XML 里配了什么，先别导出。
```

### [导出模型快照](revit_model_snapshot.md)

`revit_model_snapshot` — 读取 schema v1 项目快照用于批量审计（只读；关闭的工作集会使结果不完整）

```text
给当前项目导出一份模型快照，我要做批量审计。
```

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

### [模型警告](revit_list_warnings.md)

`revit_list_warnings` — 全模型警告按文本分组，可展开受影响构件

```text
列出数量最多的警告
```

### [导出模型文件](revit_export.md)

`revit_export` — 导出 PDF、DWG、IFC 或明细表 CSV，dry_run 返回计划文件名

```text
把视图 'A-101' 导出成 PDF 到 'C:\Out'，先用 dry_run 看计划文件名。
```

### [导出 Navisworks NWC](revit_export_nwc.md)

`revit_export_nwc` — 在 Revit 工作站导出 NWC，需装 Navisworks 导出器；覆盖已有文件需确认令牌

```text
把当前视图导出成 NWC 到 D:\\output\\塔楼.nwc，文件已存在就覆盖
```

### <span class="state part">自研</span> [导出构件 ID 清单](revit_export_element_ids.md)

`revit_export_element_ids` — 把模型中已绘制构件的 ID 清单写成 Excel（类别/族/类型/标高/构件ID/名称/工作集）

```text
把模型中已绘制构件的 ID 清单导出成 Excel，按类别、族、类型排序
```

### [生成快照报告](revit_build_report.md)

`revit_build_report` — 从快照本地生成 Excel 报告，无需连接 Revit

```text
把 snapshots 目录里的快照汇总成一份 Excel 报告
```

### [问题登记表](revit_issue_register.md)

`revit_issue_register` — 生成带构件快照的问题登记表 .xlsx，已存在的文件不覆盖

```text
把这 8 个问题整理成一份问题登记表 .xlsx
```

## 选中与显示 {#group-display}

### [构件截图](revit_capture_elements.md)

`revit_capture_elements` — 生成标记 1–500 个构件的 PNG 截图，临时视图会回滚

```text
把 1F 平面上这几根梁高亮截一张图，做问题记录用
```

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

### [着色构件](revit_override_graphics.md)

`revit_override_graphics` — 在指定视图里给构件着色，reset 可还原本次会话的覆盖

```text
把这几根柱子在 1F 平面涂成红色，其他构件调淡
```

### [标注构件](revit_tag_elements.md)

`revit_tag_elements` — 在视图里按类别或构件 ID 加标记，房间标记需平面视图

```text
给 1F 平面上所有门加上标记
```

## 编辑 {#group-edit}

### [执行 C# 代码](revit_execute_code.md)

`revit_execute_code` — 在 Revit 线程编译运行 C#，自动模式下自管一个事务与撤销记录

```text
跑一段 C#，把当前视图里所有墙的注释参数改成 Review
```

### [撤销上一步](revit_undo_last.md)

`revit_undo_last` — 通过 Revit 自带撤销命令撤销本会话上一步 MCP 操作，仅在目标文档激活且撤销记录匹配时执行

```text
撤销你刚才在活动文档里执行的最后一步操作。
```

### [移动构件](revit_move.md)

`revit_move` — 按模型轴平移构件（mm）

```text
把这 3 个构件沿 X 移动 500 mm，先彩排
```

### [旋转图元](revit_rotate.md)

`revit_rotate` — 绕 center_mm 竖直轴或包围盒中心旋转图元；dry_run 会回滚，成组、锁定等图元记入 skipped

```text
把选中的 3 根柱子绕原点旋转 30 度，先用 dry_run 预览结果。
```

### [复制构件](revit_copy.md)

`revit_copy` — 按毫米偏移复制 1 到 100 个构件，dry_run 会回滚

```text
把选中的墙沿 X 方向偏移 3000 毫米复制 5 份。
```

### [镜像图元](revit_mirror.md)

`revit_mirror` — 沿过 point_mm 的 X 或 Y 平行线镜像；dry_run 回滚，copy 保留原图元

```text
把选中的三面外墙沿过 (0, 0) 的 Y 轴平行线镜像，并保留原件
```

### [更换类型](revit_change_type.md)

`revit_change_type` — 把构件批量换成同一个兼容类型，成组构件会被跳过

```text
把这些墙换成 200mm 的混凝土墙
```

### [更新参数](revit_update_parameters.md)

`revit_update_parameters` — 按与 revit_query_elements 相同的筛选条件更新图元参数；成组成员记入 skipped，dry_run 可预测结果

```text
把一层所有墙的 Comments 参数改成“待检查”，先 dry_run 预览影响范围。
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

### [生成管线](revit_create_mep_run.md)

`revit_create_mep_run` — 按 mm 点串生成风管、水管、桥架或线管，并连成一段

```text
在 3F 上从这几个点拉一条 DN100 的水管
```

### [从 CAD 生成墙体](revit_walls_from_cad.md)

`revit_walls_from_cad` — 按 CAD 线段配对成墙并连接开口，尺寸单位为毫米

```text
用底图 'Level 1' 的 CAD 线生成基本墙体，高 3000 毫米并连接两端。
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

### [批量处理模型](revit_process_models.md)

`revit_process_models` — 在交互会话中逐个打开模型执行步骤和 C# 代码并按需导出保存；原地保存与代码需 confirm_token 确认

```text
批量打开 D:/models 下的模型，导出 PNG 并另存为新文件，不要原地保存。
```

### <span class="state part">自研</span> [创建标高](revit_create_level.md)

`revit_create_level` — 在指定高程新建标高（mm）

```text
在 15000mm 处建一个叫 4F 的标高
```

### <span class="state part">自研</span> [创建楼板](revit_create_floor.md)

`revit_create_floor` — 按闭合轮廓建楼板（至少 3 个顶点，mm）

```text
用这四个点在 2F 建一块楼板
```

## 阶段 {#group-phases}

### <span class="state part">自研</span> [设置构件阶段](revit_set_phase.md)

`revit_set_phase` — 赋创建阶段 / 拆除阶段（空串清除，null 不变）

```text
把这些构件标成在“现有”阶段拆除
```

### <span class="state part">自研</span> [合并项目阶段](revit_merge_phases.md)

`revit_merge_phases` — 把一个阶段的引用并入另一个阶段并删除空阶段

```text
把“阶段 1”合并进“新构造”
```

## 批量与 ID {#group-ids}

### <span class="state part">自研</span> [同文档替换 ID](revit_reset_element_ids.md)

`revit_reset_element_ids` — 同文档内换 ID：只对无宿主、无依赖的独立构件有效

```text
给选中的这 27 个独立构件换新 ID
```

### <span class="state part">自研</span> [新模型重建 ID](revit_rebuild_model_ids.md)

`revit_rebuild_model_ids` — 整模型换新 ID：把三维视图可选中的构件重建为一份或多份新模型

```text
把当前三维视图里能选中的构件重建到 E:\out\copy-{n}.rvt，出 10 份，每份 ID 都不要重复
```

```text
先彩排一次重建，告诉我多少个构件、新 ID 范围，先不要写文件
```

## 文档与进程 {#group-documents}

### [列出打开的文档](revit_documents.md)

`revit_documents` — 列出一个 Revit 进程中所有打开的文档，含后台文档

```text
这个进程里现在打开了哪些文档？把链接文档也列出来
```

### [打开模型](revit_open_document.md)

`revit_open_document` — 在工作站打开本地、UNC 或 RSN 模型，中央模型默认分离打开

```text
帮我打开中央模型 'Tower.rvt'，用分离模式打开。
```

### [激活文档](revit_activate_document.md)

`revit_activate_document` — 按标题或路径引用激活一个已打开的文档

```text
把后台打开的"塔楼 B.rvt"切换为活动文档
```

### [新建模型](revit_new_document.md)

`revit_new_document` — 在工作站用模板新建项目或族文件

```text
用 'Metric Generic Model.rte' 模板新建一个项目，命名为 '塔楼方案'。
```

### [关闭文档](revit_close_document.md)

`revit_close_document` — 关闭后台文档；首次调用不改任何内容，返回确认令牌

```text
关闭后台打开的"旧版示楼.rvt"，不要保存
```

### [保存文档](revit_save_document.md)

`revit_save_document` — 保存文档；首次调用只返回 confirm_token，不改动文件

```text
把当前模型存盘，覆盖原文件
```

### [同步文档](revit_sync_document.md)

`revit_sync_document` — 将工作共享文档与中心文件同步；首次调用不改动任何内容，需用返回的 confirm_token 再确认

```text
把当前工作共享文档同步到中心文件，备注“更新门窗标注”。
```

## 批量作业 {#group-batch}

### [作业列表](revit_jobs.md)

`revit_jobs` — 查看最近作业，或等待某个动作作业的结果

```text
最近跑过哪些作业？顺便等一下 jobId 为 3 的那个结果
```

### [取消作业](revit_cancel_job.md)

`revit_cancel_job` — 请求取消一个操作作业；已完成的更改保持提交状态

```text
把还在跑的那个批量作业 job-1234 取消掉
```

### [批量操作](revit_run_actions.md)

`revit_run_actions` — 一次执行最多 50 个动作，共用一个撤销记录，首个失败整批回滚

```text
一口气把这 20 个视图都导出成 PDF
```

### [启动批量采集](revit_batch_start.md)

`revit_batch_start` — 对本地、UNC 或 RSN 模型启动持久只读采集

```text
扫描 \\fileserver\models 下的所有 RVT 模型并开始批量采集
```

### [批处理状态](revit_batch_status.md)

`revit_batch_status` — 发起客户端退出后，读取留存下来的运行与模型状态

```text
刚才那个批处理跑完了吗？客户端已经关了
```

### [取消批量收集](revit_batch_cancel.md)

`revit_batch_cancel` — 持久化取消状态，阻止批量任务中未启动的模型继续运行

```text
取消 run_id 为 a1b2c3 的批量任务，还没开始的模型就别再跑了。
```

### [获取批量快照](revit_batch_fetch.md)

`revit_batch_fetch` — 把已完成的快照下载为新的本地文件，不覆盖已有文件

```text
把批次 'run-2026-10-31' 的快照下载到 'C:\Snapshots'，别覆盖已有文件。
```

## 族 {#group-families}

### [审计族](revit_family_audit.md)

`revit_family_audit` — 审计打开的族或按名称审计项目族，不保存或加载更改；detail=full 返回全部参数元数据

```text
用通配符审计项目里的所有族，看看哪些参数没有被使用？
```

### [加载族](revit_load_family.md)

`revit_load_family` — 在工作站把 .rfa 族文件加载进一个撤销步骤

```text
把 'C:\Families\M_Column.rfa' 和 'M_Beam.rfa' 加载进当前模型。
```

### [放置族实例](revit_place_families.md)

`revit_place_families` — 加载可选族并在一个事务与撤销项中放置实例

```text
先加载"双开门"族，然后在会议室里放置两个实例
```

### [编辑族](revit_edit_families.md)

`revit_edit_families` — 就地编辑已打开的族或项目族，dry_run 会回滚全部改动

```text
帮我编辑项目族 'M_Column' 的可见性参数，先用 dry_run 预览。
```

## 图纸与明细表 {#group-sheets}

### [读取明细表数据](revit_schedule_data.md)

`revit_schedule_data` — 分页读取明细表表头与单元格显示文本

```text
把"门窗明细表"前 100 行的数据读出来
```

### [创建图纸](revit_create_sheet.md)

`revit_create_sheet` — 用第一个已载入或指定的图框创建图纸

```text
创建一张编号 'A-102'、名称 '二层平面图' 的图纸，用 'A1' 图框。
```

### [图纸上布置视图](revit_place_views_on_sheet.md)

`revit_place_views_on_sheet` — 把视图和明细表布置到图纸上，坐标为图纸毫米

```text
把"首层平面"视图放到 A101 图纸的 (300, 200) 位置
```

### [创建明细表](revit_create_schedule.md)

`revit_create_schedule` — 为单个类别按命名字段和顺序创建明细表，支持筛选与排序分组；dry_run 会回滚

```text
给“门”类别建一个明细表，字段按 Mark、Level、Count 排列，命名为“门窗统计”。
```

## 链接与协同 {#group-links}

### [对比链接标高轴网](revit_compare_link_datums.md)

`revit_compare_link_datums` — 对比宿主与一个已加载 Revit 链接的轴网和标高（不改动模型）

```text
对比一下链接模型“结构参考.rvt”里的轴网和标高与当前项目有哪些差异？
```

### [移除链接](revit_remove_links.md)

`revit_remove_links` — 删除所选链接类型及其实例；dry_run 预览，删除后 Revit 内不可撤销

```text
先用 dry_run 预览，然后删除当前文档里的所有 Revit 链接
```

### [对齐链接基准](revit_align_link_datums.md)

`revit_align_link_datums` — 把宿主轴网与标高对齐到已链接模型，dry_run 可预览回滚

```text
把当前模型的轴网和标高对齐到已链接模型 'StructureLink.rvt'，公差 5 毫米。
```

### [链接 CAD 图纸](revit_link_cad.md)

`revit_link_cad` — 将 DWG 链接或导入到 Revit 工作站上的平面视图，返回 CAD 图层与毫米单位范围

```text
把 D:/drawings/L1-plan.dwg 链接到“L1 平面图”视图里。
```
