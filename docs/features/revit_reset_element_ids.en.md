# revit_reset_element_ids

<p class="facts"><b>Group</b> Batch and ids　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.8.0</p>

Replace elements with copies so Revit assigns new element IDs; the API cannot assign one itself.

!!! note "Notes"
    Limited coverage: MEP 27/1089, building 373/954, structure 0%

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `element_ids` ✔ | — | array |
| `dry_run` | `false` | boolean |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## Prompts

```text
Give these 27 standalone components new ids
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state part">build only</span> | Limited coverage: MEP 27/1089, building 373/954, structure 0% |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
