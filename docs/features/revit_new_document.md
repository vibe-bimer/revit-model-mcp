# New Document

Create a project or family from a template on the Revit workstation.

**Group:** Documents · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `activate` | No | true | `boolean` | — |
| `kind` | No | "project" | `string (project, family)` | — |
| `name` | No | null | `string / null` | — |
| `process_id` | No | null | `integer / null` | — |
| `save_as` | No | null | `string / null` | — |
| `template` | No | null | `string / null` | — |

## Behavior and returned data

Create a project or family from a template on the Revit workstation.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
