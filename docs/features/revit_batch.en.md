# revit_batch

<p class="facts"><b>Group</b> Batch and ids　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.2.0</p>

Execute up to 50 actions with one undo step; roll back the batch on its first failure.

!!! note "Notes"
    Rolls the whole batch back when a step fails

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `steps` ✔ | — | array |
| `dry_run` | `false` | boolean |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change. |

## Prompts

```text
Move and retag these ten elements as one undo step
```

```text
Show this batch of changes as a dry run first
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
