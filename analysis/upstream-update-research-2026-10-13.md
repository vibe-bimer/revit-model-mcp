# Upstream update research: useful changes and fork migration constraints

- Research date: 2026-10-13, Asia/Shanghai.
- Upstream: `sharafutdinovdi/revit-model-mcp`, commit [`c1e23f5c5dd1f926be0b36d98d21461b2ebff645`](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/c1e23f5c5dd1f926be0b36d98d21461b2ebff645>).
- Local baseline: `/home/roky/revit-mcp`, HEAD `5afcb55b4629c84135766fd567c67800b3632431`.
- Merge base: [`5a65afc47789f07c2df495e2779e69dafd2e58b0`](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/5a65afc47789f07c2df495e2779e69dafd2e58b0>).
- Scope: feature inventory, public contracts, build/package/CI changes and migration planning, supplemented by the lead's security-backport and committed-tree merge preview in section 7.

## 1. Decision summary

**Update selected feature families, not the entire upstream tree unchanged.** The most useful additions are model audit snapshots and Excel reports, multi-client job coordination, richer views/sheets and bulk edits, then session/export automation. Toolset selection and reproducible packaging are valuable supporting improvements. Keep the fork's Revit 2020 support, dual opt-in write gates, custom modeling/ID tools and bilingual documentation. Upstream deliberately removed the opt-in gates and supports only Revit 2022–2027. Those are product differences, not changes to accept accidentally. [Feature inventory][u-tools] [Default-on breaking commit][c-coordination] [Local hard rules][l-agents] [Local year matrix][l-addin]

The local and upstream version numbers are **not interchangeable product identities**. Local HEAD says `0.9.0`; upstream HEAD says `0.9.1`, but their capabilities diverged substantially. Both still use the package and CLI name `revit-model-mcp`. An unpinned upstream launcher or updater can replace the fork with the upstream distribution. Preserve fork-specific deployment/publishing identity and keep upstream update checks off until this is deliberately resolved. [Local package][l-package] [Upstream package][u-package] [Update implementation][u-server-updates]

### Published release versus upstream HEAD

The first-party [GitHub latest-release API][release-api] returned HTTP 200 during this research:

| Field | Observed value |
| --- | --- |
| Latest published non-draft, non-prerelease release | [`v0.9.1`][release-page] |
| Published at | `2026-10-06T00:51:07Z` |
| Target commit | [`d61094f41976dec852db63b83a2d3e93a7435f4c`][release-commit] |
| Public tools at that source commit | **77** |
| Commits between that release commit and the requested upstream HEAD | **43** |
| Public tools at requested upstream HEAD | **79** |

The release assets observed were six R22–R27 add-in ZIPs, SingleUser/MultiUser MSIs, an MCPB, a Python wheel/source archive and a checksum file. **The API asset list did not include the later managed/store bundles, store MSI, store MCP manifest or SBOMs.** Their presence in HEAD's release workflow is not proof they are already published. Machine policy, toolsets, tagging, schedule creation and the bundled server/App Store packaging are post-release source changes. The only genuinely new tool names after this release are tagging and schedule creation; the third HEAD-only name is the batch rename. [Release API][release-api] [Policy/features commit][c-policy] [Store/bundled-server commit][c-store] [Rename commit][c-contract]

## 2. Exact capability inventory

The counts below come from Python AST enumeration of decorated `revit_*` definitions in the three fixed source snapshots, cross-checked against upstream's generated [tool manifest][u-manifest] and [toolset registry][u-toolsets]. They are source/registry counts, not a live Revit acceptance test.

| Baseline | Read tools | Action/modifying tools | Total |
| --- | ---: | ---: | ---: |
| Common merge base | 18 | 9 opt-in | 27 |
| Local HEAD | **19** | **16 opt-in** | **35** |
| Upstream HEAD | **34** `read_only` annotations | **45** `modifying` annotations | **79** |

Local actions are absent from registration unless `REVIT_MCP_ALLOW_WRITE` is enabled, so its default exposed count is 19, not 35. Upstream registers all selected tools even in read-only mode; blocked calls are refused instead. Its default selection is `all`. An upstream `read_only` annotation does not mean “no local file writes”: report tools write workbooks, and the separately read-only batch worker is launched by a modifying tool. [Local registration][l-actions] [Upstream manifest][u-manifest] [Upstream tools][u-tools]

