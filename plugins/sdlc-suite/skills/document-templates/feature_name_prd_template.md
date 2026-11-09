# Template: Feature PRD

> **What this is:** the full Product Requirements Document expanded from an approved feature
> definition doc — built to be handed directly to an AI coding tool (Claude Code, Cursor, Copilot)
> or a human engineer as an implementation-ready spec. Unlike the feature doc it comes from, this
> document **does** carry contract-level technical detail (data shape, API contracts, UI states) —
> it still stops short of prescribing internal implementation (describe the endpoint's contract,
> not the function that implements it).
>
> **Produced by:** the `product-manager` skill's Mode B, from a confirmed feature doc plus
> the Master Functional Documentation (for dependencies and existing patterns) — never drafted
> without a confirmed feature doc first. Reuses that feature doc's existing Feature ID; never
> mints a new one.
>
> **Consumed by:** the `ux-designer` skill (its primary input for building a prototype and,
> eventually, a UX Flow doc) and `document-manager` (as "Document A" — see that skill's
> `references/input_contract.md` for the content categories it extracts from this document).
>
> **Real instance filename:** `<feature-id>_<feature-slug>_prd.md` — same ID and slug (and case
> style) as the feature doc it was expanded from. Saved alongside it by default.

---

## Structure

Fifteen sections, in this order. Every section should have real content, or explicitly say "not applicable" with a reason — a silently thin section is a defect, not a shortcut.

```markdown
# PRD: [Feature Name]

> Project: `<project_id>`
> Tech standards applied: `<docs_root>/context/tech_standards.md` (approved YYYY-MM-DD) + surface files: [backend, web, android, ios…]
> Surfaces touched: [from SDLC.md surfaces]
> Issue: [#n of the `[Feature]` issue] · Stories: one `[Story]` sub-issue per user story (§4), listed with their AC IDs
> Technical review (tech-lead Mode C): pending / passed (YYYY-MM-DD) / n/a (rigor personal)
> Test plan (qa-engineer): required / approved (YYYY-MM-DD) / verified (YYYY-MM-DD) / n/a (rigor personal)
> Prototype (ux-designer): required / signed off (YYYY-MM-DD) / exempt (YYYY-MM-DD): reason / n/a (no UI surface)
>   (exempt only by the user's explicit decision; required by default for any feature touching a UI surface)
> Source feature doc: `<feature-id>_<feature-slug>.md`
> Master doc referenced: `[path to functional spec found in repo]`
> Status: Draft / Reviewed / Approved

## 1. Summary
One paragraph: what this is, why it matters, who it's for.

## 2. Background & Context
- What exists today (from the master functional doc) that this touches or depends on.
- Why now / what triggered this requirement.

## 3. Goals & Success Metrics
- Goal(s), restated from the feature doc, made measurable where possible.
- How we'll know this succeeded (metric, behavior change, or qualitative bar).

## 4. Non-Goals / Out of Scope
- Carried over and expanded from the feature doc's Constraints section.
- Explicitly list adjacent things that might seem implied but are NOT included.

## 5. User Stories & Acceptance Criteria
For each core mechanic in the feature doc, expand into:
- **As a** [persona], **I want** [capability], **so that** [benefit].
- **Acceptance Criteria** (Given/When/Then, testable — no ambiguous verbs like "should work
  well"). Each criterion has its own ID and names the requirement(s) it proves:
  `AC-3 (FR-2): Given …, when …, then …`. IDs are permanent; qa-engineer's tests and
  traceability matrix reference them. Include negative paths, and the behavior when each
  third party involved fails, is slow, or responds badly. State differences between surfaces
  explicitly.

## 6. Functional Requirements
Numbered, unambiguous, atomic requirements. Each one should be independently verifiable and
independently implementable. Flag any requirement that is underspecified in the source feature
doc rather than inventing the missing detail.

1. FR-1: ...
2. FR-2: ...

## 7. Data Model / Schema Changes
- New entities/fields, or changes to existing ones.
- Relationships to existing schema (reference the master doc).
- If genuinely no data model impact, state that explicitly rather than omitting the section.

## 8. API / Interface Contracts
- New or changed endpoints/functions/props — inputs, outputs, error states.
- Keep at contract level (signatures, payloads), not internal implementation.

## 9. UI/UX Requirements
- Only include if the feature has a UI surface. One subsection per UI surface it touches (web,
  android, ios), or "All" where they behave identically. States to cover: empty, loading,
  success, error, edge (e.g. permission denied, offline).
- Reference existing UI patterns from the master doc where applicable instead of inventing new
  ones.

## 10. Edge Cases & Error Handling
- Enumerate the non-happy-paths explicitly. This is the section most AI coding tools under-build
  without a prompt — be exhaustive here.

## 11. Non-Functional Requirements
- Performance, security, accessibility, scale — only where relevant to this feature. Say "not
  applicable" rather than skipping silently.
- **When `rigor: production`, these subsections are mandatory** (each may say "n/a: reason"),
  following the project's core tech standards:
  - 11.1 Observability: logs, metrics and traces this feature must emit; alerts it needs.
  - 11.2 Analytics events: names and properties per the tracking plan.
  - 11.3 Notifications: channels, triggers, templates, opt-out.
  - 11.4 Security & privacy: data classification of new data, authorization rules, audit events.
  - 11.5 Performance & resilience: budgets, timeouts, offline behavior on clients.
  - 11.6 Compatibility: impact on deployed mobile clients and API versions.

## 12. Dependencies & Existing System Touchpoints
- Other modules/features/services this interacts with, per the master functional doc.
- Shared dependencies used (project_id + contract section).
- **Platform needs** (routed to platform-engineer): new infrastructure, environments, secrets,
  scheduled jobs, third-party accounts, dashboards/alerts — or "none".
- **Release needs** (routed to release-manager): feature flag, staged rollout, coordinated
  multi-surface release, forced update, store-facing changes — or "none".
- Anything blocking or blocked by this work.

## 13. Assumptions & Open Questions
- Every assumption made to fill a gap the feature doc left open, listed explicitly so a human can
  confirm or correct it.
- Unresolved questions that should be answered before/during implementation.

## 14. Rollout & Testing Considerations
- Flagging/staged rollout needs (per the project's release_process.md), migration steps and
  deploy ordering across surfaces.
- Testing: don't describe tests here. Point to the feature's test plan
  (`<id>_<slug>_test_plan.md`, written by qa-engineer from §5, §6, §10 and §11), and list only
  risks that deserve extra testing attention. Never name test tools; they come from the tech
  standards.

## 15. Appendix
- Glossary of any domain terms, links/references to the master doc sections used.
```

