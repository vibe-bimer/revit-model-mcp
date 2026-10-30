# Set View Lighting

`revit_set_view_lighting`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Fork (this repository) · Grafted</span><span><b>In the current release</b> Yes</span></p>

!!! note "Usage notes"
    Attached through the fork registry and the seven fallback hooks; the Python tool and its unit tests pass. C# compilation and live validation still happen on Windows CI and the workstation.

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `background` | No | None | any |  |
| `background_colors` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `ground_plane` | No | None | any |  |
| `ground_plane_level` | No | None | any |  |
| `lighting_scheme` | No | None | any |  |
| `shadow_intensity` | No | None | any |  |
| `shadows` | No | None | any |  |
| `sun_altitude_deg` | No | None | any |  |
| `sun_azimuth_deg` | No | None | any |  |
| `sun_date` | No | None | any |  |
| `sun_time` | No | None | any |  |
| `sunlight_intensity` | No | None | any |  |
| `view` | Yes | — | string |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any |  |

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
