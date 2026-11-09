# Template: Release Process

> **What this is:** how changes reach users safely across every surface: versioning, branching, release cadence, promotion through environments, feature-flag rollout policy, app store submission and staged rollouts, mobile-backend compatibility, go/no-go, rollback and hotfix, and release notes.
>
> **Produced by:** `release-manager` Mode A (Phase 0.5), from approved tech and platform foundations. **Required when `rigor: production`.**
>
> **Real instance path:** `<docs_root>/release/release_process.md`. Each release gets a record: `<docs_root>/release/releases/<release-id>.md` (`release_record_template.md`).

---

## Structure

```markdown
# Release Process: [Product Name]

> Project: `<project_id>`
> Status: Draft / Approved (YYYY-MM-DD)
> Derived from: tech_standards.md §3/§12, platform_foundations.md §1/§3

## 1. Versioning per Surface
| Surface | Scheme | Where it's set | Example |
|---|---|---|---|
| backend / API | e.g. semver for API contract; deploy IDs for builds | | |
| web | | | |
| android | versionName (semver) + versionCode (monotonic) | | |
| ios | CFBundleShortVersionString + CFBundleVersion | | |
Release IDs used in release records (e.g. `2026.11.1` or per-surface versions).

## 2. Branching & Release Strategy
Trunk-based or release branches, tagging, how hotfix branches work. Must match SDLC.md
`base_branch`, `branch_pattern`, `commit_tag`.

## 3. Cadence & Release Train
Continuous for backend/web? Fixed train for mobile? Code freeze rules.

## 4. Promotion Path
Environment sequence and what must pass at each step (links to platform_foundations §3).

## 5. Feature Flags & Progressive Delivery
When a feature must ship behind a flag, rollout stages (internal → % → all), success/abort
criteria, flag cleanup deadline.

## 6. Mobile Store Process (if android/ios)
Internal/beta testing tracks (Play internal/closed testing, TestFlight), review lead times,
staged rollout percentages and halt criteria, store listing/privacy labels/permissions changes,
minimum supported app version and forced-update mechanism.

## 7. Cross-Surface Compatibility
Deploy ordering (e.g. backend first, additive changes only), API compatibility window for old
mobile versions, how breaking changes are scheduled (expand → migrate → contract).

## 8. Go / No-Go Checklist
Scope frozen; features merged, verified (qa-engineer) & documented; regression suite and critical-journey tests green against the release candidate; platform readiness check passed
(platform-engineer); migrations reviewed; rollback path verified; release notes ready; flags set.

## 9. Rollback & Hotfix
Per surface: how to roll back (and what can't be rolled back: mobile binaries, destructive
migrations), hotfix flow and approvals. Every hotfix starts with a test that reproduces the bug.

## 10. Release Notes & Communication
User-facing notes (tone, languages, where published: stores, in-app, web), internal notes,
who's informed.

## 11. Post-Release
Monitoring window, metrics watched, closing the record, follow-ups.
```
