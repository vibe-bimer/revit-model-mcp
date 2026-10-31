# Synchronize Document

Synchronize a workshared document with central.

**Group:** Documents · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `comment` | Yes | — | `string` | — |
| `compact` | No | false | `boolean` | — |
| `confirm_token` | No | null | `string / null` | — |
| `process_id` | No | null | `integer / null` | — |
| `relinquish` | No | "all" | `string (all, none) / object` | — |
| `save_local_after` | No | true | `boolean` | — |
| `save_local_before` | No | true | `boolean` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Synchronize a workshared document with central. Needs confirm_token from a first call, which changes nothing.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
