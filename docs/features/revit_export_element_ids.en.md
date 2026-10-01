# revit_export_element_ids

<p class="facts"><b>Group</b> Export and checks　<b>Kind</b> Read (read-only)　<b>Since</b> 0.8.0</p>

Write the identifier register of the drawn components to an xlsx file on the Revit workstation.

!!! note "Notes"
    The workbook is written on the Revit workstation

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `fields` | — | columns to write; the defaults are category, family, type, level, component id, name and workset（any） |
| `save_to` | — | absolute .xlsx path on the Revit workstation; an existing file is an error（any） |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |
    | `pickup_timeout_seconds` | `300` | Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later.（integer） |
    | `timeout_seconds` | `120` | Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits.（integer） |

## Prompts

```text
Export the 3D view components to Excel, ordered by category and family
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
