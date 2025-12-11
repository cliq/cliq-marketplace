---
name: Fork Terminal Skill
description: Forks a terminal session to a new terminal window. Use when the user requests 'fork terminal <command>' or 'fork session <command>' or 'fork new terminal using <agent tool> <command>' or 'create a new terminal with <agent> and <command>' or 'new terminal <command>'.
---

# Purpose

Fork a terminal session to a new terminal window using one agentic coding tool or raw cli commands.
Follow the `Instructions`, execute the `Workflow` based on the `Cookbook`.

## Variables

ENABLE_RAW_CLI_COMMANDS: true
ENABLE_CLAUDE_CODE: true
ENABLE_GEMINI_CLI: true
ENABLE_CODEX_CLI: true
AGENTIC_CODING_TOOLS: claude-code, codex-cli, gemini-cli

## Instructions

- Based on the users request, follow the `Cookbook` to determine which tool to use.

### Fork Summary User Prompts

- IF: The user requests a fork terminal with a summary. This ONLY works for our agentic coding tools `AGENTIC_CODING_TOOLS`. The tool MUST BE enabled as well.
- THEN: 
  - Read, and REPLACE the `.claude/skills/fork-terminal/prompts/fork_summary_user_prompt.md` with the history of the conversation between you and the user so far. 
  - Include the next users request in the `Next User Request` section.
  - This will be what you pass into the PROMPT parameter of the agentic coding tool.
  - IMPORTANT: To be clear, don't update the file directly, just read it, fill it out IN YOUR MEMORY and use it to craft a new prompt in the structure provided for the new fork agent.
  - Let's be super clear here, the fork_summary_user_prompt.md is a template for you to fill out IN YOUR MEMORY. Once you've filled it out, pass that prompt to the agentic coding tool.
  - XML Tags have been added to let you know exactly what you need to replace. You'll be replacing the <fill_in_conversation_summary_here> and <fill_in_next_user_request_here> sections.
- EXAMPLES:
  - "fork terminal use claude code to <xyz> summarize work so far"
  - "spin up a new terminal request <xyz> using claude code include summary"
  - "create a new terminal to <xyz> with claude code with summary"

## Workflow

1. Understand the users request
2. READ: `.claude/skills/fork-terminal/tools/fork_terminal.py` to understand our tooling
3. Follow the `Cookbook` to determine which tool to use
3. Execute the `.claude/skills/fork-terminal/tools/fork_terminal.py: fork_terminal(command: str)` tool

## Cookbook

### Raw CLI Commands

IF: The user requests a non-agentic coding tool and `ENABLE_RAW_CLI_COMMANDS` is true
THEN: Read and execute: '.claude/skills/fork-terminal/cookbook/cli-command.md'

EXAMPLES:
  - "Create a new terminal using <xyz> with python"
  - "Create a new terminal using <xyz> and curl"
  - "Create a new terminal using <xyz> then grep"

### Claude Code

IF: the user requests 'claude' tool and `ENABLE_CLAUDE_CODE` is true
THEN: Read and execute: '.claude/skills/fork-terminal/cookbook/claude-code.md'

EXAMPLES:
  - "New terminal using claude code to <xyz>"
  - "launch a new terminal request <xyz> using claude code"
  - "create a new terminal to <xyz> with claude"

### Gemini CLI

IF: the user requests 'gemini' tool and `ENABLE_GEMINI_CLI` is true
THEN: Read and execute: '.claude/skills/fork-terminal/cookbook/gemini-cli.md'

EXAMPLES:
  - "New terminal using gemini cli to <xyz>"
  - "launch a new terminal request <xyz> using gemini"
  - "create a new terminal to <xyz> with gemini cli"

### Codex CLI

IF: the user requests 'codex' tool and `ENABLE_CODEX_CLI` is true
THEN: Read and execute: '.claude/skills/fork-terminal/cookbook/codex-cli.md'

EXAMPLES:
  - "New terminal using codex cli to <xyz>"
  - "launch a new terminal request <xyz> using codex"
  - "create a new terminal to <xyz> with codex cli"