# Template: Release Record

> One per release. Created by `release-manager` Mode B, closed in Mode C. Path: `<docs_root>/release/releases/<release-id>.md`.

```markdown
# Release <release-id>

> Project: `<project_id>`
> Status: Planned / In rollout / Released (YYYY-MM-DD) / Rolled back / Halted
> Surfaces: … with version per surface
> Milestone: [GitHub milestone for this release, when work_tracker: github]

## Scope
| Feature (qualified ID) | Surfaces | Merged | Verified (test plan) | Documented (changelog) | Behind flag |
|---|---|---|---|---|---|

## Dependencies & Ordering
Deploy order, API compatibility notes, migrations.

## Readiness
- Platform readiness (platform-engineer Mode C): pass/fail + date
- Regression and critical-journey suites against the release candidate (qa-engineer): pass/fail + date
- Go/No-Go: decision, date, by whom

## Rollout Plan
Stages, percentages, monitoring signals, abort criteria per surface.

## Rollback Plan

## Release Notes
User-facing (per language/channel) and internal.

## Outcome
What happened during rollout, incidents (link postmortems), follow-ups.
```
