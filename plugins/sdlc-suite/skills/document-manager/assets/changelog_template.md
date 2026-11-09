# Changelog: [Feature Name]

> Project: `<project_id>`
> Merged: [PR / commit hash into <base_branch>, or "confirmed by user on <date>"]
> Breaking: no   <!-- shared projects only: yes | no. Keep this exact line format, the script reads it -->
> Consumers affected: n/a   <!-- shared projects only, when Breaking: yes: project_ids + what each must do -->
> Source PRD: `<feature-id>_<feature-slug>_prd.md`
> Source UX Flow: `<feature-id>_<feature-slug>_ux_flow.md`
> Master doc file(s) touched: [list, e.g. `docs/functional/domains/checkout.md`, `docs/functional-spec.md` (Domain Map)]
> Date applied: YYYY-MM-DD
> Test plan: `<id>_<slug>_test_plan.md` (verification: YYYY-MM-DD) — or n/a
> Reviewed and approved by: [user, or "pending" if not yet confirmed]

## Summary

One or two sentences: what this feature changed about the product's documented functionality.

## Added

- **[ID + name]** — one-line description of what's new. *(State "None" if nothing was added.)*

## Modified

- **[ID + name]** — what changed, before → after in one line, and why (link to the PRD section or UX Flow deviation that drove it). *(State "None" if nothing was modified.)*

## Removed / Deprecated

- **[ID + name]** — what was removed and why. *(State "None" explicitly — don't omit this section.)*

## Deviations from PRD Carried Into the Docs

Anything from the UX Flow doc's "Deviations from PRD (Approved)" section that is now reflected as current truth in the master doc. Use the same "PRD said / we shipped instead / why" shape so the reasoning travels with the change. *(State "None" if the UX Flow doc had no deviations.)*

| PRD said | We documented instead | Why / who approved |
|---|---|---|

## Open Questions / Follow-Ups

Anything still unresolved from the PRD or UX Flow doc's own open-items sections that a future feature or documentation pass should address. *(State "None" if there aren't any.)*
