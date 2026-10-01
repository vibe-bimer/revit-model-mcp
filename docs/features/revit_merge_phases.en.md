# Merge project phases

`revit_merge_phases`

<p class="facts"><span><b>Group</b> Phases</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.3.0</span><span><b>Effect</b> Model elements / parameters</span></p>

Reassign references to another phase and attempt to delete the emptied phase

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Cannot run inside batch

## Copyable prompts {#prompts}

```text
Merge phase 1 into New Construction
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `source_phase` | Yes | — | `string` | the phase that is merged away and then deleted |
| `target_phase` | Yes | — | `string` | the phase that receives the references |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Merge one project phase into another by moving every element reference.

Elements created in the source phase are reassigned to the target phase,
demolitions recorded in the source phase move to the target, then the empty
source phase is deleted. Revit may refuse the deletion when views or other
objects still reference it; the response then reports reassigned counts with
sourceDeleted:false. Phases themselves are never created or renamed here.
dry_run executes and rolls back, returning the same verification block without changing the model.
Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