**26 names are shared; 53 upstream names are absent locally; 9 local names are absent upstream.** One of each is the same capability under `revit_batch` versus `revit_run_actions`. Thus the useful interpretation is **52 additive upstream tools, eight genuinely fork-specific tools to retain, plus a batch-name compatibility decision**.

### Upstream's eleven tool groups

| Toolset | Tools | Names absent from local HEAD | Main additions or purpose |
| --- | ---: | ---: | --- |
| `core` | 8 | 5 | Open-document inventory, UI state, jobs/cancel and guarded last-action undo |
| `read` | 12 | 2 | Model snapshot and schedule data; ten familiar query/coordinator tools remain |
| `actions` | 9 | 6 | Rotate/copy/mirror/change type, filtered bulk parameter updates, renamed action batch |
| `documents` | 6 | 6 | Open/activate/new/close/save/synchronize documents |
| `views-sheets` | 21 | 13 | View settings, captures, view activation/creation/templates/visibility, graphic overrides, tags, schedules, sheets/placement |
| `family` | 5 | 4 | Family audit/edit/load and bulk/room-based placement |
| `links` | 3 | 3 | Compare/align link grids and levels, remove links |
| `cad-mep` | 4 | 3 | CAD linking, walls from CAD, duct/pipe/tray/conduit runs |
| `export` | 4 | 4 | PDF/DWG/IFC/CSV export, NWC export/settings, issue register |
| `batch` | 6 | 6 | Durable collection start/status/cancel/fetch, offline report, interactive multi-model processing |
| `code` | 1 | 1 | Confirmed live C# execution |
| **Total** | **79** | **53** | Includes the batch rename, not 53 wholly new capabilities |

The manifest also contains **one resource** (`revit://guides/coordinator`) and **five prompts**: `model_overview`, `pre_issue_check`, `warnings_triage`, `parameter_fill_report`, `batch_audit`. Selecting `core,read` exposes **20 tools**; `core` is always included. Toolsets are context/visibility control, **not authorization**. Upstream documents an approximately 25.7k-token full schema payload versus 6.7k for `core,read`; these are byte/4 estimates, not tokenizer measurements reproduced here. [Toolsets][u-toolsets] [Inventory/size documentation][u-tools] [Prompts][u-prompts]

### Fork capabilities upstream does not replace

Retain `revit_create_floor`, `revit_create_level`, `revit_set_phase`, `revit_merge_phases`, `revit_set_view_lighting`, `revit_export_element_ids`, `revit_reset_element_ids` and `revit_rebuild_model_ids`. Also preserve existing callers of `revit_batch`, or migrate them deliberately. Generic C# execution is not a contract-compatible substitute for these typed tools. Local validation records actual Revit 2020 checks for the export/reset/rebuild family and live level creation on both 2020 and 2026. Its older fourteen-action validation statement predates the present sixteen-action inventory; do not treat it as validation of every current tool. [Local tool definitions][l-actions] [Local read definitions][l-server] [Local validation record][l-validation]

## 3. Feature families worth porting

### A. Audit evidence and review deliverables: highest immediate value

- **Schema-v1 model snapshots** combine model identity/health, warning groups, family signals and selected parameter-fill rules. Common `skipped`/`skippedCount` diagnostics make incomplete answers explicit.
- **Offline Excel reports** compare current/previous snapshots and carry Summary, Warnings, Families, Parameters, Skipped, optional Changes and Findings sheets. Report generation needs no running Revit.
- **Element captures and issue registers** create highlighted 3D/plan PNG evidence without persisting model changes, then embed it in an Excel review register. Health checks can also write a workbook.
- **Coordinator prompts/guide/skill** standardize tool order, completeness qualifications and evidence-based findings.

This is a better first feature slice than indiscriminately importing every action: much of the reporting/prompt layer is Python-only, although acquiring snapshots and captures still needs compatible add-in work. New runtime dependencies are `openpyxl>=3.1.0` and `pillow>=10`. Captures are local/SSH only, not HTTP; register generation can retain a failed capture as a warning instead of failing the workbook. Reports require new output files and reject duplicate model titles for current/previous matching. [Snapshot commit][c-snapshot] [Report commit][c-report] [Read/report contracts][u-tools] [Prompts][u-prompts] [Dependencies][u-package]

