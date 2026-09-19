# Adding Revit tools

How to add a read tool, an action tool, or a new Revit API surface to this
repository. Follow this document end to end before writing code.

## Step 0: verify the API in the local corpus

A local Revit 2026 API reference lives under `revit-corpus/` (28,796 CHM
documents with an FTS5 index). It is optional machine-local data: if the
directory is missing, skip this step silently and fall back to official docs.

Command line, from the repository root:

```sh
python3 revit-corpus/scripts/corpus_query.py overloads Floor.Create   # every overload page
python3 revit-corpus/scripts/corpus_query.py members FilteredElementCollector -k method
python3 revit-corpus/scripts/corpus_query.py 'Floor' -k class --show
```

Or through the `revit-docs` MCP connector (`revit_docs_symbol`,
`revit_docs_search`, `revit_docs_read`). `revit_docs_symbol` takes the bare
dotted name and handles FTS quoting for you.

Read the full document, not just the signature: overloads, parameters,
return values, exceptions and remarks matter. Example: `FilteredElementCollector`
requires at least one filter and prefers native filters over LINQ.

## Read tool checklist (8 sync points)

A job-based read tool touches both sides of the channel:

1. Python job construction: add a `ReadJob` classmethod in
   `server/revit_model_mcp/revit_channel.py` (follow `list_views`); shared
   filter semantics go into `universal_jobs.py`.
2. MCP registration: add the `@addressed_tool` function in `server.py` and
   its entry in the title map. A missing entry raises `KeyError`; titles are
   at most 40 characters (test-enforced).
3. Core contract: extend `ControlJobKind` and the `FromContract` switch in
   `Core/Control/ControlJobParser.cs` (universal queries use
   `UniversalJobParser.cs`).
4. Core models: add the response data type in `Core/Models/ReadCommandModels.cs`.
5. Addin reader: add a reader under `src/RevitModelMcp.Addin/Capture/`.
   Revit API references may appear only in the Addin project, never in Core.
6. Addin dispatch: add a case in `Control/ReadCommandExecutor.cs`.
7. Long jobs: if a single ExternalEvent may exceed 60 s, follow the paged
   session pattern in `ViewElementsSession.cs` and register the session in
   `ControlChannel.ProcessJob`.
8. Docs and tests: `docs/tools.md`, `README.md`, `docs/feed-format.md`;
   `EXPECTED_TOOLS` and `EXPECTED_PARAMETERS` in `server/tests/test_server.py`;
   parser tests under `tests/RevitModelMcp.Core.Tests/`.

New read tools must keep `readOnlyHint=true`; never widen read-only defaults.

## Action tool checklist (7 additional points)

Action tools extend the read channel and must repeat its discipline:

1. `server/revit_model_mcp/actions.py`: `@action` function plus its title
   entry; add batch-eligible arguments to `_BATCH_FIELDS`.
2. `revit_channel.py`: add the command to `ACTION_COMMANDS` so timeout and
   error semantics stay correct.
3. `Core/Control/ActionJobParser.cs`: `IsAction`, argument validation and
   the `ActionJobContract` fields.
4. `Addin/Control/ActionCommandExecutor.cs`: dispatch case and transaction
   policy (dry-run rollback, warning dismissal, dialog suppression).
5. `Addin/Control/ActionMutations.cs`: the mutation itself. Convert units
   explicitly (mm in, internal feet out) and reject read-only targets.
6. `Addin/Control/ActionVerifier.cs`: before/after facts; document the
   response shape in `docs/feed-format.md`.
7. Docs and tests: `docs/actions.md`, `README.md`, `server/tests/test_actions.py`.

Hard constraints:

- Both write gates stay: `REVIT_MCP_ALLOW_WRITE=1` in the server environment
  and the workstation `allow-write` file. Never weaken them.
- Mutations support `dry_run` and return a `verification` block.
- Actions never save the model.
- Revit 2022–2023 accept element IDs up to 2,147,483,647 only.
- `place_family` uses the level-based non-structural overload; hosted,
  face-based and adaptive families are out of scope.
- After a timeout, inspect the model before retrying; the job may have run.

## Worked example: `revit_create_floor`

The designated next action tool. Corpus facts (Revit 2026):

- `Floor.Create(Document, IList<CurveLoop>, ElementId floorTypeId, ElementId levelId)` — the core overload.
- `Floor.Create(Document, IList<CurveLoop>, ElementId, ElementId, Boolean, Line, Double)` — structural variant with slope.

Design notes:

- Accept points in model mm, build `CurveLoop` from `Line.CreateBound`
  segments, and close the loop explicitly.
- Resolve `floor_type` by name through `FilteredElementCollector` of
  `FloorType` (`null` picks the first basic floor type); resolve `level` by
  exact name.
- Verifier: before is empty, after is the created element metadata with its
  bounding box, mirroring `revit_place_family`.
- Add `create_floor` to `_BATCH_FIELDS` so it composes in `revit_batch`.
- Test matrix: dry-run rollback, real create plus verification, wrong type
  name error, open loop rejection.

## Build and deploy

- Compile check on Linux works with
  `dotnet build src/RevitModelMcp.Addin -c Release.R26 -p:DeployAddin=false -p:EnableWindowsTargeting=true`.
  (`UseWPF=false` is not enough for `net8.0-windows` targets: the
  WindowsDesktop reference pack resolves through `EnableWindowsTargeting`.)
  Windows PR CI remains the oracle for full builds.
- Run `dotnet test --project tests/RevitModelMcp.Core.Tests/RevitModelMcp.Core.Tests.csproj`
  and `cd server && uv run --with pytest pytest -q`.
- `dotnet format` (pre-commit) only runs on Windows; on Linux report it and
  rely on PR CI, per AGENTS.md.
- Deploy to the workstation: ILRepack only runs on Windows builds, so a Linux
  build produces separate assemblies. Copy `RevitModelMcp.dll`,
  `RevitModelMcp.Core.dll`, `JetBrains.Annotations.dll`,
  `Nice3point.Revit.Extensions.dll`, `Nice3point.Revit.Toolkit.dll`,
  `RevitModelMcp.deps.json` and `RevitModelMcp.runtimeconfig.json` over SSH to
  `%APPDATA%\Autodesk\Revit\Addins\2026\RevitModelMcp\`. Back up that folder
  first; the loaded DLL is locked while Revit runs, so deploy only with Revit
  closed. Never kill Revit remotely — coordinate the restart with the user.
- New tools reach MCP clients only when the Python server runs from this
  clone (`uv run --directory server revit-model-mcp`), not from the published
  `uvx revit-model-mcp` package. Point the connector at the clone while
  developing.
- Live smoke test through the `revit` MCP connector: `revit_ping`, then the
  new tool with `dry_run=true` first, then a real run plus verification and
  cleanup.

## Version caveats

The corpus covers Revit 2026 only. A corpus hit does not prove availability
in 2022–2025 or 2027: check existing `REVIT20XX_OR_GREATER` conditionals
(11 usages) and add per-year branches where the API differs. Live model
verification is required per supported year before release claims.
