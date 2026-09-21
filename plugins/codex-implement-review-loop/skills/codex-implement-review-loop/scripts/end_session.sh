#!/usr/bin/env bash
# Safely end the codex session belonging to ONE repo: kill only codex processes
# whose working directory is that repo (never pattern-kill — the user may have
# their own codex sessions running elsewhere), then remove the completion
# sentinel so the next watch cannot see a stale one.
#
# Kill the process BEFORE closing its terminal window: closing a window with a
# live process pops a confirmation dialog on macOS. This script does not close
# windows — on macOS close the window afterwards with:
#   osascript -e 'tell application "Terminal" to close window id <id>'
# (tmux sessions end themselves when the process exits.)
#
# Usage: end_session.sh <repo-dir> [sentinel-file]
set -uo pipefail

REPO="$(cd "${1:?usage: end_session.sh <repo-dir> [sentinel-file]}" && pwd)"
SENTINEL="$REPO/${2:-.codex-session-complete}"

killed=0
for pid in $(pgrep -f "codex --yolo" 2>/dev/null || true); do
  if [ "$(uname -s)" = "Darwin" ]; then
    cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')
  else
    cwd=$(readlink "/proc/$pid/cwd" 2>/dev/null || true)
  fi
  if [ "$cwd" = "$REPO" ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) killing codex pid $pid (cwd $cwd)"
    kill "$pid" 2>/dev/null && killed=$((killed+1))
  fi
done
[ "$killed" -gt 0 ] || echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) no codex process with cwd=$REPO (already exited)"

if [ -f "$SENTINEL" ]; then
  rm -f "$SENTINEL" && echo "removed sentinel $SENTINEL"
fi
