# Revit Model MCP — Manual End-to-End Test Plan

Full manual validation checklist. Goal: exercise **every tool** and **every install/transport path**, from a clean install through live model reads and gated actions, on each supported Revit version.

Run when scheduled. Tick each `[ ]`. For every checked item record: **result** (pass/fail), **evidence** (journal line, screenshot, tool JSON, elapsed), and **notes**. File a GitHub issue for each fail with the repro.

> Reference model for spot-checks: **Snowdon Towers Sample Architectural.rvt** (ships with Revit). Values cited below were recorded on 2026-09-15 with Revit 2024.3; they are historical comparison points, not guarantees for a different model or release. Discover names with `revit_list_catalog`, then capture the current model's baseline with `revit_document_info` + `revit_aggregate_elements`.

!!! note "Planned coverage, not validation evidence"
    This checklist covers the current **33 tools: 19 reads + 14 opt-in actions**, on **Revit 2020 and 2022–2027**. Revit 2021 is not supported. Cross-check the release's `tools/list` against [read contracts](tools.md), [action contracts](actions.md) and the [feature overview](features/index.md). This documentation update ran no live Revit calls, ticked no checks and added no workstation evidence; see [validation evidence](validation.md) for recorded runs. Client problems recorded on 2026-09-15 below are historical retest cases, not current compatibility guarantees.

---

## 0. Test environments (matrix)

Ideally test on **two machines**:

- **M1 — clean-ish Windows workstation**: fresh or minimally-used Windows, target Revit version installed, Claude Desktop installed and logged in. This is the "does a real user get it working from the installers" run.
- **M2 — remote client (macOS/Linux)**: Claude Desktop / Claude Code on a Mac, reaching a Windows workstation's Revit over the remote (SSH tunnel) transport.

| Field | M1 | M2 |
|---|---|---|
| OS / build | | |
| Revit version(s) | | |
| Python + uv version | | |
| Claude Desktop version | | |
| Claude Code (`claude --version`) | | |
| Release under test (add-in / server / mcpb) | | |

Record the exact release tag being tested (e.g. `v0.5.0`) and confirm all three artifacts are the same version: the `.msi`/add-in zip, the PyPI `revit-model-mcp`, and the `.mcpb`.

---

## 1. Add-in installation (fresh, per Revit version)

Do this with **Revit closed**. Repeat the whole section for each supported Revit year present (2020 / 2022 / 2023 / 2024 / 2025 / 2026 / 2027), not 2021.

- [ ] **1.1 MSI — SingleUser**: run `RevitModelMcp-<ver>-SingleUser.msi`. Installer completes without error.
- [ ] **1.2 MSI — MultiUser**: on a separate profile/machine, run `RevitModelMcp-<ver>-MultiUser.msi`. Completes; add-in visible for all users.
- [ ] **1.3 Clone script**: `./install.ps1 -Source Release` from a clone. Completes.
- [ ] **1.4 Manifest present**: `%APPDATA%\Autodesk\Revit\Addins\<year>\RevitModelMcp.addin` exists and points to a `RevitModelMcp.dll` that exists.
- [ ] **1.5 DLL version**: the installed `RevitModelMcp.dll` matches the release version.
- [ ] **1.6 Provenance**: verify the release asset's build-provenance attestation (per docs `security/#verify-downloads`) before install.
- [ ] **1.7 Load in Revit**: start Revit, accept the "unsigned add-in" trust dialog (**Always Load**), open a model. Journal (`%LOCALAPPDATA%\Autodesk\Revit\Autodesk Revit <year>\Journals\journal.*.txt`) shows `API_SUCCESS ... Starting External Application: Revit Model MCP ... Assembly Version: <ver>` and event registrations. No fatal `API_ERROR` for the MCP DLL (benign "assembly version conflict" warnings, where the reference is *lower* than the installed Revit build, are OK).
- [ ] **1.8 Uninstall**: MSI uninstall removes the manifest cleanly (no orphan files, no load error next Revit start).

**Regression to watch (found before):** the add-in must reference `RevitAPI/RevitAPIUI` pinned to `<year>.0.0.0` (≤ installed build) and `System.Diagnostics.DiagnosticSource 8.x`, or it fails to load. Confirm per version.

---

## 2. Server + client wiring (every documented method)

