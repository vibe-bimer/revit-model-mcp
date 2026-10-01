# Set view lighting

`revit_set_view_lighting`

<p class="facts"><span><b>Group</b> Views and snapshots</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.10.0</span><span><b>Effect</b> Model elements / parameters</span></p>

Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Sun and shadow settings belong to the view; a shared setting passes the change on to every view that shares it, and the shadow switch itself is unavailable when they are shared

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

| Parameter | Required | Default | Type | Meaning |
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

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Set the lighting of one view: shadows, sun position, ground plane, background and the rendering lighting scheme.

`view` is an exact non-template view name or its decimal view ID, as revit_list_views reports it; a view without sun and shadow settings is refused.
Every other argument is optional and only the ones you pass change; the response reports the readings before and after under verification.before.lighting and verification.after.lighting, and names what moved in changedSettings.
`shadows` switches the view's per-view sun and shadow display: with it off Revit draws neither the sun path nor cast shadows, so the intensity settings stop showing; Revit exposes no API for the Graphic Display Options Shadows checkbox itself, so this per-view switch is the only shadow switch the tool can write, and a view whose sun and shadow settings are shared is refused.
`shadow_intensity` is 0 (no cast shadow) to 100 (black) and `sunlight_intensity` is 0 to 100.
`sun_date` (yyyy-MM-dd) and `sun_time` (24-hour HH:mm) fix a still-image sun position and are handed to Revit as local time; the readings report the stored instant as sunDateAndTimeUtc with the project time zone, so what Revit kept is always checkable. Passing one keeps the other half of what the view already shows, and both switch a sun study back to a still image.
`sun_azimuth_deg` (clockwise from north) and `sun_altitude_deg` (degrees above the horizon) set a fixed lighting-study sun instead, and must be passed together.
`ground_plane` uses the ground plane and `ground_plane_level` names the level it sits on; Revit only accepts a level it knows as a ground plane, so a level that is not one is marked as a ground plane and the response says so.
`background` is `sky` or `gradient` and works on 3D, section and elevation views; `background_colors` gives the three gradient colors as #RRGGBB (sky, horizon, ground) and defaults to the current gradient or a light sky-to-ground ramp.
`lighting_scheme` sets the rendering lighting source: exterior-sun, exterior-sun-and-artificial, exterior-artificial, interior-sun, interior-sun-and-artificial or interior-artificial.
Sun and shadow settings belong to the view; a view that shares them reports sunSettingsShared true and passes the change on to every view that shares them.
dry_run executes and rolls back, returning the same verification block without changing the model.
Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
