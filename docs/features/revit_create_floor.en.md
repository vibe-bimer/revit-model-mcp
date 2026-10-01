# revit_create_floor

<p class="facts"><b>Group</b> Editing　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.2.0</p>

Create a floor from a closed boundary for layout on a named level. points_mm are model XY polygon vertices in millimetres (at least 3; the boundary closes automatically); null floor_type chooses the first floor type. dry_run executes and rolls back, returning the same verification block without changing the model. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

!!! note "Notes"
    On 2020 it uses Document.Create.NewFloor, from 2022 Floor.Create

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `floor_type` ✔ | — | points_mm are model XY polygon vertices in millimetres (at least 3; the boundary closes automatically); null floor_type chooses the first floor type.（any） |
| `level` ✔ | — | level name, as revit_list_catalog reports it（string） |
| `points_mm` ✔ | — | points_mm are model XY polygon vertices in millimetres (at least 3; the boundary closes automatically); null floor_type chooses the first floor type.（array） |
| `dry_run` | `false` | rehearse: execute, return the same verification block, then roll back（boolean） |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## Prompts

```text
Create a floor on 2F from these four points
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state part">build only</span> | On 2020 it uses Document.Create.NewFloor, from 2022 Floor.Create |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
