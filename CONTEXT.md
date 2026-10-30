# Context

Revit Model MCP exposes a live Revit model to an MCP client. A C# add-in runs
inside Revit and owns every Revit API call. A Python server runs on the client's
machine and exposes tools over stdio, SSH or HTTP.

This repository is a fork. The add-in and server come from upstream. A bounded
fork layer adds eight actions the upstream product does not have.

Use these terms in issues, specs, test names and commits. Do not invent
synonyms. Where a word is overloaded, the table says which reading is intended.

## Layers

| Term | Meaning | Where |
| --- | --- | --- |
| add-in | C# assembly loaded into Revit. Owns Revit API access through `ExternalEvent`. | `src/RevitModelMcp.Addin/` |
| Core | Revit-independent C# library. Parses contracts, builds results, holds policy and activity types. Has no Revit API reference. | `src/RevitModelMcp.Core/` |
| server | Python process that registers MCP tools and moves jobs to the add-in. | `server/revit_model_mcp/` |
| channel | The mailbox carrying one job to the add-in and its result back. Three kinds: file, pipe, HTTP. | `revit_channel.py`, `pipe_host.py`, `http_host.py` |
| transport | How the server reaches the add-in: stdio (local), SSH (remote), HTTP. | `server.py`, `ssh_host.py` |
| fork layer | Code this fork adds on top of upstream. Lives in `Fork/` directories and one Python module, never scattered into upstream files. | `src/RevitModelMcp.Core/Fork/`, `src/RevitModelMcp.Addin/Fork/`, `server/revit_model_mcp/fork_actions.py` |

## One call, four words

A single tool call is described by four different identifiers. Confusing them is
the most common source of wasted work in this repository.

| Term | Meaning | Example | Where |
| --- | --- | --- | --- |
| tool | The MCP tool name the client sees. Always prefixed `revit_`. Snake case. | `revit_run_actions` | `server.py` `@addressed_tool`, `actions.py` `@action` |
| command | The wire command string the add-in dispatches on. Kebab case. | `batch` | `Application.SupportedCommands`, `ActionJobParser.IsAction` |
| action | An entry in the action vocabulary: one mutating verb the add-in knows how to run. | `batch`, `create-wall` | `ActionJobParser.IsAction` |
| step | One `ControlJobContract` inside a batch's `Steps` list. A step carries an `action` plus its arguments. | `{"action": "create-wall", ...}` | `ActionJobParser.cs` `Steps`, `actions.py` `ActionStep` |

Tool and command differ on purpose. `policy.py` holds the mapping:
`normalize_tool` strips the `revit-` prefix, lowercases, and applies
`_COMMAND_ALIASES = {"run-actions": "batch", "batch-start": "batch-supervisor-start"}`.
A fork action must appear in both vocabularies, and the tool name must normalize
to its command.

## Read tools and action tools

| Term | Meaning |
| --- | --- |
| read tool | A tool whose command maps to a `ControlJobKind` and only reads. Registered with `@addressed_tool`. |
| action tool | A tool that mutates the model. Registered with `@action`, sent as an action job, subject to the write policy, and required to support `dry_run`. |
| control job | The C# job shape for read work. Parsed by `ControlJobParser.FromContract`. |
| action job | The C# job shape for mutating work. Parsed by `ActionJobParser`, runs inside a transaction. |

## batch means four different things

The word is overloaded. Never write `batch` alone.

| Reading | What it is | Command or tool |
| --- | --- | --- |
| a batch of steps | Up to 50 actions run as one undo step. Rolls back entirely on the first failure. | tool `revit_run_actions`, command `batch` |
| the C# dispatch case | The `batch` case in `ActionCommandExecutor` that loops the steps. | `ActionCommandExecutor.cs` |
| the batch supervisor | A separate process that opens many models and feeds each one a step list. Survives the add-in restarting. | tools `revit_batch_start` / `_status` / `_cancel` / `_fetch`, command `batch-supervisor-start` |
| the removed fork tool | This fork's old `revit_batch`. Deleted; `revit_run_actions` does the same work. | gone |

Say "a batch of steps", "the supervisor", or "`revit_run_actions`". Never say
"batch" on its own.

## Change vocabulary

| Term | Meaning |
| --- | --- |
| verification block | The `verification` member of an action result: before and after facts, changed elements, and what a dry run would create. Backed by `ActionFacts`. |
| before / after facts | Per-element observable state captured around the transaction. Compared to prove the action did what it claimed. |
| dry run | Runs the action, then rolls back, and returns the verification block. Every action tool supports it. |
| undo step | One Revit transaction. A whole batch of steps is one undo step. |
| rehearsal | A dry run whose verification block reports the cost of the real run, such as how many elements would lose their ids. |

## Policy

| Term | Meaning |
| --- | --- |
| policy | Machine and organization settings that decide whether writes, code, updates and HTTP are allowed. |
| fail closed | When the policy file cannot be read, the product behaves as read-only with code, updates and HTTP off. |
| read-only | No action tool runs. Tools stay listed and refuse with a read-only error code. Read tools keep working. |
| write gate | The check that refuses an action tool. The policy is the only gate. There is no second environment-variable gate. |

Policy keys: `ReadOnly`, `ToolDeny`, `ToolAllow`, `ExecuteCode`, `UpdateMode`,
`TrustedNetworkRoots`, `LogDir`, `LogRetentionDays`, `RedactPaths`, `HttpEnabled`.

## Working on the fork layer

| Term | Meaning |
| --- | --- |
| base | The exact upstream commit this fork extends. Recorded as a full SHA, never a branch name. |
| hook | A named, bounded edit inside an upstream file, placed in a fallback branch so upstream code keeps its own path. Seven hooks exist. |
| thin | The fork layer stays within 80 changed lines across those 7 hooks. Exceeding either number means the design drifted. |
| tracer action | The first fork action ported end to end, used to prove the seam. Currently `set_view_lighting`. |
| intake | Reading what upstream shipped since the base, and deciding for each commit: port, adapt, or ignore. |
| ledger | The written record of those decisions, one bucket per commit. `analysis/upstream-port-ledger.md`. |
| cursor | The upstream commit the ledger has classified up to. Moving it is only allowed when every commit up to it is classified. |

## Avoid

- Avoid "plugin" for the add-in; the repository says add-in.
- Avoid "API" for the MCP tool surface; say tool.
- Avoid "handler" for a hook; say hook.
- Avoid "bridge" and "proxy" for the channel; say channel.
- Avoid "sync" for the intake; say merge, and only when a merge is what happens.
