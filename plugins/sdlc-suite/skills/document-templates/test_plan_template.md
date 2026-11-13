# Template: Feature Test Plan

> **What this is:** for one feature, how every acceptance criterion, requirement, edge case, UI state and integration behavior in its PRD (and UX Flow) will be verified, at which level and on which surface, and the **traceability matrix** that proves coverage before merge.
>
> **Produced by:** `qa-engineer` Mode B, after the PRD is approved (and technically reviewed when `rigor: production`), updated once the UX Flow is approved. Its status column is filled in by Mode D before merge.
>
> **Real instance path:** `<features_root>/<id>_<slug>_test_plan.md`, same ID and slug as the feature's PRD.

---

## Lite variant (`rigor: personal`, only if the user asks for a test plan)

```markdown
# Test Plan: [Feature Name]
> Project: `<project_id>` · Feature: `<project_id>/<id>` · Variant: lite · Status: Draft / Approved / Verified (YYYY-MM-DD)

| AC / FR | Test (file › name) | Level | Status (pending / failing / passing) |
|---|---|---|---|
```
Nothing else. Uncovered ACs get a one-line reason.

## Structure

```markdown
# Test Plan: [Feature Name]

> Project: `<project_id>`
> Feature: `<project_id>/<id>`
> Source PRD: `<id>_<slug>_prd.md` · UX Flow: `<id>_<slug>_ux_flow.md` (or n/a)
> Status: Draft / Approved (YYYY-MM-DD) / Verified (YYYY-MM-DD)

## 1. Scope
Surfaces touched, what's in and out of scope for testing, risks that drive extra testing.

## 2. Testability Findings
Acceptance criteria or requirements that weren't testable as written, what was asked of
product-manager, and the resolution. Empty once resolved.

## 3. Test Cases
| Test ID | Covers (AC / FR / edge / NFR / state) | Surface | Level | Type (positive / negative / boundary / failure) | Data | Automated? |
|---|---|---|---|---|---|---|
Test IDs: `T-<id>-<n>`. "Automated? no" requires a reason.

## 4. Integration & Failure Behavior
Per integration touched: what's tested (contract, sandbox, double), failure modes covered,
compatibility with deployed client versions.

## 5. Test Data & Environment Needs
Fixtures, seed data, accounts, flags, environment or device needs (routed to platform-engineer if new).

## 6. Traceability Matrix
| Requirement | Test IDs | Status (pending / failing / passing / manual-pass) |
|---|---|---|
Every AC-n and FR-n of the PRD appears here. A feature is mergeable only when every row is
passing or manual-pass (production).

## 7. Verification Record
Date, commit/PR, suites run, results, anything quarantined (with ticket), verdict.
```
