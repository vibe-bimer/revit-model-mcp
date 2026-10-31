---
description: "Link or import a DWG into a plan view on the Revit workstation and return CAD layers and extents in mm"
---

# Link CAD drawing

`revit_link_cad`

<p class="facts"><span><b>Group</b> Links and coordination</span><span><b>Kind</b> Action (opt-in)</span><span><b>Since</b> 1.0.0</span><span><b>Version</b> Unreleased (1.0.0)</span><span><b>Same-name tool on the integration branch</b> Yes</span><span><b>This contract applies to the release</b> Yes</span><span><b>Effect</b> Model elements / parameters</span></p>

Link or import a DWG into a plan view on the Revit workstation and return CAD layers and extents in mm

!!! warning "Actions require both write gates"
    Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.

[Same-name integration branch page](../platform/revit_link_cad.md)

## Copyable prompts {#prompts}

```text
Link D:/drawings/L1-plan.dwg into the "L1 Plan" view
```

## Parameters {#parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `path` | Yes | — | `string` | path of the CAD file to link or import |
| `dry_run` | No | `false` | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `layers` | No | `null` | `array<string> / null` | CAD layer names to link |
| `level` | No | `null` | `string / null` | level name, as revit_list_catalog reports it |
| `link` | No | `true` | `boolean` | Whether the DWG is linked instead of imported. |
| `origin` | No | `"internal"` | `string` | origin placement: internal, shared or center |
| `units` | No | `"auto"` | `string` | units of the CAD file: `auto`, `mm`, `cm`, `m`, `in` or `ft` |
| `view` | No | `null` | `string / integer / null` | view name (or its Revit id) |

</div>

### Common parameters {#common-parameters}

<div class="rmc-tablewrap" markdown="1">

| Parameter {scope=col} | Required {scope=col} | Default {scope=col} | Type {scope=col} | Meaning {scope=col} |
| --- | :--: | --- | --- | --- |
| `document` | No | `null` | `string / null` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected |
| `timeout_seconds` | No | `600` | `integer` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job |

</div>

## Behavior and returned data {#contract}

Link or import a DWG into a plan view on the Revit workstation. Returns CAD layers and extents in mm.

## Revit year support {#year-support}

| Revit year | Validation |
| --- | --- |
| 2020 | <span class="state part">Build only, not live-tested</span> |
| 2026 | <span class="state part">Build only, not live-tested</span> |
| 2022–2025 / 2027 | <span class="state part">Build only, not live-tested</span> |

Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.

---

[All features](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
