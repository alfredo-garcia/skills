# Template: Platform Foundations

> **What this is:** how the system runs and is operated: environments, infrastructure as code, CI/CD per surface, build & signing infrastructure, observability implementation, secrets & configuration, backups & disaster recovery, security operations, cost, access. It turns the *what* in `hl_architecture.md` / `tech_standards.md` into the *how and where*.
>
> **Produced by:** `platform-engineer` Mode A (Phase 0.4), from approved tech foundations. Updated via `platform-engineer` Mode B. **Required when `rigor: production`**; for `personal` a short version (§1, §3, §5, §6) is enough.
>
> **Real instance path:** `<docs_root>/platform/platform_foundations.md`. Runbooks in `<docs_root>/platform/runbooks/`, postmortems in `<docs_root>/platform/postmortems/`.

---

## Structure

```markdown
# Platform Foundations: [Product Name]

> Project: `<project_id>`
> Rigor: personal | production
> Status: Draft / Approved (YYYY-MM-DD)
> Derived from: `architecture/hl_architecture.md`, `context/tech_standards.md` (approved YYYY-MM-DD)

## 1. Environments
Which environments exist (local, dev/preview, staging, production), purpose, who deploys,
data in each (never production personal data outside production), promotion path.

## 2. Infrastructure & Provisioning
Cloud/provider accounts, regions, resources per surface (compute, databases, queues, storage,
CDN), infrastructure as code tool and repo location, naming/tagging, how changes are reviewed.

## 3. CI/CD per Surface
| Surface | Triggers | Required checks before merge | Build artifact | Deploy target | Who/what approves |
|---|---|---|---|---|---|
Mobile rows include build signing (keystores, certificates, provisioning profiles), where
secrets live, and how internal/test builds are distributed.

## 3a. Automated Review & Branch Protection
- Automated PR review: where it runs (CI step), what it reads (the project's review checklist and
  `<id>-pr-reviewer` definition), its credentials (secret), and that its result is a required
  status check. Required when `rigor: production`.
- Branch protection on the base branch: required status checks (tests, Enforcement Map blocking
  checks, automated review), no direct pushes, no required human approvals unless a human
  reviewer actually exists.
- How high-risk PRs are held for the user's approval (e.g. a label that blocks merge until the
  user removes it, or merges done only by the user for those PRs).

## 3b. Test Infrastructure
What the test strategy (`quality/test_strategy.md` §6, §8) needs to run: CI runners and
parallelization vs the CI time budget, PR vs nightly pipelines, device farm or
emulator/simulator capacity, ephemeral or shared test environments, test data seeding and
anonymization, third-party sandbox accounts and where their secrets live.

## 4. Observability Implementation
- Logs: pipeline, retention, access.
- Metrics: stack, the golden signals per service, key business metrics.
- Tracing: tool, sampling.
- Crash & error reporting per client surface.
- Dashboards: list and purpose.
- Alerts: what pages someone vs what's a ticket, thresholds, routing, on-call (even if "the
  builder, best effort").

## 5. SLOs & Error Budgets (production)
Per critical user journey: SLI, SLO target (from hl_architecture §2), measurement, what happens
when the budget is burned.

## 6. Secrets & Configuration
Secret store, rotation, who has access; config per environment; remote config for clients.

## 7. Backups & Disaster Recovery
What's backed up, frequency, retention, restore procedure and how often it's tested, RPO/RTO
targets vs reality.

## 8. Security Operations
Access management (least privilege, MFA), dependency/vulnerability scanning, network exposure,
audit logs, incident response contacts.

## 9. Cost
Monthly budget per environment (from vision constraints), alerts on spend, main cost drivers and
how they scale.

## 10. Runbooks Index
| Runbook | When to use | Path |
|---|---|---|

## 11. Deferred & Open Items
What's intentionally not set up yet, with a revisit signal; open questions.
```

## Runbook (inline template)

```markdown
# Runbook: [Situation]
> Project: `<project_id>`
## Symptoms   ## Impact   ## Diagnosis steps   ## Mitigation steps   ## Escalation   ## Verification
```

## Postmortem (inline template)

```markdown
# Postmortem: [Incident] (YYYY-MM-DD)
> Project: `<project_id>`
## Summary   ## Impact (who, how long)   ## Timeline   ## Root cause(s)   ## What went well / badly
## Action items (owner role, due)   — blameless; action items that change standards become ADRs
```
