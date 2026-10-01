# revit_list_views

<p class="facts"><b>Group</b> Views and snapshots　<b>Kind</b> Read (read-only)　<b>Since</b> 0.1.0</p>

Find non-template views before analyzing a view.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `name_contains` | — | any — Case-insensitive substring of the view name. Default null applies no name filter; combines with view_type and excludes templates. |
| `view_type` | — | any — English Revit ViewType name, such as FloorPlan or ThreeD, matched case-insensitively. Default null includes all non-template view types; combines with name_contains. |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted. |
    | `pickup_timeout_seconds` | `300` | integer — Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later. |
    | `timeout_seconds` | `120` | integer — Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits. |

## Prompts

```text
List every floor plan view
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
