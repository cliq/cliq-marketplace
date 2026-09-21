# Handoff template

Use this structure when bootstrapping the first `NEXT_SESSION_HANDOFF.md` for a project. Sections marked
(carry forward) must survive every rewrite — they are what keeps the loop self-sustaining. Adapt freely to
the project; the structure matters more than the exact wording.

```markdown
# Next-session prompt: <one-line name of the next bounded task>

Continue <project> from the completed <previous session id / "this is the first session">.

## Ultimate goal and current position (carry forward)

<2-6 lines: what the project is ultimately building, and where this session sits in that roadmap.
A session that doesn't know the destination optimizes the wrong thing.>

## Read first

<Files the session must read before acting: prior session results/evidence, relevant docs, specs.>

## Findings now closed

<What previous sessions established, stated as conclusions with their evidence paths. Mark what must
NOT be redone or re-litigated without a new explicit scoping decision.>

## Validated retained state

<Environment facts the session may rely on and must not disturb: pinned versions, restored files,
stopped services. State them checkably (exact versions, hashes, ports).>

## Primary task

<ONE bounded task: exact inputs, exact bounds (time caps, iteration caps), what evidence to record,
and what NOT to do. Small enough to finish in one session.>

## Why this is the next smallest step (carry forward)

<Justify the task against alternatives. The reviewer will challenge this section.>

## Recorded decisions

<Decisions the project owner has made, as "**Decision (<owner>, <date>):** ...". The session must not
reopen these. If the task needs a decision that is not recorded here, STOP and say so in the handoff
rather than guessing.>

## Session hygiene and mandatory final steps (carry forward)

- Preserve evidence: inputs, hashes, logs, restoration records.
- Restore any state you temporarily changed; verify with the recorded hashes/checks.
- **Last steps, in order:**
  1. Rewrite this file for the next session: findings, retained state, goal context, the next
     smallest bounded task and its reasoning, and these same instructions so the file keeps iterating.
     Do not leave a completed task described as the next task.
  2. Commit all session documentation and this file together; verify the commit and report its hash.
  3. As the absolute LAST action, after the commit: write the completion sentinel —
     `date -u +%Y-%m-%dT%H:%M:%SZ > .codex-session-complete`
     (gitignored; an external watcher uses it to know this session is fully done).
```
