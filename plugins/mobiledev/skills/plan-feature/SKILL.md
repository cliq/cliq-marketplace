---
name: plan-feature
description: "Plan a feature, ticket, or PRD as the orchestrator: research the codebase via subagents, consult the deep-reasoner (Opus) on design decisions, and persist an implementation plan to planning/implementation/<slug>-plan.md. Use whenever the user asks to plan, spec, or prepare an implementation for a feature, a tracker issue, or a PRD document before coding starts. Usage: /plan-feature <ticket ID | path/to/prd.md | feature description>"
user_invocable: true
---

# Plan Feature (orchestrator)

You are the orchestrator: your job is to plan, decompose, and synthesize — not to read every file yourself and not to write code. Keep your own context lean by delegating research, and spend your reasoning on decisions and synthesis. The output is a plan file that `/implement-feature-plan` can execute later, possibly in a fresh session — so the plan must stand alone.

## Step 1: Understand the ask

- Parse the arguments — the requirements source is one of:
  - **An issue/ticket ID** from the project's tracker (JIRA, Linear, GitHub Issues, ...): fetch it for the description and acceptance criteria, using whatever integration is available (tracker MCP tools, `gh issue view`, or a project skill). If no integration is available, ask the user to paste the ticket contents.
  - **A PRD file path** (may live outside this repo): read it fully. PRDs can be cross-platform — plan only the scope of the repo you're in, and note anything that depends on backend or the other platform as a risk/dependency rather than a step. If the PRD is large, extract the requirements and acceptance criteria that drive this repo's work; if it references tracker issues, fetch them too.
  - **A feature description** in plain text.
  - If the source is unavailable or ambiguous, ask the user for the requirements instead of guessing.
- Derive the plan file name: `planning/implementation/<slug>-plan.md` — the issue ID when there is one (e.g. `abc-1234-plan.md`), otherwise a short kebab-case slug from the PRD/feature name (e.g. `resistance-training-daily-plan.md`).
- If a plan file for this work already exists, read it and confirm with the user whether to revise it or start over.

## Step 2: Research via subagents

Delegate so raw file contents land in subagent contexts, not yours:

- **Explore agents** — map the relevant code: existing screens/flows/services/models the feature touches, reference implementations the repo's CLAUDE.md names, similar prior features. Ask for file paths + how the pattern works, not file dumps. Run independent explorations in parallel.
- **deep-reasoner** — for each design decision with real trade-offs (data model shape, sync strategy, where logic lives, navigation structure), task it with one well-scoped question including the file paths Explore found. It reads the code and returns a recommendation.
- For a high-stakes decision, task deep-reasoner and a second independent advisor (if one is available in the session) in parallel on the same question and synthesize the best of both — neither sees the other's answer.

Only read files yourself when a specific detail must be verified for the plan (exact styling values, an API signature).

## Step 3: Check the planning checklist

Re-read the repo's CLAUDE.md for planning guidance — if it has a planning checklist or "common mistakes to avoid" section, walk through every item that applies to this feature (navigation, threading and persistence rules, enums synced from backend, feature flags, UI conventions...). Bake the applicable rules into the plan steps explicitly — the implementer may not re-derive them.

## Step 4: Write the plan file

Persist to `planning/implementation/<slug>-plan.md` with this structure:

```markdown
# <Issue ID or Feature>: <Title> — Implementation Plan

## Context
What the feature is, the ticket link or PRD path, acceptance criteria, and any decisions already made by the user.

## Design decisions
Each decision, the chosen approach, and a one-line why (note which came from deep-reasoner or another advisor).

## Steps
Ordered, independently executable steps. For each:
- **[fast-worker]** or **[deep-reasoner]** or **[orchestrator]** — the suggested delegate
- What to do, exact files to create/modify, and the pattern/reference file to follow
- New files: on iOS with a classic `.xcodeproj`, note they must be added to the Xcode project
- Which of the repo's conventions apply (localization, design-system colors, date providers, persistence threading rules...)

## Verification
How to prove it works: build target/scheme, unit tests to add/run (with reference test classes), and manual/simulator checks.

## Risks & open questions
Anything unresolved the implementer or user should watch for.
```

Each step must be self-contained enough to hand to a subagent that has no conversation context.

## Step 5: Wrap up

- Summarize the plan and the key decisions to the user; flag open questions.
- Remind: the plan file is a scratch artifact — **never commit it**; it gets deleted when implementation completes. Suggest `/implement-feature-plan <slug>` as the next step.
