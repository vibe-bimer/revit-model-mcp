# revit_merge_phases

<p class="facts"><b>Group</b> Phases　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.3.0</p>

Merge one project phase into another by moving every element reference.

!!! note "Notes"
    Cannot run inside batch

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `source_phase` ✔ | — | the phase that is merged away and then deleted（string） |
| `target_phase` ✔ | — | the phase that receives the references（string） |
| `dry_run` | `false` | boolean |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## Prompts

```text
Merge phase 1 into New Construction
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state part">build only</span> | Cannot run inside batch |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
