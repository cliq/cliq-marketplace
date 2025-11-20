## Claude Conversation Saver Plugin

A lightweight Claude Code plugin that adds automatic conversation saving via hooks and slash commands. Built on top of the [conversation-logger skill](https://github.com/sirkitree/conversation-logger).

### What is This?

This plugin is an **automation wrapper** around the `conversation-logger` skill:
- **The skill** contains all the core logic (saving, parsing, searching)
- **This plugin** adds automatic triggers (Stop hook) and convenience commands

### Why This Approach?

**Hybrid Benefits**:
- ✅ **Single source of truth**: All core logic lives in the skill
- ✅ **Real-time automatic saves**: Plugin hook triggers after each response
- ✅ **User choice**: Use just the skill manually, or add the plugin for automation
- ✅ **Easy maintenance**: Update the skill, plugin automatically benefits
- ✅ **Cross-platform**: Skill works everywhere, plugin adds Claude Code automation

### Features

- 🔄 **Auto-saves conversations** after each Claude response in real-time
- 📝 **Converts to markdown** - readable conversation transcripts
- 🔍 **Powerful search** - find past conversations instantly
- 📊 **Browse recent** - quickly review recent sessions
- 💾 **Full metadata** - preserves session info and timestamps
- ⚡ **Slash commands** - convenient `/convo-*` commands

### Prerequisites

Make sure you have:
- `git` - For cloning the skill
- `jq` - JSON processor (for hook data parsing)
- `python3` - For parsing conversations to markdown

### Quick Install

```bash
**Step 1:** Add the marketplace (once):
```bash
/plugin marketplace add https://github.com/cliq/cliq-marketplace
```

**Step 2:** Install the `conversation-saver` plugin (once):
```bash
/plugin install conversation-saver
```

**Step 3:** Restart Claude Code to load the plugin.

### What's Inside

#### 📋 Custom Commands (3)

- `/convo-list` - List all saved Claude Code conversations
- `/convo-recent` - Show recent (5) Claude Code conversations
- `/convo-search` - Search through saved Claude Code conversations

#### 🔌 Hooks (1)

- **Stop** - Saves conversation after each Claude response
