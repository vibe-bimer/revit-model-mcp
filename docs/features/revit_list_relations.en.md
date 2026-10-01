# Element relations

`revit_list_relations`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read (read-only)</span><span><b>Since</b> 0.7.0</span></p>

Read level rooms, area-scheme membership, group members, nested families and view-template dependents

## Copyable prompts {#prompts}

```text
Which rooms sit on level 1F?
```

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `relation` | Yes | — | `string` | which relation to read: level-rooms, area-scheme-elements, group-elements, nested-family or view-template-dependents |
| `source_id` | No | `null` | `integer / null` | Revit id of the source object, a group or a family instance |
| `source_name` | No | `null` | `string / null` | name of the source, a level, area scheme or view template |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `pickup_timeout_seconds` | No | `300` | `integer` | Positive seconds to wait for pickup over local or SSH (default 300); ignored over HTTP. A pending job may still execute after pickup times out |
| `timeout_seconds` | No | `120` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

## Behavior and returned data {#contract}

!!! note "Usage notes"
    The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md).

Read model object membership or dependencies.

Returns data with relation, source and elements containing IDs, names, categories, families and types; no related objects return elements=[].
relation is required: level-rooms, area-scheme-elements or view-template-dependents with source_name, or group-elements or nested-family with source_id.
Obtain source names from revit_list_catalog and IDs from element queries.
An invalid relation, missing or wrong source, missing document, read failure or timeout raises an error; partial data is not returned.


If more than one Revit instance is running, document is required; otherwise any instance may respond.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state ok">Validated live</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
