# Independent Review Checklist

The reviewer reads the PR diff and description, the task row in the implementation plan, and the referenced specs. It never trusts the author's summary as evidence.

## Scope
- The PR does one task; size within budget (or the reason is in the plan).
- No unrelated changes, no drive-by refactors outside the task.

## Requirements
- Every FR/AC the task claims is actually implemented, as the PRD states it (including negative paths and third-party failure behavior).
- No behavior beyond the PRD (scope creep) and no silent deviation.

## UX (if UI)
- Matches the UX Flow: components used are the ones it lists (registry names, or the announced `Tmp` ones), every state is handled, conditional rendering as specified.
- No new component that wasn't announced.

## Tests
- The task's tests exist, are tagged with the feature and AC IDs, and pass.
- No test deleted, skipped, or weakened (assertions removed, timeouts inflated, expectations loosened) compared with the approved test plan.
- New logic has tests at the right level.

## Standards
- The review-only rules from tech_standards §17 (Enforcement Map), one by one.
- Definition of Done (§15): observability added (logs/metrics/traces per the standards), analytics events, flags, migrations safe.
- No dependency outside the approved lists; no secrets.

## Compatibility & safety
- Works with the oldest supported client versions (API additive or versioned).
- Migrations are backward-compatible with the running code.
- Behind a flag if the slice isn't user-ready.

## High-risk changes (flag them; they need the user's explicit approval)
A PR is high-risk if it touches any of:
- data migrations or anything that deletes or rewrites stored data;
- authentication, sessions, authorization or permissions;
- payments, billing or money amounts;
- collection, storage or sharing of personal data;
- changes that break or could break deployed client versions (API, events, deep links);
- infrastructure, secrets, environment configuration;
- the standards, the Enforcement Map, CI configuration, the checks themselves, or the reviewers' definitions.
Say which item applies. When in doubt, flag it.

## Output
Findings as blocker / should-fix / nit, each with file:line and the requirement, rule or plan item it refers to. Then the risk classification (normal / high, with the reason). "Approved" only with zero blockers. A high-risk PR is "Approved, pending the user's approval", never merged on the review alone.
