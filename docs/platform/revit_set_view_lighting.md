---
description: "设置一个视图的阴影、太阳位置、地平面、背景与渲染光照方案；响应给出改动前后的读数与变化项清单。"
---

# 设置视图光照

`revit_set_view_lighting`

<p class="facts"><span><b>分组</b> 视图、图纸与明细表</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 自研（本仓库） · 已移植</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 1.0.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 有，参数一致</span><span><b>本页契约适用于发布版</b> 否</span></p>

!!! note "使用提示"
    已通过 fork 注册表接上七个兜底钩子，Python 工具注册与单元测试通过；C# 编译与真机验证仍在 Windows CI 与工作站上。

设置一个视图的阴影、太阳位置、地平面、背景与渲染光照方案；响应给出改动前后的读数与变化项清单。

[同名发布版页面](../features/revit_set_view_lighting.md)

## 与发布版的契约差异 {#contract-diff}

同名工具的契约与发布版 1.0.0 一致。

## 参数 {#parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `background` | 否 | `null` | any | （集成分支契约未提供说明） |
| `background_colors` | 否 | `null` | any | （集成分支契约未提供说明） |
| `dry_run` | 否 | `false` | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `ground_plane` | 否 | `null` | any | （集成分支契约未提供说明） |
| `ground_plane_level` | 否 | `null` | any | （集成分支契约未提供说明） |
| `lighting_scheme` | 否 | `null` | any | （集成分支契约未提供说明） |
| `shadow_intensity` | 否 | `null` | any | （集成分支契约未提供说明） |
| `shadows` | 否 | `null` | any | （集成分支契约未提供说明） |
| `sun_altitude_deg` | 否 | `null` | any | （集成分支契约未提供说明） |
| `sun_azimuth_deg` | 否 | `null` | any | （集成分支契约未提供说明） |
| `sun_date` | 否 | `null` | any | （集成分支契约未提供说明） |
| `sun_time` | 否 | `null` | any | （集成分支契约未提供说明） |
| `sunlight_intensity` | 否 | `null` | any | （集成分支契约未提供说明） |
| `view` | 是 | — | string | 视图的准确名称或十进制视图 ID。 |

</div>

### 通用参数 {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| 参数 {scope=col} | 必填 {scope=col} | 默认值 {scope=col} | 类型 {scope=col} | 说明 {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | 否 | `null` | any | 打开多个模型时，用标题或路径指定目标文档。 |

</div>

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Set the lighting of one view: shadows, sun position, ground plane, background and the rendering lighting scheme.

`view` is an exact non-template view name or its decimal view ID, as revit_list_views reports it; a view without sun and shadow settings is refused.
Every other argument is optional and only the ones you pass change; the response reports the readings before and after under verification.before.lighting and verification.after.lighting, and names what moved in changedSettings.
`shadows` switches the view's per-view sun and shadow display: with it off Revit draws neither the sun path nor cast shadows, so the intensity settings stop showing; Revit exposes no API for the Graphic Display Options Shadows checkbox, so this per-view switch is the only shadow switch the tool can write, and a view whose sun and shadow settings are shared is refused.
`shadow_intensity` is 0 (no cast shadow) to 100 (black) and `sunlight_intensity` is 0 to 100.
`sun_date` (yyyy-MM-dd) and `sun_time` (24-hour HH:mm) fix a still-image sun position and are handed to Revit as local time; the readings report the stored instant as sunDateAndTimeUtc with the project time zone. Passing one keeps the other half, and both switch a sun study back to a still image.
`sun_azimuth_deg` (clockwise from north) and `sun_altitude_deg` (degrees above the horizon) set a fixed lighting-study sun instead, and must be passed together.
`ground_plane` uses the ground plane and `ground_plane_level` names its level; a level Revit does not already hold as a ground plane is marked as one and the response says so.
`background` is `sky` or `gradient` and works on 3D, section and elevation views; `background_colors` gives the three gradient colors as #RRGGBB (sky, horizon, ground).
`lighting_scheme` sets the rendering lighting source: exterior-sun, exterior-sun-and-artificial, exterior-artificial, interior-sun, interior-sun-and-artificial or interior-artificial.
Sun and shadow settings belong to the view; a view that shares them reports sunSettingsShared true and passes the change on to every view that shares them.
dry_run executes and rolls back, returning the same verification block without changing the model.
`document` addresses one specific open model when several are open; an unknown or ambiguous reference is rejected.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
