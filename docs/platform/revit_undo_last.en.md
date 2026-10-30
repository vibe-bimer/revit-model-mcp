# Undo Last Action

`revit_undo_last`

<p class="facts"><span><b>Group</b> Connection and instances</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

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
