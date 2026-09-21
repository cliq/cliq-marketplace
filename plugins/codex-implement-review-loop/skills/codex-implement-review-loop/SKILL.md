---
name: Codex implement/review loop
description: Run an autonomous implement/review loop where Codex CLI executes work sessions driven by a NEXT_SESSION_HANDOFF.md file and Claude adversarially reviews each session between runs, gating decisions through the user. Use when the user wants to start, resume, continue, or set up a codex loop, hand a project to codex with Claude as reviewer, have codex work sessions reviewed/challenged, or says things like "let codex implement this and you review it", "start the codex loop", "spawn codex on the handoff".
---

# Codex implement/review loop

Two agents, complementary roles: **Codex CLI implements** — long, autonomous work sessions in their own
terminal, each driven by a handoff file the previous session wrote. **Claude reviews** — between sessions,
it verifies the session's claims against actual evidence, challenges the proposed next step, routes real
decisions to the user, then respawns codex. The human stays the decision-maker without watching live.

Why this shape: codex sessions are expensive (often hours). A handoff with a wrong claim, a mislabeled
input, or an under-provisioned bound wastes an entire session. The reviewer's job is to catch that before
the next session starts — and the loop's job is to make each handoff good enough that codex needs no
mid-session help.

## Variables

- `HANDOFF_FILE`: `NEXT_SESSION_HANDOFF.md` (repo root)
- `SENTINEL_FILE`: `.codex-session-complete` (repo root, must be gitignored)
- `PROJECT_CONTEXT`: `.codex-loop.md` (repo root, committed)
- `CODEX_FLAGS`: `--yolo` (bypasses codex approvals — confirm with the user on first setup)
- `SPAWN_PROMPT`: `start working on the next session now by reading NEXT_SESSION_HANDOFF.md`

Scripts live in this skill's `scripts/` directory; call them with the repo path as first argument.

## Project context file

This skill is deliberately generic; everything project-specific lives in `PROJECT_CONTEXT` in the target
repo. Read it (if present) before any loop phase — it carries what this skill cannot know: where session
evidence lives, project-specific retained-state checks, extra review checklist items, which decisions the
user reserves for themselves, and past review catches worth re-checking. Bootstrap creates it from
`references/project-context-template.md`. When a review discovers a new durable project lesson, add it to
`PROJECT_CONTEXT` (not to this skill) — the file is the loop's accumulated memory for that repo, and it is
committed so codex can read it too.

## Determine loop state, then jump in

1. `HANDOFF_FILE` missing → **Bootstrap** (below).
2. Codex running in this repo? Check with `pgrep -f codex` and verify each pid's cwd (macOS:
   `lsof -a -p <pid> -d cwd -Fn`; Linux: `readlink /proc/<pid>/cwd`). Running + no watch armed →
   arm `scripts/watch_session.sh` in the background and report the loop is live.
3. Not running, handoff exists → if its latest commit lacks a review section, **Review** it; otherwise
   **Spawn**.

## Bootstrap (first session for a project)

1. Interview the user briefly: what codex should build/investigate, hard constraints, what decisions they
   reserve for themselves.
2. Write the first `HANDOFF_FILE` from `references/handoff-template.md`. The template's "carry forward"
   sections — especially the mandatory final steps (rewrite handoff → commit → sentinel last) — are what
   make the loop self-sustaining; without the sentinel step the watcher can't tell "committed" from "done".
3. Write `PROJECT_CONTEXT` from `references/project-context-template.md` with what the interview surfaced.
4. Add `SENTINEL_FILE` to `.gitignore`.
5. Commit, then **Spawn**.

## Spawn

```sh
<skill>/scripts/spawn_codex.sh <repo-dir> [prompt] [codex-flags]
```

It writes the launch command to a temp script (guaranteeing the `cd` — launching codex in `$HOME` by
forgetting the cd is the single most repeated mistake in this loop), spawns the platform's terminal
(macOS Terminal / tmux / gnome-terminal), echoes the launch script for verification, and prints the codex
pid + terminal handle. Record both. Then arm the watch:

```sh
# run in background
<skill>/scripts/watch_session.sh <repo-dir>
```

