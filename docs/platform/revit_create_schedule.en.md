# Create Schedule

`revit_create_schedule`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `category` | Yes | — | string |  |
| `dry_run` | No | False | boolean |  |
| `fields` | Yes | — | array |  |
| `filters` | No | None | any |  |
| `itemized` | No | True | boolean |  |
| `name` | No | None | any |  |
| `sort` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Create a schedule for one category with the named fields in the given order, using Revit UI names such as Mark, Level or Count. filters keep rows by field, operator and value; sort orders and, with header or footer, groups rows. Lengths in mm, areas in m2, volumes in m3. itemized=false collapses identical rows. Returns viewId and the resolved fields; unknown names are listed in skipped. dry_run rolls back.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
