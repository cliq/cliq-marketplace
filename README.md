# Cliq Consulting's Opinionated Coding Agent Plugins

A handful of plugins for Claude Code, plus portable skills for Codex.

## Quick Install

**Add the marketplace**
```bash
/plugin marketplace add cliq/cliq-marketplace
```

# Plugins

| Name | Purpose | Skills | Agents | Commands | Hooks | MCPs |
|------|---------|--------|--------|----------|-------|------|
| [conversation-saver](plugins/conversation-saver) | Automatic conversation saving plugin built on the conversation-logger skill  | 0 | 0 | 3 | 1 | 0 |
| [fork-terminal](plugins/fork-terminal) | Fork your agentic coding tools to a new terminal window with context.  | 1 | 0 | 0 | 0 | 0 |
| [mobiledev](plugins/mobiledev) | Orchestrator planning/implementation workflows for mobile (iOS/Android) with pinned-model sub-agents  | 2 | 2 | 0 | 0 | 0 |
| [implementation-progress](plugins/implementation-progress) | Local, auto-refreshing progress dashboard for Claude Code or Codex | 1 | 0 | 0 | 0 | 0 |

## Implementation Progress: installation

Shows implementation phases, optional steps, and the agent's current activity in a
small browser panel. Requires **Python 3.8+** and a browser for the visual panel;
there are no Python dependencies, API keys, or server to configure. The same skill
works in either agent. The agent updates it at milestones; it does not monitor
other sessions automatically.

### Claude Code: marketplace plugin

Run these commands inside Claude Code after this version is available in the
marketplace repository:

```text
/plugin marketplace add cliq/cliq-marketplace
/plugin install implementation-progress@cliq-marketplace
```

Then invoke:

```text
/implementation-progress:implementation-progress Implement this feature and keep a progress panel updated.
```

Claude Code namespaces plugin skills as `/plugin-name:skill-name`.
See the [Claude Code plugin installation docs](https://code.claude.com/docs/en/discover-plugins)
and [skill docs](https://code.claude.com/docs/en/skills).

### Codex: standalone skill

For a new checkout, run the following in Bash or Zsh. If already cloned, start in
the repository root and skip the first two commands:

```bash
git clone https://github.com/cliq/cliq-marketplace.git
cd cliq-marketplace
mkdir -p "$HOME/.agents/skills/implementation-progress"
cp -R plugins/implementation-progress/skills/implementation-progress/. \
  "$HOME/.agents/skills/implementation-progress/"
```

For Windows PowerShell, after cloning and entering the repository:

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills/implementation-progress" | Out-Null
Copy-Item -Recurse -Force "plugins/implementation-progress/skills/implementation-progress/*" "$HOME/.agents/skills/implementation-progress/"
```

Codex discovers user skills in `~/.agents/skills`; for a project-only install, copy
the same skill folder into `<project>/.agents/skills/` instead. Restart Codex if it
does not pick up the new skill. See the [official Codex skill docs](https://learn.chatgpt.com/docs/build-skills).

Then invoke:

```text
$implementation-progress Implement this feature and keep a progress panel updated.
```

### Claude Code: standalone skill or local preview

As an alternative to the marketplace plugin, copy the skill from a checkout:

```bash
mkdir -p "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/implementation-progress"
cp -R plugins/implementation-progress/skills/implementation-progress/. \
  "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/implementation-progress/"
```

Use `/implementation-progress` for this installation. For a project-only install,
copy the same folder into `<project>/.claude/skills/`. Choose either the plugin or
standalone install to avoid duplicate entries. You can preview the plugin directly
from this checkout with `claude --plugin-dir ./plugins/implementation-progress`.

For custom agent configurations, copy the **entire skill folder** (`SKILL.md`,
`scripts/`, and `assets/`) into the skills directory your agent discovers. The
script resolves its bundled template relative to its own location.

Standalone copies do not auto-update: pull this repository and repeat the copy
command to update them. See the [implementation-progress README](plugins/implementation-progress/README.md)
for direct CLI usage, output paths, and verification.

# Contributing

Feel free to:
- Fork and customize for your needs
- Submit issues or suggestions
- Share your improvements

# License

MIT - Use freely in your projects

# Author

Created by the good folks at Cliq Consulting
