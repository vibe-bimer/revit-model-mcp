---
description: "Load one family file from the workstation: the whole family, or one named type"
---

# Load family file

`revit_load_family_file`

<p class="facts"><span><b>Group</b> Families</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 0.10.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> No</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span><span><b>Origin</b> Fork (this repository)</span></p>

Load one family file from the workstation: the whole family, or one named type

!!! warning "Actions are allowed by default; read-only is explicit"
    Actions are allowed unless one of three switches is on: the machine policy `ReadOnly`, the workstation `read-only` file, or `REVIT_MCP_READ_ONLY=1`. A fresh install ships with the machine policy read-only. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

!!! note "Usage notes"
    The load always carries the family load options, so Revit's own dialog never appears; an existing family is reused with its parameter values kept, and a missing path reports the closest filenames. The base also ships the batch `revit_load_family`, which takes a `paths` list; this tool is one file with an optional single type

## Copyable prompts {#prompts}

```text
Load C:\lib\M_Door.rfa into the model
```

```text
Load only the 0900 x 2100 type from M_Door.rfa
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `path` | Yes | — | `string` | absolute path of the family file on the workstation (a .rfa) |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `overwrite_parameters` | No | `false` | `boolean` | overwrite the project's parameter values with the family's; off by default |
| `type_name` | No | `null` | `string / null` | load only this type; empty loads the whole family |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |

</div>

## Behavior and returned data {#contract}

Load one family file from the workstation: the whole family, or the single type `type_name`.

The load always carries the family load options, so it never waits on Revit's own dialog.
An existing family is reused, and its parameter values are left alone unless
`overwrite_parameters` is true. The response reports `state` ("new" or "existing") and every
type the family now offers. A path that does not exist is refused with the closest filenames
beside it. dry_run returns the same verification block without changing the model.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state ok">Validated live</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
