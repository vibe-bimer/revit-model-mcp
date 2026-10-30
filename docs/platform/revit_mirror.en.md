# Mirror Elements

`revit_mirror`

<p class="facts"><span><b>Group</b> Editing primitives</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `axis` | Yes | — | string |  |
| `copy` | No | True | boolean |  |
| `dry_run` | No | False | boolean |  |
| `element_ids` | Yes | — | array |  |
| `point_mm` | Yes | — | array |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Mirror across a model X or Y parallel line through point_mm; copy keeps originals. dry_run rolls back. Group members, pinned, hosted and constrained elements are reported in skipped.inGroup, skipped.pinned, skipped.hosted and skipped.constrained and are not changed; the call is refused if every element is a group member.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
