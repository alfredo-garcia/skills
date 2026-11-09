# Subagents Guide (Mode D)

Claude Code subagents are specialized assistants defined as Markdown files with frontmatter in the project's `.claude/agents/` folder. Claude Code can delegate to them based on their `description`, or the user can invoke them explicitly. Each runs with its own context and its own tool list.

## The one that's always required

**`<id>-pr-reviewer` is created in every project, at any rigor**, in Phase 0.2c. The user may have no human reviewer, so this agent (plus the CI review in production) is what makes "the author never approves its own work" real. Read-only, following engineering-lead's review checklist.

## When the others are warranted (protocol §12)

Create them only if at least one of these holds, **and** the user approves:
- `rigor: production` with 2+ code surfaces: per-surface reviewers keep each surface's rules applied without loading every standard into every session.
- A team, or parallel workstreams per surface.
- Heavy cross-cutting rules (API compatibility with deployed clients, security, observability) that benefit from a dedicated reviewer.
- The user explicitly asks.

Otherwise, say they aren't needed yet and why, in one line. A personal single-surface project almost never needs more than the pr-reviewer.

## Design rules

1. **Read, don't embed.** An agent's prompt lists which project documents to read at the start of every task. It never contains copies of rules, so it can't drift from the standards.
2. **Narrow scope.** One surface, or one concern, per agent. Explicit paths it may touch.
3. **Least privilege.** Reviewers get read-only tools (`Read, Grep, Glob`). Implementers get edit tools only if the user wants delegated implementation, and are never allowed to touch other surfaces, shared dependencies or docs.
4. **Specific descriptions.** The `description` must say exactly when to use it (which paths, which moment: after implementing, before merge). Vague descriptions cause wrong delegation.
5. **Actionable reports.** Findings with file:line, the violated standard (doc + section), severity and a suggested fix, plus "standards silent or contradictory" when that's the case.
6. **Named with the project id** (`<project_id>-<surface>-reviewer`), so agents from different projects never get confused.

## Typical minimal set for a production multi-surface project

| Agent | Tools | Reads |
|---|---|---|
| `<id>-backend-reviewer` | Read, Grep, Glob | core TS, TS/backend, PRD |
| `<id>-web-reviewer` | Read, Grep, Glob | core TS, TS/web, ui_standards, UX Flow |
| `<id>-android-reviewer` | Read, Grep, Glob | core TS, TS/android, ui_standards, UX Flow |
| `<id>-ios-reviewer` | Read, Grep, Glob | core TS, TS/ios, ui_standards, UX Flow |
| `<id>-pr-reviewer` | Read, Grep, Glob | PRD, UX Flow, test plan, impl plan task, core TS §15/§17 review-only rules (engineering-lead's review checklist) |
| `<id>-api-contract-reviewer` (optional) | Read, Grep, Glob | core TS §3, release_process §7, API schema |

Implementer agents (`<id>-<surface>-implementer`, with edit tools limited to that surface's paths) only when the user wants delegated implementation per surface; `engineering-lead` assigns them one task at a time. Add `<id>-test-reviewer` (read-only; reads the test strategy and the feature's test plan) when `qa-engineer` is active in production: it checks that every acceptance criterion has a tagged test and that no test was skipped or weakened compared with the plan. Add `security-reviewer` / `observability-reviewer` only when those rules are extensive enough to deserve separate attention.

## Maintenance

- List every agent in `SDLC.md` (`subagents`). The context script flags agents that are undeclared or missing.
- When a surface is added or removed, or the standards are restructured, update the agents' reading lists in the same change.
- Monorepos: agents live in each project's own `.claude/agents/`. Launch Claude Code from the project folder so the right set is in scope, and never share agents between projects.
