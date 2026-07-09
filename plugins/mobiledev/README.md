# mobiledev

Orchestrator workflows for mobile engineering (iOS/Android). Plan a feature from a ticket, PRD, or plain description, then implement it by delegating to pinned-model sub-agents — an Opus reasoner for the hard decisions and a Sonnet worker for the mechanical edits — keeping the main (orchestrator) context lean and the cost profile sane.

Client, project, and tracker agnostic: requirements can come from any issue tracker (JIRA, Linear, GitHub Issues, ...), a PRD file, or a plain-text description. Project-specific conventions are read from the target repo's `CLAUDE.md` at plan time, not baked into the plugin.

## Skills

### `/plan-feature <ticket ID | path/to/prd.md | feature description>`

Runs a planning session as the orchestrator:

1. Resolves requirements from a tracker issue, PRD file, or description.
2. Researches the codebase via parallel Explore sub-agents (file paths and patterns, not file dumps).
3. Consults the `deep-reasoner` agent on each design decision with real trade-offs.
4. Walks the repo CLAUDE.md's planning checklist (if it has one) and bakes the applicable rules into the steps.
5. Persists a standalone plan to `planning/implementation/<slug>-plan.md`, with each step tagged for a delegate (`[fast-worker]`, `[deep-reasoner]`, `[orchestrator]`).

The plan file is a scratch artifact — never committed, deleted when implementation completes.

### `/implement-feature-plan [<ticket ID, plan slug, or plan file path>]`

Executes a plan produced by `/plan-feature`:

1. Loads the plan, confirms/creates the working branch, and mirrors the steps into a task list.
2. Delegates each step by its tag — mechanical work to `fast-worker`, hard failures and diagnoses to `deep-reasoner` — reviewing every diff for scope.
3. Builds at milestones and runs the plan's verification section (unit tests, app run when UI changed).
4. Deletes the plan file and summarizes what was built.

## Agents

| Agent | Model | Role |
|-------|-------|------|
| `deep-reasoner` | Opus | Read-only advisor for architecture decisions, complex debugging, and tricky refactors. It advises; the orchestrator decides. |
| `fast-worker` | Sonnet | Mechanical implementer for well-defined edits, boilerplate, and tests. Executes a decided approach; never designs. |

## Install

```
/plugin install mobiledev@cliq-marketplace
```
