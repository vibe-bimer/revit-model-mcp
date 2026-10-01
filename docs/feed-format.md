<a id="feed-format"></a>

# 数据格式

当前通道协议使用 UTF-8 JSON，字段名区分大小写。
协议没有 `schemaVersion` 字段；程序包版本标识本文档描述的契约。
独立插件不会在 `%LOCALAPPDATA%\RevitDevLoader` 下写入数据流。
其默认通道为 `%LOCALAPPDATA%\RevitModelMcp`。

<a id="files-and-directories"></a>

## 文件与目录

| 位置 | 内容 |
|---|---|
| 通道目录 | `trigger.txt`、`mcp_<uuid>.tmp`、`response_<timestamp>_<command>_<correlationId>.json`、`view_<timestamp>_<id>.png`、`instance_<processId>.json` 和心跳 `.tmp` 文件 |
| 通道目录，旧版快照 | `latest.json`、`latest.txt`、`snapshot_yyyyMMdd_HHmmss.json` |
| 通道目录，旧版视图转储 | `views_dump_yyyyMMdd_HHmmss_fff.json` 及同名 `.txt`；数字后缀用于避免已有名称冲突 |
| `%LOCALAPPDATA%\RevitModelMcp\settings.json` | HTTP 监听器设置和持久化 Bearer 令牌 |
| `%LOCALAPPDATA%\RevitModelMcp\allow-write` | 工作站动作门禁；文件存在即启用动作 |
| Windows“文档”文件夹下的 `RevitModelMcp\Logs` | `RevitModelMcp-yyyyMMdd.log`，以及按大小轮转产生的编号日志 |
| `%TEMP%\RevitModelMcp\Logs` | “文档”文件夹不可用时的日志备用位置 |

`REVIT_MCP_CHANNEL_DIR` 在服务器和 Revit 环境中覆盖通道目录。
它不会移动 HTTP 设置、动作门禁或日志。
响应时间戳使用本地时间，精确到毫秒，并可带有避免名称冲突的后缀。
HTTP 将已完成的响应 JSON 存储在内存中；导出的 PNG 仍使用通道目录。

<a id="jobs"></a>

## 任务

MCP 工具将 snake_case 参数转换为通道 JSON 字段。
请求 `{"command":"ping"}` 无需活动模型即可检查连接。
读取任务可以包含 `targetDocument`；动作会添加实例发现得到的 `targetProcessId`。
插件用 `targetDocument` 对活动文档标题或路径的文件名进行不区分大小写的子串匹配。
HTTP 端点还会拒绝发往其他进程的任务。

| MCP 参数 | JSON 字段 |
|---|---|
| `document` | `targetDocument` |
| `element_id` | `element-details` 使用 `id`；`set-parameter` 使用 `elementId` |
| `element_ids` | `elementIds` |
| `dry_run` | `dryRun`（可选布尔值，默认为 false） |
| `view_type`、`name_contains` | `viewType`、`nameContains` |
| `pixel_size` | `pixelSize`；服务器还设置 `zoomToFit:true` |
| `group_by`、`sum_field` | `groupBy`、`numericField` |
| `type_name`、`area_scheme`、`parameter_filters` | 查询筛选条件使用 `type`、`areaScheme`、`parameterFilters`；放置操作使用 `typeName` |
| `sort_field`、`sort_direction` | `sort:{field,direction}` |
| `include_geometry`、`include_elements`、`warning_text` | `includeGeometry`、`includeElements`、`warningText` |
| `source_id`、`source_name` | `sourceId`、`sourceName` |
| `dx_mm`、`dy_mm`、`dz_mm`、`x_mm`、`y_mm` | `dxMm`、`dyMm`、`dzMm`、`xMm`、`yMm` |
| `start_mm`、`end_mm`、`wall_type`、`height_mm`、`rotation_deg` | `startMm`、`endMm`、`wallType`、`heightMm`、`rotationDeg` |

