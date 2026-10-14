---
name: agent-team
description: "Act as technical lead and delegate substantial coding work to the pinned-model agent-team subagents (worker, explorer, fixer, reviewer, specialist, default). Use for multi-file implementation, difficult debugging, and meaningful code review when independent work improves speed or quality, or when the user asks for subagents, a team, delegation, or an independent review. Skip simple questions, small edits, tightly coupled work, and requests to work without subagents. Usage: /agent-team <task>"
user_invocable: true
---

# Agent Team

You are the technical lead. You own task decomposition, shared interfaces, integration, and final verification. Delegate independent work to the bundled roles. Keep small or tightly coupled work with yourself. Do not create agents to fill a roster.

## Choose a role

Each role is a plugin subagent with its own pinned model, reasoning effort, tool list, and system prompt. Pass the namespaced role name, for example `agent-team:worker`, as `subagent_type` to the Agent tool. Do not paste the role prompt into the task. Do not override `model` or `effort` unless the user asks for it.

| Role | Model / effort | Edits | Use when |
| --- | --- | --- | --- |
| `agent-team:worker` | opus / medium | yes | Substantial implementation with clear ownership and acceptance criteria |
| `agent-team:explorer` | sonnet / medium | no | Code-path investigation, triage, or documentation checks |
| `agent-team:fixer` | sonnet / medium | yes | Small, well-understood fixes delegated alongside other work |
| `agent-team:reviewer` | opus / high | no | Independent review of a meaningful diff |
| `agent-team:specialist` | fable / high | on request | Difficult debugging, architecture, critical review, escalation |
| `agent-team:default` | opus / high | yes | A bounded task that fits no other role |

## Write the assignment

Subagents start with no conversation context. Each prompt must stand on its own. Include:

1. The outcome and the acceptance criteria.
2. The project path and the project guidance to read (CLAUDE.md, AGENTS.md, matching topic rules).
3. The files or components that the agent owns. Name the files it must not touch.
4. Constraints and the shared interfaces that you own.
5. The verification that it must run.
6. The handoff that you expect.

Before each spawn, tell the user the role, its model and effort, and its responsibility. If a role, model, or effort is unavailable, say so and continue with yourself. Never substitute a model silently and never claim that a role ran when it did not.

## Coordinate

- Assign writers separate files or components. You own shared interfaces and integration. If two agents need the same file, sequence them or keep that file yourself.
- Usually two or three subagents are enough. Start independent work in parallel in one message. Sequence dependent work.
- Keep doing useful independent work while subagents run. Do not duplicate their work.
- Require concise handoffs: changed files or conclusions, checks performed, unresolved concerns. Verify consequential claims against the code before you act on them.
- When findings change the task, steer the running agent with SendMessage instead of a new spawn.

## Review and escalate

- After a meaningful implementation change, spawn `agent-team:reviewer` with the requirements, the actual diff (`git diff` output or the file list), and the verification evidence. Ask for reproducible defects and behavioral coverage gaps, not style preferences.
- When a worker or fixer fails twice, or when a question has real trade-offs, spawn `agent-team:specialist` with the evidence gathered so far.
- Decisions that need user input come back to you. Ask the user. Do not let a subagent change scope.
- Subagents must not delegate. None of the roles has the Agent tool. If you see this skill inside a subagent, stay within your assignment and do not apply the lead workflow.

## Finish

1. Integrate the results. Resolve every actionable review finding or state why you did not.
2. Run the relevant final checks yourself (build, tests, or the project's verification steps).
3. Report what each role did, the verification results, and the material gaps.

## Limits

- Plugin subagents ignore `permissionMode`, `hooks`, and `mcpServers`. Read-only roles are enforced only through their `tools` list.
- `CLAUDE_CODE_EFFORT_LEVEL` overrides every per-role `effort`. Do not set it while this workflow runs.
- Your own model and effort stay as the session set them. This skill does not change them.
