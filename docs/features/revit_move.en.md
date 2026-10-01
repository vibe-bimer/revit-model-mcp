# revit_move

<p class="facts"><b>Group</b> Editing　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.1.0</p>

Move elements when adjusting their position; dx_mm, dy_mm and dz_mm are offsets in millimetres on model axes. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

!!! note "Notes"
    Supports dry_run

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `dx_mm` ✔ | — | number |
| `dy_mm` ✔ | — | number |
| `element_ids` ✔ | — | array |
| `dry_run` | `false` | boolean |
| `dz_mm` | `0` | number |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change. |

## Prompts

```text
Move these three elements 500 mm along X, dry run first
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
