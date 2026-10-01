# Revit instance list

`revit_list_instances`

<p class="facts"><span><b>Group</b> Connection and documents</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.6.0</span></p>

List running Revit instances and their active documents

## Copyable prompts {#prompts}

```text
Which Revit instances are running, and what does each hold?
```

## Parameters {#parameters}

No additional business parameters; use the common parameters below.

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

## Behavior and returned data {#contract}

List Revit processes and their active documents.

Returns a list of documentName, documentPath, revitVersion, pluginVersion, processId and pluginResponding records; no matching instances return [].
pluginVersion identifies the add-in build, for example 0.6.0+68febc5d, and is empty for heartbeats written by older add-ins.
Local and SSH modes use add-in heartbeats with process fallback; fallback records have an empty document and pluginResponding=false.
HTTP mode reports only its connected process; transport failures raise errors.
Use this tool before choosing a unique document substring for other tools.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
