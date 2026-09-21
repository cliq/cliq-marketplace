# Implementation Progress

A local progress panel for long implementations in Codex or Claude Code. It shows
phases, optional steps, current activity, and the time of the last update, with
light/dark styling. The browser refreshes the data every two seconds.

See the [repository README](../../README.md#implementation-progress-installation)
for installation in either agent. Only Python 3.8+ is required to write progress;
a browser on the same machine can display the panel. No third-party dependencies,
network service, hooks, or agent SDK are needed.

## Use without an agent

From this repository's root in Bash or Zsh:

```bash
P="$PWD/plugins/implementation-progress/skills/implementation-progress/scripts/progress.py"
DIR="$(mktemp -d)"
python3 "$P" init --dir "$DIR" --title "Example implementation" \
  --phase "Plan::Understand requirements" \
  --phase "Build::Implement changes" \
  --phase "Verify::Run checks" \
  --now "Reviewing the requirements" --open

python3 "$P" phase --dir "$DIR" 1 done
python3 "$P" phase --dir "$DIR" Build active
python3 "$P" step --dir "$DIR" Build "Implement behavior" done
python3 "$P" step --dir "$DIR" Build "Handle errors" active
python3 "$P" now --dir "$DIR" "Checking error handling"
python3 "$P" show --dir "$DIR"
```

On Windows, use `py -3` or `python` in place of `python3`, and pass a writable
absolute `--dir` using your shell's syntax. Browser opening uses Python's
cross-platform `webbrowser` module. If opening fails, use the printed file URI
manually. For remote/headless sessions, `show` provides a terminal view; a local
browser cannot read files on another machine. If your browser blocks local script
loading, use `show` or a browser that permits it.

## Commands and storage

| Command | Effect |
| --- | --- |
| `init --title TITLE --phase "Title::detail" ... [--now TEXT] [--open]` | Create a panel; first phase active, the rest pending |
| `now TEXT` | Update the current activity |
| `phase PHASE STATE [--detail TEXT]` | Change a phase; completing it also completes non-blocked steps |
| `step PHASE TITLE STATE` | Add/update a step; activates a pending phase |
| `show` | Print current phases and steps |
| `open` | Request opening the panel in the default browser |

Every command accepts `--dir PATH` **after the command name**. `PHASE` is a 1-based
index or an unambiguous, case-insensitive title prefix. `STATE` is `pending`,
`active`, `done`, or `blocked`. Each phase is independent; finishing one does not
activate the next. `init --force` deliberately resets an existing panel.

Directory precedence is `--dir`, then `PROGRESS_DIR`, then
`<OS temp>/implementation-progress/<cwd-name>-<path-hash>`. The hash distinguishes
projects with the same folder name. Set an explicit directory per task to keep
parallel sessions separate and to keep using the same panel after changing the
working directory. Use one writer per panel; atomic file replacement protects
browser reads, but does not merge concurrent updates.

The output directory contains `index.html`, `progress.json`, and `progress.js`.
Nothing is written to the project by default. Keep generated files outside Git;
use a persistent directory if you need to retain progress across OS temp cleanup.
No daemon runs in the background, so closing the page stops the refreshes.

The percentage is an equal-weight phase estimate: completed phases count fully,
active phases use their proportion of completed steps, and active phases without
steps count as half complete. The footer marks data older than 20 minutes as stale.

## Verify changes

From the repository root:

```bash
python3 -m unittest discover -s plugins/implementation-progress/tests -v
```
