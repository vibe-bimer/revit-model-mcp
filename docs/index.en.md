# Revit Model MCP

<p class="facts"><span><b>Add-in / MCP version 0.9.0</b></span><span>Revit <b>2020 / 2022–2027</b></span><span>19 read + 15 action tools, 34 in total</span></p>

A feature handbook for Revit technical users: inspect parameters and geometry, count elements, check models, export registers, edit elements, and copy models with new IDs. Read-only by default; actions require both gates. **Revit years** and **add-in release versions** are different version axes. See the support matrix for live validation coverage.

## Choose an entry point {#entry-points}

<div class="grid cards" markdown>

- **Check your Revit year**

    [Revit 2020](features/v2020.md) · [Revit 2026](features/v2026.md) · [Support matrix](features/matrix.md)

- **Look up a feature and its parameters**

    [Feature overview](features/index.md): grouped by task, with behavior, parameters, returned data and limits.

- **Copy a prompt**

    [Prompt library](features/prompts.md): replace the model, level, element IDs and file paths with your own.

- **Install and connect MCP**

    [Installation and configuration](server.md) · [Transport and connection](transport.md) · [Action gates](actions.md#gates)

</div>

## Get started in three steps {#get-started}

1. Install the add-in on the Windows Revit workstation and configure the MCP server in your AI client. See [installation and configuration](server.md).
2. Start with a read-only query, such as `How many of each wall type are on 1F?` Discover filter names from the model catalog first.
3. Enable both gates only when actions are needed. Preview edits with tools supporting `dry_run`; after a timeout, inspect the model before retrying.

## Common prompts {#common-prompts}

| Task | Prompt |
| --- | --- |
| Count | `How many of each wall type are on 1F?` |
| Check | `Run a pre-handover health check: size, category counts, units and top warnings` |
| Export | `Export the ID register of the drawn model components to Excel, ordered by category, family and type` |
| Move | `Move element 123456 by 500 mm along X, dry run first` |
| New-model IDs | `Rebuild selectable components from the current 3D view into E:\out\copy-{n}.rvt, ten copies; check each copy's count and ID mapping` |

## Further reading {#further-reading}

<a id="tools"></a>
<a id="actions-opt-in"></a>

- Feature usage: [overview](features/index.md) · [prompts](features/prompts.md)
- Cross-tool contracts: [read contracts](tools.md) · [action contracts](actions.md)
- Project information: [changelog](changelog.md) · [privacy](privacy.md)

Use the top-right controls for Chinese / English and light / dark. Switching language keeps you on the corresponding page.
