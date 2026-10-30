# Replace IDs in place

Replace eligible standalone elements with copies to obtain new IDs.

**Group:** Id management · **Kind:** Action (opt-in) · **Since:** 1.0.0

This fork adds this tool; the rest of the catalogue comes from upstream 1.0.

!!! warning "Runs only on a read-write workstation"

    An action runs only while the workstation is not read-only: the `read-only`
    file in `%LOCALAPPDATA%\RevitModelMcp` refuses action calls over every transport.
    The call names its target document, and with more than one open document it is
    refused. `dry_run` returns the same verification block without changing the model.

!!! note "Usage notes"

    Run `dry_run` first; hosted, dependent, grouped and MEP-system elements are refused.

## Copyable prompts

```text
Give these 27 standalone components new ids
```

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `element_ids` | Yes | — | `array of integer` | elements to replace; hosted, dependent, grouped or MEP system members are refused |
| `dry_run` | No | false | `boolean` | rehearse: replace, report the mapping, then roll back |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Give elements new element IDs by copying each one over its original.

The API cannot assign an element ID, so every element is copied, checked and then replaces
its original. Elements that cannot be replaced are refused by name, and a real run is
refused when any element in the selection is. dry_run returns the same block without keeping
the changes.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
