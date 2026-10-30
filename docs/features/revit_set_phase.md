# Set element phases

Assign created and demolished phases; an empty string clears one and null leaves it unchanged.

**Group:** Phases · **Kind:** Action (opt-in) · **Since:** 1.0.0

This fork adds this tool; the rest of the catalogue comes from upstream 1.0.

!!! warning "Runs only on a read-write workstation"

    An action runs only while the workstation is not read-only: the `read-only`
    file in `%LOCALAPPDATA%\RevitModelMcp` refuses action calls over every transport.
    The call names its target document, and with more than one open document it is
    refused. `dry_run` returns the same verification block without changing the model.

!!! note "Usage notes"

    The phase order check uses the API that appears from Revit 2022.

## Copyable prompts

```text
Mark these elements as demolished in the Existing phase
```

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `element_ids` | Yes | — | `array of integer` | element ids whose phase changes |
| `created_phase` | No | null | `string / null` | created phase name; an empty string clears it, null leaves it |
| `demolished_phase` | No | null | `string / null` | demolished phase name; an empty string clears it, null leaves it unchanged |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Set the creation and demolition phase of elements.

An empty string clears a phase and null leaves it alone; at least one must be given.
dry_run returns the same verification block without changing the model.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
