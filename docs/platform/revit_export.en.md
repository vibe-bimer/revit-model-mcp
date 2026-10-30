# Export Model Files

`revit_export`

<p class="facts"><span><b>Group</b> Export and registers</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `all_sheets` | No | False | boolean |  |
| `confirm_token` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `format` | Yes | — | string |  |
| `options` | No | None | any |  |
| `output_dir` | No | None | any |  |
| `overwrite` | No | False | boolean |  |
| `sheet_set` | No | None | any |  |
| `sheets` | No | None | any |  |
| `views` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | 1800 | integer |  |

## Behavior (registry text) {#behavior}

```text
Export PDF, DWG, IFC or schedule CSV files on the Revit workstation; dry_run returns planned file names. Replacing existing files (overwrite=true) needs a confirm_token from a first call. A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
