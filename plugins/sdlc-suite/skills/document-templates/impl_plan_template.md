# Template: Implementation Plan

> **What this is:** how one approved feature gets built: thin vertical slices, small tasks per surface, each tied to the requirements it delivers and the tests that prove it, in a safe order, plus the record of every PR's independent review. It's the bridge between the specs (PRD, UX Flow, test plan) and the code, and the place where you can see progress without reading code.
>
> **Produced by:** `engineering-lead` Mode A, after the PRD, UX Flow (if UI) and test plan are approved and the acceptance tests are written (qa-engineer Mode C). Updated by Modes B and C as work progresses.
>
> **Real instance path:** `<features_root>/<id>_<slug>_impl_plan.md`.

---

## Structure

```markdown
# Implementation Plan: [Feature Name]

> Project: `<project_id>`
> Feature: `<project_id>/<id>`
> Sources: `<id>_<slug>_prd.md` · `<id>_<slug>_ux_flow.md` (or n/a) · `<id>_<slug>_test_plan.md`
> Status: Draft / Approved (YYYY-MM-DD) / In progress / Done (YYYY-MM-DD)

## 1. Approach
Two or three sentences: how the feature is built, which modules/surfaces change, and the main
technical risk.

## 2. Slices
Thin vertical slices, each one shippable on its own (behind a flag if not yet user-ready).
| Slice | User-visible outcome | ACs delivered | Flag | Surfaces |
|---|---|---|---|---|

## 3. Tasks
One task = one small PR (default: under ~400 changed lines excluding generated code and tests;
bigger needs a reason).
| Task | Slice / Story | Surface | What changes (modules/files) | FR / AC | Tests that prove it | Risk (normal/high: why) | Depends on | Assignee (agent) | Issue |
|---|---|---|---|---|---|---|---|---|---|
Status is **not** kept here when `work_tracker: github`: it lives in each task's issue and its PR
(`Closes #n`). With `work_tracker: none`, add a Status column (todo / in progress / in review /
changes requested / merged) and a PR column.

## 4. Order & Compatibility
Deploy and merge order across surfaces (backend first, additive), migrations (expand → migrate →
contract), compatibility with deployed clients, flags to decouple deploy from release.

## 5. Needs from Other Roles
Platform (new infra, secrets, CI), release (flags, coordinated rollout), standards (ADR needed?).
Each with its status.

## 6. Risks & Mitigations

## 7. Review Record
| PR | Task | Reviewers (pr-reviewer / CI review / others) | Result (approved / changes requested) | Blockers found | Risk | User approval (high-risk only: date) | Date |
|---|---|---|---|---|---|---|---|

## 8. Deviations
Anything implemented differently from the PRD / UX Flow / test plan, with who approved it.
Unapproved deviations are not allowed; they're stopped and routed instead.
```
