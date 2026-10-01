# revit_rebuild_model_ids

<p class="facts"><b>Group</b> Batch and ids　<b>Kind</b> Action (changes the model)　<b>Since</b> 0.8.0</p>

Give every component new IDs by copying a 3D view's selectable elements into a new model, because Revit does not allow assigning an element ID.

!!! note "Notes"
    The source stays read-only; 899 components a copy, no shared ids

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `destination_path` ✔ | — | new model path (.rvt); {n} numbers the copies（string） |
| `copies` | `1` | how many copies one new model produces (1–50), each in an id block of its own（integer） |
| `dry_run` | `false` | rehearse: copy, report the mapping, then roll back without writing（boolean） |
| `duplicate_names` | `"override"` | duplicate names: override keeps the source types, reuse keeps the version the new model holds (the batch default), rename is the legacy path（string） |
| `overwrite` | `false` | replace the destination when it exists（boolean） |
| `remove_template_levels` | `true` | drop the template levels after copying (on by default)（boolean） |
| `seed` | `0` | push the ids N forward before copying, to reserve a block per run（integer） |
| `template_path` | — | starting template (.rte/.rvt); the metric template is used when omitted（any） |
| `view` | — | view name (or its Revit id)（any） |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.（any） |

## Prompts

```text
Rebuild the selectable components into E:\out\copy-{n}.rvt, ten copies, no id shared between them
```

```text
Rehearse the rebuild first: how many components, which new id range, write nothing yet
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state part">build only</span> | The source stays read-only; 899 components a copy, no shared ids |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
