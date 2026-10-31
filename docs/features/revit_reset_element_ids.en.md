---
description: "Replace eligible standalone elements with copies to obtain new IDs"
---

# Replace IDs in place

`revit_reset_element_ids`

<p class="facts"><span><b>Group</b> Batch and ids</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.8.0</span><span><b>Version</b> Released 0.9.0</span><span><b>Same-name tool on the integration branch</b> No</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span><span><b>Origin</b> Fork (this repository)</span></p>

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

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `element_ids` | Yes | — | `array<integer>` | elements to replace; hosted, dependent, grouped or MEP system members are refused |
| `dry_run` | No | `false` | `boolean` | rehearse: replace, report the mapping, then roll back |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Give elements new element IDs by copying each one over its original.

The API cannot assign an element ID, so every element is copied, checked and then replaces
its original. Elements that cannot be replaced are refused by name, and a real run is
refused when any element in the selection is. dry_run returns the same block without keeping
the changes.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
