# Template: Shared Contract

> **What this is:** the public face of a `type: shared` project, and the only document (together with any other files listed in its `public_docs`) that consuming apps are allowed to read. It describes what consumers can rely on: modules, functions, components, configuration, behavior and guarantees. It doesn't describe internals. It's the shared project's equivalent of a library's API reference.
>
> **Produced and maintained by:** `document-manager` in the shared project, **after merge**, like the master functional doc for an app. It's created on the first merged feature, with its overview taken from the Shared Charter.
>
> **Consumed by:** every skill working in a consuming app (read-only), exactly like the documentation of a third-party library.
>
> **Real instance path:** `<docs_root>/contract.md` (must be listed in `public_docs` in the shared project's `SDLC.md`). A UI kit typically also exposes `ui_standards.md` and `ui_kit_registry.md` through `public_docs`.

---

## Structure

```markdown
# Contract: [Name]

> Project: `<project_id>`
> Type: shared — consumers use the current state of the repo (no versions)
> Last updated: YYYY-MM-DD (from changelog `<id>_<slug>_changelog.md`)

## 1. Overview
What it provides and when to use it (from the Shared Charter §1-§3).

## 2. How to Consume
Import path(s) / package name inside the repo, required setup or configuration, environment
variables, and prerequisites.

## 3. Public Surface
One entry per public module, function, hook, component or endpoint:
### [Name]
- Kind: function / component / hook / endpoint / config
- Signature / props / payload: the exact contract
- Behavior & guarantees: what consumers can rely on, including errors and edge cases
- Stability: stable / evolving / deprecated (→ replacement, and planned removal)
- Platforms: web / mobile / both (only when relevant)

## 4. Cross-Cutting Behavior
Behavior that spans the surface: auth/session semantics, logging format, theming, i18n, error
conventions.

## 5. Not Public
Explicitly internal areas that consumers must not import or depend on.

## 6. Breaking Change History
| Date | Changelog | What broke | What consumers must do |
|---|---|---|---|
```

## Rules
- Only public surface. If it isn't here (or in another `public_docs` file), consumers may not use it.
- Merge, don't append: the contract always shows the current state. History lives in the changelogs and the §6 table.
