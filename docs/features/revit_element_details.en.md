# revit_element_details

<p class="facts"><b>Group</b> Query and totals　<b>Kind</b> Read (read-only)　<b>Since</b> 0.1.0</p>

Read parameters and geometry of an element by Revit ID.

!!! note "Notes"
    Rooms also return area, volume and boundaries

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `element_id` ✔ | — | integer — Required positive integer Revit element ID from revit_query_elements or revit_view_elements; no default. The ID must exist in the target document. |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted. |
    | `pickup_timeout_seconds` | `300` | integer — Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later. |
    | `timeout_seconds` | `120` | integer — Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits. |

## Prompts

```text
Show every parameter and the geometry of element 357640
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
