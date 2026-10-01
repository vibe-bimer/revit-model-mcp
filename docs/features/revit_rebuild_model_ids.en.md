# Rebuild IDs in new models

`revit_rebuild_model_ids`

<p class="facts"><span><b>Group</b> Batch and ids</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.8.0</span><span><b>Effect</b> New model files; source unchanged</span></p>

Copy selectable 3D-view components into one or more new models with fresh IDs

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    The source stays unchanged; only selectable 3D-view elements and required datums are copied, not the full project; check every count and ID mapping

## Copyable prompts {#prompts}

```text
Rebuild the selectable components into E:\out\copy-{n}.rvt, ten copies, no id shared between them
```

```text
Rehearse the rebuild first: how many components, which new id range, write nothing yet
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `destination_path` | Yes | — | `string` | new model path (.rvt); {n} numbers the copies |
| `copies` | No | `1` | `integer` | how many copies one new model produces (1–50), each in an id block of its own |
| `dry_run` | No | `false` | `boolean` | rehearse in a temporary new document and report the mapping without saving; the source always stays unchanged |
| `duplicate_names` | No | `"override"` | `string` | duplicate names: override keeps the source types, reuse keeps the version the new model holds (the batch default), rename is the legacy path |
| `overwrite` | No | `false` | `boolean` | replace the destination when it exists |
| `remove_template_levels` | No | `true` | `boolean` | drop the template levels after copying (on by default) |
| `seed` | No | `0` | `integer` | create and remove N temporary levels to advance new-document IDs; use different seeds across runs and verify overlap in the mappings |
| `template_path` | No | `null` | `string / null` | starting template (.rte/.rvt); the metric template is used when omitted |
| `view` | No | `null` | `string / null` | view name (or its Revit id) |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Give every component new IDs by copying a 3D view's selectable elements into a new model, because Revit does not allow assigning an element ID.

The open model is never modified: the result is written to `destination_path` on the workstation, and the source stays as it is.
`view` chooses the 3D view to read; without it the first non-perspective 3D view is used, and only the elements that view can select are copied.
Levels, grids and reference planes travel so hosts resolve; cameras, the sun path, the section box, views and elements without a category are left behind and reported under excluded.
Views, sheets, schedules, annotations, phases, worksets, MEP systems and any unselected host do not travel, so the result is geometry, types and parameters.
Data carries destinationPath, saved, count, sourceView, sourceElementCount, datumCount, sourceCategoryCounts, copiedCategoryCounts, newIdMin/newIdMax, idMapping (old to new, verified against category and type) and excluded elements with a reason each.
`overwrite` replaces an existing file, `template_path` starts the copy from a template instead of the default metric template, and remove_template_levels drops the template's own levels.
`seed` adds that many temporary levels to the new model before the copy and removes them again, which moves the new IDs into their own block: rebuilding the same source twice otherwise yields the same IDs, so pass a different seed per copy (for example 0, 1000, 2000) when you need copies whose IDs do not overlap.
`duplicate_names` decides what happens when the new project already holds a name the source pastes: `override` answers Revit's question with OK so the copy keeps the source's own types, `rename` renames the template's elements first and removes them again afterwards, which is slower and can fail on elements Revit refuses to delete.
`copies` writes that many files from one new model: every copy holds the same components with ids of its own, because each copy's ids start after the copy before it. The copies are written to `destination_path` with `{n}` replaced by the copy number, or with the number appended before the extension when the path has no `{n}`; each copy's own mapping is reported under `copyResults`, and the per-copy phase timings are in the plugin log.
`dry_run` performs the copy and reports the mapping without saving a file.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
