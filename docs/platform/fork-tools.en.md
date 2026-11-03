---
description: "Migration status of this repository's 13 fork tools: 1 attached to the new base and 12 still queued."
---

# Fork tool migration status

This repository owns 13 tools. 1 is attached to the new base and 12 are still queued. None of them change base behaviour; they append commands through the fork registry.

| Tools | Base and fork tools | Migration status |
| --- | --- | --- |
| [Set view lighting](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | Fork (this repository) | <span class="state ok">Grafted</span> |
| [Create level](#revit-create-level)<br>`revit_create_level` | Fork (this repository) | <span class="state no">Pending</span> |
| [Create floor](#revit-create-floor)<br>`revit_create_floor` | Fork (this repository) | <span class="state no">Pending</span> |
| [Load family file](#revit-load-family-file)<br>`revit_load_family_file` | Fork (this repository) | <span class="state no">Pending</span> |
| [Create grid](#revit-create-grid)<br>`revit_create_grid` | Fork (this repository) | <span class="state no">Pending</span> |
| [Create column](#revit-create-column)<br>`revit_create_column` | Fork (this repository) | <span class="state no">Pending</span> |
| [Create beam](#revit-create-beam)<br>`revit_create_beam` | Fork (this repository) | <span class="state no">Pending</span> |
| [Place hosted family](#revit-place-hosted-family)<br>`revit_place_hosted_family` | Fork (this repository) | <span class="state no">Pending</span> |
| [Set phase](#revit-set-phase)<br>`revit_set_phase` | Fork (this repository) | <span class="state no">Pending</span> |
| [Merge phases](#revit-merge-phases)<br>`revit_merge_phases` | Fork (this repository) | <span class="state no">Pending</span> |
| [Export element ID register](#revit-export-element-ids)<br>`revit_export_element_ids` | Fork (this repository) | <span class="state no">Pending</span> |
| [Reset element IDs](#revit-reset-element-ids)<br>`revit_reset_element_ids` | Fork (this repository) | <span class="state no">Pending</span> |
| [Rebuild model IDs](#revit-rebuild-model-ids)<br>`revit_rebuild_model_ids` | Fork (this repository) | <span class="state no">Pending</span> |

Grafted means the branch lists and runs it. Pending means the implementation exists in the local version but the branch has no command yet.

## Create level {#revit-create-level}

`revit_create_level` — The local implementation exists with dry_run and a verification block; it still has to be remapped onto the fork registry.

## Create floor {#revit-create-floor}

`revit_create_floor` — The local implementation exists; it still has to be remapped.

## Load family file {#revit-load-family-file}

`revit_load_family_file` — Implemented on the fork registry (one file, an optional single type, the load options always supplied, closest names for a missing path) with Python and Core tests passing; flips to grafted with the first batch.

## Create grid {#revit-create-grid}

`revit_create_grid` — Implemented on the fork registry (line and three-point arc, duplicate-name refusal, batch step vocabulary) with Python and Core tests passing; flips to grafted with the first batch.

## Create column {#revit-create-column}

`revit_create_column` — Implemented on the fork registry (the tool writes both levels and both offsets, the top is a level or a height, nothing is attached, a missing type lists the ones that exist) with Python and Core tests passing; flips to grafted with the first batch.

## Create beam {#revit-create-beam}

`revit_create_beam` — Implemented on the fork registry (the curve-and-level overload, an axis that is never snapped, structural usage written from the enum, the vertical offset through the family's elevation parameter with a move as the fallback, a missing type listing the ones that exist) with Python and Core tests passing; flips to grafted with the first batch.

## Place hosted family {#revit-place-hosted-family}

`revit_place_hosted_family` — Implemented on the fork registry (a named host or the nearest wall, ties and out-of-radius points refused with the candidates, hostResolution reported, sill and flip supported, a non-zero angle refused because the host wall sets the orientation, non-hosted families refused, nothing attached) with Python and Core tests passing; flips to grafted with the first batch.

## Set phase {#revit-set-phase}

`revit_set_phase` — The local implementation exists; Revit cannot create or rename phases, so it only assigns existing ones.

## Merge phases {#revit-merge-phases}

`revit_merge_phases` — The local implementation exists; the command is excluded from the batch step vocabulary.

## Export element ID register {#revit-export-element-ids}

`revit_export_element_ids` — The local implementation writes an xlsx register and reads system members and connectors.

## Reset element IDs {#revit-reset-element-ids}

`revit_reset_element_ids` — The local implementation is rehearsable, reports the cost in dry_run, and commits each element in its own subtransaction.

## Rebuild model IDs {#revit-rebuild-model-ids}

`revit_rebuild_model_ids` — The local implementation is about a thousand lines and supports templates, copies and duplicate-name policies; it is the last item to migrate and roughly equals the first five together.

---

[Back to the catalog](index.md)
