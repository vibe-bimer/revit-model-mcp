# revit_view_elements

<p class="facts"><b>Group</b> Views and snapshots　<b>Kind</b> Read (read-only)　<b>Since</b> 0.2.0</p>

Read one page of elements in a selected view.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `view` ✔ | — | string — Required exact, case-sensitive non-template view name from revit_list_views, or its Revit view ID as a decimal string; no default. An exact name takes precedence over interpreting a numeric string as an ID. |
| `categories` | — | any |
| `limit` | `100` | integer |
| `offset` | `0` | integer |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted. |
    | `pickup_timeout_seconds` | `300` | integer — Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later. |
    | `timeout_seconds` | `120` | integer — Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits. |

## Prompts

```text
Page through the elements of the 3D view, 200 at a time
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
