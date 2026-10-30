---
description: "Compile and run C# against the live Revit API on the Revit thread. Accepts a method body or a public static Script class with Execute(ScriptContext ctx). Auto mode owns one transaction and undo entry; transaction=\"none\" is refused by default. Needs confirm_token from a first call, which runs nothing; dry_run needs none and forces transaction=\"auto\". A long action can return status=running and jobId when the wait budget expires; it may already have changed the model, and revit_jobs returns its result. Resubmitting repeats the action."
---

# Execute C# Code

`revit_execute_code`

<p class="facts"><span><b>Group</b> C# escape hatch</span><span><b>Kind</b> Action</span><span><b>Base and fork tools</b> Base (upstream)</span><span><b>Status</b> Unreleased (integration branch)</span><span><b>Release version</b> 0.9.0</span><span><b>Source branch</b> <code>integration/upstream-1.0</code></span><span><b>Source commit</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>Same-name tool in the release</b> No</span><span><b>This contract applies to the release</b> No</span></p>

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
