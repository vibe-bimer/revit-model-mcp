# Working on a Windows workstation

This page explains how to develop this repository directly on the Windows workstation that runs Revit. Revit and the add-in live on the same machine, so a build is a deploy and a call is local: nothing has to be copied between a development machine and the workstation.

!!! note "Scope"
    This page covers developing on the workstation itself. When the development machine and the workstation are separate, use the remote channel instead; see [transport](../transport.en.md).

<a id="the-two-machines"></a>
## How the two machines divide the work

| Location | Purpose | Channel |
| --- | --- | --- |
| Development machine (not covered here) | Edit, commit, push | Remote |
| Workstation (this page) | Build the add-in, run Revit, verify on the real API | Local channel |

The repository lives at `C:\Users\Administrator\revit-model-mcp` on the workstation.

<a id="toolchain"></a>
## Toolchain

The workstation already has:

- .NET SDK 10.0.401 and 8.0.427 (`global.json` asks for 10.0.100, which `rollForward: latestMinor` satisfies);
- Python 3.14 and `uv` (`C:\Users\Administrator\.local\bin\uv.exe`);
- Git and VS Code.

There is no Visual Studio or Rider on the workstation, only VS Code. With the C# extension (`ms-dotnettools.csharp`) VS Code can attach a debugger.

<a id="one-time-setup"></a>
## One-time setup

```powershell
cd $env:USERPROFILE\revit-model-mcp\server
uv sync                      # installs the server dependencies; the version comes from server/pyproject.toml
```

`uv sync` installs this repository into the environment as an editable package. **Without it the server reports the add-in version as 0.0.0** and refuses every call:

> This server needs a Model MCP add-in of major version 0; the Revit workstation has 1.0.0+…

<a id="the-dev-loop"></a>
## The development loop

### 1. Close Revit

Revit holds the add-in DLLs open, so it has to be closed before a build.

```powershell
# First confirm the model has no unsaved changes
# (from an MCP client on the workstation itself, call revit_ui_state and read activeDocument.isModified)
Stop-Process -Name Revit -Force
```

`CloseMainWindow()` is blocked by the save prompt, so closing Revit after a verification always uses `Stop-Process -Force` — provided the model was never saved in the first place.

### 2. Build and deploy

`DeployAddin` defaults to `true` in the csproj and the Nice3point SDK writes the output straight into the add-in folder on Windows, so one command both builds and deploys:

```powershell
cd $env:USERPROFILE\revit-model-mcp
dotnet build src/RevitModelMcp.Addin/RevitModelMcp.Addin.csproj -c Debug.R26 -p:LaunchRevit=false
```

The deployment target is `%APPDATA%\Autodesk\Revit\Addins\2026\RevitModelMcp\`.

The first build in a fresh clone fails once:

```
error NETSDK1004: ... Assets file ... not found. Run a NuGet package restore
```

The `PinMergedRevitApiReferences` target at the end of the build runs `build/RevitApiReferencePin` with `--no-restore`, and that subproject has not been restored yet. **Restore it once on its own**:

```powershell
dotnet restore build/RevitApiReferencePin/RevitApiReferencePin.csproj
```

After that, `dotnet build` stops failing.

`Debug.R22` through `Debug.R27` work the same way, and the year in the deployment folder follows the configuration. The csproj in this repository only defines R22–R27; there is no R20.

### 3. Sign

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $env:USERPROFILE\sign-addin.ps1
```

The certificate is `CN=RevitModelMcp Dev`. The script re-signs `RevitModelMcp.dll` in every year folder and prints a line such as `2026: RevitModelMcp.dll signed`. **Re-sign after every new build.**

### 4. Start Revit

A command that arrives over SSH runs in Windows session 0, where `Start-Process Revit.exe` exits immediately. The interactive session is session 1, so start Revit through a scheduled task:

```powershell
schtasks /Run /TN RevitMcpLaunchVerify
```

That task runs `C:\Users\Administrator\startrevit.ps1`, which opens `E:\revitmcp-test\mcp-verify-2026.rvt`. Revit is up after about 75–90 seconds.

The repository also ships a `RevitMcpLaunch` task, which opens a different, larger project model; do not use it for verification.

### 5. Call over the local channel

```powershell
cd $env:USERPROFILE\revit-model-mcp\server
$env:REVIT_MCP_HOST = 'local'
uv run python -m revit_model_mcp.server
```

