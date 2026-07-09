---
name: implement-feature-plan
description: "Execute an implementation plan produced by /plan-feature (from planning/implementation/) as the orchestrator: delegate mechanical steps to the fast-worker (Sonnet) subagent, escalate hard failures to the deep-reasoner (Opus), verify with builds/tests, and delete the plan file when done. Use whenever the user asks to implement, execute, or build out a plan, or references a plan file or a ticket/PRD that already has one. Usage: /implement-feature-plan [<ticket ID, plan slug, or plan file path>]"
user_invocable: true
---

# Implement Feature Plan (orchestrator)

You are the orchestrator: decompose, delegate, verify, synthesize. Don't implement steps inline except trivial glue (a one-line fix, a wiring tweak) — your value is judgment and verification, and your context should stay lean enough to see the whole task through.

## Step 1: Locate and load the plan

- Resolve the plan file: from the argument (`planning/implementation/<issue-id>-plan.md` or a path), or if none given, list `planning/implementation/*.md` — if exactly one exists use it, otherwise ask the user which.
- Read the plan fully. If steps are missing delegate tags or file paths, fill the gaps yourself before starting.
- Confirm the working branch matches the work, following the repo's branch naming convention (e.g. `feature/<ticket-id>-...`, or `feature/<slug>` for plans without a ticket); create it if needed.
- Create a task list (TaskCreate) mirroring the plan steps so progress is visible.

## Step 2: Execution loop

For each step, in plan order (parallelize only steps that touch disjoint files):

1. **Delegate by tag:**
   - **[fast-worker]** → Task the `fast-worker` agent. Subagents have no conversation context, so each prompt must be self-contained: paste the plan step verbatim, exact file paths, the reference file/pattern to copy, and the repo conventions the step touches (localization mechanism, design-system colors, date providers, persistence threading rules; on iOS with a classic `.xcodeproj`: new files registered in `project.pbxproj` with relative references).
   - **[deep-reasoner]** → Task the `deep-reasoner` agent with the question and relevant file paths; it returns an approach or diagnosis. Then hand the resulting concrete change to fast-worker.
   - **[orchestrator]** → decisions, user check-ins, and verification stay with you.
2. **Review the result.** Read the diff of what the subagent changed (`git diff --stat` then targeted diffs). Check it did what the step asked and nothing beyond scope. Mark the task completed.
3. **On failure or surprise** (build error the fast-worker couldn't resolve, plan assumption contradicted by the code): escalate to deep-reasoner with the error output and file paths for a root-cause diagnosis — don't let fast-worker guess-iterate, and don't burn your own context debugging inline. If the plan itself is wrong, update the plan file and tell the user what changed and why.

## Step 3: Verify

- Build after each milestone (not each tiny step) — use the project's build skill if one exists, otherwise the platform standard (iOS: `xcodebuild` on the app scheme; Android: `./gradlew assembleDebug` or the repo's debug variant). Fix-forward failures before moving on.
- After the last step, run the plan's **Verification** section: unit tests (following any simulator/device assignments in the user's or repo's CLAUDE.md; Android: `./gradlew test`), plus a run of the app when UI changed.
- Report test results faithfully — if something fails and can't be fixed within scope, say so plainly.

## Step 4: Complete

- Walk the plan top-to-bottom and confirm every step landed; list anything deliberately skipped.
- Delete the plan file (`rm planning/implementation/<issue-id>-plan.md`) — plans are scratch artifacts and must not be committed.
- Summarize for the user: what was built, files touched, verification results, and suggested next steps (commit, PR). Don't commit or push unless asked.