### 2.1 Local server via `uvx` (Windows workstation)
- [ ] `uvx revit-model-mcp` resolves and installs the package from PyPI on first run (record package count + time).
- [ ] Server starts and reports `serverInfo: { name: "Revit Model Reader", version: "<ver>" }` on `initialize`.
- [ ] With actions disabled, `tools/list` returns exactly **19 read tools** (§3); after restarting with `REVIT_MCP_ALLOW_WRITE=1`, it returns **33 tools: 19 reads + 14 actions** (§4). The workstation gate still decides whether listed actions may execute.

### 2.2 Claude Code registration (`claude mcp add`)
- [ ] `claude mcp add revit-model-mcp -s user -e REVIT_MCP_HOST=local -e REVIT_MCP_REDACT_PATHS=1 -- uvx revit-model-mcp` writes to `~/.claude.json`.
- [ ] `claude mcp list` shows `revit-model-mcp: ... ✓ Connected`.
- [ ] `claude -p "what model is open in Revit?"` (headless) returns real model data (capture stdout to a file — headless output can be lost over a raw pipe).
- [ ] **App local agent**: in Claude Desktop's Code surface with the **"Local"** chip, ask a Revit question → agent calls `mcp__revit-model-mcp__*` and answers with real data.

<a id="23-claude-desktop-mcpb-one-click-install-known-broken-re-verify"></a>
### 2.3 Claude Desktop `.mcpb` one-click install (historical issue; retest)
- [ ] Double-clicking `revit-model-mcp-<ver>.mcpb` on Windows opens it **in Claude Desktop** (file association). *2026-09-15: FAILED — Windows showed "choose an app", Claude not registered as the `.mcpb` handler. Confirm whether fixed / document the correct install entry point (Settings → Extensions/Connectors → install from file).*
- [ ] Install via Claude Desktop **Settings → Extensions/Connectors → install `.mcpb`**; the config form sets `REVIT_MCP_HOST` (local/remote), redaction, actions, HTTP token without editing JSON.
- [ ] After install the connector appears and its tools are usable **in a surface that can reach a local stdio server**.

<a id="24-manual-claude_desktop_configjson-surface-limitation-re-verify"></a>
### 2.4 Manual `claude_desktop_config.json` (historical surface issue; retest)
- [ ] Write the documented `mcpServers` block, restart Claude Desktop.
- [ ] Determine which surfaces pick it up in the installed client version. *Historical 2026-09-15 observation: the app's **cloud chat** could not reach the local stdio MCP ("doesn't reach this cloud session"). Retest cloud chat and the local agent separately; record actual access and current setup requirements rather than treating this old limitation as a present guarantee.*

### 2.5 Remote workstation (M2 → M1)
- [ ] From a Mac/Linux client, configure the remote workstation (SSH tunnel to the workstation loopback endpoint) per docs `transport/`.
- [ ] Client `revit_ping` succeeds against the remote Revit; a read tool returns real data.

---

<a id="3-read-tools-full-coverage-18"></a>
## 3. Read tools — full coverage (19)

Model open on the workstation. For universal model queries, call **`revit_list_catalog` first, `revit_aggregate_elements` second, `revit_query_elements` only when rows are needed**. Discover processes with `revit_list_instances` before choosing a unique `document` substring. Record each JSON result and spot-check values. Read responses normally have `success: true`; `revit_list_instances` instead returns a list of process records, including `[]` when none match. The two export tools write files but do not modify the model.

