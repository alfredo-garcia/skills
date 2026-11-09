# Template: Tech Standards (per surface)

> **What this is:** the binding rules specific to one surface (backend, web, android, ios, cli, worker). It complements, and never contradicts, the core `tech_standards.md`. Read by every skill and agent working on that surface, and by the surface's subagent if one exists.
>
> **Produced by:** `tech-lead` Mode A, after evaluating that surface's options with its lens (`tech-lead/references/surfaces/<surface>.md`). Changed through ADRs.
>
> **Real instance path:** `<docs_root>/context/tech_standards/<surface>.md`. Required for every surface when `rigor: production`, and when a project has 2+ surfaces.

---

## Structure

```markdown
# Tech Standards — [surface]: [Product Name]

> Project: `<project_id>`
> Surface: backend | web | android | ios | cli | worker
> Status: Draft / Approved (YYYY-MM-DD)
> Core rules: `../tech_standards.md` (wins on contradiction)

## 1. Options Evaluated
The real alternatives considered for this surface (e.g. native Kotlin/Compose vs a cross-platform
framework), the decision, and the ADR that records it.

## 2. Stack & Approved Libraries
Language, framework, minimum OS/runtime/browser versions, libraries per purpose (one per purpose).
**Not allowed / avoid**, with reasons.

## 3. Project Structure & Architecture Pattern
Folder/module structure, layering or pattern (e.g. MVVM, clean architecture, modular monolith),
dependency injection, navigation/routing.

## 4. Coding Conventions
Formatting/lint tools and configs, naming, error handling, concurrency model.

## 5. How the Core Rules Apply Here
Concrete implementation of each core cross-cutting rule on this surface: logging, observability
(crash reporting, metrics, tracing), events, notifications, auth/session storage, configuration &
flags, i18n, accessibility, analytics. One line each, pointing to the library/mechanism used.

## 6. Data, State & Offline
Local storage, caching, state management, offline/sync behavior (client surfaces), persistence
& migrations (backend/worker).

## 7. Performance Budgets
Surface-specific targets (e.g. cold start, bundle size, p95 latency, memory).

## 8. Security (surface-specific)
E.g. keychain/keystore use, certificate pinning policy, CSP, secure cookies, root/jailbreak policy.

## 9. Testing
Options evaluated and chosen (per the tech-lead surface lens), one tool per level: unit,
integration, UI/component, end-to-end, visual regression where used; how tests are tagged with
criterion IDs here; test doubles and fixtures; device / OS / browser matrix (PR vs release);
what can only run on real devices or real browsers; minimum expectations per change.

## 10. Enforcement
The surface-specific rows of core §17 (Enforcement Map) live there, not here; this section only
lists surface tools' config files (lint, dependency rules, budgets) so agents know where they are.

## 11. Build & Distribution Inputs
What platform-engineer and release-manager need from code: build variants/flavors, environment
config injection, signing requirements, versioning fields (versionName/versionCode,
CFBundleShortVersionString/CFBundleVersion, package version).
```
