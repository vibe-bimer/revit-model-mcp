# Parameter Fill Check

`revit_parameter_fill_check`

<p class="facts"><span><b>Group</b> Query and totals</span><span><b>Kind</b> Read</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> Yes</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `categories` | Yes | — | array | Category names (1 to 20) from the categories catalog; matches any listed category. |
| `include_types` | No | True | boolean |  |
| `level` | No | None | any |  |
| `parameters` | Yes | — | array | Exact localized parameter names (1 to 30); names that do not match count as missing. |
| `sample_limit` | No | 20 | integer | Maximum sampled element IDs per empty and missing list, 1 to 100 (default 20); counts always cover all elements. |
| `view` | No | None | any | Exact non-template view name; limits the search to that view. |
| `workset` | No | None | any |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target document; needed when several Revit instances run. |
| `process_id` | No | None | any | Revit process ID; takes precedence over document. |
| `timeout_seconds` | No | 120 | integer | Seconds to wait for a result (default 120). |

## Behavior (registry text) {#behavior}

```text
Count filled, empty and missing parameters per parameter and category, with samples of empty and missing element IDs. Numeric zero counts as filled. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
