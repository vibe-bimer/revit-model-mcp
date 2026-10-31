---
description: "Tag elements by category or element ids in a view; room tags need a plan view"
---

# Tag elements

`revit_tag_elements`

<p class="facts"><span><b>Group</b> Selection and display</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Selection / view state</span></p>

Tag elements by category or element ids in a view; room tags need a plan view

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_tag_elements.md)

## Copyable prompts {#prompts}

```text
Tag every door on the Level 1 plan
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | `string / integer` | view name (or its Revit id) |
| `categories` | No | `null` | `array<string> / null` | category names, combined with OR |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `element_ids` | No | `null` | `array<integer> / null` | element ids (unitless Revit ids) |
| `leader` | No | `false` | `boolean` | whether to add a leader to the tag |
| `max_elements` | No | `5000` | `integer` | maximum number of elements tagged in one call |
| `orientation` | No | `"horizontal"` | `string` | tag orientation: `horizontal` or `vertical` |
| `skip_tagged` | No | `true` | `boolean` | Whether already tagged elements are skipped. |
| `tag_type` | No | `null` | `string / null` | tag type to place |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Tag elements in a view, chosen by category names or by element IDs (exactly one of the two). Returns created tag IDs in createdElementIds; already tagged elements are skipped unless skip_tagged is false, and untaggable inputs are listed in skipped. tag_type matches a tag type name, a family name or "Family: Type"; the default tag type is used otherwise. Room tags need a plan view. dry_run rolls back and returns the tags that would be created.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
