---
description: "Migration status of this repository's 8 fork tools: 1 attached to the new base and 7 still queued."
---

# Fork tool migration status

This repository owns 8 tools. 1 is attached to the new base and 7 are still queued. None of them change base behaviour; they append commands through the fork registry.

| Tools | Base and fork tools | Migration status |
| --- | --- | --- |
| [Set view lighting](revit_set_view_lighting.md)<br>`revit_set_view_lighting` | Fork (this repository) | <span class="state ok">Grafted</span> |
| [Create level](#revit-create-level)<br>`revit_create_level` | Fork (this repository) | <span class="state no">Pending</span> |
| [Create floor](#revit-create-floor)<br>`revit_create_floor` | Fork (this repository) | <span class="state no">Pending</span> |
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
