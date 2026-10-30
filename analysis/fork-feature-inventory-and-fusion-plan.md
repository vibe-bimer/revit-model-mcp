# Fork feature inventory and fusion plan

- Inventory date: 2026-10-30. Local `main` = `5afcb55`, merge base `5a65afc`, upstream `main` = `760bb7c` (v1.0.0 + 11).
- Scope: every one of the 55 fork-only commits classified by capability line, then each line mapped against upstream to decide keep / graft / drop, then an ordered fusion plan.
- Companion: [`upstream-update-research-2026-10-30.md`](upstream-update-research-2026-10-30.md) (delta numbers, decision points) and [`upstream-update-research-2026-10-13.md`](upstream-update-research-2026-10-13.md) (full 0.10.0 feature inventory).

## Part 1 — What the fork actually built

Six capability lines, ordered by depth of work rather than by commit order.

### Line A — Element identifier governance (export → reset → rebuild)

The largest and most original body of work: 22 of the 55 commits, ~1.9k lines of new add-in code plus a benchmark harness. The through-line is "a model's element ids are a contract you can audit, rehearse, and regenerate".

| Piece | Files | Size |
| --- | --- | --- |
| Register export | `src/RevitModelMcp.Addin/Capture/ElementIdExportReader.cs`, `src/RevitModelMcp.Addin/Output/XlsxWriter.cs`, `server/revit_model_mcp/server.py` (+35), `server/tests/test_element_id_export.py` | 310 + 229 + 337 (tests) |
| Rehearsable id reset | `src/RevitModelMcp.Addin/Control/ActionMutations.cs` (+498/−14) | ~500 |
| Model id rebuild | `src/RevitModelMcp.Addin/Control/ModelRebuild.cs`, `src/RevitModelMcp.Addin/Control/DialogOverride.cs` | 1003 + 64 |
| Farm benchmark | `bench/rebuild-farm.ps1`, `docs/rebuild-performance{,.en}.md`, commit `6bbd281` | 354 + 62 |

Correctness work embedded in the rebuild series is not cosmetic; each commit names a real failure mode:

- `c81fa91` refuse every MEP system member, not only MEP curves; `dc9d34c` read the system member set as elements and check connectors.
- `c0ac48a` replace each element in its own sub-transaction.
- `a141ea1` keep sketch and helper lines out of the component register.
- `a405693` rehost copies, restore joins, and report what a reset costs.
- `13194e4`/`5aaea7c` answer Revit's duplicate-name question instead of renaming the template.
- `ca6b77b`/`b9867de`/`20354ec` several copies from one model, clearing pasted types between copies.
- `2357a7d` give every farm instance its own copy of the model.
- `437b78b`/`a15fdb8`/`2bc8cc8` retry a refused copy, reuse pasted types, keep one backup, only repeat a copy when mapping really failed.

### Line B — First-batch modeling actions

`ActionMutations.cs` plus `Control/ViewLighting.cs` (388 lines new) and the parser/verification surface:

| Tool | Wire command | Commit |
| --- | --- | --- |
| `revit_create_floor` | `create-floor` | `a63c580` |
| `revit_create_level` | `create-level` | `5afcb55` |
| `revit_set_phase` | `set-phase` | `afd83c0` |
| `revit_merge_phases` | `merge-phases` (refused inside `batch`) | `afd83c0` |
| `revit_set_view_lighting` | `set-view-lighting` | `973b1ef` |

Supporting contract growth: `src/RevitModelMcp.Core/Control/ActionJobParser.cs` (+385/−6, adds the seven action names to `IsAction` and ~30 contract fields), `src/RevitModelMcp.Core/Control/ActionVerificationModels.cs` (+104, adds `name`/`elevationMm`, phase reassignment counters, `ViewLightingFacts`), `Control/ActionVerifier.cs` (+46), `Control/ActionCommandExecutor.cs` (+36), `Application.cs` (+56). Specification and API constraints are written down in `docs/modeling-tools{,.en}.md` and commit `b820aaf` (settled Revit phase API limits).

### Line C — Revit 2020 support

`14ed865`, `a59e567`, `5ac9a55`, `ca65487`. New compatibility shims: `Compatibility/ParameterDataType.cs` (172), `Compatibility/RevitUnits.cs` (93), `Compatibility/BasePoints.cs` (40); csproj adds `Debug.R20`/`Release.R20`; CI asserts the installed year count it actually builds. Upstream supports R22–R27 only, so this is a unique platform reach.