**Keep collection separate from processing.** `revit_batch_start/status/cancel/fetch` drives a persistent supervisor and a separate read-only Revit worker; `revit_process_models` performs steps/scripts/exports/optional saves in the interactive session. The former closes without saving; the latter can write. Collection can survive an MCP client restart. It routes by saved year, allows in-memory upgrade without changing the source, recycles only its owned worker and records modal-dialog failures. [Batch implementation commit][c-batch] [Batch contract][u-batch] [Processing contract][u-actions]

Migration constraints: supported routing years are currently 2022–2027; UNC access needs trusted roots; RSN metadata needs a configured matching REST endpoint; cloud sources are unsupported. SSH worker startup needs an interactive scheduled task, a logged-in Windows user, and workstation validation. Revit licensing/memory must be checked. The recorded batch pass completed 11 of 13 models, stopped two at modifying-answer dialogs, and peaked near 7 GB; large upgraded models took 12–26 minutes to open. This is useful operational evidence, not a promise for every model. [Batch prerequisites][u-batch] [Live evidence][u-validation]

### B. Multi-client coordination and action visibility: platform-level value

Upstream adds per-process channels, a same-user named pipe, a shared scheduler for pipe/HTTP/file jobs, independent client job identities, long-action progress polling and cancellation. The activity pane shows summaries and changed/created/deleted elements; `revit_undo_last` operates only while the MCP action is still Revit's most recent eligible undo entry. This is valuable for multiple AI clients, long rebuild/export tasks and user confidence. [Coordination commit][c-coordination] [Transport contract][u-transport] [Activity/undo/jobs][u-actions]

Port as a coherent channel/scheduler/heartbeat feature, not a Python transport swap alone. Cancellation does not undo completed work or interrupt an already-running export/open/script. Long actions may return after a default 40-second tool budget with a `jobId`; callers must poll rather than resubmit. Add the same behavior to fork-specific long rebuilds only after defining their lifecycle and compatibility. [Long-job contract][u-actions]

### C. Views, sheets, schedules and bulk model edits: high practical value

New families cover view creation/duplication/template application, sheet creation/view placement, graphic highlighting, filtered bulk parameter edits, rotation/copy/mirror/type changes, bulk family loading and placement at rooms. Later HEAD adds **tagging** and **schedule creation** with named fields/filters/sorting. These directly complement the fork's floor/level/phase tools. [Session feature commit][c-session] [Later tagging/schedule commit][c-policy] [Action contracts][u-actions]

Respect the allowlists: tagging, schedule creation and sheet placement are not general batch steps. Family audit/edit coverage is version-dependent; upstream documents full purge candidates on 2024+, but only families/types on 2022–2023. Older link graphics inspection is also narrower. These descriptions do **not** establish 2020 support. Typed parameter resolution and the new numeric value contract need explicit migration tests against the fork's string-valued `revit_set_parameter`. [Family/view read constraints][u-tools] [Parameter/action contracts][u-actions] [Local parameter interface][l-actions]

### D. Session, exports, CAD/MEP and C# execution: useful but second-stage

Session tools add open/new/activate/close/save/sync and UI state. Exports cover PDF/DWG/IFC/schedule CSV plus NWC with XML settings. Other tools compare/align linked datums, manage families/links, construct walls from CAD lines and route basic MEP segments. Multi-model processing composes steps, scripts, exports, save-copy/in-place and close. [Coordination commit][c-coordination] [Session feature commit][c-session] [Action reference][u-actions]

Constraints matter: NWC requires the matching workstation exporter; exports and saved outputs generally stay on the workstation, unlike report/PNG downloads. Save/sync/close are not guaranteed undoable model transactions. Save and sync require confirmation; link removal cannot be restored by Revit Undo. C# execution uses a confirmation flow, cannot be stopped while running, defaults to an owned transaction and currently refuses `transaction="none"`. The store variant disables code execution until explicitly enabled. These are new product capabilities needing separate acceptance decisions, not “turn them all on” upgrades. [Confirmation/session/export contracts][u-actions] [Store code policy][u-updates]

