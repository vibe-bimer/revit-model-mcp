# Undo Last Action

`revit_undo_last`

<p class="facts"><span><b>Group</b> Connection and instances</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

No additional business parameters; use the common parameters below.

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Undo the last MCP action through Revit's own undo command. Runs only when the target document is active, no command is pending and Revit's last undo entry is the one this session recorded; otherwise the result carries a refusal reason.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
