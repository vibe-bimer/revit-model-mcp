---
description: "Create a schedule for one category with named fields in order, with filtering and sorting/grouping; dry_run rolls back"
---

# Create schedule

`revit_create_schedule`

<p class="facts"><span><b>Group</b> Sheets and schedules</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Create a schedule for one category with named fields in order, with filtering and sorting/grouping; dry_run rolls back

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_create_schedule.md)

## Copyable prompts {#prompts}

```text
Create a schedule for the Doors category with fields Mark, Level, Count in that order, named "Door and Window Takeoff"
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `category` | Yes | — | `string` | category name the schedule is created for |
| `fields` | Yes | — | `array<string>` | fields to return or write; the tool picks its usual ones by default |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `filters` | No | `null` | `array<any> / null` | schedule filters by field, operator and value |
| `itemized` | No | `true` | `boolean` | Whether identical rows are kept separate. |
| `name` | No | `null` | `string / null` | name of the new schedule |
| `sort` | No | `null` | `array<any> / null` | sort and grouping rules, each with a field and a direction |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Create a schedule for one category with the named fields in the given order, using Revit UI names such as Mark, Level or Count. filters keep rows by field, operator and value; sort orders and, with header or footer, groups rows. Lengths in mm, areas in m2, volumes in m3. itemized=false collapses identical rows. Returns viewId and the resolved fields; unknown names are listed in skipped. dry_run rolls back.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
