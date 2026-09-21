#!/usr/bin/env bash
# Watch for a codex session to complete. Completion = a NEW commit touching the
# handoff file AND the completion sentinel existing. The sentinel is written by
# codex as its absolute last action, so a session that has committed but is
# still wrapping up (verifying, printing its report) is not declared complete.
#
# A sentinel with no new commit is stale and ignored. If the commit lands but no
# sentinel appears within the grace period, the watcher exits with a FALLBACK
# line — verify the codex process is idle before closing it.
#
# Run in the background (e.g. Claude Code's run_in_background). Emits one line
# per state change; exits when the session is complete.
#
# The base commit defaults to the handoff's current HEAD. Set WATCH_BASE to pin a
# different one. Any commit touching the handoff moves the watcher, including the
# reviewer's own — so re-arm after any post-spawn review commit, or the watcher
# will report a session that has not happened yet.
#
# Usage: watch_session.sh <repo-dir> [handoff-file] [sentinel-file] [grace-seconds]
set -uo pipefail

REPO="$(cd "${1:?usage: watch_session.sh <repo-dir> [handoff] [sentinel] [grace]}" && pwd)"
HANDOFF="${2:-NEXT_SESSION_HANDOFF.md}"
SENTINEL="$REPO/${3:-.codex-session-complete}"
GRACE="${4:-180}"

BASE="${WATCH_BASE:-$(git -C "$REPO" log -1 --format=%H -- "$HANDOFF" 2>/dev/null || echo "none")}"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) watching $HANDOFF from base ${BASE:0:12} (completion = new commit + sentinel, grace ${GRACE}s)"

commit_seen=""
while true; do
  cur=$(git -C "$REPO" log -1 --format=%H -- "$HANDOFF" 2>/dev/null || echo "none")
  if [ "$cur" != "$BASE" ]; then
    if [ -z "$commit_seen" ]; then
      commit_seen=$(date +%s)
      echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) handoff commit detected: ${cur:0:12} — waiting up to ${GRACE}s for completion sentinel"
    fi
    if [ -f "$SENTINEL" ]; then
      echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) SESSION COMPLETE (sentinel written at: $(cat "$SENTINEL"))"
      break
    fi
    if [ $(( $(date +%s) - commit_seen )) -gt "$GRACE" ]; then
      echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) FALLBACK: commit landed but no sentinel after ${GRACE}s — verify codex is idle before closing it (if this commit was yours, not codex's, just re-arm)"
      break
    fi
    sleep 15
  else
    sleep 30
  fi
done
git -C "$REPO" log -1 --format='%h %ad %s' --date=iso -- "$HANDOFF"
