# Template: Test Strategy

> **What this is:** the project's binding testing approach: what gets tested, at which level, on which surface, how acceptance criteria become executable tests, how integrations are tested, what blocks a merge or a release, and how regressions and flaky tests are handled. It turns the test platform chosen by `tech-lead` (core `tech_standards.md` §14 + each surface file §9) into a working strategy.
>
> **Produced by:** `qa-engineer` Mode A (Phase 0.2b), after tech foundations are approved. **Required when `rigor: production`**; a short version (§1, §2, §4, §8) is enough for `personal`.
>
> **Real instance path:** `<docs_root>/quality/test_strategy.md`.

---

## Structure

```markdown
# Test Strategy: [Product Name]

> Project: `<project_id>`
> Rigor: personal | production
> Status: Draft / Approved (YYYY-MM-DD)
> Built on: tech_standards.md §14 + tech_standards/<surface>.md §9 (approved YYYY-MM-DD)

## 1. Quality Goals
What "good enough to ship" means for this product, derived from the vision (§10 availability,
data sensitivity) and hl_architecture §2 quality targets. Which failures are unacceptable.

## 2. Test Levels per Surface
| Surface | Unit | Integration | Contract | UI / component | End-to-end | Visual | Non-functional |
|---|---|---|---|---|---|---|---|
Each cell: tool (from tech_standards), scope, and what it must cover, or "n/a: reason".

## 3. Acceptance Tests
- Format (executable specs or tagged tests, as decided in tech_standards §14).
- How each PRD acceptance criterion (`AC-n`) becomes at least one automated test, at which level.
- Tagging convention linking tests to `<project_id>/<feature-id>` + `AC-n` / `FR-n`.
- When an AC may be verified manually (only with a reason, recorded in the feature's test plan).

## 4. Critical Journeys
The end-to-end journeys that must always pass across surfaces (from the vision's core
job-to-be-done and hl_architecture §7). Kept short; everything else is tested at lower levels.

## 5. Integrations
- Backend ↔ clients: contract approach (schema-based or consumer-driven), where it runs,
  compatibility checks against the oldest supported app versions (release_process §7).
- Third parties: per provider, sandbox / test double / recorded responses, which failure modes
  are tested (timeouts, errors, malformed responses), and how often the real sandbox is exercised.

## 6. Test Data & Environments
Fixtures and factories, seed data, anonymization (never production personal data outside
production), ephemeral or shared test environments (with platform-engineer), device and browser
matrix per surface.

## 7. Non-Functional Testing
Performance (budgets from tech_standards §11), accessibility, security scanning, resilience —
what's automated, on which cadence.

## 8. Gates
| Gate | Required checks | Blocks |
|---|---|---|
| Pull request | | merge |
| Pre-release | | go/no-go |
CI time budget per pipeline, and what runs per PR vs nightly.

## 9. Regressions & Flaky Tests
- Every bug fix starts with a failing test that reproduces it.
- Flaky policy: detection, quarantine (time-boxed, tracked), and ownership; a quarantined test
  never silently stays skipped.
- Never delete, skip or weaken a failing test without explicit user approval, recorded.

## 10. Exploratory & Manual Testing
When it's done (e.g. before major releases), by whom, and how findings become tests.

## 11. Metrics & Reporting
Requirement coverage (ACs with passing tests), escaped defects, flaky rate, suite duration.

## 12. Deferred & Open Items
```
