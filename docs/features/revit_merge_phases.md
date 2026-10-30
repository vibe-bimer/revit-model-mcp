# Merge project phases

Reassign references to another phase and attempt to delete the emptied phase.

**Group:** Phases · **Kind:** Action (opt-in) · **Since:** this fork's 1.0.0

This fork adds this tool; the rest of the catalogue comes from upstream 1.0.

!!! warning "Runs only on a read-write workstation"

    An action runs only while the workstation is not read-only: the machine policy
    gate refuses action calls over every transport. The gate is the policy's
    `ReadOnly` value, held in the registry under
    `HKLM\Software\Policies\RevitModelMcp` or in
    `%ProgramData%\RevitModelMcp\policy.json`. The installer sets `ReadOnly` to
    `1` by default and writes the default `policy.json`, so a fresh install refuses
    actions until an administrator allows writes. When both stores exist, the
    registry value wins for every value it sets, and a policy that cannot be read
    fails closed to read-only. The call names its target document, and with more
    than one open document it is refused. `dry_run` returns the same verification
    block without changing the model.

!!! note "Usage notes"

    A batch call refuses it.

## Copyable prompts

```text
Merge phase 1 into New Construction
```

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `source_phase` | Yes | — | `string` | the phase that is merged away and then deleted |
| `target_phase` | Yes | — | `string` | the phase that receives the references |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Merge one phase into another and delete the emptied phase.

Reports how many elements moved each way and how many references remain to the source.
dry_run returns the same verification block without changing the model.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