## 4. Build, packaging, CI and version support

| Area | Local HEAD | Upstream HEAD | Useful adoption constraint |
| --- | --- | --- | --- |
| Revit configurations | R20 and R22–R27 | R22–R27 | Preserve R20 throughout build, package and test matrices; neither add-in configuration list includes R21. |
| Core targets | `net47;net48;net8.0` | `net48;net8.0` | Retain `net47`; dropping it removes the fork's older runtime target. |
| Toolchain floors | Python 3.11+, .NET SDK 10.0.100 | Same floors | No Python minimum or SDK-major migration is required by this comparison. |
| Python packaging | `mcp>=2.0.0`, Ruff 0.16.7 | Adds OpenPyXL/Pillow, Ruff 0.16.10, committed uv/runtime locks | Adopt report dependencies and a coherent frozen-lock workflow, not only new dependency declarations. |
| Revit API package selection | Year-bounded package ranges | Exact lowest-build pins and post-repack reference pin verification | Add a separately established R20 package/assembly pin before enabling the upstream verification target. |
| CI year coverage | Builds R20/R22/R26/R27 for PR/package checks; release builds seven configured years | Builds all six R22–R27 with locked restore; richer installer/bundle checks | Extend the upstream jobs/lock files/asset assertions to R20 instead of replacing the local matrix. |
| Distribution | Separate add-in and Python launch; MCPB | Regular/managed/store bundles and MSIs; self-contained Windows server in MSIs/store bundle | Store/bundled assets are HEAD features, not observed v0.9.1 assets. Remote macOS/Linux clients still need an appropriate server/transport. |

Sources: [Local add-in project][l-addin], [local Core project][l-core], [local SDK][l-sdk], [local package][l-package], [local CI][l-ci], [local release matrix][l-release], [upstream add-in project][u-addin], [upstream Core project][u-core], [upstream SDK][u-sdk], [upstream package][u-package], [upstream CI][u-ci].

Additional worthwhile delivery improvements:

1. **Reproducible artifacts and schema drift checks.** Locked NuGet restores and frozen uv inputs; generated MCPB/tool manifests; a committed golden tool-schema snapshot; offline Autodesk bundle validation checking per-year paths and excluding Autodesk binaries. These are better than manually extending an inventory and hoping docs, bundles and schemas agree. [Manifest/validator documentation][u-manifest-doc] [Stability contract/tests][u-stability] [CI][u-ci]
2. **Explicit deployment channels.** `release`, `managed`, `store`, `dev` distinguish update behavior. Release per-user installs now default to notification, managed/store never check for add-in updates, dev is never auto-installed over, and the frozen server never checks PyPI. Managed bundles omit the server and document a pinned external launcher; store packages contain the server. [Update channels][u-updates] [Installation][u-install] [Frozen-server update switch][u-server-updates]
3. **Self-contained Windows server.** PyInstaller `onedir` packaging installs hashed build/runtime dependencies and carries Python/runtime-package licenses. CI smoke-tests initialize/tool-list behavior before packaging. This reduces Python/uv setup burden on Windows, but creates another artifact to test and maintain. [Build source][u-server-exe] [Store commit][c-store] [CI smoke/build][u-ci]
4. **Machine policy and client setup.** Registry/ProgramData settings, ADMX templates, per-tool allow/deny, read-only and execute-code controls, update/logging choices, and a ribbon dialog for Claude Desktop/Cursor/VS Code/Codex setup with backup/atomic changes. Policy should supplement—not replace—the fork's existing hard gates. Server-side policy for locally handled tools needs the server on the workstation; it is not a blanket remote-client enforcement claim. [Policy reference][u-policy] [Client setup][u-install]
5. **Release evidence.** CycloneDX SBOM generation, scheduled dependency audits, checksum/provenance checks, and conditional SignPath signing are useful. Signing still depends on external project approval/configuration; the workflow explicitly allows unsigned output when its credentials/settings are absent. Do not describe future releases as signed just because a signing job exists. [Release workflow][u-release] [Dependency audit][u-audit] [Install/signing notice][u-install]

