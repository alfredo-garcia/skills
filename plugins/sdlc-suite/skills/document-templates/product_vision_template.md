# Template: Product Vision

> **What this is:** the founding document of a project: what problem it solves, for whom, what the MVP is (and isn't), and the real-world constraints and scale it must live with. Every later decision traces back here: the stack and architecture (`tech-lead`), the UI standards (`ux-designer`), and whether a feature belongs in the MVP (`product-manager`).
>
> **Why it comes first:** architecture chosen without a vision tends to be built for an imagined scale. §9 (Constraints) and §10 (Scale & Quality Expectations) exist specifically so `tech-lead` can justify the *simplest* architecture that fits, and push back on anything bigger.
>
> **Produced by:** `product-manager` Mode 0, after a challenge interview (`references/vision_playbook.md`). **Consumed by:** `tech-lead` Mode A, `ux-designer` Mode 0, `product-manager` Mode A (MVP scope check), `document-manager` (Product Overview in the master doc).
>
> **Real instance path:** `<docs_root>/product/product_vision.md`. One per project. It evolves; changes after approval go through a visible diff and approval, and material changes flag downstream foundations for review (`project_context_protocol.md` §8).

---

## Structure

Twelve sections, in this order. Prose in the project's `docs_language`. A section may say "not applicable" with a reason, but never be silently thin.

```markdown
# Product Vision: [Product Name]

> Project: `<project_id>`
> Status: Draft / Approved (YYYY-MM-DD)
> Last material change: YYYY-MM-DD

## 1. Problem
What hurts today, for whom, and how they cope now (current alternatives, workarounds). Concrete,
observable, not "people need a better way to…".

## 2. Vision Statement
One or two sentences: what this product will be for its users if it succeeds.

## 3. Target Users & Personas
At most 3 personas for the MVP. For each: name/label, context, main job-to-be-done, what they
use today. Mark the primary persona.

## 4. Value Proposition
Why a persona would choose this over their current alternative. What it deliberately does
differently or better.

## 5. MVP Definition
- **Hypothesis the MVP must test** (what we need to learn or prove).
- **In scope**: the minimum capabilities needed to test it, as short capability statements
  (not features with designs).
- **Explicitly out of scope for the MVP**: tempting things that wait, each with a one-line
  reason.
- **MVP done when**: the observable condition that means the MVP is complete.

## 6. Success Metrics
How we'll know the MVP worked. Metric or qualitative bar, plus a target. Name which kind each is.

## 7. Initial Feature Backlog
Candidate features derived from §5, in priority order. They're not specified yet and have no IDs
yet; IDs are minted when product-manager Mode A defines each one.

| # | Candidate feature | Persona | MVP? (yes/no) | Priority (Must/Should/Could) | Notes |
|---|---|---|---|---|---|

## 8. Product Principles
3-5 short rules that settle trade-offs (e.g. "offline first, sync later"; "fewer options, good
defaults"). These guide product-manager and ux-designer when the docs are silent.

## 9. Constraints
- Team: who builds this, their skills and preferred technologies, available time.
- Budget: monthly hosting/services ceiling, paid tools allowed or not.
- Timeline: target dates, if any.
- Platforms: must match `SDLC.md` `platforms`.
- Regulatory / legal: data protection, payments, health, age restrictions, etc. Only what applies.
- Other hard limits (must integrate with X, must run on Y).

## 10. Scale & Quality Expectations
Realistic numbers, not aspirations. These are the main input against over-architecture.
- Users: at MVP launch / after ~12 months (order of magnitude).
- Usage pattern: how often, peaks, concurrency.
- Data: volume, sensitivity (personal / financial / health / none), retention.
- Availability: what happens if it's down for an hour? (annoying / costly / unacceptable)
- Offline, real-time, or multi-device needs: only if genuinely required.

## 11. Risks & Assumptions
What we're assuming is true without proof, and what could kill the product.

## 12. Open Questions
Unresolved items, each with who/when it should be answered.
```

## Section guidance

- **§5 is the heart.** Push for the smallest MVP that tests the hypothesis. A long in-scope list usually means the hypothesis isn't clear yet.
- **§7 vs §5.** §5 says *what capabilities* the MVP needs; §7 slices them into candidate features with priority. Every "MVP? yes" row must map to something in §5's in-scope list.
- **§9 and §10 must be honest.** "Solo developer, a few hours a week, ~50 users at launch, ≤ $20/month" is a perfectly good answer, and it should drive a very different architecture than "10M users".
- **No technology here.** Stack choices belong to `tech-lead`. A constraint like "the team only knows Python" or "must run on the client's existing Azure" is a constraint (§9), not a stack decision.

## Quality bar before approval

- The hypothesis (§5) is testable and the MVP done-condition is observable.
- Every MVP backlog item (§7) maps to §5's in-scope list; nothing in §5 lacks a backlog item.
- §10 has real numbers or explicit "unknown, assume small".
- Out-of-scope (§5) names at least the 2-3 most tempting things being deferred.