Completion = new commit touching `HANDOFF_FILE` **and** the sentinel present. Commit alone means codex may
still be wrapping up; sentinel alone (no commit) is stale and ignored. If the commit lands but no sentinel
appears within the grace period, the watcher says FALLBACK — then check the codex process is idle before
touching it.

## On session completion

Completion is ONLY the watcher reporting commit + sentinel (or its explicit FALLBACK line). A modified
handoff file on disk is NOT completion — codex rewrites the file before committing, so killing on
file-modification alone kills it mid-wrap-up and loses its commit (this happened: a session died at the
commit step and the reviewer had to commit its surviving working-tree changes). Always read the watcher
output first.

1. `scripts/end_session.sh <repo-dir>` — kills only `codex --yolo` pids whose cwd is this repo (never
   `pkill -f codex`; the user may run their own codex elsewhere, and a bare "codex" pattern also matches
   this skill's own script paths — it once killed the watcher). On macOS, close
   the recorded Terminal window afterwards — process first, window second, or the close prompts a dialog.
2. **Review** the new handoff.

## Review — challenge, don't summarize

Read `PROJECT_CONTEXT`, the new `HANDOFF_FILE`, the diff of the session's commit(s), and whatever evidence
the handoff cites (result files, logs, test output). The handoff was written by the same agent whose work it
describes — treat every claim as unverified:

- Re-verify checkable claims against primary sources: run the tests it says pass, recompute the hashes it
  states, read the log lines it quotes. Numbers copied between files drift.
- Verify on-disk facts the next task depends on — paths exist, versions/architectures are what the handoff
  says they are. (Real catch from this loop's history: a binary labeled "classic" was actually a different
  major version, which changed what the experiment would prove.)
- Check retained-state claims: services stopped, ports free, temp files cleaned, working tree clean.
- Challenge the "next smallest step" reasoning: does it follow from what was actually observed? Are its
  bounds (time caps, retries) justified by precedent, or guesses that could waste the session? Is there a
  cheaper alternative already available?
- Confirm the mandatory final steps (handoff rewrite → commit → sentinel) survived the rewrite; re-add if
  codex dropped them.

Write findings into the handoff as a dated `## Review (after commit <hash>)` section; fix wrong claims in
place.

## Gate decisions through the user — mandatory

If the next session involves choices that belong to the user — scope changes, which variant/branch to use,
resource bounds, anything the project docs reserve for them — write the options into the handoff, ask
(AskUserQuestion; push notification if they may be away), and **wait**. Never commit updated handoff
instructions before the user has answered. Record outcomes in the file as
`**Decision (<user>, <date>):** ...` so codex treats them as settled.

## Close the loop

1. Commit the reviewed handoff.
2. Re-arm `watch_session.sh` **before** spawning (nothing gets missed). The watcher
   baselines on the handoff's current commit and cannot tell your commits from codex's,
   so if you commit to the handoff again after arming — a late subagent finding, a
   correction — re-arm afterwards. Otherwise the watcher fires on your own commit and
   reports FALLBACK for a session that has barely started. It will not declare
   completion (no sentinel), so nothing gets killed, but you lose the real signal.
3. Spawn codex again. Report: what the session established, what you corrected, decisions recorded, and
   that the next session is running.
4. **End every between-runs report with a timestamped cycle timeline** — spawn, handoff commit, sentinel,
   teardown, review committed, respawn — sourced from the scripts' UTC-stamped output, `git log` dates,
   and the sentinel's content. The user reads these later to see where each cycle's time went; a report
   without timestamps makes the loop's history unreconstructable.

Messaging a running codex session is a last resort and UNRELIABLE on macOS: `do script "<text>" in window
id <id>` types into the TUI but the newline may not submit — the message can sit in the input box unseen
until the session ends, so never depend on it having been received (the watcher's FALLBACK path covers
exactly this). Prefer putting instructions in the handoff file, which codex reliably reads at session
start. If truly needed: after `do script`, send a Return keystroke via System Events and verify visually;
on tmux, `tmux send-keys -t <session> "<one line>" Enter` submits reliably.
