---
description: "Tag elements in a view, chosen by category names or by element IDs (exactly one of the two). Returns created tag IDs in createdElementIds; already tagged elements are skipped unless skip_tagged is false, and untaggable inputs are listed in skipped. tag_type matches a tag type name, a family name or \"Family: Type\"; the default tag type is used otherwise. Room tags need a plan view. dry_run rolls back and returns the tags that would be created."
---

# Tag Elements

`revit_tag_elements`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `categories` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `element_ids` | No | None | any |  |
| `leader` | No | False | boolean |  |
| `max_elements` | No | 5000 | integer |  |
| `orientation` | No | horizontal | string |  |
| `skip_tagged` | No | True | boolean |  |
| `tag_type` | No | None | any |  |
| `view` | Yes | — | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Tag elements in a view, chosen by category names or by element IDs (exactly one of the two). Returns created tag IDs in createdElementIds; already tagged elements are skipped unless skip_tagged is false, and untaggable inputs are listed in skipped. tag_type matches a tag type name, a family name or "Family: Type"; the default tag type is used otherwise. Room tags need a plan view. dry_run rolls back and returns the tags that would be created.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
