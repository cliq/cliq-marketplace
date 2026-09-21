#!/usr/bin/env bash
# Spawn an interactive Codex CLI session in a new terminal window/pane, guaranteed
# to run inside the target repo (avoids the classic "forgot the cd" launch bug by
# writing the launch command to a temp script and spawning THAT, so no quoting or
# working-directory mistakes are possible).
#
# Usage: spawn_codex.sh <repo-dir> [prompt] [codex-flags]
#   repo-dir     directory codex must run in (required)
#   prompt       initial prompt (default: read the handoff file and start)
#   codex-flags  flags for codex (default: --yolo)
#
# Prints the launch script path and contents (verify the cd line!), then the
# spawned terminal handle (macOS window id / tmux session name) and, after a
# short wait, the codex PID(s) whose cwd is the repo.
set -euo pipefail

REPO="$(cd "${1:?usage: spawn_codex.sh <repo-dir> [prompt] [codex-flags]}" && pwd)"
PROMPT="${2:-start working on the next session now by reading NEXT_SESSION_HANDOFF.md}"
FLAGS="${3:---yolo}"

LAUNCH="$(mktemp -t codex-launch.XXXXXX).sh"
{
  echo '#!/usr/bin/env bash'
  printf 'cd %q || exit 1\n' "$REPO"
  printf 'exec codex %s %q\n' "$FLAGS" "$PROMPT"
} > "$LAUNCH"
chmod +x "$LAUNCH"

echo "== launch script ($LAUNCH) =="
cat "$LAUNCH"
echo "=============================="

# SPAWN_DRY_RUN=1 prints the launch script and exits without opening a terminal
# (used by tests; also handy to inspect what would run).
if [ "${SPAWN_DRY_RUN:-}" = "1" ]; then
  echo "dry run: not spawning"
  exit 0
fi

case "$(uname -s)" in
  Darwin)
    WINDOW=$(osascript -e "tell application \"Terminal\"
      activate
      do script \"$LAUNCH\"
    end tell")
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) spawned — terminal: $WINDOW"
    ;;
  Linux)
    if command -v tmux >/dev/null 2>&1; then
      SESSION="codex-$(basename "$REPO")-$$"
      tmux new-session -d -s "$SESSION" "$LAUNCH"
      echo "terminal: tmux session $SESSION (attach with: tmux attach -t $SESSION)"
    elif command -v gnome-terminal >/dev/null 2>&1; then
      gnome-terminal -- "$LAUNCH" && echo "terminal: gnome-terminal"
    elif command -v x-terminal-emulator >/dev/null 2>&1; then
      x-terminal-emulator -e "$LAUNCH" & echo "terminal: x-terminal-emulator"
    else
      echo "No tmux or GUI terminal found; run manually: $LAUNCH" >&2
      exit 1
    fi
    ;;
  *)
    echo "Unsupported platform $(uname -s); run manually: $LAUNCH" >&2
    exit 1
    ;;
esac

sleep 5
FOUND=0
for pid in $(pgrep -f "codex --yolo" 2>/dev/null || true); do
  if [ "$(uname -s)" = "Darwin" ]; then
    cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')
  else
    cwd=$(readlink "/proc/$pid/cwd" 2>/dev/null || true)
  fi
  if [ "$cwd" = "$REPO" ]; then
    echo "codex pid $pid cwd $cwd"
    FOUND=1
  fi
done
[ "$FOUND" = 1 ] || echo "warning: no codex process with cwd=$REPO found yet (may still be starting)"
