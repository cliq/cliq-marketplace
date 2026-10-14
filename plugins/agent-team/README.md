# agent-team

A technical-lead workflow for Claude Code. The main agent decomposes substantial coding work, delegates independent pieces to six pinned-model subagents, integrates the results, and runs an independent review. Small or tightly coupled tasks stay with the lead.

This is a port of the Codex `agent-team` plugin from `cliq/codex-plugins`. In Codex the roles are Markdown references that the lead pastes into each spawn. In Claude Code each role is a real subagent with its model, reasoning effort, and tool list pinned in frontmatter.

Client and project agnostic. Project conventions come from the target repo's `CLAUDE.md` and `AGENTS.md` at run time.

## Invoke

```text
/agent-team Implement this feature using focused subagents where useful.
/agent-team Use an explorer to find the main entry points without editing files.
/agent-team Review my changes with an independent reviewer.
```

The skill description also allows automatic selection for suitable substantial work. Explicit invocation is the reliable way to request it.

## Roles

| Role | Model / effort | Edits | Job |
| --- | --- | --- | --- |
| `agent-team:worker` | opus / medium | yes | Substantial implementation with clear ownership |
| `agent-team:explorer` | sonnet / medium | no | Investigation and triage |
| `agent-team:fixer` | sonnet / medium | yes | Small, well-understood fixes |
| `agent-team:reviewer` | opus / high | no | Independent review of a diff |
| `agent-team:specialist` | fable / high | on request | Difficult debugging, architecture, escalation |
| `agent-team:default` | opus / high | yes | Bounded task that fits no other role |

Model mapping from the Codex plugin: Astra is fable, Sol is opus, Terra is sonnet. The lead keeps the session's model and effort.

The subagents are also available directly, outside the skill, as `subagent_type` values on the Agent tool. Plugin agents are namespaced, so the value is `agent-team:worker`, not `worker`.

## Install

```text
/plugin install agent-team@cliq-marketplace
```

Start a new session after install. Disable the plugin to remove the workflow and the roles.

## Limits

- Plugin subagents ignore `permissionMode`, `hooks`, and `mcpServers`. Read-only roles (`explorer`, `reviewer`) are enforced only through their `tools` list.
- `CLAUDE_CODE_EFFORT_LEVEL` overrides every per-role `effort`. Leave it unset.
- Per-call `effort` on the Agent tool requires Claude Code 2.1.292 or later.
- The `fable` model must be available on the account. If it is not, change `agent-team:specialist` to `opus` with `effort: xhigh`.
