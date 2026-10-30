# Execute C# Code

`revit_execute_code`

<p class="facts"><span><b>Group</b> C# escape hatch</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>In the current release</b> No</span></p>

## Parameters {#parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `code` | Yes | — | string |  |
| `confirm_token` | No | None | any |  |
| `dry_run` | No | False | boolean |  |
| `transaction` | No | auto | string |  |

### Common parameters {#common-parameters}

| Parameter | Required | Default | Type | Meaning |
| --- | :--: | --- | --- | --- |
| `document` | No | None | any | Title or file name substring of the target open document; needed when several are open. |
| `timeout_seconds` | No | 600 | integer |  |

## Behavior (registry text) {#behavior}

```text
Compile and run C# against the live Revit API on the Revit thread. Accepts a method body or a public static Script class with Execute(ScriptContext ctx). Auto mode owns one transaction and undo entry; transaction="none" is refused by default. Needs confirm_token from a first call, which runs nothing; dry_run needs none and forces transaction="auto". A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action.
```

---

[Back to the catalog](index.md) · [Fork tool migration status](fork-tools.md)
