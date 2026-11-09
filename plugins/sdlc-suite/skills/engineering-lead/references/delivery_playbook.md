# Delivery Playbook

## Vertical slices
A slice delivers a thin piece of user value through every layer it needs (UI → API → data), so it can be tested and, if needed, released on its own. Typical first slice: the happy path for one persona, with the simplest data; later slices add edge cases, other surfaces, and polish. Enabling slices (a migration, a new endpoint not yet used) ship behind a flag or are unused-but-safe.

Avoid horizontal plans ("all the backend, then all the web, then all the apps"): integration surprises appear late, and nothing is shippable until the end.

## Task sizing
- One task = one PR = one reviewable idea.
- Default budget: under ~400 changed lines excluding generated code, lockfiles and tests. Bigger needs a reason in the plan (e.g. a mechanical rename).
- One surface per task where possible; cross-surface changes are split and ordered.
- Each task names its FR/ACs and the tests that prove it. A task with no test to prove it is either refactoring (still covered by existing tests) or a planning gap.

## Ordering for safety
1. Schema/data: expand (add columns/tables, nullable or defaulted).
2. Backend: new behavior, additive API changes, behind flags if user-visible.
3. Clients: consume the new API; old clients keep working.
4. Data migration/backfill if needed.
5. Contract: remove old paths only when the oldest supported client no longer needs them (release_process §7).

## Working with subagents
- Implementer subagents per surface (if they exist) get one task at a time, with the task row, the relevant spec excerpts' paths, and the tests to make pass.
- Reviewer subagents never implement; implementers never review.
- If no subagents exist, the main session implements and a fresh context reviews (Mode C).

## When to stop and route
Stop the task (not necessarily the whole feature) when: the spec is ambiguous or contradicts itself; a test seems wrong; a new dependency or technology seems needed; the change would break deployed clients; new infrastructure or secrets are needed; the UX Flow doesn't cover a state the code must handle. Record it in §5 or §8 of the plan and name the owning role.
