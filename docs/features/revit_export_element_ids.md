# Export element ID register

Write the ID register of drawn model components to an Excel workbook.

**Group:** Element registers · **Kind:** Read (read-only) · **Since:** this fork's 1.0.0

This fork adds this tool; the rest of the catalogue comes from upstream 1.0.

!!! note "Usage notes"

    The workbook is written on the Revit workstation.

## Copyable prompts

```text
Export the ID register of drawn model components to Excel, ordered by category, family and type
```

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `fields` | No | null | `array of string / null` | columns to write; the defaults are category, family, type, level, component id, name and workset |
| `path` | No | null | `string / null` | absolute .xlsx path on the Revit workstation; an existing file is an error |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Write the element identifier register of the drawn components to a workbook, read-only.

`fields` picks the columns and `path` names the file, which must not already exist; without
one the workbook goes to Documents/RevitModelMcp/Exports with a timestamp. Non-component
categories are reported under skippedCategories and the list is capped at 50,000 rows.
The workbook is written on the Revit workstation; nothing is downloaded.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
