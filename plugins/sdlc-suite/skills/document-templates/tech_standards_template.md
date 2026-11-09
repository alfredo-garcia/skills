# Template: Tech Standards (core)

> **What this is:** the project's binding technical rules that apply across every surface: stack overview, cross-cutting rules (logging, errors, events, security…), contracts between surfaces, quality baseline. Each surface (backend, web, android, ios, …) has its own file for surface-specific rules (`tech_standards_surface_template.md`). Every SDLC skill reads this core file in full on every run, plus the surface files its task touches (`project_context_protocol.md` §4). Claude Code loads it through the project's `CLAUDE.md`. Anything not allowed here or in a surface file needs an ADR first.
>
> **Produced by:** `tech-lead` Mode A, from the approved Product Vision and the High-Level Architecture. Changed only through `tech-lead` Mode B (an ADR).
>
> **Depth depends on `rigor`:** with `personal`, sections can be brief and several may say "n/a (personal project)". With `production`, **every section is mandatory** and each rule must be concrete enough for an agent to follow literally.
>
> **Real instance paths:** core at `<docs_root>/context/tech_standards.md`; surface files at `<docs_root>/context/tech_standards/<surface>.md`. The core wins on any contradiction.

---

## Structure

```markdown
# Tech Standards: [Product Name]

> Project: `<project_id>`
> Rigor: personal | production
> Surfaces: backend, web, android, ios (from SDLC.md)
> Status: Draft / Approved (YYYY-MM-DD)
> Derived from: `product/product_vision.md` (approved YYYY-MM-DD), `architecture/hl_architecture.md`
> Change process: ADR via tech-lead (see §16) · Enforcement: §17

## 1. Stack Overview
| Surface / layer | Choice | Version policy | Why (vision driver / ADR) | Detail in |
|---|---|---|---|---|
| backend | | | | tech_standards/backend.md |
| web | | | | tech_standards/web.md |
| android | | | | tech_standards/android.md |
| ios | | | | tech_standards/ios.md |
| Database(s) | | | | |
| Messaging / events | | | | |
| Auth / identity | | | | |
| Hosting / runtime | (summary; detail in platform_foundations.md) | | | |

## 2. Repository Structure
Monorepo or not, where each surface lives, shared code, docs. Must match SDLC.md paths.

## 3. Cross-Surface Contracts
- API style (REST/GraphQL/gRPC…), schema source of truth (e.g. OpenAPI), code generation for
  clients, naming.
- **API versioning and compatibility**: how versions are expressed, minimum compatibility
  window for deployed mobile clients (coordinate with release-manager), deprecation rules.
- Error contract (format, codes, localization of messages).
- Pagination, filtering, idempotency keys, rate limiting.
- Date/time, money, IDs, locales over the wire.

## 4. Identity, Authentication & Authorization
Identity provider, token/session model per surface, refresh, logout everywhere, roles/permissions
model, service-to-service auth.

## 5. Logging
Structured format and required fields (timestamp, level, service, correlation/request ID, user
or tenant ID where lawful), levels and when to use them, what must NEVER be logged (secrets,
tokens, personal data beyond policy), client-side logging policy (mobile/web).

## 6. Observability
Metrics (what every service/surface emits; naming), distributed tracing (propagation across
surfaces), crash & error reporting per surface, health checks. The stack and dashboards are
implemented by platform-engineer (platform_foundations.md); this section is the rule code follows.

## 7. Events & Asynchronous Processing
Domain events (naming, schema, versioning, ownership), delivery guarantees, idempotent
consumers, retries & dead-lettering, outbox or equivalent, background jobs and schedules.
"n/a" only with a reason.

## 8. Notifications
Channels (push, email, SMS, in-app), which service owns sending, templates & localization, user
preferences & opt-out, push token lifecycle per mobile surface, rate limits/quiet hours.

## 9. Data & Persistence
Ownership per service, schema migration process, ID strategy, timestamps/timezones, soft vs hard
delete, data retention & deletion (incl. user deletion requests), multi-tenancy, caching rules.

## 10. Security & Privacy
Secrets handling, encryption in transit/at rest, input validation, dependency and supply-chain
hygiene, OWASP baseline per surface, personal-data classification and handling per the vision's
regulatory constraints, audit logging of sensitive actions.

## 11. Resilience & Performance
Timeouts, retries with backoff, circuit breaking, graceful degradation, offline behavior on
clients, performance budgets (API latency, app start, web vitals). Targets come from the vision's
scale & availability expectations; SLOs are formalized in platform_foundations.md.

## 12. Configuration & Feature Flags
Configuration sources per environment, remote config for clients, feature-flag tool and naming,
flag lifecycle (creation → rollout → removal); rollout policy itself lives in release_process.md.

## 13. Internationalization, Accessibility & Analytics
Locales and translation workflow; accessibility baseline per surface; product analytics: event
taxonomy, naming, consent, where it's defined.

## 14. Test Platform
Decided by tech-lead (Mode A, with qa-engineer's needs as input); the strategy built on it lives in
`quality/test_strategy.md` (qa-engineer).
- Tools per level and surface (summary; detail in each surface file §9): unit, integration,
  contract, UI/component, end-to-end, visual regression, performance, accessibility, security
  scanning. One tool per purpose; ADRs for real alternatives.
- **Acceptance-test format:** executable specifications (Gherkin-style) or regular tests tagged
  with the criterion ID. Pick one.
- **Tagging convention:** how a test declares `<project_id>/<feature-id>` and `AC-n` / `FR-n`, so
  traceability is computed from test results.
- **Integration testing approach:** backend ↔ clients contract (schema-based or consumer-driven),
  compatibility with old client versions; third parties via sandbox / test doubles / recorded
  responses (which, where, how often against the real sandbox).
- Test data: factories/fixtures, seeding, anonymization rules.
- CI: what runs per PR vs nightly, time budget per pipeline, parallelization, flaky-test handling.
- What's deliberately not required yet (with a revisit signal).

## 15. Definition of Done (technical)
Checklist every feature must meet before merge, across surfaces: acceptance tests written first
and passing (qa-engineer verification, when production), tests, lint, migrations,
observability (logs/metrics/traces added), analytics events, feature flag, docs trigger,
compatibility with deployed clients.

## 16. Changing These Standards
Any new technology, library outside the approved lists, or rule change requires an ADR
(`architecture/adr/`) accepted by the user. Until then it isn't allowed. **Every ADR that adds or
changes a rule states how it will be enforced** (a new or updated row in §17), or why it can't be
automated.

## 17. Enforcement Map
How each rule is enforced, so consistency doesn't depend on anyone remembering it. Built by
tech-lead Mode E; checks are wired into CI with platform-engineer.
| Rule (section · short name) | Enforced by | Check (tool · config path) | Runs | Blocking | Status |
|---|---|---|---|---|---|
| §2 · module boundaries | automated | e.g. dependency-rules tool · `<path>` | PR | yes | active |
| §3 · no breaking API changes | automated | API schema diff · `<path>` | PR | yes | active |
| §5 · no personal data in logs | review | — | PR review | yes | review-only |
"Enforced by": automated / review (the independent reviewer checks it on every PR, see
engineering-lead) / manual (rare; say when). "Status": active / planned (with a target date) /
review-only. Every rule in this file and in the surface files appears here exactly once.
```

## Guidance

- **Every choice cites a driver** (vision section or ADR). No driver means it's a preference: say so, and prefer what the team knows.
- **Write rules an agent can follow literally.** "Every HTTP request log line includes `request_id` propagated from the `X-Request-Id` header" is a rule; "log properly" isn't.
- **`production`: no section may be silently empty.** Use "deferred: <signal to revisit>" or "n/a: <reason>" explicitly.
