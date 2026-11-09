# Architecture Playbook: Simplest Thing That Fits

> **Rigor matters.** For `rigor: personal`, use this ladder as the main tool. For `rigor: production`, use it *together with* `cross_cutting_checklist.md` and the surface lenses: you still climb down the ladder only with drivers, but every concern must be explicitly decided, and quality targets (availability, RPO/RTO, latency, compliance) are drivers in their own right. Production drivers often legitimately justify more (managed queues, tracing, staged environments), and that's correct, not over-architecture, as long as each one cites its driver.

Use this in Mode A (proposing foundations) and Mode B (evaluating a change). The goal isn't the "best" architecture in the abstract. It's the simplest one that satisfies *this* vision's drivers, built by *this* team.

## The simplicity ladder

For each concern, start at the top rung and move down only when a cited driver forces it.

| Concern | Start here | Move down only if… |
|---|---|---|
| Deployables | One app (monolith; may serve web + API) | A driver needs independent scaling/teams/runtimes |
| Frontend | Framework the team knows; server-rendered or simple SPA | Offline/real-time/very rich interaction is a stated need |
| Mobile | None, or a responsive web/PWA | Vision lists mobile as a platform and needs native capabilities |
| Database | One managed relational DB (or SQLite for tiny/local) | Data shape or scale in the vision genuinely doesn't fit |
| Auth | The framework's built-in auth, or one managed provider | Regulatory or enterprise SSO needs |
| Background work | In-process scheduled jobs | Long-running/retry-critical work at real volume |
| Caching | None | Measured latency problem (put the signal in Deferred) |
| Search | DB queries / full-text in the DB | Volume or relevance needs beyond that |
| Messaging/queues | None | Multiple services or real async workflows |
| Infra | PaaS / managed hosting | Budget or control constraints rule it out |
| Observability | Platform logs + an error tracker | Availability needs in vision §10 demand more |
| Environments | Local + production (+ preview if the platform gives it for free) | Team size or risk demands staging |

## Over-architecture red flags

Stop and ask "which vision driver requires this?" when you see:
- Microservices, Kubernetes, service mesh, or event sourcing for a small team or MVP.
- Several databases, a cache, or a queue before any measured need.
- Multi-region, HA clusters, or a 99.99% target when vision §10 says an hour of downtime is "annoying".
- A technology the builder doesn't know, chosen for being "modern", when a known one fits.
- Abstractions built "in case we switch providers later".
- Planning for the 12-month scale at day one when the vision says launch scale is tiny. Design so growth is *possible*, not pre-built.

When there's no driver, recommend deferring it, write it in hl_architecture §9 with a concrete revisit signal, and let the user decide with the trade-off visible.

## Under-architecture checks (the opposite failure)

For `rigor: production`, the full list is `cross_cutting_checklist.md`: every row decided. The items below are the minimum even for `personal`.

Simple doesn't mean careless. Always cover:
- Secrets are out of the repo; there's a plan for backups of real user data.
- Personal or sensitive data is handled according to the vision's regulatory constraints.
- Schema migrations are versioned.
- There's a minimal automated check before merge (lint + tests that exist).
- There's a clear path to production that the builder can run alone.

## Questions to resolve with the user (only if the vision doesn't answer them)
- What do you know well enough to debug at 11pm?
- Which hosting/cloud accounts do you already have?
- Maximum monthly spend for the MVP?
- How much ops work are you willing to do: none (fully managed), some, or full control?

## Mode B evaluation checklist
- Restate the need and quote the standard it conflicts with.
- Show the "use what we have" option concretely first.
- For each option: driver fit, the team's familiarity, operational cost, reversibility (one-way or two-way door).
- Prefer reversible choices; spend debate time only on one-way doors.
