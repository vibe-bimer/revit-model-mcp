# revit_set_parameter

<p class="facts"><b>Group</b> Editing　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.1.0</p>

Set a named instance parameter, falling back to its shared type; use for edits, with length in mm, area in m2 and other doubles in internal units. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

!!! note "Notes"
    Supports dry_run

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `element_id` ✔ | — | one element id（integer） |
| `parameter` ✔ | — | parameter name as the model reports it（string） |
| `value` ✔ | — | value to write; lengths in millimetres, areas in m², other doubles in internal units（string） |
| `dry_run` | `false` | rehearse: execute, return the same verification block, then roll back（boolean） |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## Prompts

```text
Set the fire rating of these walls to two hours
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
