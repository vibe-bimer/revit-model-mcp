# 动作工具（显式启用）

默认只读。动作工具是必须主动启用的一组独立工具。
事务警告会被忽略，并记录在 `warningsDismissed` 中（为空时省略）；无法安全解决的错误会使动作回滚。

<a id="instance-and-document-targeting"></a>
## 实例与文档寻址

所有动作工具都接受 `document=null`；没有任何动作工具提供自定义超时参数。
它们使用默认的 120 秒响应等待和 300 秒接单等待预算；接单等待仅适用于本地和 SSH 传输。
发送任何动作前，MCP 传输必须发现且只发现一个正在运行的 Revit 实例，即使提供了 `document` 也不例外。
否则，调用会报错：`Actions require exactly one running Revit instance.`
HTTP 指向一个端点；文件传输会发现工作站上的实例。
`document` 用于选择这个进程内已打开的文档，不能从多个进程中选择一个实例。
所有 ID 都是无单位的正整数 Revit 构件 ID，上限为 9,223,372,036,854,775,807。
Revit 2020–2023 只接受不超过 2,147,483,647 的 ID；更大的 ID 在这些年份版本中会失败。

MCP 的 `document` 参数会转换为动作任务中的 `targetDocument`。
目标进程打开多个文档时应提供该参数；只有打开单个文档时才应省略。
带有 `targetDocument` 的动作任务在插件执行时解析该引用。
引用通过标题或文件名的不区分大小写子串匹配，必须且只能匹配一个已打开文档。
解析后的文档以标题和完整路径绑定，所有修改与验证都使用该文档，即使另一个文档处于活动状态。
未知或已关闭的目标返回 `The addressed document '<TargetDocument>' is not open.`
不明确的目标返回 `The document reference '<TargetDocument>' is ambiguous (N open documents match); use a more specific substring.`
解析失败会在任何步骤运行前终止整个批次；显式寻址的任务绝不会退回活动文档。
目标只在批次循环开始前解析一次；之后发生的文档或事务失败会作为步骤错误报告。
`select`、`show` 和 `isolate`（包括 `reset=true`）要求解析后的目标文档处于活动状态。
否则返回 `Cannot run '<command>' on '<title>' because it is not the active document; activate it in Revit first.`
不带 `targetDocument` 的任务保留使用活动文档的行为。
即使修改指向另一个文档，`activeView` 也始终报告实际的活动视图。

<a id="tool-catalogue"></a>
## 工具目录

每一行工具都还接受通用参数 `document=null`。未列出默认值的参数是必填参数，即使它们接受 `null`。
各工具的完整参数表、提示词和 Revit 年份验证状态见[功能总览](features/index.md)。

