# Execute C# Code

Compile and run C# against the live Revit API on the Revit thread.

**Group:** Code execution · **Kind:** Action (opt-in)

## Parameters

| Name | Required | Default | Type | Meaning |
| --- | --- | --- | --- | --- |
| `code` | Yes | — | `string` | — |
| `confirm_token` | No | null | `string / null` | — |
| `dry_run` | No | false | `boolean` | rehearse: execute, return the same verification block, then roll back |
| `transaction` | No | "auto" | `string (auto, none)` | — |

### Common parameters

| Name | Meaning |
| --- | --- |
| `document` | Case-insensitive document-title or file-name substring. Reads use it to address an instance; it must be unique with multiple instances. Actions use it to choose an open document in the addressed instance; required with multiple open documents. Unknown or ambiguous targets are rejected. |
| `timeout_seconds` | Positive result-wait budget in seconds after pickup (default 120); HTTP uses it as the response budget. Does not override add-in execution limits; a timeout does not cancel a pending job. |

## Behavior and returned data

Compile and run C# against the live Revit API on the Revit thread. Accepts a method body or a public static Script class with Execute(ScriptContext ctx). Auto mode owns one transaction and undo entry; transaction="none" is refused by default. Needs confirm_token from a first call, which runs nothing; dry_run needs none and forces transaction="auto". A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.

## Revit year support

| Revit year | State |
| --- | --- |
| 2020 | Not supported yet |
| 2022–2025, 2027 | Built |
| 2026 | Built |

**Built** means the release workflow compiles that Revit configuration. **Not supported yet** means no build target exists: adr/0006 records Revit 2020 as a required follow-up with a date. Nothing on this branch has been verified against a running Revit instance, so no page claims a live result.

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