### Line D — Channel observability

`155a7e9` + `5c9f4c1`: `src/RevitModelMcp.Addin/PluginVersion.cs` (37), `server/revit_model_mcp/revit_channel.py` (+20), `server.py` `pluginVersion` field, and a fix that stops heartbeat writes from blocking. Paired with `04550e4` (`isModified` in document info, `ReadCommandModels.cs` +55) and the operational rule in `70b6582`: check `isModified` before a remote Revit restart.

### Line E — Bilingual, generated documentation site

`382b971` … `7a8e68b` and `b36ad02`, 13 commits. Generator and checks: `tools/site/generate_features.py`, `tools/site/check_site.py`, `tools/site/test_site.py`, content in `tools/site/content/{capabilities,contracts}.yaml` + `tools.json`. Serving and scheduling: `scripts/{serve-site,update-site,site-cron,site-supervisor,install-site-timer}.sh`, `scripts/systemd/revit-model-mcp-site.{service,timer}`, `mkdocs-lan.yml`. ~30 paired documents (`docs/*.en.md` alongside the Chinese originals), plus `CHANGELOG.zh.md`, `CONTRIBUTING.zh.md`, `SECURITY.zh.md`, `server/README.zh.md`. `130dfb9` makes the bilingual build fail closed on unpaired pages; `b6d1ad1` checks both languages end to end.

### Line F — Engineering process

`dacdafd` agent skills configuration (`.claude/`, `docs/agents/`), `e0b821a` Revit API corpus workflow plus project analysis, `e0848f8`/`679b4fc` the Linux build and `dotnet format` workarounds, `e4139f3` signing and automated restart, `docs/manual-test-plan{,.en}.md` (216 + 177), `analysis/t4-features-and-extension.md` (193), `analysis/t5-synthesis.md` (393), `dcd1425` newline hygiene.

### Fork defects found during the inventory

1. `bundle/manifest.json` `tools[]` lists the 19 read tools and **none** of the 16 action tools; `aa7f8ce` fixed this for `revit_export_element_ids` only, so the other 15 stayed missing.
2. `revit_export_element_ids` sits in the same name family as upstream `revit_export` (model files) and `revit_export_nwc(export_element_ids=…)` (a Navisworks exporter toggle). Three different meanings behind one token.

## Part 2 — Relationship to upstream, line by line

| Fork line | Upstream equivalent | Verdict |
| --- | --- | --- |
| A. Element id register | none. `revit_export` = model files; `revit_export_nwc(export_element_ids)` is an NWC setting; `revit_model_snapshot` + `revit_build_report` capture model state, not an id register | **Novel.** Keep; rename the tool |
| A. Id reset / rebuild | none. Closest is `revit_process_models` (open each model, steps/code/exports/save, ≤500 models, `confirm_token`, `dry_run`, `stop_on_error`) and `revit_batch_start/status/cancel/fetch` | **Novel core, but re-house it** as a `process_models` specialization |
| A. `DialogOverride.cs` | `Control/BatchDialogHandler.cs`, `Control/NativeDialogReader.cs`, `Core/Batch/BatchDialogPolicy.cs`, `Core/Batch/BatchDialogText.cs` + two test files, with the shared `IFailuresPreprocessor` pattern across seven executors | **Superseded.** Drop the fork's 64-line version, adopt the policy engine |
| B. Modeling actions | `revit_create_wall`, `revit_walls_from_cad`, `revit_create_mep_run`, `revit_place_families`, `revit_create_view/sheet/schedule`. No floor, level, phase, or view-lighting action exists; `revit_execute_code` is the only escape hatch | **Complementary.** Keep all five |
| B. Verification block | upstream has `ActionPreflight.cs` + a verification block in the batch response | **Overlaps partially.** Merge the phase/lighting/datum fact fields into the upstream shape rather than keeping a second model |
| C. Revit 2020 | R22–R27 only, and the year handling changed: upstream pins `MinimumRevitApiPackageVersion`/`MinimumRevitApiAssemblyVersion` per year and runs `build/RevitApiReferencePin` to rewrite assembly references; fork uses a floating `[$(RevitVersion).0.0, next.0.0)` range | **Novel, but must be re-expressed** in the upstream pin mechanism, including the `net472` TFM branch R20 needs |
| D. `isModified` | `revit_document_info` describes file name, versions, levels, area schemes, worksets, view count — no modified flag; `ReadCommandReader` has no `IsModified` | **Vacuum. Keep and upstream it** |
| D. `pluginVersion` | `Application.AddinVersion` (AssemblyInformationalVersion) exists for heartbeats/updates but no tool returns it; ping does not report a version | **Half exists.** Reuse `AddinVersion`, add the field in upstream's report shape |
| D. heartbeat non-blocking fix | upstream rebuilt the HTTP path (`61a3567` graceful shutdown, stored-response caps) and added retryable `transport_unavailable` (`32b6528`) | **Superseded by a better fix.** Take upstream's |
| E. Bilingual site | `mkdocs.yml` single language; the fork's `docs/*.en.md` pairs and `tools/site` generator have no counterpart | **Novel, but expensive to re-land.** Upstream rewrote 13 `docs/` files |
| F. Process docs | upstream deleted `CLAUDE.md` and grew its own `docs/agents/` + `guides/` + `skills/` | **Needs re-authoring**, not merging |

