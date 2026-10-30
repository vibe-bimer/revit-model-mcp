# List Instances

`revit_list_instances`

<p class="facts"><span><b>Group</b> Connection and instances</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

No additional business parameters; use the common parameters below.

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |

## Behavior (registry text) {#behavior}

```text
List Revit processes with documentName, documentPath, revitVersion, processId and pluginResponding. Busy or unresponsive processes stay listed with pluginResponding=false. HTTP mode reports only its connected process.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
