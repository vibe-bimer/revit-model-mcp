# Set view lighting

Set a view's shadows, sun position and intensities, ground plane, background and rendering lighting scheme.

**Group:** View settings · **Kind:** Action (opt-in) · **Since:** this fork's 1.0.0

This fork adds this tool; the rest of the catalogue comes from upstream 1.0.

!!! warning "Runs only on a read-write workstation"

    An action runs only while the workstation is not read-only: the machine policy
    gate refuses action calls over every transport. The gate is the policy's
    `ReadOnly` value, held in the registry under
    `HKLM\Software\Policies\RevitModelMcp` or in
    `%ProgramData%\RevitModelMcp\policy.json`. The multi-user installer sets `ReadOnly`
    to `1` by default and writes the default `policy.json`, so a fresh machine install
    refuses actions until an administrator allows writes; a per-user install writes no
    policy (adr/0008). When both stores exist, the
    registry value wins for every value it sets, and a policy that cannot be read
    fails closed to read-only. The call names its target document, and with more
    than one open document it is refused. `dry_run` returns the same verification
    block without changing the model.

!!! note "Usage notes"

    Sun and shadow settings belong to the view; a shared setting passes the change on to every view that shares it, and the shadow switch itself is unavailable when they are shared.

## Copyable prompts

```text
Turn on shadows in the 3D view, set the shadow intensity to 60, use a sky background and light the rendering with exterior sun
```

```text
Set the sun in {3D} to 2026-06-21 15:00 with a sunlight intensity of 80, and rehearse it first
```

```text
Fix the sun in lighting mode at azimuth 135° and altitude 45°, and turn on the ground plane at level 01
```

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `view` | Yes | — | `string` | view name as revit_list_views reports it, or its decimal view id; a non-template view |
| `background` | No | null | `string (sky, gradient) / null` | view background: sky or gradient, on 3D, section and elevation views only |
| `background_colors` | No | null | `array of string / null` | gradient colors (sky, horizon, ground), for example #C8DEF0 |
| `dry_run` | No | false | `boolean` | rehearse: change, read, then roll back, returning the same readings as a real write |
| `ground_plane` | No | null | `boolean / null` | whether the sun and shadow settings use a ground plane |
| `ground_plane_level` | No | null | `string / null` | level the ground plane sits on; a level Revit does not accept is marked as a ground plane |
| `lighting_scheme` | No | null | `string (exterior-sun, exterior-sun-and-artificial, exterior-artificial, interior-sun, interior-sun-and-artificial, interior-artificial) / null` | rendering lighting source: exterior or interior, with sun, artificial light or both |
| `shadow_intensity` | No | null | `integer / null` | cast shadow intensity from 0 to 100, where 0 means no cast shadow |
| `shadows` | No | null | `boolean / null` | the view's sun and shadow display switch; off draws neither the sun path nor cast shadows, which also mutes the intensities; a view that shares its settings refuses it |
| `sun_altitude_deg` | No | null | `number / null` | lighting-mode sun altitude above the horizon, from -90 to 90 |
| `sun_azimuth_deg` | No | null | `number / null` | lighting-mode sun azimuth clockwise from north; pass it with the altitude |
| `sun_date` | No | null | `string / null` | still-image date as yyyy-MM-dd, handed to Revit as local time; the reading reports it as UTC with the time zone |
| `sun_time` | No | null | `string / null` | still-image time as 24-hour HH:mm, handed to Revit as local time; the reading reports it as UTC with the time zone |
| `sunlight_intensity` | No | null | `integer / null` | simulated sunlight intensity from 0 to 100 |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Set a view's lighting: shadows, sun position, ground plane, background and lighting scheme.

View-specific sun and shadow settings; a view that shares them passes the change on.
Sun angles come as a pair, and gradient colors need the gradient background.
dry_run returns the same verification block without changing the model.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
