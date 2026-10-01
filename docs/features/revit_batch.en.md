# Batch actions

`revit_batch`

<p class="facts"><span><b>Group</b> Batch and ids</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.2.0</span><span><b>Effect</b> Model elements / parameters</span></p>

Execute 1–50 actions as one undo step and roll back on the first failed step

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Rolls the whole batch back when a step fails

## Copyable prompts {#prompts}

```text
Move and retag these ten elements as one undo step
```

```text
Show this batch of changes as a dry run first
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `steps` | Yes | — | `array<any>` | one to fifty action steps; the batch rolls back when a step fails |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Execute up to 50 actions with one undo step; roll back the batch on its first failure.

dry_run executes and rolls back, returning the same verification block without changing the model.
Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
