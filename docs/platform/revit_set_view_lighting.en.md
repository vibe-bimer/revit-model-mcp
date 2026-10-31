---
description: "Set the lighting of one view: shadows, sun position, ground plane, background and the rendering lighting scheme. `view` is an exact non-template view name or its decimal view ID, as revit_list_views reports it; a view without sun and shadow settings is refused. Every other argument is optional and only the ones you pass change; the response reports the readings before and after under verification.before.lighting and verification.after.lighting, and names what moved in changedSettings. `shadows` switches the view's per-view sun and shadow display: with it off Revit draws neither the sun path nor cast shadows, so the intensity settings stop showing; Revit exposes no API for the Graphic Display Options Shadows checkbox, so this per-view switch is the only shadow switch the tool can write, and a view whose sun and shadow settings are shared is refused. `shadow_intensity` is 0 (no cast shadow) to 100 (black) and `sunlight_intensity` is 0 to 100. `sun_date` (yyyy-MM-dd) and `sun_time` (24-hour HH:mm) fix a still-image sun position and are handed to Revit as local time; the readings report the stored instant as sunDateAndTimeUtc with the project time zone. Passing one keeps the other half, and both switch a sun study back to a still image. `sun_azimuth_deg` (clockwise from north) and `sun_altitude_deg` (degrees above the horizon) set a fixed lighting-study sun instead, and must be passed together. `ground_plane` uses the ground plane and `ground_plane_level` names its level; a level Revit does not already hold as a ground plane is marked as one and the response says so. `background` is `sky` or `gradient` and works on 3D, section and elevation views; `background_colors` gives the three gradient colors as #RRGGBB (sky, horizon, ground). `lighting_scheme` sets the rendering lighting source: exterior-sun, exterior-sun-and-artificial, exterior-artificial, interior-sun, interior-sun-and-artificial or interior-artificial. Sun and shadow settings belong to the view; a view that shares them reports sunSettingsShared true and passes the change on to every view that shares them. dry_run executes and rolls back, returning the same verification block without changing the model. `document` addresses one specific open model when several are open; an unknown or ambiguous reference is rejected."
---

# Set View Lighting

`revit_set_view_lighting`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Fork (this repository) · Grafted</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, but the parameters differ</span><span><b>This contract applies to the release</b> No</span></p>

!!! note "Usage notes"
    Attached through the fork registry and the seven fallback hooks; the Python tool and its unit tests pass. C# compilation and live validation still happen on Windows CI and the workstation.

[Same-name release page](../features/revit_set_view_lighting.md)

## Contract differences from the release {#contract-diff}

The table below is computed from the registry inputSchema; it is not a hand-written list.

- Parameter ground_plane_level (anyOf[0]) pattern: release \S / integration —
- Parameter view pattern: release \S / integration —

This contract belongs to the integration branch, not to release 0.9.0; copying the branch parameters fails on the release.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} |
| --- | :--: | --- | --- |
| `background` | No | `null` | any |
| `background_colors` | No | `null` | any |
| `dry_run` | No | `false` | boolean |
| `ground_plane` | No | `null` | any |
| `ground_plane_level` | No | `null` | any |
| `lighting_scheme` | No | `null` | any |
| `shadow_intensity` | No | `null` | any |
| `shadows` | No | `null` | any |
| `sun_altitude_deg` | No | `null` | any |
| `sun_azimuth_deg` | No | `null` | any |
| `sun_date` | No | `null` | any |
| `sun_time` | No | `null` | any |
| `sunlight_intensity` | No | `null` | any |
| `view` | Yes | — | string |

</div>

The branch contract ships no parameter descriptions.

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} |
| --- | :--: | --- | --- |
| `document` | No | `null` | any |

</div>

The branch contract ships no parameter descriptions.

## Behavior (registry text) {#behavior}

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

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