| # | Tool | How to invoke (natural prompt or direct call) | Expected / spot-check | [ ] |
| --- | --- | --- | --- | --- |
| 1 | `revit_ping` | "Is Revit reachable?" | `data="pong"`, including without an active document; responder metadata | [ ] |
| 2 | `revit_document_info` | "Which model is open, and which levels, area schemes and worksets does it have?" | File name, Revit version, levels with `elevationMm`, area schemes, worksets and `viewCount`; `isWorkshared`. Historical Snowdon area counts: Gross Building 14, Rentable 87. Get room counts separately with aggregation | [ ] |
| 3 | `revit_model_health` | "Give me a model health summary" | Project metadata, file size, counts, units and top warnings; unavailable metrics are null with `skipped` reasons | [ ] |
| 4 | `revit_links_status` | "List RVT, CAD and image links and their status" | Summary plus `rvtLinks`, `cadLinks`, `images`; empty lists valid; inspect per-entry errors and the 100-entry list cap | [ ] |
| 5 | `revit_shared_coordinates` | "What are the shared coordinates and survey point?" | Base/survey points, active site, project locations and link offsets; mm and degrees | [ ] |
| 6 | `revit_parameter_fill_check` | Use catalog category and parameter names | Filled/empty/missing counts, instance/type ownership and ID samples; numeric zero is filled | [ ] |
| 7 | `revit_list_catalog` | Test `categories`, `family-types`, `levels`, `area-schemes`, `views`, `worksets`, `phases`, `parameters` | Names, IDs and section-specific counts/types; exact localized parameter names | [ ] |
| 8 | `revit_aggregate_elements` | "How many doors and windows?" with `group_by=["category"]` | `matchedElements`, grouped counts and optional numeric totals/units; historical Snowdon: Doors 142, Windows 106 | [ ] |
| 9 | `revit_query_elements` | Find largest room with fields `name`, `level`, `area`, `sort_field="area"`, `sort_direction="desc"` | Paged rows and units; historical Snowdon: Parking Garage, level Parking, 957.6 m²; room geometry when requested | [ ] |
| 10 | `revit_list_views` | "List non-template views" | IDs/names, type, level, scale, template, `total` and `processed`; test type/name filters | [ ] |
| 11 | `revit_view_summary` | Pass an exact name or view ID from #10 | Header metadata, category counts and `differentTypes`; no implicit active-view default | [ ] |
| 12 | `revit_export_view` | Export a discovered 3D/plan view | PNG, client-side `localPath`, size and view metadata; open it, confirm rendering and unchanged active view | [ ] |
| 13 | `revit_view_elements` | Page through a view discovered in #10 | IDs, category/family/type/level, measurements and `hasMore` | [ ] |
| 14 | `revit_element_details` | Inspect an ID from #9 or #13 | Instance/type parameters, related warnings and available geometry; rooms include area, volume, boundaries and `roomCenterMm` | [ ] |
| 15 | `revit_view_warnings` | Pass a discovered view | Warnings involving elements present in the view; `presentOnView` distinguishes affected elements outside it | [ ] |
| 16 | `revit_list_warnings` | List groups, then use a returned `warning_text` with `include_elements=true` | `totalWarnings`, grouped counts and affected IDs; empty groups valid | [ ] |
| 17 | `revit_list_relations` | Test `level-rooms`, `area-scheme-elements`, `view-template-dependents` with `source_name`; `group-elements`, `nested-family` with `source_id` | `relation`, `source`, related element records; no arbitrary host/hosted graph. Discover names in catalogs and IDs in queries | [ ] |
| 18 | `revit_list_instances` | "Which Revit processes and active documents are available?"; repeat with `document` filter | List of `documentName`, `documentPath`, `revitVersion`, `pluginVersion`, `processId`, `pluginResponding`; not family/type instances. Local/SSH fallback may have empty document and `pluginResponding=false`; HTTP lists its connected process only | [ ] |
| 19 | `revit_export_element_ids` | Export the drawn components' ID register with default/custom `fields` to a new workstation `.xlsx` path | `path`, `fileName`, `sheetName`, columns, row/total/category counts, `truncated`, size; rows ordered by category/family/type. Default columns: 类别, 族, 类型, 标高, 构件ID, 名称, 工作集. IDs unchanged; level may be empty for MEP runs | [ ] |

- [ ] **3.19 Redaction on**: with `REVIT_MCP_REDACT_PATHS=1`, path fields are redacted but names, parameter values, errors, channel files and export `localPath` remain visible.
- [ ] **3.20 Redaction off**: `REVIT_MCP_REDACT_PATHS=0` shows full paths.
- [ ] **3.21 Query boundaries**: paginate while `hasMore=true`; check no matches, offsets beyond results, invalid fields/filters and nonexistent IDs/views. Missing documents, read failures and timeouts are errors, not complete results. The declared contract promises no partial data, but the current file channel can return terminal `success:false`, `partial:true` data: record the exception, never count it as complete evidence, and accept full results only with `success:true` and `partial:false` (or no partial field). A wait timeout does not cancel the job. Aggregate room counts by level and area totals by level plus the selected area scheme.
- [ ] **3.22 Relations**: cover all five supported relations, empty membership and invalid/missing/wrong sources; do not infer unsupported host relations.
- [ ] **3.23 Export safety**: check custom/default fields, workbook columns and counts, existing destination refusal, workstation `.xlsx` versus client PNG paths, and the 50,000-row workbook truncation flag where a suitable fixture exists. Confirm neither export modifies model elements or assigns IDs.

