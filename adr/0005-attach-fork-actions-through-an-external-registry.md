# 0005. Attach fork actions through an external registry reached from seven fallback hooks

- Status: Accepted
- Date: 2026-10-30

## Context

Adding one action to upstream 1.0 by following upstream's own shape touches eleven files: the action vocabulary, the dispatch switch, the two verification switches, the summary builder, the activity title dictionary, the supported-command list, the Python action step union, the Python registration list, the channel command list, the toolkit grouping, and the bundle manifest. Eight fork actions at eleven points is roughly ninety edits, and every upstream release re-conflicts at all of them.

The fork cannot keep its actions in a separate assembly. The verification helpers are `internal`: `ActionVerifier.CaptureBefore` and `CaptureAfter`, and the mutation helpers. A separate assembly cannot reach them. The contracts themselves are public, so logic that only touches contract types can live in Core; anything that captures or mutates must live in the Addin assembly.

Upstream already solves the naming half of this problem: `policy.py` maps a tool name to a differing command name through `_COMMAND_ALIASES`. So "the tool name is not the command name" is an established concept, not a fork invention.

## Decision

Fork actions live in a registry. Upstream code reaches the registry only from branches that today mean "I do not know this command."

Registry:

- `src/RevitModelMcp.Core/Fork/` holds the action definitions and any logic that touches only contract types.
- `src/RevitModelMcp.Addin/Fork/` holds anything that needs the Revit API or the internal helpers.
- `ForkActions` is the single registration point. It exposes the action names, the command list, and per-command lookup.
- `server/revit_model_mcp/fork_actions.py` registers the Python tools and builds its own send path from the existing `_send_action` and `policy_gate`; it does not require a line inside the upstream registration function beyond the import.

The seven hooks, all in fallback branches:

| # | File | Anchor | What the hook does |
| --- | --- | --- | --- |
| 1 | `src/RevitModelMcp.Core/Control/ActionJobParser.cs` | `IsAction` at line 21 | Or the registry predicate onto the literal list |
| 2 | `src/RevitModelMcp.Addin/Control/ActionCommandExecutor.cs` | the `Unknown action` arm at line 1309 | Ask the registry before throwing |
| 3 | `src/RevitModelMcp.Addin/Control/ActionVerifier.cs` | `CaptureBefore` at line 10 | Ask the registry before returning null |
| 4 | `src/RevitModelMcp.Addin/Control/ActionVerifier.cs` | `CaptureAfter` at line 19 | Same, on the after path |
| 5 | `src/RevitModelMcp.Core/Activity/ActionSummaryBuilder.cs` | the `_ =>` arm at line 99 | Ask the registry for a summary line |
| 6 | `src/RevitModelMcp.Core/Activity/ActivityTitleBuilder.cs` | the `Phrases` dictionary at line 14 | Merge fork phrases at construction |
| 7 | `src/RevitModelMcp.Addin/Application.cs` | `SupportedCommands` at line 33 | Spread the registry command list |

Budget: at most 80 changed lines across those hooks. The prototype measured the anchor set at 35.

## Consequences

Upstream keeps its own code path for its own commands. Nothing in the fork sits in front of an upstream action's dispatch, so an upstream fix reaches its action without passing through fork code.

A new fork action costs one file in `Fork/` plus one Python tool. It does not touch the seven hooks again, and it does not touch the manifest by hand once the drift check derives the manifest from the registry.

The registry must shadow two things upstream owns: the step vocabulary union, and the manifest tool list. Both are generated or asserted from the registry rather than hand-edited.

Hook 5 and hook 6 duplicate a concept: one builds a summary sentence, one builds an activity title. They are separate files in upstream, so the fork needs two hooks for one idea. This is accepted as the cost of not refactoring upstream code.

## Alternatives rejected

**Insert at all eleven points per action, following upstream's shape.** Ninety edits, each a fresh conflict site, and the count grows with every action.

**Rewrite upstream's dispatch into a registry.** Cleaner long term, and it would remove the eleven-point cost entirely. Rejected: it changes the shape of six upstream files, so every upstream release conflicts inside the code the fork rewrote, and the fork becomes responsible for the dispatch of tools it does not own.

**Generate the dispatch code with a source generator.** Solves the edit count without changing runtime shape. Rejected for now: it still requires the anchor edits to call the generated code, so the saving is smaller than it looks, and a generator adds a build step the Windows CI must carry.