| 工具 | 除 `document=null` 外的参数 | 动作与单位 |
| --- | --- | --- |
| `revit_select` | `element_ids` | 选择指定 ID；`[]` 清除选择。返回 `count`，表示调用后当前选中构件的数量。 |
| `revit_show` | `element_ids`、`select=true` | 定位非空 ID 列表中的构件；返回 `activeView`、`viewOpened` 和 `count`，后者为调用后当前选择数量。`select=false` 时，`count` 表示原有选择数量。 |
| `revit_isolate` | `element_ids`、`reset=false` | 临时隔离指定 ID；`element_ids=[]` 配合 `reset=true` 清除临时隐藏／隔离。 |
| `revit_move` | `element_ids`、`dx_mm`、`dy_mm`、`dz_mm=0` | 按模型轴偏移量移动，单位为 mm。 |
| `revit_place_family` | `family`、`type_name`、`x_mm`、`y_mm`、`level`、`rotation_deg=0` | 在指定标高放置已载入的族，模型 XY 坐标单位为 mm；绕 Z 轴旋转，单位为度。 |
| `revit_create_wall` | `start_mm`、`end_mm`、`level`、`wall_type`、`height_mm=3000` | 创建直墙；端点为模型坐标中的 `[x,y]`，单位为 mm。 |
| `revit_create_floor` | `points_mm`、`level`、`floor_type` | 从闭合边界创建楼板；`points_mm` 是模型坐标中的 `[x,y]` 多边形顶点，单位为 mm，至少 3 个，自动闭合；`floor_type` 为 null 时选择第一个楼板类型。 |
| `revit_create_level` | `name`、`elevation_mm`、`create_view=false` | 在指定高程新建标高，单位为 mm；已存在同名标高时被拒绝，避免后续工具解析到有歧义的标高；`create_view=true` 时同时创建对应的楼层平面视图，视图类型按视图族选择，不按名称。 |
| `revit_set_phase` | `element_ids`、`created_phase`、`demolished_phase` | 按阶段的准确名称赋值；每个阶段参数可为名称、清除赋值的 `""`，或保持不变的 null；至少一个参数非 null。这些工具不创建或重命名阶段，应先在 Revit 界面中添加新阶段。 |
| `revit_merge_phases` | `source_phase`、`target_phase` | 将所有创建与拆除引用从源阶段移到目标阶段，再删除空源阶段；删除被拒绝时以 `sourceDeleted:false` 和 `phaseDeleteError` 报告。不支持放入批次。 |
| `revit_set_parameter` | `element_id`、`parameter`、`value` | 按参数名传入字符串形式的值；长度使用 mm，面积使用 m2，其余 Double 使用内部单位。 |
| `revit_set_view_lighting` | `view`、`shadows=null`、`shadow_intensity=null`、`sunlight_intensity=null`、`sun_date=null`、`sun_time=null`、`sun_azimuth_deg=null`、`sun_altitude_deg=null`、`ground_plane=null`、`ground_plane_level=null`、`background=null`、`background_colors=null`、`lighting_scheme=null`、`dry_run=false` | 按视图名称或视图 ID 设置一个非样板视图的光照：阴影开关、阳光与阴影强度、太阳日期与时间或固定光照方位角／高度角、地面平面、背景与渲染光源方案。响应在 `verification.before.lighting`／`verification.after.lighting` 给出改动前后的读数，并用 `changedSettings` 列出真正变化的项。 |
| `revit_delete` | `element_ids` | 删除非空 ID 列表中的构件及其依赖。 |
| `revit_reset_element_ids` | `element_ids`、`dry_run=false` | 用副本替换构件，让 Revit 分配新 ID；报告 `idMapping`。若删除会移除依赖、构件有宿主或属于组、构件是 MEP 曲线或 MEP 系统成员（副本不会重新接入网络，Revit 会在删除的原构件周围自动修复管线），或 Revit 无法复制该构件，则拒绝替换。 |
| `revit_batch` | `steps`、`dry_run=false` | 执行 1–50 个动作，合并为名为 `revit_batch` 的一次撤销记录。 |
| `revit_rebuild_model_ids` | `destination_path`、`view=null`、`template_path=null`、`overwrite=false`、`remove_template_levels=true`、`seed=0`、`duplicate_names="override"`、`copies=1`、`dry_run=false` | 将三维视图中可选择的构件复制到新模型，让 Revit 为每个构件分配新 ID；不改变已打开模型。先复制标高、轴网和参照平面，以解析宿主；相机、太阳路径、剖面框、视图及无类别元素不复制，并在 `excluded` 中报告。视图、图纸、明细表、注释、阶段、工作集、MEP 系统和未选中的宿主均不带入，因此结果保留几何、类型和参数。数据报告 `count`、`newIdMin`／`newIdMax`、`sourceCategoryCounts`、`copiedCategoryCounts`，以及按类别和类型校验的 `idMapping`。 |

`type_name`、`wall_type` 和 `floor_type` 是接受 `null` 的必填参数。

<a id="dry-runs-and-id-replacement"></a>
## 试运行与 ID 替换

`revit_move`、`revit_place_family`、`revit_create_wall`、`revit_create_floor`、`revit_create_level`、`revit_set_phase`、`revit_merge_phases`、`revit_set_parameter`、`revit_set_view_lighting` 和 `revit_delete` 还接受 `dry_run=false`，其位置在通用 `document` 参数之前。
试运行会执行修改、读取预期结果，然后回滚事务。
成功的试运行包含 `data.dryRun:true`、`data.rolledBack:true`，以及与真实写入相同结构的 `verification`。
动作抛出异常时返回错误，不带验证块；单动作工具遇到缺失族时还返回 `closestFamilies`。
`revit_select`、`revit_show` 和 `revit_isolate` 没有 `dry_run` 参数；隔离仅为临时隔离。
`revit_reset_element_ids` 也支持 `dry_run`；应先试运行，因为真实替换不可撤销。
只要有一个构件不符合条件，它就拒绝整个选择集；它从不原地修改 ID，也不把旧 ID 写入参数。
试运行中创建的 ID 是临时值，不能用来标识已持久化构件。

<a id="view-lighting"></a>
## 视图光照