### The philosophical difference that should drive the plan

Upstream became a **platform**: 79 tools, machine policy, auto-update, store packaging, an `execute_code` escape hatch, a supervised batch model. The fork became a **precision instrument**: eight tools, each with a rehearsal path (`dry_run`), a verification block, and hard-won Revit-specific correctness (MEP system membership, phase reassignment counters, duplicate-name dialogs, per-instance farm copies).

Fusion is therefore not "who wins". The defensible shape is: **upstream as the base** (protocol, safety, policy, update, transports, batch), **the fork's eight tools grafted onto it** under upstream's own conventions, and the fork's rebuild farm re-expressed as a `process_models` specialization so it inherits the supervisor instead of maintaining a parallel one.

## Part 3 — Fusion plan

### Ordering principle

Align the base before inserting anything. Inserting tools into a moving parser is what produced the current 13-hunk conflict; inserting them once, after the base is stable and against upstream's `@action` + `ActionStep` + three-allowlist convention, is one edit per tool.

### Phase 0 — Repair the base (no upstream involvement)

1. Fix `bundle/manifest.json` to carry all 16 action tools, or generate its `tools[]` from `server.py` at build time so it cannot drift again. The existing `tools/site/generate_features.py` already parses the tool surface; reuse that parse.
2. Land the 47 uncommitted working-tree changes or park them on a branch, so the merge has a clean floor.
3. Re-baseline: create `integration/upstream-1.0` from `upstream/main`, and open the fork's 8-tool surface as one tracking issue set (one issue per tool, each naming its wire command, its contract fields and its verification facts).

### Phase 1 — Align the skeleton

Take upstream wholesale for: `server/revit_model_mcp/` (24 modules), `src/RevitModelMcp.Core/{Batch,Policy,Connect,Updates}`, `Control/ActionJobParser.cs`, `Application.SupportedCommands`, `bundle/manifest.json` shape, `.github/workflows/`, `build/`, `.sln` (+ the `BatchSupervisor` and `Updater` projects), and `docs/` structure.

Decisions to make explicitly at this point, because they change user-visible behavior:

- **Write default.** Re-impose the fork's read-only default + dual gate on top of upstream's policy engine, or adopt upstream's default-on + policy restriction. The fork must not be silently upgraded into default-on actions.
- **Version line.** Continue from `1.1.0` (`bump-minor-pre-major: false`); keep 0.6.0–0.9.0 in `CHANGELOG.md`.
- **`revit_batch` prefix collision.** Upstream owns `revit_batch_start/status/cancel/fetch`; the fork's single-call batch must take upstream's `revit_run_actions` name. Any local caller or doc using `revit_batch` for the single-call meaning is migrated, not aliased, so there is exactly one meaning per name.
- **`pickup_timeout_seconds`** disappears from schemas in favor of `REVIT_MCP_PICKUP_TIMEOUT_SECONDS`; the 43 local call sites move at the same time, since the channel is rewritten anyway.

### Phase 2 — Re-insert the eight tools, in dependency order

Each step = wire command into `ActionJobParser.IsAction` + contract fields + executor branch + `Application.SupportedCommands` + `actions.py` `@action` + bundle allowlist + toolset membership + tests. Order chosen so no step waits on a later one:

