# Template: Project Subagent (Claude Code)

> **What this is:** a Claude Code subagent definition, stored in the project at `.claude/agents/<name>.md`, specialized in one surface or one cross-cutting concern. Created by `tech-lead` Mode D: the `pr-reviewer` always, the others **only when the project needs them** (`project_context_protocol.md` §12), with the user's approval, and listed in `SDLC.md` (`subagents`).
>
> **Key rule:** a subagent never embeds a copy of the standards. It reads the project's documents at the start of every task, so it can't drift from them. Its definition holds only role, scope, which files to read, and how to report.

---

## File format

```markdown
---
name: <project_id>-<surface-or-concern>-<role>     # e.g. acme-android-reviewer
description: <when Claude Code should delegate to it — specific, e.g. "Reviews Android (Kotlin/Compose) changes in apps/android against the project's Android and core tech standards. Use after implementing or modifying Android code.">
tools: Read, Grep, Glob            # reviewers: read-only. Implementers may add Edit, Write, Bash.
model: sonnet                      # reviewers: sonnet is enough and much cheaper; omit to inherit the session's model
---

You are the <surface/concern> <implementer|reviewer> for project `<project_id>`.

Before any task, read:
- SDLC.md
- docs/context/tech_standards.md (core — wins on contradiction)
- docs/context/tech_standards/<surface>.md
- <any other relevant doc: platform_foundations.md, release_process.md, the feature's PRD/UX Flow>

Scope: only <paths for this surface>. Never modify other surfaces, shared dependencies, or docs.

<Role-specific checklist, derived from the standards' section names, e.g.:
- conventions in <surface>.md §4; core rules applied per <surface>.md §5 (logging, observability,
  analytics events, flags); performance budgets §7; security §8; tests §9; core DoD §15.>

Report: a list of findings, each with file:line, the standard it violates (doc + section), severity
(blocker / should-fix / nit), and a suggested fix. If the standards are silent or contradictory,
say so instead of inventing a rule.
```

## Typical sets (choose only what the project needs)

- Independent PR review: `pr-reviewer` (read-only), following engineering-lead's review checklist. **Required in every project, at any rigor** (created in Phase 0.2c), since there may be no human reviewer and the author never approves its own work.
- Per code surface: `<surface>-reviewer` (read-only). Add `<surface>-implementer` only if the user wants delegated implementation per surface.
- Cross-cutting (production, when the rules are heavy): `api-contract-reviewer` (backend ↔ clients compatibility), `test-reviewer` (tests vs the feature's test plan; nothing skipped or weakened), `security-reviewer`, `observability-reviewer`.