`revit_set_view_lighting` 用视图名称或十进制视图 ID 定位一个非样板视图，并且只改动传入的参数。
`shadows` 开关该视图的太阳与阴影显示，对应 `SunAndShadowSettings.Visible`：关闭后 Revit 既不画太阳路径也不画投影，强度设置因此没有可见效果；共享太阳与阴影设置的视图无法单独开关，会被直接拒绝。
Revit 没有为「图形显示选项」里的「阴影」复选框提供 API——`GRAPHIC_DISPLAY_OPTIONS_SHADOWS` 只是枚举成员，在视图上取不到该参数（已在 Revit 2020 实测确认），因此 `shadows` 是 API 真正提供的那个开关。
`shadow_intensity`（0–100，0 表示没有投影）和 `sunlight_intensity`（0–100）分别控制投影浓度与模拟阳光强度。
没有太阳与阴影设置的视图（例如明细表）会被直接拒绝，不会静默忽略。

`sun_date`（`yyyy-MM-dd`）和 `sun_time`（24 小时 `HH:mm`）确定「静止图像」的太阳位置，作为本地时间交给 Revit；读数以 `sunDateAndTimeUtc` 和 `sunTimeZoneHours` 回读，因此始终可以核对 Revit 实际保存的时刻。只传其中一个时，另一半沿用视图当前值；两者都会把单日或多日日照研究切回静止图像。
需要固定的太阳位置时改用 `sun_azimuth_deg`（自北顺时针）与 `sun_altitude_deg`（地平线以上），两者必须同时提供，会把太阳设置切到「光照」模式。

`ground_plane` 开关地面平面，`ground_plane_level` 指定地面所在的标高。
Revit 只接受它认定为地面平面的标高，因此传入其他标高时，工具会先把该标高标记为地面平面（`LEVEL_IS_GROUND_PLANE`）再重试，并在 `notes` 中说明这一步；选定地面平面标高时若地面平面仍是关闭状态，也会一并打开。
`background` 取 `sky` 或 `gradient`，只对三维、剖切和立面视图有效；`background_colors` 依次给出渐变的天顶、地平线、地面三色（`#RRGGBB`），省略时沿用当前渐变，当前背景不是渐变时使用 `#C8DEF0`／`#F5F5F5`／`#BFBFBF`。
Revit 的 API 只能把背景换成天空、渐变或图片，无法恢复成「无背景」，也无法清除已选定的地面平面标高；两项都是本项目记录的 API 限制，改动前应先确认视图当前状态。
`lighting_scheme` 设置渲染光源方案：`exterior-sun`、`exterior-sun-and-artificial`、`exterior-artificial`、`interior-sun`、`interior-sun-and-artificial`、`interior-artificial`；只影响渲染，不改变着色显示。

太阳与阴影设置属于视图。若该视图与其他视图共享设置，读数的 `sunSettingsShared` 为 true，改动会一并作用到共享这些设置的所有视图，响应会在 `notes` 中提示。
`verification.before.lighting` 与 `verification.after.lighting` 给出改动前后的完整读数：视图 ID、名称、类型、阴影、两种强度、太阳类型与时间（UTC）、项目时区与夏令时、光照模式的方位角与高度角、地面平面与标高、背景类型与颜色、渲染光源方案。
视图没有可报告的构件 ID，因此真正变化的项列在 `changedSettings`（例如 `["shadows","sun_date_time"]`）中，而不是 `verification.changed`。

<a id="rebuilding-into-new-model-files"></a>
## 重建为新模型文件

