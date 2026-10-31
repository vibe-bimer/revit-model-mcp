---
description: "Build a local Excel report from snapshots without contacting Revit."
---

# Build Snapshot Report

`revit_build_report`

<p class="facts"><span><b>Group</b> Batch and reports</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 1.0.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> Yes, with identical parameters</span><span><b>This contract applies to the release</b> No</span></p>

[Same-name release page](../features/revit_build_report.md)

## Contract differences from the release {#contract-diff}

The same-name tool has an identical contract to release 1.0.0.

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `findings` | No | `null` | any | Optional findings with model, severity, rule, element_ids (or elementIds), and recommendation. |
| `output_path` | Yes | — | string | New .xlsx file path, resolved on the machine running this server; existing files are never replaced. |
| `previous_dir` | No | `null` | any | Optional directory of earlier snapshots matched by model title for the Changes sheet. |
| `snapshots_dir` | Yes | — | string | Directory of schema-version-1 JSON snapshots on the MCP client machine. |

</div>

## Behavior (registry text) {#behavior}

```text
Build a local Excel report from snapshots without contacting Revit.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