Upstream also schedules WinGet submission weekly and gates release-please merges to Monday in Europe/Moscow, with a hotfix override. WinGet submission has an explicit upstream-repository guard and dedicated-token requirement; publishing identities/secrets/OIDC grants do not become valid for this fork by copying YAML. The release cadence is optional policy, not a feature dependency. [WinGet workflow][u-winget] [Release window][u-window] [Publishing workflow][u-release]

## 5. Breaking migrations to decide before any port

| Change | Consequence for this fork |
| --- | --- |
| `REVIT_MCP_ALLOW_WRITE` and workstation `allow-write` removed upstream; default-on actions, `REVIT_MCP_READ_ONLY`/`read-only` opt-out | **Do not inherit the widening default.** Preserve both existing opt-in gates required by local instructions; add organizational restrictions above them. |
| File channel requires version 2; no shared-root/old-heartbeat fallback | The local transport/add-in pair cannot be upgraded independently to HEAD's contract. Same major version is necessary but insufficient: channel version and advertised command checks also apply. |
| Per-process named pipe, queue, IDs and discovery metadata | Update heartbeat parsing, transport, scheduler and response handling together. Old shared trigger publication is not compatible. |
| HTTP now off by default | Preserve a deliberate remote-use configuration. Existing `httpEnabled:true` settings stay enabled; migration does not switch stored settings off. |
| `revit_batch` → `revit_run_actions` | Keep a tested fork alias or update callers, docs, feature-site generator and MCPB manifest together; retain custom batch steps. |
| `save_to` → `output_path`; `response_timeout_s` → `timeout_seconds`; `wait_s` → `wait_seconds`; `dest_dir`/export output `folder` → `output_dir` | PNG callers using the fork's `save_to` need migration. Not all old names exist locally, but newly ported upstream tools must use the new contract consistently. Former names are not silently accepted. |
| Uniform read diagnostics and error/refusal handling | `revit_list_instances` changes from a bare list to `{instances, skipped, skippedCount}`. Read diagnostics move to the common shape. Callers should inspect `isError` for tool failures, versus `success:false/errorCode` for refused/failed actions. |
| Stricter argument and parameter typing | Unknown tool arguments are rejected; valid documented aliases remain. Parameter writes accept JSON strings/integers/numbers upstream rather than only the fork's string input. Update caller schemas and tests. |
| Delete over 500 elements, save/sync, overwrites, link removal and code confirmations | Clients must display the preview and await human agreement before retrying with the single-use token. Batch deletion over the threshold is refused rather than automatically confirmed. |
| Server/display name now `Model MCP`; internal `ReadJob`/`RevitReadChannel` renamed | MCP configuration keys and package/CLI names stay unchanged; name-matching integrations and internal Python imports may break. |
| Upstream update feed/package identity | Pin fork builds and disable upstream checks until a deliberate release-feed/package strategy exists; a shared `0.x` major does not prove fork compatibility. |

Sources: [Default-on breaking commit][c-coordination], [public contract breaking commit][c-contract], [product rename commit][c-brand], [transport/version rules][u-transport], [feed contracts][u-feed], [read/error reference][u-tools], [confirmation/actions][u-actions], [local registration][l-actions], [local instance output][l-server], [local hard rules][l-agents]. The upstream 1.x stability promise starts **from 1.0.0**, not from the still-0.9.1 HEAD package field; it cannot erase these pre-1.0 breaking changes. [Stability policy][u-stability]

### Revit 2020 preservation checklist

- Keep R20 add-in/solution/release/installer/CI entries and Core `net47`, not merely a documentation row.
- Extend frozen NuGet locks and minimum API-reference pins to R20; upstream has no R20 pin and explicitly errors when the configured minimum assembly version is missing.
- Keep the existing compatibility branches and all custom tool contracts/tests. Before implementing or reviewing any newly ported C# Revit API code, query the version-matched 2020/2026 corpus; then compile R20 and test on Revit 2020. This report did not perform that API review.
- Revalidate new family/schedule/tag/export/UI behavior on 2020 rather than extrapolating upstream's R22–R27 live checks. Retain the fork's known working 2020 models/evidence.
- Add R20 routing, installer content/upgrade/uninstall checks and package manifests when adopting the supervisor or bundled delivery. A modern runtime that opens an old model in memory is not a substitute for supporting the 2020 runtime.

