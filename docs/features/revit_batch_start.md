# Start batch collection

Start a persistent, read-only run over local, UNC or RSN models.

**Group:** Batch processing · **Kind:** Read (read-only)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `folder` | No | null | `string / null` | — |
| `open_timeout_minutes` | No | null | `integer / null` | — |
| `parameter_rules` | No | null | `array of object / null` | — |
| `paths` | No | null | `array of string / null` | — |
| `recursive` | No | false | `boolean` | — |
| `years` | No | null | `array of integer / null` | — |

## Behavior and returned data

Start a persistent, read-only run over local, UNC or RSN models. open_timeout_minutes is the per-model open deadline (default 30, 45 when upgrading in memory).

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
