# Project context template (`.codex-loop.md`)

Create this file at the target repo's root during bootstrap and keep it committed. It is the loop's
accumulated per-project memory: the reviewer reads it before every phase, codex can read it too, and new
durable lessons from reviews get added here rather than to the generic skill. Keep entries checkable —
exact paths, ports, versions, commands — not vague advice.

```markdown
# Codex loop — project context

## What this loop is doing

<1-3 lines: the project and what codex sessions work on.>

## Decision owner and reserved decisions

<Who decides, and which classes of decision must be gated through them before a session runs:
scope changes, resource bounds beyond precedent, version/branch selections, anything project docs
mark as theirs.>

## Where session evidence lives

<Paths the reviewer must read after each session: results directories, summary file conventions,
logs. State what "authoritative" means here.>

## Documents the handoff must stay consistent with

<Project docs/specs whose ordering or decisions the handoff must agree with; the reviewer
cross-checks these every cycle.>

## Retained-state checks (run every review)

<Checkable invariants: services stopped, ports free, pinned versions intact, working tree clean.
One command or path per line where possible.>

## Standing constraints

<Rules codex must never violate without a new recorded decision.>

## Past review catches (re-check these patterns)

<Dated one-liners of real catches, so future reviews re-check the same failure patterns.>
```