Evidence: [Local projects][l-addin] [Local Core target][l-core] [Local release years][l-release] [Local installer][l-installer] [Upstream pin/error target][u-addin] [Batch year routing][u-batch] [Local live evidence][l-validation] [Upstream live evidence][u-validation].

## 6. Recommended adoption order and evidence boundaries

**Before the feature sequence, port selected security and reliability fixes with their regression tests.** Section 7 names the candidates and the local behavior they improve. Do not require a full scheduler migration before addressing the independently portable fixes.

1. **Contract/CI preparation:** freeze schemas for the fork's 35-tool maximum, preserve gates/R20/custom tools, define backward aliases and package/feed identity. Port generated manifests, locked builds and artifact tests with the seven-year fork matrix.
2. **Read/review slice:** prompts/guide, skipped diagnostics, snapshots and offline report. Add captures/registers after the transport and R20 behavior are validated.
3. **Coordination slice:** per-process discovery/channel, scheduler, named pipe, progress/cancellation and activity/undo. Migrate client response parsing together and retain opt-in behavior.
4. **Productivity slices:** bulk parameters/families, views/sheets, tags/schedules, then selected coordination/CAD/MEP/export tools. Keep fork floor/level/phase/lighting/ID features in every registry and test inventory.
5. **Explicit higher-impact opt-ins:** document save/sync, multi-model modifications and C# execution. Managed/store deployment and enterprise policy follow once fork release identity and Windows acceptance are settled.

This ordering is an engineering recommendation inferred from feature dependencies and public contracts, not an upstream promise or an effort estimate. The large coordination and session commits are useful reference slices, not safe one-command cherry-picks into this divergent fork. [Coordination commit][c-coordination] [Session commit][c-session] [Policy commit][c-policy]

The delegated feature research used existing Git objects only: `git log/show/ls-tree/rev-list`, with text snapshots materialized outside the working tree and read through file tools. Git reports 117 upstream-only and 55 local-only commits at these endpoints. The lead first ran `git fetch --no-tags upstream main`, updating the upstream tracking ref, then inspected source snapshots and previewed the committed-tree merge without changing the working tree or checking out another branch. No source edit, existing-document edit, issue operation, dependency installation or Revit action was performed. No C# Revit API implementation internals were reviewed. Only this new report was added and supplemented. The user's existing modified and untracked files were left untouched.

Local links below open the workspace files; analysis refers to their **fixed HEAD content**, read from Git snapshots, not the user's uncommitted changes. Previous [analysis synthesis](</home/roky/revit-mcp/analysis/t5-synthesis.md>) is historical context, not evidence for the current 35/79 inventories. Upstream citations use immutable commit/blob URLs. The GitHub latest-release endpoint is necessarily mutable; its observed result is recorded above. No builds, suites or live runs were reproduced; upstream validation claims are attributed to the owning source and retain its gaps. The older [validation page][u-validation] is supplemented by the later [policy][c-policy] and [store][c-store] commit records, not silently treated as comprehensive HEAD acceptance.

## 7. Lead verification: security backports and merge risk

### First update batch: security and reliability

These are targeted update candidates, not a claim that every upstream implementation has been security-audited. The local observations below come from the current working-tree source, whose server implementation matches the fixed HEAD inspected for this comparison.

