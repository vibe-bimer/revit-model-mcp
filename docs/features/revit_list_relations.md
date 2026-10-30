# List Relations

Read model object membership or dependencies.

**Group:** Model queries · **Kind:** Read (read-only)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `relation` | Yes | — | `string` | — |
| `process_id` | No | null | `integer / null` | Revit process ID; takes precedence over document. |
| `source_id` | No | null | `integer / null` | Revit ID of the source group (group-elements) or family instance (nested-family). |
| `source_name` | No | null | `string / null` | Source name, case-insensitive: a level (level-rooms), area scheme (area-scheme-elements) or view template (view-template-dependents). |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Read model object membership or dependencies. relation is level-rooms, area-scheme-elements or view-template-dependents (with source_name), or group-elements or nested-family (with source_id). A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
