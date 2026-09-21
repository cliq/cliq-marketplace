# Codex implement/review loop

An autonomous two-agent loop for long-running projects: **Codex CLI implements**, **Claude reviews**, the
**human decides**.

## How it works

```
┌─────────────────────────────────────────────────────────────┐
│  NEXT_SESSION_HANDOFF.md  (the loop's shared memory)        │
└─────────────────────────────────────────────────────────────┘
     ▲ rewrites + commits                    │ reads
     │                                       ▼
┌──────────────┐    sentinel + commit   ┌──────────────────────┐
│  Codex CLI   │ ─────────────────────▶ │  Claude (reviewer)   │
│  work session│                        │  verify · challenge  │
│  (own term.) │ ◀───────────────────── │  fix · respawn       │
└──────────────┘        spawns          └──────────┬───────────┘
                                                   │ decisions only
                                                   ▼
                                                 Human
```

1. A handoff file describes one bounded task, the project's goal, validated state, and recorded decisions.
2. Codex runs the session in its own terminal (`codex --yolo`), rewrites the handoff for the next session,
   commits, and writes a completion sentinel as its very last action.
3. Claude's background watcher fires on **commit + sentinel** (so codex is never killed mid-wrap-up),
   closes the session, then adversarially reviews the handoff: re-verifies claims against primary evidence,
   checks on-disk facts, challenges the proposed next step and its bounds.
4. Decisions that belong to the human are written into the handoff and asked explicitly; the loop waits.
5. Claude commits the reviewed handoff, re-arms the watcher, and spawns the next codex session.

## Why

Codex sessions are long and expensive. A single wrong claim or mislabeled input in a handoff wastes hours.
The reviewer catches it between sessions, and the human stays in control of real decisions without
babysitting either agent.

## Requirements

- `codex` CLI on PATH
- A git repository
- macOS (Terminal.app) or Linux (tmux / gnome-terminal / x-terminal-emulator)

## Usage

Ask Claude Code to "start the codex loop" (bootstraps the handoff on first use), "resume the codex loop",
or just "let codex implement this and review its sessions".
