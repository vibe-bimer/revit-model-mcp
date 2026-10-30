# Rebuild IDs in new models

Copy selectable 3D-view components into one or more new models with fresh IDs.

**Group:** Id management · **Kind:** Action (opt-in) · **Since:** 1.0.0

This fork adds this tool; the rest of the catalogue comes from upstream 1.0.

!!! warning "Runs only on a read-write workstation"

    An action runs only while the workstation is not read-only: the `read-only`
    file in `%LOCALAPPDATA%\RevitModelMcp` refuses action calls over every transport.
    The call names its target document, and with more than one open document it is
    refused. `dry_run` returns the same verification block without changing the model.

!!! note "Usage notes"

    The source stays unchanged; only selectable 3D-view elements and required datums are copied, not the full project; check every count and ID mapping.

## Copyable prompts

```text
Rebuild the selectable components into E:\out\copy-{n}.rvt, ten copies, no id shared between them
```

```text
Rehearse the rebuild first: how many components, which new id range, write nothing yet
```

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `destination_path` | Yes | — | `string` | new model path (.rvt); {n} numbers the copies |
| `copies` | No | 1 | `integer` | how many copies one new model produces (1-50), each in an id block of its own |
| `dry_run` | No | false | `boolean` | rehearse in a temporary new document and report the mapping without saving; the source always stays unchanged |
| `duplicate_names` | No | "override" | `string (override, rename)` | duplicate names: override keeps the source types, reuse keeps the version the new model holds (the batch default), rename is the legacy path |
| `overwrite` | No | false | `boolean` | replace the destination when it exists |
| `remove_template_levels` | No | true | `boolean` | drop the template levels after copying (on by default) |
| `seed` | No | 0 | `integer` | create and remove N temporary levels to advance new-document ids; use different seeds across runs and verify overlap in the mappings |
| `template_path` | No | null | `string / null` | starting template (.rte/.rvt); the metric template is used when omitted |
| `view` | No | null | `string / null` | view name (or its Revit id) |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Rebuild the model into a new document so every element gets a new element ID.

`destination_path` is the new model, with {n} replaced by the copy number when `copies`
exceeds one. Reports the old to new pairing, the per-file results and the category counts.
dry_run reports the plan without writing files.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
