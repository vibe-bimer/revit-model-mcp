# 0003. Ship read-only by default, and express it through the upstream policy

- Status: Accepted
- Date: 2026-10-30

## Context

Upstream 1.0 inverted its write model. Saying "off" now means the model can be written: a fresh install writes unless something says otherwise. Three things can say otherwise: the environment variable `REVIT_MCP_READ_ONLY=1`, a machine or organization policy with `ReadOnly` set, or a policy file that cannot be read, which fails closed to read-only with code, updates and HTTP off.

This fork gates differently. `register_actions` returns early unless `REVIT_MCP_ALLOW_WRITE=1`, so a default install does not register action tools at all. When the gate is closed the tools are not merely refusing, they are absent.

Keeping both would mean an action the fork owns is refused while an upstream action next to it succeeds, on a machine where the user changed nothing. Nobody can explain that difference to a user, and the fork's own hard rule would then forbid what upstream permits.

## Decision

Read-only is the default. The policy is the only gate.

1. The installer sets `READONLY=1`. Upstream already has this property, a secured `Property("READONLY", "")` wired to `SetPropertyAction`, and it remembers the value across upgrades. The fork reuses it instead of inventing a gate.
2. A shipped default `policy.json` sets `ReadOnly`, so a machine without the installer behaves the same way.
3. `REVIT_MCP_ALLOW_WRITE` and the workstation allow-write file retire. `AGENTS.md` loses the hard rule that names them and gains one that names the policy.
4. A refused action lists the tool and refuses the call with the upstream read-only error code. Tools stay visible. "The tool does not exist" and "the tool will not do that" are different failures to an agent, and only the second one is debuggable.
5. The gate test is rewritten from an environment-variable assertion to a policy assertion.

## Consequences

Existing fork users who relied on `REVIT_MCP_ALLOW_WRITE=1` will find writes refused until they change the policy or the installer setting. The migration note goes in the release notes, not in a silent alias.

The fork inherits upstream's policy machinery, including its failure modes: an unreadable policy file turns writes off and says so.

Read tools are unaffected. They never depended on the fork's gate.

## Alternatives rejected

**Follow upstream and write by default.** Honest to the base, wrong for this product. The fork's eight actions rewrite element ids and rebuild whole models. A default install must not be one tool call away from that.

**Keep both gates.** This was the first proposal and it is the worst option. It produces the split behaviour described above, and it makes the fork's documentation describe a rule that does not match what the code does.

**Gate the fork's actions only.** Requires touching the fork layer's registration path, produces the same split behaviour, and adds a fork-only concept to a product whose whole point is that the two sets of actions behave alike.