`REVIT_MCP_HOST=local` makes the server publish to the same channel directory, `%LOCALAPPDATA%\RevitModelMcp\`, through the local PowerShell, with no SSH round trip. Measured on the workstation: `revit_ping` takes about 0.4 s and `revit_list_catalog` about 0.04 s.

<a id="debugging"></a>
## Setting breakpoints

The action code in the `Fork*` layer is all in static methods, so breakpoints land cleanly:

- `src/RevitModelMcp.Addin/Fork/ForkColumns.cs` — `Apply`, `Validate`, `Read`;
- `src/RevitModelMcp.Addin/Fork/ForkGrids.cs` and `ForkFamilies.cs` — the same shape;
- `src/RevitModelMcp.Addin/Fork/ForkActions.cs` — the three switches that dispatch a command to its `Fork` class.

In VS Code, open Run and Debug, choose Attach to Process, attach to `Revit.exe`, then trigger one MCP call and the breakpoint stops.

Without an IDE the only option is to infer behavior from the response JSON — for example, the `boundingBoxMinMm` and `boundingBoxMaxMm` of `verification.after` show whether a rotation and an offset took effect.

<a id="gates"></a>
## Gates

Some gates behave differently on Windows than on a development machine:

- **The C# formatting hook actually runs.** The `dotnet format` hook prints a notice and exits successfully off Windows; on Windows it edits files. The first run may produce a batch of formatting changes, so read the diff before committing.
- **Line endings.** The repository has `.editorconfig` and a Git CRLF setting; do not change `core.autocrlf`.
- **PowerShell script encoding.** A `.ps1` containing Chinese must be UTF-8 with BOM, otherwise PowerShell decodes it as GBK and fails with "字符串缺少终止符".
- **Command output encoding.** PowerShell output that comes back over SSH is GBK; pipe it through `iconv -f GBK -t UTF-8` before reading.

The full gate list:

```powershell
cd $env:USERPROFILE\revit-model-mcp
dotnet test --project tests/RevitModelMcp.Core.Tests/RevitModelMcp.Core.Tests.csproj
cd server; uv run --with pytest pytest -q
cd ..; uvx ruff==0.16.10 check .; uvx ruff==0.16.10 format --check .
pre-commit run --all-files
python build/check_fork_budget.py
```

<a id="the-fork-bound"></a>
## The fork layer boundary

A new action tool has to go through the fork layer: `src/RevitModelMcp.Core/Fork/`, `src/RevitModelMcp.Addin/Fork/` and `server/revit_model_mcp/fork_actions.py`.

`build/check_fork_budget.py` sorts every changed file into one of three classes: hook (nine dispatch files, 80 changed lines in total), read (each one listed in `build/fork.json`'s `reads` table with its reason), and fork (path prefix). **Any file outside those three fails the gate as unowned** — upstream's `ActionMutations.cs` sits outside them, so it cannot be edited.

Registering a tool makes `ForkRegistry.IsAction` true on its own, so `ActionJobParser.cs` needs no validation branch for a fork command; the checks live in the `Validate` method of the matching `Fork*.cs`.

<a id="verification"></a>
## Verification on the real API

Verification records go into `docs/validation.md` and `docs/validation.en.md`, following the `revit_create_level` entry. Each action covers at least:

1. after a `dry_run` rollback `isModified` is still `false`, and the rolled-back element id cannot be found with `revit_element_details`;
2. a real write reports an id, a category, a type and a bounding box in `verification.after`;
3. an error path refuses with a stated reason;
4. after the write the model file's **size and mtime are both unchanged** — the action does not save the model.

`activeDocument.isModified` from `revit_ui_state` is the entry point for judging model state.

A model does not always contain the family a tool needs. Family files used in verification so far:

- columns: `C:\ProgramData\Autodesk\RVT 2020\Libraries\China\结构\柱\混凝土\混凝土 - 正方形 - 柱.rfa`;
- doors: `C:\ProgramData\Autodesk\RVT 2020\Libraries\China\建筑\门\其它\入口门厅.rfa`.

The 2026 Chinese library ships only the 结构预制 and 路径分析 folders; structural column families exist only in the 2020 library.

<a id="year-limits"></a>
## Year limits

The csproj in this repository only defines R22–R27. `Release.R20` fails to restore, so **a 2020 verification cannot be done inside this repository** — the validation pages must say "no 2020 record" rather than pretend otherwise. The workstation has Revit 2020 installed, but the add-in has no 2020 build configuration.