`revit_rebuild_model_ids` 不是一个可回滚的模型事务：`dry_run=true` 执行复制并报告映射，但不保存文件；真实运行写入新模型，源模型从不被修改或保存。
`destination_path` 是 Revit 工作站上的路径，不是 MCP 客户端路径。
不指定 `view` 时使用第一个非透视三维视图；只复制该视图中可选择的构件。
`template_path` 用于选择模板，代替默认公制模板；`remove_template_levels=true` 移除模板自带的标高。
`overwrite=true` 明确允许替换已有目标文件；默认值为 false。
响应还包括 `destinationPath`、`saved`、`sourceView`、`sourceElementCount`、`datumCount`，以及每个排除元素的原因。
新模型使用的模板没有实际视图，因此缺少三维视图时重建工具会添加一个；否则 Revit 会拒绝打开文件。
源模型使用的名称已存在于新项目时，Revit 会在粘贴过程中询问如何处理重名，这会阻塞无人值守运行；默认重建工具以 OK 自动回答（`duplicate_names=override`），保留源模型自己的类型，并通过 `autoAnsweredDialogs` 报告自动回答次数。`duplicate_names=rename` 先重命名模板元素，再尝试删除它们：每份副本约多花 30 秒，且 Revit 会拒绝许多删除操作，因此它仅作为后备方式。
`duplicate_names=reuse` 不询问重名处理方式，保留新模型已有的版本；一次写入多份副本时默认使用该方式，因为弹出询问会导致 Revit 拒绝粘贴。即使如此，若 Revit 仍拒绝复制，工具会以同一设置重试；记录中的重试恢复了一份少了 11 个构件的副本，但调用者仍必须校验返回的映射。
`copies=2` 或更大值会从一个新模型依次写入多份文件，每次复制后删除当前副本的构件再进行下一次：Revit 在同一文档中不断分配更大的 ID，因此各副本拥有相同构件和各自的 ID，无须提前消耗 ID。`destination_path` 可用 `{n}` 表示副本编号；不含该占位符时，编号追加在扩展名之前。每份副本的路径、大小和 ID 映射在 `copyResults` 中报告。Revit 有时会拒绝后续副本的批量粘贴：工具随后退回逐元素复制，结果可能更小，其 `copyResults` 项中 `idMappingVerified=false`，因此调用者必须检查每一项。记录中的测试以每次运行一份副本的方式较可靠；测量见[重建性能与成本](rebuild-performance.md)。若要在多个 Revit 实例中并行运行，应使用独立 HTTP 端点或各自只发现一个实例的传输；`document` 不能绕过单实例门禁。实例分别通过 `REVIT_MCP_HTTP_PORT`、`REVIT_MCP_TOKEN` 和 `REVIT_MCP_CHANNEL_DIR` 获取端口、令牌和通道目录。
Revit 为复制构件分配紧接新模型已有元素之后的 ID，因此从同一源模型重建两次会得到相同 ID；`seed` 在复制前添加指定数量的临时标高，再将它们删除，让副本的 ID 移入独立号段。
重建试运行报告的创建 ID 同样不能标识已保存的输出模型。

<a id="verification-and-committed-changes"></a>
## 验证与已提交修改

成功的真实写入返回 `data.dryRun:false`，并在提交后重新读取受影响构件。
`verification.before` 在修改前捕获；`verification.after` 在提交后重新读取，试运行则在回滚前读取。
`verification.error` 表示提交后的重读失败；修改已经提交。
单动作响应包含 `failedStep:null`。
`verification` 块包含模型事实：移动时的包围盒、参数编辑时的参数值及所属实例／类型、创建时的构件元数据，以及删除时的已删除／依赖 ID 和存续检查。
包围盒使用模型 XYZ 坐标，单位为 mm，保留一位小数；不可用的包围盒省略。
例如，为构件 123 设置 Comments 返回：

```json
{
  "dryRun": false,
  "verification": {
    "before": {"id": 123, "parameter": "Comments", "value": "", "storageType": "String", "owner": "instance"},
    "after": {"id": 123, "parameter": "Comments", "value": "Reviewed", "storageType": "String", "owner": "instance"},
    "changed": [123]
  }
}
```

<a id="batch-execution"></a>
## 批次执行

`revit_batch` 接受动作名及其通常的 snake_case 参数。应在批次上统一设置 `document`，不要放入各步骤的 `args`：

```json
{
  "steps": [
    {"action": "move", "args": {"element_ids": [123], "dx_mm": 100, "dy_mm": 0}},
    {"action": "set_parameter", "args": {"element_id": 123, "parameter": "Comments", "value": "Reviewed"}}
  ],
  "dry_run": false
}
```

成功批次将各事务合并为名为 `revit_batch` 的一次撤销记录。
第一个失败步骤使整个批次回滚；所有尝试过的步骤，包括失败步骤，均带有 `rolledBack:true`。
`Assimilate` 失败记录在最后一个步骤上，`failedStep` 指向该步骤。
执行前验证所有步骤；后面的步骤无效也会拒绝整个批次，不执行任何动作，且不带 `failedStep`。
结果为每个尝试过的步骤包含从零开始的 `index`、`command`、`success`，以及 `data` 或 `error`，并包含批次的 `undoName`、`committed` 和 `failedStep`（成功时为 null）。
批次试运行逐步执行，每一步都可看到前面步骤的修改，最后回滚整个事务组并恢复原选择集。
真实批次中的单步 `dry_run:true` 可以使用，只预览该步骤。
验证描述各步骤的即时结果；后续步骤可能再次改变这些构件。
批次接受 1–50 步；允许 `select` 和 `isolate`，拒绝 `show`、嵌套批次以及未知参数键。

