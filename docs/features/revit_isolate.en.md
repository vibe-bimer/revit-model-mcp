# Temporary isolation

`revit_isolate`

<p class="facts"><span><b>Group</b> Selection and display</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.2.0</span><span><b>Effect</b> Selection / view state</span></p>

Temporarily isolate selected elements or reset the active view

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    Temporary effect only

## Copyable prompts {#prompts}

```text
Isolate the windows of this level
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `element_ids` | Yes | — | `array<integer>` | element ids to isolate; combine with reset=true to restore |
| `reset` | No | `false` | `boolean` | Set true with an empty element_ids list to reset temporary hide/isolate in the active view |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

Temporarily isolate IDs for visual review in the active view, or reset with an empty list; IDs are unitless.
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
