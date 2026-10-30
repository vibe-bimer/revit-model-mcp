# List Instances

List Revit processes with documentName, documentPath, revitVersion, processId and pluginResponding.

**Group:** Connection and core · **Kind:** Read (read-only)

## Parameters

This tool takes no parameters of its own.

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

List Revit processes with documentName, documentPath, revitVersion, processId and pluginResponding. Busy or unresponsive processes stay listed with pluginResponding=false. HTTP mode reports only its connected process.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
