# Replace IDs in place

`revit_reset_element_ids`

<p class="facts"><span><b>Group</b> Batch and ids</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.8.0</span><span><b>Effect</b> Model elements / parameters</span></p>

Replace eligible standalone elements with copies to obtain new IDs

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Run dry_run first; hosted, dependent, grouped and MEP-system elements are refused

## Copyable prompts {#prompts}

```text
Give these 27 standalone components new ids
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `element_ids` | Yes | — | `array<integer>` | elements to replace; hosted, dependent, grouped or MEP system members are refused |
| `dry_run` | No | `false` | `boolean` | rehearse: replace, report the mapping, then roll back |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Replace elements with copies so Revit assigns new element IDs; the API cannot assign one itself.

Returns data with count, idMapping (old to new) and ineligible elements with a reason each.
An element is refused when deleting it would delete dependents too, when it is hosted (copies are not rehosted), when it belongs to a group, when it is an MEP curve or MEP system member (the copy does not rejoin the network and Revit re-heals the run), or when Revit reports it cannot be copied.
dry_run executes and rolls back, returning the same verification block without changing the model; run it first, because the exchange cannot be undone.
A real run refuses the whole selection while any element is ineligible, so dependent elements cannot be destroyed by accident.
This never changes an element's ID in place and never writes the old ID into a parameter.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
