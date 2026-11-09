# Fitness Functions: Standards as Automated Checks (Mode E)

A fitness function is an automated check that fails when the code drifts from an architectural rule. In a large codebase written mostly by agents, rules that only live in prose erode one change at a time. Rules that a machine checks on every PR don't.

## Principles
1. **Automate what a machine can judge;** send the rest to the independent reviewer (engineering-lead Mode C) as review-only rules. Nothing is "enforced by memory".
2. **Highest drift risk first:** module boundaries, the API contract, forbidden dependencies, UI-kit usage, logging of personal data.
3. **Fast or it gets skipped:** PR checks fit in the CI time budget agreed with platform-engineer and qa-engineer; slow checks run nightly and report.
4. **Rules point to checks and checks point to rules:** every §17 row names its config path, and every config file references the rule (section) it enforces, in a comment.
5. **Use the stack's own tools,** chosen like any tool (one per purpose, ADR when there are real alternatives). The tool families below are examples to evaluate, not mandates.
6. **Start as warning, then block:** a new check runs in report mode until the existing violations are fixed or explicitly baselined, then it becomes blocking. A baseline is a tracked list with a deadline, never a permanent exemption.

## Catalog: rule families and typical checks

| Rule family | What the check verifies | Typical tool families (evaluate per stack) |
|---|---|---|
| Module boundaries & layering | Allowed imports between modules/layers; no cycles; domain doesn't import infrastructure | Dependency-rule tools (e.g. dependency-cruiser, import-linter, ArchUnit/Konsist, depguard, Swift package boundaries) |
| Approved dependencies only | Every third-party dependency is in the approved lists (core §1, surface §2); nothing on the "not allowed" list | A dependency allowlist check over manifests/lockfiles (often a small script) |
| API contract | No breaking change without a version/ADR; implementation matches the schema; clients generated from the schema are up to date | Schema diff tools (e.g. OpenAPI diff), schema validation in tests, "generated code is fresh" check |
| Coding conventions | Formatting, naming, forbidden constructs | The surface's formatter and linter, plus custom rules |
| Logging & privacy | No raw print/console logging; structured logger only; no known personal-data fields in log calls | Custom lint rules; log-schema tests |
| Observability | Required fields/propagation present (e.g. request ID middleware registered) | Tests or custom lint rules |
| UI kit & design tokens | Only kit components are used; no direct imports of the underlying library outside the kit; no hardcoded colors/spacing instead of tokens | Custom lint rules; stylelint-like token rules; registry ↔ code check |
| Security | No secrets in the repo; dependency vulnerabilities; risky APIs | Secret scanners, dependency audit, SAST |
| Performance budgets | Bundle/binary size, startup time, API latency on a benchmark | Size-limit-style checks, benchmark jobs (nightly) |
| Migrations | Backward-compatible with the running version (no drop/rename without the expand-contract steps) | Migration linting, review-only for complex cases |
| Tests & traceability | Every acceptance criterion of the feature has a tagged test; no `skip`/`only` left; no test removed without approval | A small script over test tags (with qa-engineer); lint rules for skip/only |
| Docs coherence | Each feature in the PR has an approved PRD; UI changes have a UX Flow or exemption | Checks wired in SDLC-04 (mechanical gates) |

## Mode E steps (summary; full flow in SKILL.md)
1. List every rule in core and surface standards; classify each as automatable / review-only / manual.
2. For automatable rules: propose the check (tool family, where it runs, blocking or not), highest drift risk first.
3. Write §17 (Enforcement Map) with the user's approval.
4. Implement the configs in the repo (Claude Code), each referencing its rule; ask platform-engineer to wire them into CI (report mode first).
5. Baseline existing violations (tracked, with a deadline), then switch to blocking.
6. Keep it alive: every ADR that changes a rule updates §17; code-health audits drift later.

## Rigor
- `personal`: formatter + linter + approved-dependency check, blocking on PR. Everything else is optional.
- `production`: every rule classified; the families in bold risk (boundaries, approved dependencies, API contract, logging & privacy, UI kit, security, tests & traceability) are active and blocking before the first feature is implemented.
