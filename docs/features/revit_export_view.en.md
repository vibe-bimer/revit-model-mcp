# revit_export_view

<p class="facts"><b>Group</b> Views and snapshots　<b>Kind</b> Read (read-only)　<b>Since</b> 0.3.0</p>

Export a selected view to PNG when numbers do not explain geometry.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `view` ✔ | — | string — Required exact, case-sensitive non-template view name from revit_list_views, or its Revit view ID as a decimal string; no default. An exact name takes precedence over interpreting a numeric string as an ID. |
| `pixel_size` | `1600` | integer — PNG size in pixels along the fitted image dimension, an integer from 1 to 4000. Default 1600 fits the view at that size while preserving its aspect ratio. |
| `save_to` | — | any — New PNG file path on the MCP client machine, not the Revit host; an existing destination causes an error. Default null downloads to a local temporary directory and returns localPath. |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted. |

## Prompts

```text
Export the 1F plan as a PNG, 2000 pixels wide
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
