# iphone-duo-readiness

Audit an iOS app for iPhone Duo (foldable iPhone) support and produce a prioritized,
evidence-backed implementation plan — then, when asked, implement the fixes.

The skill drives the review from a catalog of 19 rules (D01–D19) covering geometry and
state continuity, adaptive containers and presentations, bars and action semantics, and
conditional work for camera, game, and legacy-compatibility paths. Every finding is tied
to a real file and symbol, an observable trigger, and an acceptance check — with runtime
evidence separated from static-only inspection, so a clean build is never reported as
device readiness.

## Skill

### `/iphone-duo-readiness`

Triggers whenever the conversation mentions iPhone Duo, a foldable or folding iPhone,
fold/hinge layout, inner or outer displays, or reserved regions — including a request to
implement those fixes. It does not take over general iOS code review or ordinary
iPad/size-class adaptation work.

**Audit** (the default when asked what needs to be done):

1. Establishes the target, a baseline build, and the available runtime environments; records pre-existing failures separately.
2. Maps applicable rule IDs to user journeys and source locations, inspecting shared abstractions before individual screens.
3. Reproduces suspected failures where a simulator or device allows, and labels the rest as unverified behavior.
4. Classifies each rule per component as pass, gap, needs runtime verification, not applicable, or blocked.
5. Prioritizes by demonstrated user impact — lost work, crashes, and inaccessible core actions first.
6. Returns a dependency-ordered implementation map in the conversation, separating essential fixes from optional enhancements.

**Implementation**: makes the smallest coherent change that resolves the evidenced
problem, repairing existing containers and shared components rather than adding a
device-specific parallel UI, and verifies transitions with work in progress — not only
clean launches at different sizes.

## Contents

| Path | Purpose |
|------|---------|
| `skills/iphone-duo-readiness/SKILL.md` | Scope, audit and implementation workflow, required report format |
| `skills/iphone-duo-readiness/references/review-rules.md` | The D01–D19 rule catalog: basis, search targets, acceptance evidence |
| `skills/iphone-duo-readiness/references/repository-audit.md` | Discovery commands, search leads, build/runtime evidence handling |
| `skills/iphone-duo-readiness/agents/openai.yaml` | Interface metadata for Codex-style agents |

## Install

### Claude Code: marketplace plugin

```text
/plugin marketplace add cliq/cliq-marketplace
/plugin install iphone-duo-readiness@cliq-marketplace
```

Claude Code namespaces plugin skills, so invoke it as
`/iphone-duo-readiness:iphone-duo-readiness`.

### Claude Code: standalone skill

```bash
mkdir -p "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/iphone-duo-readiness"
cp -R plugins/iphone-duo-readiness/skills/iphone-duo-readiness/. \
  "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/iphone-duo-readiness/"
```

### Codex: standalone skill

From a checkout of this repository, in Bash or Zsh:

```bash
mkdir -p "$HOME/.agents/skills/iphone-duo-readiness"
cp -R plugins/iphone-duo-readiness/skills/iphone-duo-readiness/. \
  "$HOME/.agents/skills/iphone-duo-readiness/"
```

In Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills/iphone-duo-readiness" | Out-Null
Copy-Item -Recurse -Force "plugins/iphone-duo-readiness/skills/iphone-duo-readiness/*" "$HOME/.agents/skills/iphone-duo-readiness/"
```

Codex discovers user skills in `~/.agents/skills`; for a project-only install, copy the
same folder into `<project>/.agents/skills/` instead. Restart Codex if it does not pick up
the new skill. Then invoke:

```text
$iphone-duo-readiness Audit this app for iPhone Duo support.
```

Copy the **entire** skill folder — `SKILL.md` and `references/` — since the workflow reads
the rule catalog and audit guide by relative path. Standalone copies do not auto-update:
pull this repository and repeat the copy command.
