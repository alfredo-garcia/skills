# Platform Playbook

## Depth by rigor

| Area | personal | production |
|---|---|---|
| Environments | local + production | local, preview/dev, staging, production (drop staging only with a reason) |
| Provisioning | PaaS console or simple config | infrastructure as code, reviewed in PRs |
| CI | lint + tests on PR | per-surface pipelines, required checks, security scans, artifact versioning |
| Observability | platform logs + an error tracker | logs/metrics/traces + crash reporting + dashboards + alert routing |
| SLOs | none | per critical journey, with error budgets |
| Backups | provider default, one restore test | scheduled, retention policy, periodic restore drills, RPO/RTO |
| Security ops | MFA, no secrets in repo | least privilege, secret rotation, dependency/vulnerability scanning, audit logs |
| Cost | rough monthly number | budget per environment + spend alerts |
| Runbooks | none | one per paging alert and per risky manual procedure |

## Per-surface delivery specifics

**Backend / worker**
- Build once, promote the same artifact through environments; configuration via environment, never baked in.
- Zero-downtime deploys (rolling or blue/green); migrations run as a separate, observable step, backward-compatible with the running version.
- Health checks gate traffic; automatic rollback on a failed health check where the platform supports it.

**Web**
- Preview deployments per PR when the host supports them; CDN caching rules; immutable asset hashing.
- Source maps uploaded to error reporting and not publicly served (or access-controlled).
- Environment-specific config injected at build time or runtime (pick one, document it).

**Android**
- Signing: Play App Signing with an upload key; the upload key and passwords live in CI secrets, never in the repo.
- Build variants/flavors per environment; versionCode monotonic and generated in CI.
- Distribution: internal testing track → closed/open testing → production with staged rollout (release-manager decides percentages).
- Upload R8 mapping files to crash reporting.

**iOS**
- Certificates and provisioning profiles managed reproducibly (e.g. a match-style encrypted store, or Xcode Cloud / CI-managed signing). Document who holds the developer account.
- Build numbers generated in CI; TestFlight for internal and external testing.
- Upload dSYMs to crash reporting for every build.
- App Store Connect API keys live in CI secrets.

**Cross-surface**
- One place where every surface's current version per environment is visible.
- The same release/version tag on logs, traces and crashes across surfaces.

## Observability implementation checklist (production)
- Every service emits golden signals; every client surface reports crashes and key performance metrics.
- Trace context flows client → API → downstream calls.
- Dashboards: service health, critical journeys, business KPIs from the vision, release health (crash-free rate per app version).
- Alerts: symptom-based (SLO burn, error rate, latency), not just resource-based; each paging alert has a runbook.

## Questions worth asking
- Who gets woken up, if anyone? If nobody, design for that: fewer pages, safer defaults, auto-rollback.
- What's the most expensive thing at 10x scale?
- How long would a full restore take today, and has anyone tried it?
