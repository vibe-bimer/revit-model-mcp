---
description: "Change category, workset and filter visibility in one view, with a dry-run preview"
---

# Set View Visibility

`revit_set_view_visibility`

<p class="facts"><span><b>Group</b> Views and snapshots</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Change category, workset and filter visibility in one view, with a dry-run preview

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_set_view_visibility.md)

## Copyable prompts {#prompts}

```text
Hide the OST_StructuralColumns category in the 'A-101' plan view, previewing with a dry run first.
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `view` | Yes | — | `string` | view name (or its Revit id) |
| `category_classes` | No | `null` | `object / null` | Visibility per category class, keyed by category name. |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `filters` | No | `null` | `array<object> / null` | visibility filters applied to the view |
| `hide_categories` | No | `null` | `array<string / integer> / null` | categories to hide, by name or id |
| `hide_categories_by_type` | No | `null` | `array<string> / null` | category names to hide by type |
| `show_categories` | No | `null` | `array<string / integer> / null` | Categories to make visible in the view. |
| `template_mode` | No | `null` | `string / null` | visibility template mode |
| `worksets` | No | `null` | `object / null` | workset visibility, with hide_mask and show_mask lists |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Change category, workset and filter visibility in one view; dry_run previews. Categories accept the Revit UI name, the BuiltInCategory name (OST_StructuralColumns), the English name or an ID.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
