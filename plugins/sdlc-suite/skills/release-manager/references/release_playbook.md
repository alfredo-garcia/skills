# Release Playbook

## Versioning defaults (propose, don't impose)
- **API:** the contract version changes only on breaking changes (prefer additive changes and no version bumps); deploys identified by build ID/commit.
- **Web:** continuous deploys, identified by commit or date-based version.
- **Android:** `versionName` = semver (user-visible), `versionCode` = monotonic integer generated in CI.
- **iOS:** `CFBundleShortVersionString` = semver (user-visible), `CFBundleVersion` = monotonic build number from CI.
- **Release ID** for records: a calendar version (e.g. `2026.11.1`) works well across surfaces; per-surface versions are listed inside.

## Strategy
- Trunk-based with short-lived feature branches (matching `branch_pattern`) plus feature flags is the default. Use release branches mainly for mobile trains or when a stabilization period is needed.
- Tag every release per surface; tags trigger store-bound builds where the platform supports it.

## Mobile store specifics
- **Google Play:** internal testing → closed/open testing → production with staged rollout (e.g. 1% → 5% → 20% → 50% → 100%); a rollout can be halted, but a released binary can't be recalled, only superseded. Keep the Data safety form consistent with real data collection.
- **Apple App Store:** TestFlight (internal, then external testing, which may need beta review) → App Review → release (manual or automatic) with an optional phased release over several days for automatic updates; a phased release can be paused. Keep privacy details and the privacy manifest consistent.
- Plan for review lead times and rejections. Never schedule a coordinated launch for the same day a binary is submitted.
- **Minimum supported version:** a server-driven check that can show an optional or forced update; define the policy (e.g. force only for security or broken compatibility).

## Cross-surface coordination
1. Ship backend changes first, additive only.
2. Ship clients that use them, behind flags if the backend isn't fully rolled out.
3. Turn flags on progressively.
4. Remove the old paths only after the oldest supported app version no longer needs them (contract phase).

## Go/No-Go quick checklist
- Scope frozen, every feature merged (and documented, for production).
- CI green on every surface; builds signed and on the right tracks.
- Platform readiness check passed.
- Migrations reviewed (backward-compatible, with a rollback/forward plan).
- Flags configured per environment.
- Rollback per surface verified; irreversible parts acknowledged.
- Release notes approved in every required language.
- Monitoring window and owner defined.

## Release notes
- Written for the persona, about outcomes ("You can now share lists with your family"), not implementation details.
- One source (the record), adapted per channel (store text limits, in-app, web).
- Never include internal feature IDs or ticket references.
