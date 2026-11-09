# Cross-Cutting Concerns Checklist

Every concern below becomes a row in the hl_architecture §9 register.

- **`rigor: production`:** every row gets an explicit decision: **adopt** (how, and where the rule lives), **defer** (with a concrete revisit signal), or **n/a** (with a reason). An empty or implicit row means the architecture is incomplete.
- **`rigor: personal`:** decide the rows marked **[always]**; the rest can be one-line "n/a / defer".

For each concern, the questions to answer and where the outcome lands: core `tech_standards.md` (TS §), per-surface file (TS-surface §5), or platform_foundations (PF §, decided with platform-engineer).

## Observability & operations

**1. Logging [always]** (TS §5, PF §4)
- Structured (JSON) or not? Required fields: timestamp, level, service/surface, environment, version, correlation/request ID, user/tenant ID (only where lawful).
- Level policy; what is NEVER logged (secrets, tokens, passwords, payment data, personal data beyond policy).
- Client logging (mobile/web): what's sent, when, consent, batching. Retention and access (PF).

**2. Metrics** (TS §6, PF §4)
- Golden signals per service (latency, traffic, errors, saturation); business KPIs from the vision's success metrics; naming conventions; cardinality limits.

**3. Distributed tracing** (TS §6, PF §4)
- Propagation standard across surfaces (e.g. W3C Trace Context), spans for external calls and DB, sampling policy.

**4. Crash & error reporting [always for client surfaces]** (TS-surface §5, PF §4)
- Tool per surface, symbol/source-map upload in CI, release tagging, PII scrubbing.

**5. Health checks, SLOs & alerting** (PF §4-5)
- Liveness/readiness; SLIs for critical journeys; what pages vs what tickets; on-call reality.

**6. Audit logging** (TS §10)
- Which sensitive actions are audited (auth events, permission changes, data exports/deletions, admin actions), immutability, retention.

## Asynchrony & communication

**7. Domain events & messaging** (TS §7)
- Is there async work at all? Event naming/schema/versioning, ownership, delivery guarantees (at-least-once + idempotent consumers), ordering needs, retries/backoff, dead-letter handling, outbox pattern for DB+event consistency.

**8. Background jobs & scheduling** (TS §7)
- Cron/scheduled jobs, long-running work, retries, concurrency limits, visibility (failed job alerts).

**9. Notifications** (TS §8)
- Channels: push (APNs/FCM), email, SMS, in-app, webhooks to third parties. Owning service, templates & localization, user preferences/opt-out (legal), push token lifecycle, deep links from notifications, rate limits & quiet hours, deliverability (email domain auth).

**10. Real-time** (TS §3/§7)
- Is it needed (vision), or is polling/push enough? WebSockets/SSE, presence, fan-out, and the scaling implications.

## Identity, security & privacy

**11. Identity & authentication [always]** (TS §4)
- Build vs managed IdP; methods (password, magic link, OAuth/social, passkeys); MFA; session/token model per surface (cookies on web, secure storage on mobile); refresh & revocation; account recovery.

**12. Authorization** (TS §4)
- Model (roles, permissions, ownership/ABAC, multi-tenant isolation); where it's enforced (always server-side); admin capabilities.

**13. Secrets & configuration [always]** (TS §10/§12, PF §6)
- Secret store, no secrets in repo or client binaries, rotation, per-environment config.

**14. Application security** (TS §10, TS-surface §8)
- OWASP baseline per surface, input validation, output encoding, CSRF/CORS/CSP (web), certificate pinning policy and jailbreak/root policy (mobile), dependency & supply-chain scanning, SAST in CI.

**15. Privacy & compliance** (TS §10)
- Data classification; lawful basis and consent (incl. analytics/tracking); data subject rights (access, deletion, export); data residency; third-party processors; store privacy labels (App Store privacy details, Play Data safety). Regulations come from the vision's constraints (§9).

**16. Abuse & rate limiting** (TS §3)
- Rate limits per endpoint/user, bot/fraud protection where relevant, spam in user-generated content.

## Data

**17. Data storage & ownership [always]** (TS §9)
- Which store(s), ownership per module/service, schema migrations (versioned, backward-compatible with running code), seeds.

**18. Data lifecycle [always: backups]** (TS §9, PF §7)
- Retention and deletion, soft vs hard delete, archival, backups & tested restores (RPO/RTO).

**19. Caching** (TS §9)
- Where (CDN, server, client), invalidation, what must never be cached (personal data on shared caches).

**20. Search** (TS §9)
- DB full-text first; dedicated engine only with a driver.

**21. Files & media** (TS §9)
- Object storage, upload limits, scanning, image processing, signed URLs, CDN.

**22. Multi-tenancy** (TS §9)
- If B2B: isolation model (row, schema, database), tenant context propagation, noisy neighbors.

## Contracts & clients

**23. API style & contract [always if backend + clients]** (TS §3)
- REST/GraphQL/gRPC; single schema source of truth; generated clients; error contract; pagination; idempotency keys for unsafe operations.

**24. API versioning & deployed-client compatibility** (TS §3, release_process §7)
- How long old mobile versions must keep working; additive-only rule; expand → migrate → contract for breaking changes; minimum supported app version and forced update. Agree with release-manager.

**25. Offline & sync** (TS-surface §6)
- Is offline required (vision)? Local storage, conflict resolution, sync triggers, what's read-only offline.

**26. Deep links & universal links** (TS-surface §3)
- Routing scheme shared across web/android/ios, App Links / Universal Links, notification deep links.

## Product-facing

**27. Feature flags & remote config** (TS §12, release_process §5)
- Tool, naming, ownership, lifecycle and cleanup, server- vs client-evaluated, kill switches for risky features.

**28. Product analytics** (TS §13)
- Event taxonomy (naming, properties), single tracking plan location, consent gating, identity stitching across surfaces.

**29. Internationalization & localization** (TS §13)
- Locales at launch, string externalization per surface, formats (dates, numbers, currency), RTL if relevant, translation workflow.

**30. Accessibility** (TS §13, TS-surface)
- Baseline (WCAG AA on web; TalkBack/VoiceOver, dynamic type and font scaling on mobile), testing approach.

**31. Payments & monetization** (TS §3/§10)
- Payment provider, PCI scope minimization, in-app purchases vs external payments (store rules), receipts/entitlements, refunds, taxes.

## Quality & delivery

**32. Test platform & testing strategy [always]** (TS §14, TS-surface §9; strategy by qa-engineer)
- Tools per level and surface (unit, integration, contract, UI/component, e2e, visual, performance, accessibility, security scanning); acceptance-test format and tagging convention for traceability.
- Integrations: contract approach backend ↔ clients, old-client compatibility, third-party testing (sandbox / doubles / recorded responses).
- Test data, CI time budget, PR vs nightly suites, device/browser matrix, flaky handling.

**33. Performance budgets** (TS §11, TS-surface §7)
- API p95, web vitals, app cold start, bundle/binary size, memory.

**34. Resilience** (TS §11)
- Timeouts, retries with backoff and jitter, circuit breakers, graceful degradation, dependency failure modes, idempotency.

**35. Environments, CI/CD & build signing** (PF §1-3; decided with platform-engineer)
- Covered in platform foundations; here, only confirm the architecture doesn't block it.

**36. Cost** (PF §9)
- Expected monthly cost at launch and at the 12-month scale, main cost drivers.

**37. Developer experience** (TS §2/§4)
- Local setup in one command, seed data, codegen, formatting/lint on save, docs for onboarding.