视图导出的 `save_to` 和超时是客户端选项，不是任务字段。Excel ID 清单的 `save_to` 会转换为任务中的 `saveTo`，因为工作簿写在 Revit 工作站上。文件传输会添加唯一的 `correlationId`；上述示例仅展示命令相关字段。
`parameterFilters` 的条目包含 `parameter`、`operator` 和可选的 `value`。
数值筛选值中，长度使用 mm、面积使用 m2、体积使用 m3。
其他可测量筛选值使用文档的显示单位；不可测量的双精度数值使用内部值。
返回的查询字段包含 `value`，以及可选的 `numericValue`、`unit`、`hasValue` 和 `source`。
聚合使用这些数值；解释求和结果前应检查返回单位。
参数默认值和单位见[工具表](../README.md#tools)。
[任务构造器](../server/revit_model_mcp/universal_jobs.py)和[解析器](../src/RevitModelMcp.Core/Control/ControlJobParser.cs)定义了请求契约。

<a id="coordinator-checks"></a>

### 协调检查

这些任务使用读取响应封装，不需要动作门禁。
它们都接受可选的 `targetDocument`；超时选项留在 Python 客户端。
以下示例单独展示 `data`，不包含外层响应封装。

`model-health` 任务：

```json
{"command":"model-health"}
```

响应数据结构：

```json
{
  "revitVersion":"2026", "revitBuild":"build", "fileName":"Model.rvt",
  "isWorkshared":false, "fileSizeBytes":null,
  "projectInfo":{"name":"Model","number":"01","client":"","address":"","buildingName":"","status":"","author":""},
  "counts":{"elements":0,"warnings":0,"warningGroups":0,"levels":0,"grids":0,"views":0,
    "viewsNotOnSheets":0,"viewTemplates":0,"sheets":0,"rooms":0,"roomsUnplaced":0,
    "roomsNotEnclosed":0,"families":0,"familiesInPlace":0,"familyTypesUnused":0,
    "groupsModel":0,"groupsDetail":0,"groupTypes":0,"designOptions":0,"worksets":0,
    "linksRvt":0,"linksCad":0,"cadImports":0,"images":0},
  "topWarnings":[{"text":"Warning description","count":1}],
  "units":{"length":"unit type id","area":"unit type id","volume":"unit type id"},
  "skipped":[]
}
```

`elements` 统计全部非类型元素，包括视图和图纸。
`familyTypesUnused` 统计未被任何非类型元素的类型 ID 引用的元素类型。
`linksRvt` 统计 RVT 类型；`linksCad` 统计具有外部文件引用的 CAD 类型；`cadImports` 和 `images` 统计实例。
`viewsNotOnSheets` 排除模板，统计未放置在图纸上的平面、剖面、立面、三维、绘图和图例视图。
未放置房间的面积不大于零且没有位置；未封闭房间的面积不大于零但有位置。
`topWarnings` 最多包含十组，按计数降序排列。
读取失败的指标为 null，并在 `skipped` 中添加 `{"metric":"counts.rooms","error":"description"}`。
没有已保存路径时，`fileSizeBytes` 为 null；文件无法访问时还会记录一个跳过的指标。

`links-status` 任务：

```json
{"command":"links-status"}
```

响应数据结构：

```json
{
  "rvtLinks":[{"name":"A.rvt","typeId":10,"status":"Loaded","pathType":"Absolute","path":"C:\\Models\\A.rvt","instances":1,"pinned":true,"nested":false}],
  "cadLinks":[{"name":"Plan.dwg","typeId":20,"isLinked":true,"status":"Loaded","path":"C:\\Models\\Plan.dwg","instances":1,"viewSpecific":true}],
  "images":[{"name":"Logo.png","typeId":30,"status":"Loaded","path":"C:\\Models\\Logo.png","instances":1}],
  "summary":{"rvt":1,"rvtLoaded":1,"cad":1,"cadImports":0,"images":1},
  "listLimit":100
}
```

每个列表最多包含 100 个类型，按类型 ID 排序；汇总计数覆盖所有类型，而 `cadImports` 统计导入实例。
RVT/CAD 状态为 `Loaded`、`Unloaded`、`NotFound`、`LocallyUnloaded`、`InClosedWorkset` 或 `Other`。
图像保留 Revit 的 `ImageTypeStatus`：`Loaded`、`Unloaded`、`FailedToLoad`、`Imported`、`Generated` 或 `Unknown`。
单个类型读取失败时返回 `status:"Other"` 和 `error`；不可用的路径被省略。
RVT 的 `pathType` 为 `Absolute`、`Relative`、`Cloud`、`Server` 或 `Unknown`。
插件提供路径；启用 `REVIT_MCP_REDACT_PATHS=1` 时，Python 服务器将嵌套 `path` 字段缩减为文件名。

`shared-coordinates` 任务：

```json
{"command":"shared-coordinates"}
```

响应数据结构：

```json
{
  "activeProjectLocation":"Internal", "projectLocations":["Internal"],
  "projectBasePoint":{"eastWestMm":0.0,"northSouthMm":0.0,"elevationMm":0.0,"angleToTrueNorthDeg":0.0,"clipped":false},
  "surveyPoint":{"eastWestMm":0.0,"northSouthMm":0.0,"elevationMm":0.0,"clipped":null},
  "internalOriginToBasePointMm":{"x":0.0,"y":0.0,"z":0.0},
  "trueNorthAngleDeg":0.0, "siteName":"Internal",
  "sharedSiteFromLinks":[{"linkName":"A.rvt","sharedSiteName":null,"hasOffset":true,"offsetMm":{"x":100.0,"y":0.0,"z":0.0},"rotationDeg":0.0}],
  "listLimit":100, "projectLocationsTotal":1, "linkInstancesTotal":1
}
```

坐标使用 mm，角度使用度，均四舍五入到一位小数。
真北角是活动项目位置在内部原点处的项目位置角度。
`clipped` 报告项目基点的 API 值；不可用时为 null。
链接数据描述总变换；`hasOffset` 在四舍五入前将该变换与单位变换比较，`sharedSiteName` 为 null。
项目位置和链接实例最多列出 100 项；总数字段报告未截断的数量。

`parameter-fill-check` 任务：

```json
{"command":"parameter-fill-check","categories":["Walls","Doors"],"parameters":["Mark","Comments"],"level":"Level 1","workset":"Shell","view":"Plan","sampleLimit":20,"includeTypes":true}
```

`categories` 要求 1–20 个名称，`parameters` 要求 1–30 个名称。
可选的 `level`、`workset` 和 `view` 使用通用查询筛选语义，包括本地化类别解析和未知名称错误。
`sampleLimit` 默认为 20，拒绝 1–100 之外的值；`includeTypes` 默认为 true。
Python 参数 `sample_limit` 和 `include_types` 映射为 `sampleLimit` 和 `includeTypes`。
响应数据结构：

```json
{
  "scope":{"categories":["Walls","Doors"],"elements":3,"level":"Level 1","workset":"Shell","view":"Plan"},
  "parameters":[{"name":"Mark","elements":3,"filled":1,"empty":1,"missing":1,
    "storageTypes":{"String":2},"owner":{"instance":1,"type":1},
    "emptySampleIds":[101],"missingSampleIds":[102],
    "byCategory":[{"category":"Walls","elements":3,"filled":1,"empty":1,"missing":1}]}]
}
```

范围计数覆盖所有匹配的非类型元素，不分页。
每个参数的 `filled + empty + missing` 等于 `elements`；存储类型和归属计数仅包含已存在的参数。
只有实例上没有同名参数时，才回退到类型参数。
已填写参数需要满足 `HasValue`；字符串还要求包含非空白文本，元素 ID 必须不同于 `InvalidElementId`。
当 `HasValue` 为 true 时，双精度和整数的零值也计为已填写。
每个采样列表独立限制在 `sampleLimit` 范围内；`byCategory` 仅包含存在匹配元素的类别。

<a id="command-responses"></a>

## 命令响应

```json
{
  "command": "ping",
  "success": true,
  "partial": false,
  "data": "pong",
  "elapsedMs": 0,
  "responder": {
    "documentName": "Sample model",
    "documentPath": "C:\\Models\\Sample model.rvt",
    "processId": 1234,
    "revitVersion": "2026"
  }
}
```

`data` 取决于命令，为 null 时省略。
`message` 携带可选的诊断文本。
读取失败使用 `success:false` 和 `message`；Python 服务器将其转换为 MCP 工具错误。
部分读取使用 `success:false`、`partial:true` 和任何可用的 `data`。当前文件通道实现会在 `data` 为字典/列表且 `elapsedMs` 为正数时返回终态部分响应，虽然公开读取工具说明承诺此时抛出错误。只有 `success:true` 且 `partial:false`（或没有 `partial` 字段）时，才能将其作为完整统计结果。客户端等待响应超时仍会抛出错误，但不会取消任务。
动作失败保留响应对象，并添加 `error`。
`revit_list_instances` 直接返回实例对象列表，不使用该响应封装。

| 动作响应字段 | 契约 |
|---|---|
| `activeView` | 响应时的活动视图名称；没有文档时为空字符串；由动作执行器提供 |
| `viewOpened` | 在 `show` 中提供；表示其显式打开视图步骤是否打开了此前关闭的视图 |
| `dialogsSuppressed` | 成功覆盖 TaskDialog 时产生的消息；没有覆盖的动作会输出空列表 |
| `warningsDismissed` | 成功事务中消除的警告描述；为空或动作失败时省略 |
| `failedStep` | 单个动作中提供，值为 null |
| `data.closestFamilies` | 单动作工具找不到族时，返回相似的已加载族名称和类别；批量仅返回 `steps[].error` 文本 |
| `data.parameterScope` | `set-parameter` 后为 `instance` 或 `type`；类型编辑影响所有使用该类型的实例 |

传输错误和目标不匹配可能发生在动作执行器之前，因而不包含这些字段。
参见[响应模型](../src/RevitModelMcp.Core/Models/ReadCommandModels.cs)和[动作模型](../src/RevitModelMcp.Core/Control/ActionJobParser.cs)。

<a id="action-writes-and-batches"></a>

## 动作写入与批量

文件通道和 HTTP 接受 `move`、`place-family`、`create-wall`、`create-floor`、`set-phase`、`merge-phases`、`set-parameter`、`delete` 和 `batch` 的 `dryRun`。
成功的修改始终返回 `data.dryRun`。
成功的试运行返回 `data.rolledBack:true`；预期变化的事实在回滚前读取。
动作抛出异常时返回错误，不包含验证块。
`verification.before` 在修改前采集。
实际写入在提交后重新读取 `verification.after`。
`verification.error` 报告提交后的重新读取失败；修改本身已经提交。
不可用的包围盒会被省略；可用边界为模型坐标系下以 mm 表示的 XYZ 数组，四舍五入到一位小数。
参数值为不受区域设置影响的字符串：长度使用 mm、面积使用 m2、其他双精度值使用内部单位。
`owner` 为 `instance` 或 `type`。

| 命令 | `data.verification` 结构 |
|---|---|
| `move` | `{"before":{"elements":[{"id":1,"category":"Walls","boundingBoxMinMm":[0,0,0],"boundingBoxMaxMm":[100,100,3000]}]},"after":{"elements":[{"id":1,"category":"Walls","boundingBoxMinMm":[10,0,0],"boundingBoxMaxMm":[110,100,3000]}]},"changed":[1]}` |
| `set-parameter` | `{"before":{"id":1,"parameter":"Comments","value":"","storageType":"String","owner":"instance"},"after":{"id":1,"parameter":"Comments","value":"Reviewed","storageType":"String","owner":"instance"},"changed":[1]}` |
| `place-family`、`create-wall`、`create-floor` | `{"after":{"id":2,"category":"Walls","family":"Basic Wall","type":"Generic","level":"01","boundingBoxMinMm":[0,0,0],"boundingBoxMaxMm":[1000,200,3000]}}`；试运行会在 `verification` 内添加 `"wouldCreate":true`。 |
| `set-phase` | `{"before":{"elements":[{"id":3,"category":"Walls","createdPhase":"新构造","demolishedPhase":""}]},"after":{"elements":[{"id":3,"category":"Walls","createdPhase":"现有","demolishedPhase":"拆除"}]},"changed":[3]}`；空字符串表示未分配阶段。 |
| `merge-phases` | `{"before":{"sourcePhase":"临时","targetPhase":"新构造"},"after":{"reassignedCreated":12,"reassignedDemolished":3,"sourceRemaining":0}}`；`data.sourceDeleted` 和 `data.phaseDeleteError` 报告删除尝试。 |
| `delete` | `{"before":{"requested":[1],"dependents":[2]},"after":{"stillPresent":[]},"changed":[1,2]}` |

`changed` 包含四舍五入后的边界或参数值发生变化的 ID，或 `Document.Delete` 返回的全部 ID。
`dependents` 不包含显式请求的 ID。
试运行产生的创建 ID 是临时的。
创建元数据来自所创建元素及其类型和标高。

批量任务包含一个非空的 `steps` 数组，最多有 50 个命令对象：

```json
{"command":"batch","dryRun":false,"steps":[
  {"command":"move","elementIds":[1],"dxMm":10,"dyMm":0},
  {"command":"set-parameter","elementId":1,"parameter":"Comments","value":"Reviewed"}
]}
```

步骤使用各命令正常的通道字段。
执行前，在解析时校验所有步骤；即使后面的步骤无效，也会拒绝整个批量任务，不执行任何步骤，且不包含 `failedStep`。
允许的命令为 `move`、`place-family`、`create-wall`、`create-floor`、`set-phase`、`set-parameter`、`delete`、`select` 和 `isolate`。
每个模型步骤使用自己的事务；整个事务组被合并为单个撤销记录 `revit_batch`。
批量试运行会保留各步骤的修改供后续步骤使用，并在最后回滚整个事务组。
实际执行的批量中，单个通道步骤可以包含 `dryRun:true`（MCP 中为 `dry_run:true`）；这只预览该步骤。
批量回滚会恢复选择状态。

`data.steps[]` 包含 `index`（从零开始）、`command`、`success`，以及 `data` 或 `error`。
每个成功修改步骤的 `data` 携带与单动作相同的验证结构。
首个失败步骤会停止执行；所有已尝试的步骤（包括失败步骤）及任何保留的步骤数据都带有 `rolledBack:true`。
`Assimilate` 失败会报告在最后一步，`failedStep` 指向该步骤。
`data.undoName` 为 `"revit_batch"`，`data.committed` 报告事务组合并情况，`data.failedStep` 为失败步骤索引或 null。
成功的试运行为 `committed:false`、`failedStep:null` 和 `rolledBack:true`。
验证立即记录每个步骤；后续步骤可能覆盖这些事实。

<a id="geometry-and-image-exports"></a>

## 几何与图像导出

当数据可用时，`revit_element_details` 直接在 `data` 下返回 `location`、`boundingBox` 和 `roomCenterMm`。
`revit_query_elements(include_geometry=true)` 会在每个返回元素上包含这些字段。
点位置使用 `type:"point"`、`xMm`、`yMm`、`zMm`。
曲线位置使用 `type:"curve"`、`startMm`、`endMm`、`lengthMm`。
包围盒使用 `minMm`、`maxMm`、`centerMm` 数组。
`roomCenterMm` 是已放置房间的位置点，而非计算得到的几何质心。
坐标使用模型坐标轴，以 mm 表示，四舍五入到一位小数。

导出在 `data` 中返回 `fileName`、`width`、`height`、`sizeBytes`、`viewName` 和 `viewType`。
Python 服务器下载 PNG 后添加 `localPath`。
`width` 和 `height` 使用像素；`sizeBytes` 是 PNG 的字节大小。
直接获取图像见 [HTTP 端点](transport.md#http-configuration)。

<a id="heartbeats-and-legacy-reports"></a>

## 心跳与旧版报告

心跳 JSON 包含 `processId`、`revitVersion`、`documentTitle`、`documentPath` 和 `updatedUtc`。
`updatedUtc` 是 ISO 8601 UTC 时间戳。
插件每五秒写入一次；文件客户端忽略超过 60 秒的记录。
HTTP 实例发现使用 `/health`，而非心跳文件。

插件接受旧版快照和 `views-dump` 任务，但它们不是 MCP 工具。
快照使用 [Snapshot 契约](../src/RevitModelMcp.Core/Models/Snapshot.cs)，不使用命令响应封装。
视图转储使用 `command:"views-dump"`、`status`、时间戳、`responder`、进度计数，以及 [ViewDumpReport](../src/RevitModelMcp.Core/Models/ViewDumpReport.cs) 中的 `views` 列表。
它们跟踪视图的打开和关闭，以及原始视图的恢复。
旧版格式没有模式版本，不应视为稳定的外部 API。
