# revit_list_instances

<p class="facts"><b>Group</b> Connection and documents　<b>Kind</b> Read (read-only)　<b>Since</b> 0.6.0</p>

List Revit processes and their active documents.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | any — Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted. |

## Prompts

```text
Which Revit instances are running, and what does each hold?
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