---

<a id="4-action-tools-gated-writes-9"></a>
## 4. Action tools — gated actions (14)

Actions require **both gates**: `REVIT_MCP_ALLOW_WRITE=1` **and** the workstation allow-write file. Direct HTTP callers also need the bearer token. These are instructions for a separately authorized manual run, not actions executed during documentation maintenance. Use disposable model copies and dedicated output paths, capture a backup and baseline, and obtain the owner's permission before real changes.

The connection must discover exactly one Revit process. `document` selects an open model within it and is required when multiple documents are open. Unknown or ambiguous targets are rejected before changes. `revit_select`, `revit_show` and `revit_isolate` also require the addressed document to be active.

**Safety is tool-specific:** selection and show/navigation use UI calls without model transactions; isolation changes temporary view state and has no `dry_run`. The eight normal model-edit tools below support transactional `dry_run=true`: execute, verify the prospective result, then roll back. A batch supports group rollback. Resetting IDs is a separate irreversible replacement workflow: dry run first, and any ineligible element blocks the whole real selection. Rebuilding IDs writes new model files, not the source; its dry run copies without saving.

!!! warning "An error is not proof of rollback"
    `verification.error` can occur after **COMMIT**: the edit happened but the post-commit re-read failed. A transport or pickup timeout does not cancel a pending job; it may execute later. Inspect the addressed model, IDs and output files before any retry. Do not claim that every failed response leaves the model unchanged.

- [ ] **4.0 Enumerate**: with the server flag enabled, `tools/list` contains exactly the **14 named actions below**, alongside 19 reads (33 total). Save the schemas; there is no standalone open-view-by-name or undo tool.

