---
description: "Colour elements in selected views; reset restores this session's overrides"
---

# Highlight elements

`revit_override_graphics`

<p class="facts"><span><b>Group</b> Selection and display</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Selection / view state</span></p>

Colour elements in selected views; reset restores this session's overrides

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_override_graphics.md)

## Copyable prompts {#prompts}

```text
Colour these columns red in the Level 1 plan and halftone the rest
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `element_ids` | Yes | — | `array<integer>` | element ids (unitless Revit ids) |
| `color` | No | `"#FF0000"` | `string` | hex colour applied by the override, such as |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `fill` | No | `true` | `boolean` | fill the graphics override |
| `halftone_others` | No | `false` | `boolean` | Whether other elements are drawn in halftone. |
| `line_weight` | No | `null` | `integer / null` | line weight value to override |
| `reset` | No | `false` | `boolean` | Set true with an empty element_ids list to reset temporary hide/isolate in the active view |
| `transparency` | No | `0` | `integer` | transparency percentage of the override colour, 0 to 100 |
| `views` | No | `"active"` | `string / array<string / integer>` | views to override; `active` means the active view |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Colour elements in selected model views; reset restores overrides saved in this Revit session.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
