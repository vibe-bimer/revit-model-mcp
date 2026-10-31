# Create floor

Create a floor from a closed XY boundary with at least three vertices.

**Group:** Model editing · **Kind:** Action (opt-in) · **Since:** this fork's 1.0.0

This fork adds this tool; the rest of the catalogue comes from upstream 1.0.

!!! warning "Runs only on a read-write workstation"

    An action runs only while the workstation is not read-only: the machine policy
    gate refuses action calls over every transport. The gate is the policy's
    `ReadOnly` value, held in the registry under
    `HKLM\Software\Policies\RevitModelMcp` or in
    `%ProgramData%\RevitModelMcp\policy.json`. The multi-user installer sets `ReadOnly`
    to `1` by default and writes the default `policy.json`, so a fresh machine install
    refuses actions until an administrator allows writes; a per-user install writes no
    policy (adr/0008). When both stores exist, the
    registry value wins for every value it sets, and a policy that cannot be read
    fails closed to read-only. The call names its target document, and with more
    than one open document it is refused. `dry_run` returns the same verification
    block without changing the model.

!!! note "Usage notes"

    The floor goes through `Floor.Create`, which needs Revit 2022 or later.

## Copyable prompts

```text
Create a floor on 2F from these four points
```

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `level` | Yes | — | `string` | level name, as revit_list_catalog reports it |
| `points_mm` | Yes | — | `array of array of number` | at least three model XY vertices, each [x,y] in millimetres; the boundary closes automatically |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `floor_type` | No | null | `string / null` | floor-type name; required argument, but null selects the first floor type |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |

## Behavior and returned data

Create a floor from a closed boundary on a level.

`points_mm` is the polygon, three vertices or more, each [x, y] in millimetres; consecutive
duplicates are refused. dry_run returns the same verification block without changing the model.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists on this branch: adr/0006 records Revit 2020 as a required follow-up and names no calendar date; the maintainer chooses the date when the follow-up is scheduled. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