| Candidate | Local observation | Recommended port and immutable upstream evidence |
| --- | --- | --- |
| HTTP endpoint token proof | The client validates the health JSON, then sends a bearer token without checking that the endpoint owns it. | Port the nonce/HMAC proof on both Python and add-in sides. The newer client intentionally refuses an older add-in, so deploy the pair together. This does not replace TLS or a tunnel. [Commit 69af8d0](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/69af8d01e60d6f0fbf3cbe96c99b452207d09d12>) and [local HTTP client](</home/roky/revit-mcp/server/revit_model_mcp/http_host.py#L47-L83>). |
| SSH and artifact hardening | The multiplexing directory is created/chmodded without an owner/symlink check. The shared artifact helper checks existence then writes bytes, unlike the HTTP path's exclusive create. | Port secure multiplexing-directory validation, transport/name validation, PNG validation and safer artifact creation. Preflight the local destination before deleting a remote capture. [Commit 002fb17](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/002fb17e35783ee7700e4ef8af5c3c22e81edc18>), [commit a10a0cc](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/a10a0cc60ad4b91d8c274dd13bd24db640a3a552>), [local SSH setup](</home/roky/revit-mcp/server/revit_model_mcp/ssh_host.py#L323-L342>) and [local artifact helper](</home/roky/revit-mcp/server/revit_model_mcp/artifact_download.py#L8-L22>). |
| SSH timeout budget and connection reuse | `_reserve_connection()` executes before the timeout on process communication; waiting for a rate-limit slot is outside that budget. | Bound limiter wait and execution by one caller deadline; avoid throttling an already multiplexed connection as though it were a new connection. [Commit 1e93efe](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/1e93efec3db334598a046926726ab7c9d25e6e0a>), [commit 99dfba8](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/99dfba8>) and [local execution](</home/roky/revit-mcp/server/revit_model_mcp/ssh_host.py#L346-L355>). |
| Terminal result preservation | The channel's cleanup can include the observed response after an error or timeout; progress and terminal responses need separate treatment. | Adapt the terminal-result preservation fix and its regression tests to the fork's long rebuild action as well. Preserve the warning that timeout is not evidence an action did not commit. [Commit b1ae1d5](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/b1ae1d5694571f196c5e03aa401bdbe28b8a7157>) and [local cleanup](</home/roky/revit-mcp/server/revit_model_mcp/revit_channel.py#L442-L475>). |
| Response redaction | Local redaction scrubs `documentPath` and `path`, not paths embedded in error/warning/message strings. | Port message-field and central-path redaction with tests. Apply it consistently to the fork's custom action failures without promising that all arbitrary model strings are scrubbed. [Commit 6c557aa](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/6c557aa97a3ecd269207203dac40f966253a2bbd>) and [local redaction](</home/roky/revit-mcp/server/revit_model_mcp/server.py#L44-L56>). |
| HTTP resource bounds | The request body has a 1 MiB accumulated-size cap, but the read loop has no independent total read deadline. | Port declared-size rejection, read deadlines, result-count/byte caps, listener status and graceful drain. The result-retention/scheduler part must be adapted to the fork or migrated as one coordinated slice, not cherry-picked in isolation. [Commit db5ed7d](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/db5ed7d>), [commit 61a3567](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/61a35670f785a7ac923fbedf65f1789fece98946>) and [local body loop](</home/roky/revit-mcp/src/RevitModelMcp.Addin/Control/HttpChannel.cs#L130-L147>). |
| Strict public contracts | Local batch models already forbid extra keys, but the same rule needs enforcement across all public tool calls, including documented aliases. | Adopt the all-tool unknown-argument guard and schema snapshot tests, adapted to both default read-only registration and explicitly enabled fork actions. Preserve intentional legacy aliases. [Commit bff8d7c](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/bff8d7c61a3b0c7376ba3794fc183289c63b93ad>) and [upstream schema regression tests](<https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/server/tests/test_tool_schemas.py>). |

Path/ACL hardening is also relevant before adopting open/save/export capabilities: upstream explicitly restricts the file channel to the current user and introduces trusted network-root rules. Extend equivalent checks to the fork's workbook-export and model-rebuild paths if this policy is adopted; copying only the upstream tool allowlist would miss the fork-specific tools. [Channel ACL commit](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/2f9f172>) [File-path validation commit](<https://github.com/sharafutdinovdi/revit-model-mcp/commit/4b09359>)

### Committed-tree merge preview

The lead ran `git merge-tree --write-tree --name-only HEAD upstream/main`. The intentional nonzero result was **exit 1: merge conflicts**, not an executed working-tree merge. There are **49 conflicted paths**. A merge-base path comparison reports **219 locally changed paths**, **449 upstream changed paths**, and **68 paths changed on both sides**. The overlap includes 9 server, 23 add-in/Core, 2 test, 8 workflow, 2 build and 14 documentation paths; the remaining 10 are root/other paths.

The most important conflicts span the Python tool registry/actions/channel/SSH modules; C# application, action parsers/executors and HTTP channel; add-in project and solution; installers and release workflows; package/release metadata; and documentation/site navigation. The user's **37 already-modified tracked files and nine untracked entries** existed before the new report and are not included in this committed-tree preview. They need separate preservation before any implementation branch is created.

Do not perform a wholesale merge or resolve conflicts by taking upstream wholesale. First preserve the user's work, then implement isolated backports with regression tests and paired server/add-in deployment. Keep release-please ownership of version/changelog fields. Validate Python/Core tests, all seven configured Revit years including R20, Windows packaging and representative live actions before accepting an update. This research did not run those acceptance checks.

## Source references

[u-tools]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/tools.md>
[u-actions]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/actions.md>
[u-toolsets]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/server/revit_model_mcp/toolsets.py>
[u-manifest]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/tool-manifest.json>
[u-manifest-doc]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/tool-manifest.md>
[u-prompts]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/prompts.md>
[u-batch]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/batch.md>
[u-transport]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/transport.md>
[u-feed]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/feed-format.md>
[u-stability]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/stability.md>
[u-validation]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/validation.md>
[u-package]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/server/pyproject.toml>
[u-sdk]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/global.json>
[u-addin]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj>
[u-core]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/src/RevitModelMcp.Core/RevitModelMcp.Core.csproj>
[u-ci]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/.github/workflows/ci.yml>
[u-release]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/.github/workflows/release.yml>
[u-audit]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/.github/workflows/dependency-audit.yml>
[u-winget]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/.github/workflows/winget.yml>
[u-window]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/.github/workflows/release-window.yml>
[u-updates]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/updates.md>
[u-server-updates]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/server/revit_model_mcp/updates.py>
[u-server-exe]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/build/server-exe/build.py>
[u-install]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/install.md>
[u-policy]: <https://github.com/sharafutdinovdi/revit-model-mcp/blob/c1e23f5c5dd1f926be0b36d98d21461b2ebff645/docs/admin/policy-reference.md>
[c-coordination]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/42b6aa366377054786cd3468c686e7876713d328>
[c-snapshot]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/27a1cd2afe96b3a44b470c156bd2c369289b31c2>
[c-report]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/ca8963e657ee6d8db374aa43348a74afd02b6ccd>
[c-batch]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/e7654de5024c896338991aa64be0a7654e2f9129>
[c-session]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/f646389f81cf206c26ed7a4e08b2ee2affcfda7c>
[c-policy]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/41be1fe645a50fd811d7cb3740afe6fbcca6bfd6>
[c-store]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/7b86e56a379aedb06a9557fd34febd8b69e44c98>
[c-contract]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/a9e14a504eb4f307210ce6dfb48116cd232e99b5>
[c-brand]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/5c56f89ac727c9553e5ecacbf7de26d6d4ccb091>
[release-api]: <https://api.github.com/repos/sharafutdinovdi/revit-model-mcp/releases/latest>
[release-page]: <https://github.com/sharafutdinovdi/revit-model-mcp/releases/tag/v0.9.1>
[release-commit]: <https://github.com/sharafutdinovdi/revit-model-mcp/commit/d61094f41976dec852db63b83a2d3e93a7435f4c>
[l-agents]: </home/roky/revit-mcp/AGENTS.md#L75-L91>
[l-addin]: </home/roky/revit-mcp/src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj#L1-L38>
[l-core]: </home/roky/revit-mcp/src/RevitModelMcp.Core/RevitModelMcp.Core.csproj#L1-L14>
[l-sdk]: </home/roky/revit-mcp/global.json#L1-L10>
[l-package]: </home/roky/revit-mcp/server/pyproject.toml#L5-L45>
[l-actions]: </home/roky/revit-mcp/server/revit_model_mcp/actions.py#L219-L698>
[l-server]: </home/roky/revit-mcp/server/revit_model_mcp/server.py#L281-L780>
[l-ci]: </home/roky/revit-mcp/.github/workflows/ci.yml#L65-L119>
[l-release]: </home/roky/revit-mcp/.github/workflows/release.yml#L40-L65>
[l-installer]: </home/roky/revit-mcp/install.ps1#L32-L64>
[l-validation]: </home/roky/revit-mcp/docs/validation.en.md>
