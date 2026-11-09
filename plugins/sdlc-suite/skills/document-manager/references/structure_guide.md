# Structure Guide

This file covers the **operational decisions** this skill makes while maintaining the Master Functional Documentation — when to split a domain, how to assign a feature to one, how to handle an approved deviation. Read it before Init mode, before proposing a new domain, and before proposing a structural split.

The **structural facts themselves** — file layout, the entry-file and domain-file section-by-section shape, the ID scheme, source/provenance conventions, what counts as a screen vs. a modal/tab/wizard step, the exact split thresholds, the functionally-significant-component rule, the shared-components mechanism, shared data entities, navigation structure, the screen & flow index, cross-cutting concepts, and platform divergence notation — are all defined in one place now: `TEMPLATES/master_functional_spec_template.md`. That file is the single source of truth for "what does this document contain and how is it shaped" — this file is only about the judgment calls made on top of that structure. If you find yourself needing a structural fact (an ID format, a threshold number, which section something belongs in), it's there, not here.

## Why structure this way at all

The user's product is built on a design system, and may have several surfaces (web, Android, iOS — per `SDLC.md` `surfaces`) that sometimes diverge in features, not just layout. Left unstructured, a functional doc for a product like this tends to fail in one of two directions: it either duplicates the design system's visual specs inside every screen description (drifts out of sync the moment the design system changes), or it duplicates itself across web/mobile and across domains (the same flow described three slightly-different ways in three files). The structure defined in the shared template exists to prevent both.

## When to split a domain out

The exact thresholds are in the template (§7). This skill's job is the judgment call around them: this is a judgment call, not a hard trigger — if you're close to the threshold and mid-review anyway, it's reasonable to just ask the user if they want to split now rather than next time. This applies equally to splitting a domain out, splitting the Screen & Flow Index into `_screen-index.md`, and splitting `_shared-components.md` / `_data-dictionary.md` out of the entry file. **Always propose the split explicitly and get confirmation before moving content** (see `SKILL.md` Step 6) — it changes file paths, so every link to the moved content must be updated in the same approved change.

## Domain assignment

When a new feature arrives, match it against the Domain Map in `functional-spec.md`:
- **Clear match** → use that domain, no need to ask.
- **Genuinely new territory** → propose a new domain name + one-line description, confirm before creating the file.
- **Ambiguous between two existing domains** → ask; don't guess. A feature landing in the wrong domain tends to accumulate cross-links that point at the wrong file, which is more work to unwind later than asking once up front.

## New-temporary components (not yet in the design system)

The design/flow document's component legend distinguishes components reused from `ui_kit_registry.md` from new ones the feature introduced that aren't yet in the design system — however that distinction is flagged in this particular document (a naming prefix, an explicit note, a separate list; see `references/input_contract.md`). If a new, not-yet-formalized component is functionally significant, give it a master-doc entry like any other, following the template's guidance (§3) for how its "Design system reference" field should read in that case. Once the design system team formalizes it and it gets a real entry in `ui_kit_registry.md`, update this field to a normal reference — that update itself is a small `[MODIFIED]` in some future redline, not something to backfill silently.

## Handling approved PRD deviations

When the UX Flow doc's §6 (Deviations from PRD, Approved) shows the shipped behavior diverged from the original PRD, the master doc reflects what shipped — that's current truth (see the template's §13). Don't re-litigate the deviation in the domain file itself; a one-line note plus a pointer to the feature's changelog (which has the full "PRD said / we shipped instead / why" table) is enough. The domain file describes the product as it is, not the history of how it got there.