| # | Tool | Wire command | Depends on | Notes |
| --- | --- | --- | --- | --- |
| 1 | `revit_view_lighting` (renamed from `revit_set_view_lighting`) | `set-view-lighting` | — | Self-contained; `Control/ViewLighting.cs` ports largely intact |
| 2 | `revit_create_level` | `create-level` | — | First datum writer; establishes the datum `ActionFacts` (`name`, `elevationMm`) |
| 3 | `revit_create_floor` | `create-floor` | #2 (`LevelName`) | Needs the level resolver |
| 4 | `revit_set_phase` | `set-phase` | — | Carries `reassignedCreated`/`reassignedDemolished` counters |
| 5 | `revit_merge_phases` | `merge-phases` | #4 | Must keep the batch exclusion (`ActionJobParser.cs:74` locally) and be refused inside `revit_run_actions` |
| 6 | `revit_element_id_register` (renamed from `revit_export_element_ids`) | read command | — | `ElementIdExportReader.cs` + `XlsxWriter.cs` port cleanly; joins the `export` toolset; keeps its Python-side test |
| 7 | `revit_reset_element_ids` | `reset-element-ids` | #6 (register for rehearsal) | Keep sub-transaction-per-element, MEP system refusal, connector check, sketch/helper exclusion |
| 8 | `revit_rebuild_model_ids` | `rebuild-model-ids` | #7, upstream batch supervisor | Re-house as a `process_models` specialization; replace `DialogOverride.cs` with `BatchDialogPolicy`; keep per-instance copy, pasted-type reuse, one backup, refused-copy retry, and the `bench/rebuild-farm.ps1` regression |

Renames in this table are deliberate: `revit_export_element_ids` collides semantically with `revit_export`/`revit_export_nwc(export_element_ids)`, and `revit_set_view_lighting` reads as a setter while it also reports before/after lighting facts.

### Phase 3 — Platform additions, smallest surface first

1. `isModified` in `revit_document_info` — reuse `ReadCommandModels.cs` (+55); upstream has no equivalent.
2. Version reporting in the ping/document report shape — reuse upstream's `Application.AddinVersion` instead of the fork's `PluginVersion.cs`, keeping the fork's intent (a client can confirm the paired add-in build).
3. Revit 2020 — port `Compatibility/{ParameterDataType,RevitUnits,BasePoints}.cs`, add the R20 year to `Configurations`, express the version in `MinimumRevitApiPackageVersion`/`MinimumRevitApiAssemblyVersion`, add the `net472` TFM branch, and confirm `build/RevitApiReferencePin` handles a 2020 assembly. Highest build risk of anything here; do it after the tool surface is stable so a build break cannot mask a tool regression.
4. Bilingual site — re-run `tools/site/generate_features.py` against the post-alignment tool surface and upstream's rewritten `docs/`, then re-establish the fail-closed pairing check (`130dfb9`). Treat this as a fresh authoring pass, not a merge.
5. Process docs — re-author against upstream's `docs/agents/`, `guides/`, `skills/` layout; the fork's existing `docs/agents/*` was written against a repo upstream has since restructured.

### What not to carry over

- `DialogOverride.cs` (superseded by `BatchDialogPolicy`).
- The heartbeat write fix (superseded by the HTTP rebuild).
- `PluginVersion.cs` (fold into `AddinVersion`).
- The old parameter spellings and any `revit_batch` alias.
- The second verification model — merge its fact fields into upstream's block instead.

## Part 4 — Risks and how to check them

| Risk | Check |
| --- | --- |
| Actions silently become default-on | After Phase 1, a test asserts the write gate refuses an action when the gate is off, and a doc line states the default |
| Eight tools re-inserted into a parser that later moves again | One issue per tool with a checklist of the four allowlists; a test that asserts every supported command appears in all four |
| Rebuild loses its hard-won correctness during re-housing | `bench/rebuild-farm.ps1` as the regression: one model, ten copies, fresh ids, unique names, joins restored |
| R20 port breaks the other years | Build every year in `Configurations` in CI; `ca65487`'s installed-year assertion already does this — extend it to R20 |
| Bilingual site drifts from a rewritten `docs/` | Keep `130dfb9` fail-closed pairing in CI from the first site commit |
| Version line confusion (fork 0.9.0 vs upstream 1.0.0) | One release PR sets `CHANGELOG` 1.0.0 (upstream-aligned) before any feature release |

## Evidence boundaries

Every claim above comes from git objects in this checkout (`git log/show/ls-tree/grep` against `upstream/main`, `git diff 5a65afc..HEAD`, and reading the working tree) plus the two prior reports. No build, test, Revit run, or live tool listing was executed. Line counts are `git diff --numstat` additions/deletions, not final file sizes. Upstream behavior is read from its own code and commit messages; it is not locally reproduced. The 47 uncommitted working-tree changes were not touched.
