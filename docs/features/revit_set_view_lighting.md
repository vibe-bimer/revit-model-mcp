# 设置视图光照

`revit_set_view_lighting`

<p class="facts"><span><b>分组</b> 视图与截图</span><span><b>类型</b> 动作（需授权）</span><span><b>起始版本</b> 0.10.0</span><span><b>影响范围</b> 模型构件 / 参数</span></p>

设置视图的阴影、太阳位置与强度、地面平面、背景和渲染光源方案

!!! warning "动作工具需要双门禁"
    客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。

!!! note "使用提示"
    阳光与阴影设置属于视图；共享设置时改动会传递到共享该设置的其他视图，阴影开关在共享设置下不可用

## 可复制提示词 {#prompts}

```text
把三维视图的阴影打开，阴影浓度 60，背景换成天空，渲染光源用室外阳光
```

```text
把 {3D} 的太阳设成 2026-06-21 15:00，阳光强度 80，先彩排一次
```

```text
用光照模式把太阳固定在方位角 135°、高度角 45°，并打开标高 01 的地面平面
```

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `view` | 是 | — | `string` | 视图名称（与 revit_list_views 一致）或十进制视图 ID；非样板视图 |
| `background` | 否 | `null` | `string / null` | 视图背景 sky 或 gradient，仅三维、剖切和立面视图支持 |
| `background_colors` | 否 | `null` | `array<string> / null` | 渐变三色（天顶、地平线、地面），如 #C8DEF0 |
| `dry_run` | 否 | `false` | `boolean` | 彩排：改完读取并回滚，返回与真实写入相同的读数 |
| `ground_plane` | 否 | `null` | `boolean / null` | 是否使用地面平面 |
| `ground_plane_level` | 否 | `null` | `string / null` | 地面平面所在标高；Revit 不认可的标高会被标记为地面平面 |
| `lighting_scheme` | 否 | `null` | `string / null` | 渲染光源方案：室外或室内，配阳光、人工光或两者 |
| `shadow_intensity` | 否 | `null` | `integer / null` | 投影浓度 0–100，0 表示没有投影 |
| `shadows` | 否 | `null` | `boolean / null` | 视图的太阳与阴影显示开关；关闭后不画太阳路径与投影，强度设置随之失效；共享设置的视图会拒绝 |
| `sun_altitude_deg` | 否 | `null` | `number / null` | 光照模式的太阳高度角，地平线以上，-90–90 |
| `sun_azimuth_deg` | 否 | `null` | `number / null` | 光照模式的太阳方位角，自北顺时针；必须与高度角同时给出 |
| `sun_date` | 否 | `null` | `string / null` | 静止图像的日期 yyyy-MM-dd；作为本地时间交给 Revit，读数以 UTC 与时区回读 |
| `sun_time` | 否 | `null` | `string / null` | 静止图像的时间 24 小时 HH:mm；作为本地时间交给 Revit，读数以 UTC 与时区回读 |
| `sunlight_intensity` | 否 | `null` | `integer / null` | 模拟阳光强度 0–100 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | `string / null` | 文档标题或文件名的不区分大小写子串；读取时用于选择 Revit 实例，多个实例时必须唯一；动作时用于选择实例中已打开的文档，多个文档时必填。未知或歧义目标会被拒绝 |

## 功能说明与返回结果 {#contract}

设置一个视图的光照：阴影、太阳位置、地面平面、背景以及渲染光源方案。

`view` 是准确的非样板视图名称，或 `revit_list_views` 报告的十进制视图 ID；没有太阳与阴影设置的视图会被拒绝。
其余参数都是可选的，只有传入的参数会被修改；响应在 `verification.before.lighting` 与 `verification.after.lighting` 中给出改动前后的读数，并在 `changedSettings` 中列出真正发生变化的项。
`shadows` 开关该视图的太阳与阴影显示：关闭后 Revit 既不画太阳路径也不画投影，强度设置随之没有可见效果；Revit 没有为「图形显示选项」的「阴影」复选框提供 API，因此这是工具能写入的唯一阴影开关，而共享太阳与阴影设置的视图会被拒绝。
`shadow_intensity` 取 0（没有投影）到 100（全黑），`sunlight_intensity` 取 0 到 100。
`sun_date`（yyyy-MM-dd）与 `sun_time`（24 小时 HH:mm）确定「静止图像」的太阳位置，并作为本地时间交给 Revit；读数以 `sunDateAndTimeUtc` 与 `sunTimeZoneHours` 回读，因此 Revit 实际保存的时刻始终可以核对。只传其中一个时，另一半沿用视图当前值，两者都会把日照研究切回静止图像。
需要固定太阳时改用 `sun_azimuth_deg`（自北顺时针）与 `sun_altitude_deg`（地平线以上），两者必须同时给出，会把太阳设置切到光照模式。
`ground_plane` 开关地面平面，`ground_plane_level` 指定地面所在的标高；Revit 只接受它认定为地面平面的标高，因此传入其他标高时该标高会被标记为地面平面，响应会说明这一点。
`background` 取 `sky` 或 `gradient`，对三维、剖切和立面视图有效；`background_colors` 依次给出渐变的天顶、地平线、地面三色（#RRGGBB），省略时沿用当前渐变，或使用浅天空到地面的默认渐变。
`lighting_scheme` 设置渲染光源：exterior-sun、exterior-sun-and-artificial、exterior-artificial、interior-sun、interior-sun-and-artificial 或 interior-artificial。
太阳与阴影设置属于视图；共享这些设置的视图读数为 sunSettingsShared true，改动会一并作用到共享该设置的所有视图。
`dry_run` 会执行操作后回滚，在不改变模型的情况下返回相同的验证数据块。
同时打开多个模型时，传入 `document` 以指定目标模型；未知或有歧义的引用会被拒绝。

## Revit 年份支持 {#year-support}

| Revit 年份 | 验证状态 |
| --- | --- |
| 2020 | <span class="state ok">已实测</span> |
| 2026 | <span class="state part">仅构建，未实测</span> |
| 2022–2025 / 2027 | <span class="state part">仅构建，未实测</span> |

已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。

---

[全部功能](index.md) · [版本支持矩阵](matrix.md) · [提示词库](prompts.md)