| # | Action tool | Test and verification | Cleanup / safety | [ ] |
| --- | --- | --- | --- | --- |
| 1 | `revit_select` | Select a discovered room/element ID; confirm highlight and selection `count`; `element_ids=[]` clears it | Restore original selection; no model transaction or `dry_run` | [ ] |
| 2 | `revit_show` | Show discovered IDs with `select=true` and `false`; verify `activeView`, `viewOpened`, selection and navigation to a level plan/3D view when needed | Restore view/selection; UI-only, not open-by-name; no model transaction or `dry_run` | [ ] |
| 3 | `revit_isolate` | Temporarily isolate IDs in the active view, then `element_ids=[]`, `reset=true`; verify temporary hide/isolate state | Reset view state; no `dry_run`, not persistent geometry editing | [ ] |
| 4 | `revit_move` | Dry run, then move a test instance by model-axis `dx_mm`, `dy_mm`, `dz_mm`; compare before/after position or bounding box | Reverse move or discard fixture; check mm units | [ ] |
| 5 | `revit_place_family` | Dry run, then place a loaded unhosted family on a catalog level; test rotation, explicit/null `type_name`, `Family: Type`, conflicting types and missing-family suggestions | Use `roomCenterMm` inside rooms; delete test instance or discard fixture | [ ] |
| 6 | `revit_create_wall` | Dry run, then create a straight wall with distinct model-XY endpoints, catalog level/type and positive height; verify new ID/type/geometry | Delete test wall or discard fixture; `wall_type` is required but accepts null | [ ] |
| 7 | `revit_create_floor` | Dry run, then create a floor with at least three model-XY vertices; verify automatically closed boundary, ID, type and level; reject repeated consecutive points | Delete test floor or discard fixture; `floor_type` is required but accepts null | [ ] |
| 8 | `revit_set_phase` | Dry run, then use catalog phase names; test creation/demolition, `""` to clear and null to leave unchanged; inspect assignments | Restore recorded assignments or discard fixture; no phase creation/rename; both null rejected | [ ] |
| 9 | `revit_merge_phases` | Dry run, then reassign source creation/demolition references to target; check counts and `sourceDeleted`; a referenced phase may remain with `sourceDeleted=false` | Dedicated disposable fixture; source/target must differ; not batchable | [ ] |
| 10 | `revit_set_parameter` | Dry run, then edit a writable parameter; verify before/after and instance/type ownership; lengths mm, areas m², other doubles internal units | Restore value or discard fixture; shared-type changes affect all instances; read-only/ElementId parameters rejected | [ ] |
| 11 | `revit_delete` | Dry run first; inspect IDs including dependents, then delete only the approved test elements; verify survival check and returned count | Deletion count includes dependents; discard fixture or use authorized Revit UI undo | [ ] |
| 12 | `revit_reset_element_ids` | **Dry run first**: inspect `ineligible` reasons and `idMapping`; a mixed eligible/ineligible real selection must be refused as a whole. For an approved eligible-only fixture, verify old IDs gone, new copies and preserved type/category | **Irreversible; do not rely on undo.** Refuse hosted/grouped/dependent/MEP-curve/MEP-system members or uncopyable elements. Discard fixture and restore backup; no in-place ID assignment or old-ID parameter write | [ ] |
| 13 | `revit_rebuild_model_ids` | Dry run: mapping but no saved file. Real run to a new workstation `destination_path`; check `saved`, source/copy counts, exclusions and each ID mapping. Cover view/template, `seed`, duplicate-name modes and `copies`/`{n}` paths; inspect each `copyResults` entry | Source stays unchanged and unsaved. No overwrite without approval; inspect every output. Only selectable 3D-view components plus datums travel, not a full project archive; no preservation of views/sheets/schedules/annotations/phases/worksets/MEP systems/unselected hosts | [ ] |
| 14 | `revit_batch` | Dry run, then 1–50 approved steps; confirm prospective verification, rollback and selection restoration. Real success has one `revit_batch` undo entry; first execution failure rolls back the group; inspect `committed`, zero-based `failedStep` and per-step results | Use disposable fixtures; invalid later-step arguments reject before any execution. Allowed names: `move`, `place_family`, `create_wall`, `create_floor`, `set_phase`, `set_parameter`, `delete`, `select`, `isolate`; no `show`, phase merge, ID reset/rebuild or nested batch | [ ] |

- [ ] **4.1 Gate negative test**: with the server flag disabled, actions are absent from `tools/list` even if the workstation gate exists. With the flag enabled but no workstation gate, listed actions are refused. Removing the workstation gate takes effect without restarting Revit. Reads remain usable.
- [ ] **4.2 HTTP token gate**: a direct HTTP action without the bearer token is refused; `/health` works without token.
- [ ] **4.3 Transaction safety**: for normal transactional edits and batches, confirm successful dry runs report `dryRun:true` and `rolledBack:true`; created IDs are provisional. Verify execution/commit failures that roll back leave no partial edits. Separately check UI state, irreversible ID replacement and external-file behavior; do not apply a blanket transaction guarantee.
- [ ] **4.4 Model restored**: restore selection/isolation/view and reversible fixture edits; re-run `revit_aggregate_elements` and compare IDs, parameters and phase references, not just counts. Discard ID-reset/phase-merge fixtures and reopen backups; inspect/remove only approved test output files.
- [ ] **4.5 Addressing**: test explicit `document`, multiple open documents, unknown/ambiguous targets and inactive-target UI refusal. Multiple discovered processes must refuse actions rather than choose an arbitrary process.
- [ ] **4.6 Batch boundaries**: test 1 and 50 steps, reject 0/51, unknown actions/keys and invalid later arguments; cover per-step `dry_run`, first-failure rollback, single undo entry and immediate per-step verification (later steps can change it again).
- [ ] **4.7 Verification and timeout recovery**: use a controlled test fixture or mocked failure to check post-commit `verification.error` handling and pending-job timeout warnings. Record actual model/file state before retrying; never infer rollback or cancellation from a failed response.
- [ ] **4.8 Cleanup path**: verify the supported selection-clear/isolation-reset/delete operations and, where applicable, authorized Revit UI undo. Do not invent an MCP undo tool or use undo as the ID-reset recovery path.

---

## 5. Transports

