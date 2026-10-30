# Set Parameter

`revit_set_parameter`

<p class="facts"><span><b>Group</b> Editing primitives</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `dry_run` | No | False | boolean |  |
| `element_id` | Yes | — | integer |  |
| `parameter` | Yes | — | string |  |
| `parameter_id` | No | None | any |  |
| `value` | Yes | — | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |

## Behavior (registry text) {#behavior}

```text
Set one instance or type parameter. parameter_id selects by BuiltInParameter name, shared GUID or ParameterElement ID; otherwise parameter takes a localized UI name, BuiltInParameter name or English alias, and ambiguous matches are refused. Value is a string, integer or number by storage type; lengths in mm, areas in m2. Group members fail with a clear message. dry_run rolls back and returns the verification block.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
