# revit_create_wall

<p class="facts"><b>Group</b> Editing　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.2.0</p>

Create a straight wall for layout on a named level; model XY endpoints and height are millimetres; null wall_type chooses the first basic type. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `end_mm` ✔ | — | end point [x, y] in millimetres（array） |
| `level` ✔ | — | level name, as revit_list_catalog reports it（string） |
| `start_mm` ✔ | — | start point [x, y] in millimetres（array） |
| `wall_type` ✔ | — | Create a straight wall for layout on a named level; model XY endpoints and height are millimetres; null wall_type chooses the first basic type.（any） |
| `dry_run` | `false` | rehearse: execute, return the same verification block, then roll back（boolean） |
| `height_mm` | `3000` | wall height in millimetres (3000 by default)（number） |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## Prompts

```text
Draw a 200 mm wall on 1F from 0,0 to 6000,0
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