- [ ] **5.1 Local** (`REVIT_MCP_HOST=local`) on the workstation — all of §3 passes.
- [ ] **5.2 SSH tunnel** (remote client → workstation loopback) — `revit_ping` + a read tool pass from M2.
- [ ] **5.3 HTTP** (loopback + bearer token) — `/health` (no token) responds; an authenticated read works. **Historical regression to retest — issue #44**: a previous run reported the HTTP listener on port 53110 not binding. Check the current release and issue status; this is not a claim of a current defect.
- [ ] **5.4 Concurrency / channel contention**: issue several **read** calls in quick succession. Historical 2026-09-15 run: *4 of 7* parallel calls failed with the single-file-channel error "busy: trigger.txt exists". Retest current rapid/parallel reads and record the failure rate; file an issue if contention persists. Do not overlap destructive action tests.

---

## 6. Multi-version Revit

Repeat the **§3 read smoke set** (at minimum: ping, document_info, list_catalog, aggregate_elements, list_warnings, export_view) with a model open in each installed version:

- [ ] 6.1 Revit 2022 (net48)
- [ ] 6.2 Revit 2023 (net48)
- [ ] 6.3 Revit 2024 (net48)
- [ ] 6.4 Revit 2025 (net8)
- [ ] 6.5 Revit 2026 (net8)
- [ ] 6.6 Revit 2027 (net10) — if available
- [ ] 6.7 **Two instances open**: with 2+ Revit versions running, confirm the read tools require `document` and correctly route to the intended instance (`revit_ping` with/without `document`). `revit_list_instances` remains the discovery exception; actions must refuse multiple processes even when `document` is supplied.
- [ ] 6.8 Revit 2020 (net48)
- [ ] 6.9 **Support boundary**: confirm installer/build targets cover 2020 and 2022–2027 only; do not list Revit 2021 as supported. Record build-only versus live-tested results separately; unavailable versions remain untested.

---

## 7. Client-surface matrix (which Claude surface actually works)

Record installed client versions, configuration and actual pass/fail per surface. The 2026-09-15 observations are historical; fill current results rather than assuming compatibility from them. Distinguish a locally running stdio server that uses SSH/HTTP to the workstation from a cloud-hosted connector.

| Surface | Reaches local stdio MCP? | Reaches remote MCP? | [ ] |
| --- | --- | --- | --- |
| Claude Desktop — **cloud chat** (Chat/Cowork) | Retest; historically unavailable | Record connector and reachability, if configured | [ ] |
| Claude Desktop — **local agent** (Code + "Local" chip) | Retest current registration | Record result with remote-workstation settings, if configured | [ ] |
| Claude Code CLI (`claude -p`, `claude`) local | Retest current registration | Record result with remote-workstation settings, if configured | [ ] |
| Claude Desktop with **remote workstation** config (M2) | Record whether this surface launches stdio locally | Retest workstation connection and authentication | [ ] |

- [ ] Document the *recommended* setup for each user type (Windows-local vs Mac-remote) based on what actually passed.

---

## 8. Known-issue regression (must re-test)

Explicit re-tests for historical failures or surprising behavior, including 2026-09-15 client observations. These are not a list of guaranteed current defects; record the release/client version and present outcome:

- [ ] **8.1** `.mcpb` file association / open-in-Claude (see §2.3).
- [ ] **8.2** Local stdio MCP unavailable in the cloud chat (see §2.4).
- [ ] **8.3** HTTP listener 53110 bind — issue #44 (see §5.3).
- [ ] **8.4** Channel contention on parallel tool calls (see §5.4).
- [ ] **8.5** Add-in load: benign vs fatal `API_ERROR` (assembly version conflict) per version (see §1.7).
- [ ] **8.6** `uvx`/`claude` not on the non-interactive shell PATH (use full paths) — a setup-doc note, not a product bug.

---

## 9. Reporting

For the run, produce a short results table: environment, release tag, per-section pass/fail counts, and a list of filed issues. Optionally record a **clean demo video** — but arrange the UI first (see the preferences note): open a real 3D/model view in Revit (not just the project browser), size Claude and Revit panels so both are legible, then start the screen recording. Ask the owner to set the layout before recording.

**Definition of done for the release:** §1–§7 all pass on at least Revit 2024 + 2026 (local) and one remote (M2) run; all §8 regressions either pass or have a tracked issue; the client-surface matrix (§7) is documented in the README/docs.
