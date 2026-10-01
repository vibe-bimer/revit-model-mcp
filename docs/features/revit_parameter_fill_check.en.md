# revit_parameter_fill_check

<p class="facts"><b>Group</b> Export and checks　<b>Kind</b> Read (read-only)　<b>Since</b> 0.6.0</p>

Count filled, empty and missing parameters before an export or hand-over.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `categories` ✔ | — | Required list of 1-20 category names from the categories catalog; no default. Matches any listed category and combines with level, workset and view filters.（array） |
| `parameters` ✔ | — | Required list of 1-30 exact localized parameter names; no default. Each name uses the first LookupParameter match, with type fallback controlled by include_types; missing names are counted as missing.（array） |
| `include_types` | `true` | count element types as well (true by default)（boolean） |
| `level` | — | restrict to one level（any） |
| `sample_limit` | `20` | Maximum element IDs sampled per parameter for each empty and missing list, an integer from 1 to 100. Default 20 limits samples only; all matching elements contribute to counts.（integer） |
| `view` | — | Exact non-template view name from the views catalog, matched case-insensitively, to restrict the element collector. Default null searches the document without a view filter; combines with the other model filters.（any） |
| `workset` | — | restrict to one workset（any） |

??? note "Common parameters"
    |  Parameter | Default | Meaning |
    | --- | --- | --- |
    | `document` | — | Case-insensitive substring of the target active document title or file name; default null leaves requests unaddressed, so any instance may respond. Use a unique substring with multiple instances; revit_list_instances instead returns all matching instances, or all instances when omitted.（any） |
    | `pickup_timeout_seconds` | `300` | Positive integer seconds to wait for the add-in to pick up a local or SSH job (300 when omitted); ignored over HTTP. A pickup timeout raises an error but the pending job may still execute later.（integer） |
    | `timeout_seconds` | `120` | Positive integer seconds to wait for a result after pickup (120 when omitted); HTTP uses this as its response budget. Expiry raises an error, and increasing it does not override the add-in's execution limits.（integer） |

## Prompts

```text
How well is the fire rating filled in on walls? Give me the empty ids
```

## Per year

| Year | State | Note |
| --- | --- | --- |
| 2020 | <span class="state ok">validated</span> |  |
| 2026 | <span class="state ok">validated</span> |  |
| Other years | <span class="state part">build only</span> | 2022–2025 / 2027 |

---

[All tools](index.md) · [Version matrix](matrix.md) · [Prompt library](prompts.md)
