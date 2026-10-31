---
description: "Place views and schedules on a sheet. Coordinates are sheet mm."
---

# Place Views on Sheet

`revit_place_views_on_sheet`

<p class="facts"><span><b>Group</b> Views, sheets and schedules</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 1.0.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, with identical parameters</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_place_views_on_sheet.md)

## Contract differences from the release {#contract-diff}

The same-name tool has an identical contract to release 1.0.0.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} |
| --- | :--: | --- | --- |
| `dry_run` | No | `false` | boolean |
| `sheet` | Yes | — | string |
| `views` | Yes | — | array |

</div>

The branch contract ships no parameter descriptions.

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | any | Title or file name substring of the target open document; needed when several are open. |

</div>

## Behavior (registry text) {#behavior}

```text
Place views and schedules on a sheet. Coordinates are sheet mm.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