<a id="navigation-dialogs-and-family-names"></a>
## 导航、对话框与族名称

`revit_show` 在调用 `ShowElements` 前检查已打开的界面视图。
若没有视图包含请求中的任何构件，就为某个构件的标高打开一个非样板平面视图。
优先楼层平面，其次优先名称以标高名称开头的视图。
没有匹配平面时，使用第一个非样板三维视图。
处理器在 ExternalEvent 内同步设置 `UIDocument.ActiveView`，不使用事务；`ShowElements` 需要视图立即处于活动状态。
`RequestViewChange` 则会推迟到控制权返回 Revit 后才切换视图。
响应包含 `activeView` 和 `viewOpened`，后者表示处理器是否打开了此前关闭的视图。

动作执行期间，处理器尝试先用 OK、再用 Yes 关闭 TaskDialog 提示。
成功覆盖的提示文本记录在 `dialogsSuppressed` 中。
对话框处理器在 `finally` 中移除，错误路径也不例外。
单动作 `revit_place_family` 遇到缺失族时，在 `closestFamilies` 中返回最多五个相近名称及其族类别；不返回无关名称。
在 `revit_batch` 内，缺失族只作为 `steps[].error` 文本报告，不提供 `closestFamilies`。
使用 `Family: Type` 时，`type_name=null` 使用其中指定的类型；另行提供冲突的 `type_name` 会被拒绝。
只提供族名称时，`type_name=null` 选择第一个已载入类型。

## 动作门禁 {#gates}

两个门禁都必须启用：

1. 在 Python 服务进程的环境中设置 `REVIT_MCP_ALLOW_WRITE=1`，然后重启服务。
   布尔解析器会去除首尾空白且不区分大小写：`1`、`true`、`yes`、`on` 启用动作；`0`、`false`、`no`、`off` 禁用动作。
   未设置时默认禁用，MCP `list_tools` 不列出动作工具。无法识别的值会抛出配置错误，而不是静默禁用。
2. 在 Revit 工作站创建 `%LOCALAPPDATA%\RevitModelMcp\allow-write`：

   ```powershell
   New-Item -ItemType Directory -Force "$env:LOCALAPPDATA\RevitModelMcp" | Out-Null
   New-Item -ItemType File -Force "$env:LOCALAPPDATA\RevitModelMcp\allow-write" | Out-Null
   ```

插件对每个动作都检查门禁文件，包括选择与导航。
文件不存在时，响应包含 `success:false` 和 `error:"actions disabled on the workstation"`。
删除该文件即可立即禁用动作，无须重启 Revit。
即使传输使用 `REVIT_MCP_CHANNEL_DIR`，门禁文件也仍位于默认的本地应用数据目录。

直接 HTTP 动作请求要求认证及工作站门禁；Python 环境门禁控制是否暴露 MCP 动作工具。

<a id="units-and-parameter-scope"></a>
## 单位与参数作用范围

动作寻址传输报告的进程 ID。
坐标使用模型轴和所选标高的项目高程。
`type_name` 或 `wall_type` 传入 `null`，分别选择族的第一个类型或第一个基本墙类型。
族放置使用基于标高的非结构重载；有宿主、基于面的族和自适应族可能需要其他放置 API，并返回错误。
单动作族放置工具遇到未载入族时返回最多五个最相近的已载入名称。
参数值使用与区域设置无关的数值记法；其余 Double 参数使用 Revit 内部单位。
编辑类型参数会影响该类型的所有实例，并返回 `parameterScope:"type"`。
不能设置 ElementId 参数或只读参数。

<a id="transactions-and-timeout-safety"></a>
## 事务与超时安全

动作执行器的响应包含 `activeView`，动作错误也不例外。
传输拒绝和目标不匹配响应可能省略动作元数据。
模型修改和临时隔离使用以工具命名的独立事务。
`revit_batch` 以名为 `revit_batch` 的 `TransactionGroup` 包裹各步骤事务，并将它们合并为一次撤销记录。
提交时的警告会被忽略，并在成功动作中报告。
Revit 允许时，错误可尝试一次 `FixElements` 或 `SetValue` 解决；未解决或重复错误使事务回滚。
选择与导航使用界面调用，不使用模型事务。
动作不保存被寻址的源模型；`revit_rebuild_model_ids` 只在工作站保存新输出模型文件。
超时不能证明动作已回滚或从未运行；即使接单超时，也可能留下之后才执行的待处理任务。
超时或提交后验证失败时，应先检查模型和输出文件再重试；上一调用可能已执行。
