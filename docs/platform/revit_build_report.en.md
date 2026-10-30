# Build Snapshot Report

`revit_build_report`

<p class="facts"><span><b>Group</b> Batch and reports</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `findings` | No | None | any | Optional findings with model, severity, rule, element_ids (or elementIds), and recommendation. |
| `output_path` | Yes | — | string | New .xlsx file path, resolved on the machine running this server; existing files are never replaced. |
| `previous_dir` | No | None | any | Optional directory of earlier snapshots matched by model title for the Changes sheet. |
| `snapshots_dir` | Yes | — | string | Directory of schema-version-1 JSON snapshots on the MCP client machine. |

## Behavior (registry text) {#behavior}

```text
Build a local Excel report from snapshots without contacting Revit.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
