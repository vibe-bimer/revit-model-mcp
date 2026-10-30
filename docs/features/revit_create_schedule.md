# Create Schedule

Create a schedule for one category with the named fields in the given order, using Revit UI names such as Mark, Level or Count.

**Group:** Views and sheets · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `category` | Yes | — | `string` | — |
| `fields` | Yes | — | `array of string` | fields to return or write; the tool picks its usual ones by default |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `filters` | No | null | `array of any / null` | — |
| `itemized` | No | true | `boolean` | — |
| `name` | No | null | `string / null` | — |
| `sort` | No | null | `array of any / null` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Create a schedule for one category with the named fields in the given order, using Revit UI names such as Mark, Level or Count. filters keep rows by field, operator and value; sort orders and, with header or footer, groups rows. Lengths in mm, areas in m2, volumes in m3. itemized=false collapses identical rows. Returns viewId and the resolved fields; unknown names are listed in skipped. dry_run rolls back.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
