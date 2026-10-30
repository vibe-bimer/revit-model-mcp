# Link CAD Drawing

Link or import a DWG into a plan view on the Revit workstation.

**Group:** CAD and MEP · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `path` | Yes | — | `string` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `layers` | No | null | `array of string / null` | — |
| `level` | No | null | `string / null` | level name, as revit_list_catalog reports it |
| `link` | No | true | `boolean` | — |
| `origin` | No | "internal" | `string (internal, shared, center)` | — |
| `units` | No | "auto" | `string (auto, mm, cm, m, in, ft)` | — |
| `view` | No | null | `string / integer / null` | view name (or its Revit id) |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Link or import a DWG into a plan view on the Revit workstation. Returns CAD layers and extents in mm.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
