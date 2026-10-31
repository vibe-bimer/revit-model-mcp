# Build Snapshot Report

Build a local Excel report from snapshots without contacting Revit.

**Group:** Batch processing · **Kind:** Read (read-only)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `output_path` | Yes | — | `string` | New .xlsx file path, resolved on the machine running this server; existing files are never replaced. |
| `snapshots_dir` | Yes | — | `string` | Directory of schema-version-1 JSON snapshots on the MCP client machine. |
| `findings` | No | null | `array of object / null` | Optional findings with model, severity, rule, element_ids (or elementIds), and recommendation. |
| `previous_dir` | No | null | `string / null` | Optional directory of earlier snapshots matched by model title for the Changes sheet. |

## Behavior and returned data

Build a local Excel report from snapshots without contacting Revit.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
