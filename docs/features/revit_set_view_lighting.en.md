---
description: "Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme"
---

# Set view lighting

`revit_set_view_lighting`

<p class="facts"><span><b>Group</b> Views and snapshots</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.10.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span><span><b>Origin</b> Fork (this repository)</span></p>

Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Sun and shadow settings belong to the view; a shared setting passes the change on to every view that shares it, and the shadow switch itself is unavailable when they are shared

[Same-name integration branch page](../platform/revit_set_view_lighting.md)

## Copyable prompts {#prompts}

```text
Turn on shadows in the 3D view, set the shadow intensity to 60, use a sky background and light the rendering with exterior sun
```

```text
Set the sun in {3D} to 2026-06-21 15:00 with a sunlight intensity of 80, and rehearse it first
```

```text
Fix the sun in lighting mode at azimuth 135° and altitude 45°, and turn on the ground plane at level 01
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | `string` | view name as revit_list_views reports it, or its decimal view ID; a non-template view |
| `background` | No | `null` | `string / null` | view background: sky or gradient, on 3D, section and elevation views only |
| `background_colors` | No | `null` | `array<string> / null` | gradient colors (sky, horizon, ground), for example #C8DEF0 |
| `dry_run` | No | `false` | `boolean` | rehearse: change, read, then roll back, returning the same readings as a real write |
| `ground_plane` | No | `null` | `boolean / null` | whether the sun and shadow settings use a ground plane |
| `ground_plane_level` | No | `null` | `string / null` | level the ground plane sits on; a level Revit does not accept is marked as a ground plane |
| `lighting_scheme` | No | `null` | `string / null` | rendering lighting source: exterior or interior, with sun, artificial light or both |
| `shadow_intensity` | No | `null` | `integer / null` | cast shadow intensity from 0 to 100, where 0 means no cast shadow |
| `shadows` | No | `null` | `boolean / null` | the view's sun and shadow display switch; off draws neither the sun path nor cast shadows, which also mutes the intensities; a view that shares its settings refuses it |
| `sun_altitude_deg` | No | `null` | `number / null` | lighting-mode sun altitude above the horizon, from -90 to 90 |
| `sun_azimuth_deg` | No | `null` | `number / null` | lighting-mode sun azimuth clockwise from north; pass it with the altitude |
| `sun_date` | No | `null` | `string / null` | still-image date as yyyy-MM-dd, handed to Revit as local time; the reading reports it as UTC with the time zone |
| `sun_time` | No | `null` | `string / null` | still-image time as 24-hour HH:mm, handed to Revit as local time; the reading reports it as UTC with the time zone |
| `sunlight_intensity` | No | `null` | `integer / null` | simulated sunlight intensity from 0 to 100 |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Set a view's lighting: shadows, sun position, ground plane, background and lighting scheme.

View-specific sun and shadow settings; a view that shares them passes the change on.
Sun angles come as a pair, and gradient colors need the gradient background.
dry_run returns the same verification block without changing the model.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
