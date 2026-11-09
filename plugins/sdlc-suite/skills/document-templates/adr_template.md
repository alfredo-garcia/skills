# Template: Architecture Decision Record (ADR)

> **What this is:** a short, permanent record of one technical decision that changes or extends `tech_standards.md` / `hl_architecture.md`: a new library, service or pattern, or a change to an existing rule. Until an ADR is accepted, the change isn't allowed in any project output.
>
> **Produced by:** `tech-lead` Mode B, usually when another skill (or the user) hits a stack conflict.
>
> **Real instance path:** `<docs_root>/architecture/adr/<NNN>_<slug>.md`. `NNN` is sequential (001, 002, …), separate from Feature IDs. ADRs are never deleted. A reversed decision gets a new ADR that supersedes the old one.

---

## Structure

```markdown
# ADR <NNN>: [Decision title]

> Project: `<project_id>`
> Status: Proposed / Accepted (YYYY-MM-DD) / Rejected / Superseded by ADR <NNN>
> Triggered by: [feature ID / PRD section / user request]

## Context
What need or problem forces a decision now. Cite the vision driver and the tech_standards rule
it touches.

## Options Considered
For each option (always including "do nothing / use what we already have"): what it is, pros,
cons, cost/complexity for this team.

## Decision
The chosen option, in one or two sentences.

## Consequences
What changes in tech_standards.md / hl_architecture.md (exact sections), what becomes harder,
and what we'd watch to know it was wrong.

## Enforcement
How the new or changed rule will be enforced: the row added to tech_standards §17 (automated
check, tool and config, or review-only with the reason it can't be automated).
```
