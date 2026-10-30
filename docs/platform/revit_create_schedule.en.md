---
description: "Create a schedule for one category with the named fields in the given order, using Revit UI names such as Mark, Level or Count. filters keep rows by field, operator and value; sort orders and, with header or footer, groups rows. Lengths in mm, areas in m2, volumes in m3. itemized=false collapses identical rows. Returns viewId and the resolved fields; unknown names are listed in skipped. dry_run rolls back."
---

# Create Schedule

`revit_create_schedule`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `category` | Yes | — | string |  |
| `dry_run` | No | `false` | boolean |  |
| `fields` | Yes | — | array |  |
| `filters` | No | `null` | any |  |
| `itemized` | No | `true` | boolean |  |
| `name` | No | `null` | any |  |
| `sort` | No | `null` | any |  |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |

</div>

## Behavior (registry text) {#behavior}

```text
Create a schedule for one category with the named fields in the given order, using Revit UI names such as Mark, Level or Count. filters keep rows by field, operator and value; sort orders and, with header or footer, groups rows. Lengths in mm, areas in m2, volumes in m3. itemized=false collapses identical rows. Returns viewId and the resolved fields; unknown names are listed in skipped. dry_run rolls back.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
