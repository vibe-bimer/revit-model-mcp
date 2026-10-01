# Set element phases

`revit_set_phase`

<p class="facts"><span><b>Group</b> Phases</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.3.0</span><span><b>Effect</b> Model elements / parameters</span></p>

Assign created/demolished phases; an empty string clears and null leaves unchanged

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    The phase order API exists from 2022; 2020 uses a fallback

## Copyable prompts {#prompts}

```text
Mark these elements as demolished in the Existing phase
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `created_phase` | Yes | — | `string / null` | created phase name; an empty string clears it, null leaves it |
| `demolished_phase` | Yes | — | `string / null` | demolished phase name; an empty string clears it, null leaves it unchanged |
| `element_ids` | Yes | — | `array<integer>` | element ids whose phase changes |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Assign the created or demolished project phase of elements by exact phase name.

Each phase argument is a phase name from revit_list_catalog(section="phases"),
an empty string to clear that assignment, or null to leave it unchanged;
at least one argument must be non-null. Creation APIs cannot add phases;
create new phases in the Revit UI first. Example: demolished_phase="现有"
marks elements demolished in that phase, demolished_phase="" clears it.
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
