# revit_select

<p class="facts"><b>Group</b> Selection and display　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.1.0</p>

Select element IDs for inspection in Revit; an empty list clears selection; IDs are unitless. Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

!!! note "Notes"
    Does not change the model

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `element_ids` ✔ | — | array |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change. |

## Prompts

```text
Select element 123456
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
