# revit_place_family

<p class="facts"><b>Group</b> Editing　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.2.0</p>

Place a loaded unhosted family on a named level for layout.

!!! note "Notes"
    Not run live on 2026

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `family` ✔ | — | family name（string） |
| `level` ✔ | — | level name, as revit_list_catalog reports it（string） |
| `type_name` ✔ | — | type name, together with the family（any） |
| `x_mm` ✔ | — | model X in millimetres（number） |
| `y_mm` ✔ | — | model Y in millimetres（number） |
| `dry_run` | `false` | rehearse: execute, return the same verification block, then roll back（boolean） |
| `rotation_deg` | `0` | rotation about Z in degrees（number） |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## Prompts

```text
Place a 900x2100 door at 3000,4000 on 1F
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state part">build only</span> | Not run live on 2026 |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
