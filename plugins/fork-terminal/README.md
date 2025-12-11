# Fork Terminal Skill

A Claude Code skill that spawns new terminal windows with agentic coding tools or raw CLI commands.

## Quick Start

**Step 1:** Add the marketplace (once):
```bash
/plugin marketplace add https://github.com/cliq/cliq-marketplace
```

**Step 2:** Install the `fork-terminal` plugin (once):
```bash
/plugin install fork-terminal
```

**Step 3:** Restart Claude Code to load the plugin.

## Supported Tools

| Tool | Default Model | Fast Model | Auto-approve Flag |
|------|---------------|------------|-------------------|
| **Claude Code** | opus | haiku | `--dangerously-skip-permissions` |
| **Gemini CLI** | gemini-2.5-pro | gemini-2.5-flash | `-y` |
| **Codex CLI** | gpt-5.1-codex-max | gpt-5.1-codex-mini | `--dangerously-bypass-approvals-and-sandbox` |
| **Raw CLI** | N/A | N/A | N/A |

## Usage Examples

### Single Fork

```
# Fork with Claude Code
"fork a new terminal using claude to fix the failing tests"

# Fork with Gemini CLI
"create a terminal with gemini to refactor the auth module"

# Fork with Codex CLI
"new terminal using codex to add input validation"

# Fork with raw CLI command
"fork terminal with python to run the benchmark script"
```

### Fork with Conversation Summary

Pass your current conversation context to the new agent:

```
# Include conversation history
"fork a claude terminal with summary to continue debugging"

# Summary with specific task
"create a gemini terminal with summary to implement the feature we discussed"
```

### Multiple Parallel Forks

Ask Claude to spawn several agents simultaneously:

```
# Parallel tasks with same tool
"fork 3 claude terminals to:
 1. fix the unit tests
 2. update the documentation
 3. refactor the error handling"

# Parallel tasks with different tools
"fork terminals in parallel:
 - claude to review the security
 - gemini to optimize performance
 - codex to add test coverage"
```

### Model Selection

Request faster or heavier models:

```
# Use fast model for quick tasks
"fork a fast claude terminal to check the syntax"

# Use heavy model for complex tasks
"fork a heavy gemini terminal to architect the new module"
```

## Project Structure

```
.claude/skills/fork-terminal/
|-- SKILL.md                        # Skill definition & routing logic
|-- cookbook/
|   |-- claude-code.md              # Claude Code configuration
|   |-- gemini-cli.md               # Gemini CLI configuration
|   |-- codex-cli.md                # Codex CLI configuration
|   +-- cli-command.md              # Raw CLI configuration
|-- prompts/
|   +-- fork_summary_user_prompt.md # Summary template
+-- tools/
    +-- fork_terminal.py            # Terminal spawning script
```

## Platform Support

- **macOS**: Full support via AppleScript
- **Windows**: Basic support via cmd
- **Linux**: Not yet implemented

## Configuration

Edit the variables in `SKILL.md` to enable/disable tools:

```
ENABLE_RAW_CLI_COMMANDS: true
ENABLE_CLAUDE_CODE: true
ENABLE_GEMINI_CLI: true
ENABLE_CODEX_CLI: true
```

## License

MIT
