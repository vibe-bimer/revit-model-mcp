# revit_set_phase

<p class="facts"><b>Group</b> Phases　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.3.0</p>

Assign the created or demolished project phase of elements by exact phase name.

!!! note "Notes"
    The phase order API exists from 2022; 2020 uses a fallback

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `created_phase` ✔ | — | any |
| `demolished_phase` ✔ | — | any |
| `element_ids` ✔ | — | array |
| `dry_run` | `false` | boolean |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## Prompts

```text
Mark these elements as demolished in the Existing phase
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state part">build only</span> | The phase order API exists from 2022; 2020 uses a fallback |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
