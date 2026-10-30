# Move Elements

`revit_move`

<p class="facts"><span><b>Group</b> Editing primitives</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | False | boolean |  |
| `dx_mm` | Yes | — | number |  |
| `dy_mm` | Yes | — | number |  |
| `dz_mm` | No | 0 | number |  |
| `element_ids` | Yes | — | array |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Move elements by dx_mm, dy_mm and dz_mm on model axes. dry_run rolls back and returns the verification block. Group members, pinned, hosted and constrained elements are reported in skipped.inGroup, skipped.pinned, skipped.hosted and skipped.constrained and are not changed; the call is refused if every element is a group member.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
