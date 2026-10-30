# Capture Elements

Render a highlighted PNG that marks 1 to 500 elements, for issue evidence.

**Group:** Views and sheets · **Kind:** Read (read-only)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `element_ids` | Yes | — | `array of integer` | element ids (unitless Revit ids) |
| `mode` | No | "3d" | `string` | — |
| `output_path` | No | null | `string / null` | New PNG path, resolved on the machine running this server; an existing file is an error. Default null downloads to a temporary directory and returns localPath. |
| `padding_mm` | No | 1500 | `number` | — |
| `pixel_size` | No | 1600 | `integer` | PNG size in pixels along the fitted dimension, 32 to 4000 (default 1600); Revit rejects smaller images. |
| `process_id` | No | null | `integer / null` | Revit process ID; takes precedence over document. |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Render a highlighted PNG that marks 1 to 500 elements, for issue evidence. Supports 3d or plan mode over local or SSH transport. The temporary view is rolled back. A non-empty skipped list means the result is incomplete; skippedCount counts all skipped entries.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