## Section-by-Section Guidance

- **§5 (User Stories & Acceptance Criteria):** acceptance criteria must be testable (Given/When/Then). Reject vague criteria like "works well" or "is fast" — push for a concrete condition (e.g. "Given a cart with 1 item, when the user taps quick-add on a second item, then the cart shows 2 items and the subtotal updates within 1 render cycle").
- **§6 (Functional Requirements):** atomic, numbered, independently verifiable. A requirement that depends on an unresolved foundational question shouldn't appear unmarked — it should already have been resolved before drafting (see the authoring convention below), not slip through silently.
- **§10 (Edge Cases):** be exhaustive. Cross-check the master functional spec for how existing error/edge states are handled elsewhere in the app, for consistency (e.g. don't invent a new empty-state pattern if one is already established).
- **§7-9 (Data / API / UI):** fill in what's grounded in the feature doc or master doc as fact; everything else should be marked as a proposed default (see below), never an unmarked assertion.

## Authoring Convention: Marking Proposed Defaults

Not every implementation-adjacent detail needs to be nailed down before drafting — some gaps are safe to fill with a sensible default and confirm later, as long as that default is visible rather than silently asserted as fact. Two kinds of gaps, handled differently:

- **Foundational gaps** — anything that changes what the feature *means* if guessed wrong (core data semantics, which persona/plan it applies to, scope boundaries, business-logic math). These should be resolved by asking before this document is drafted at all — they should never appear as a proposed default here, because guessing wrong on one of these derails the whole document.
- **Proposable gaps** — implementation-adjacent detail that doesn't change the feature's meaning either way (UI placement, exact endpoint shape, minor edge-case handling with an obviously reasonable default). These get a visible inline marker while in draft:

```markdown
FR-2: **[PROPOSED]** Display the count as a badge next to the teammate's avatar. *Rationale:
matches the existing avatar-based pattern elsewhere on the Team Board.*
```

**This tag is draft-phase-only.** It exists so a review pass can find every open proposal at a glance before the document is finalized. It must **never appear in a finalized/saved version** of this document — by the time a PRD is saved as final, every `**[PROPOSED]**` item has either been folded into confirmed plain prose (indistinguishable from any other confirmed content) or moved into §13 (Assumptions & Open Questions) as a genuinely still-open item the user chose to defer, never left as a lingering proposal tag.

## Quality Bar Before Finalizing

- No section is silently thin — either it has real content or it explicitly says "not applicable" with a reason.
- No `**[PROPOSED]**` tags remain anywhere in the final document.
- Every still-open item is visible in §13, not buried invisibly in the requirements prose.
- Cross-references to the master functional spec are concrete (name the domain/screen/component ID), not vague gestures at "existing code."
