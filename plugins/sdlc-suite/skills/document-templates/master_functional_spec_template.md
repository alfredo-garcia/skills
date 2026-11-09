# Template: Master Functional Documentation

> **What this is:** the canonical, always-current description of what the product does and how — for both web and mobile. Anyone (person or AI agent) should be able to read this document alone and understand the product's functional behavior, with zero other context.
>
> **What this is not:** a visual/design-system spec. Colors, spacing, typography, component props, and variants live in `ui_standards.md` and `ui_kit_registry.md` and are only ever referenced here by name or link — never restated. If you catch yourself writing a hex code, a px value, or a prop name into this document, stop; it belongs in one of those two files instead.
>
> **Produced/maintained by:** the `document-manager` skill. Ongoing updates come from a requirements doc + a design/flow doc for each feature (see that skill's `references/input_contract.md` for what those inputs must contain). The *initial* version of this document, for an existing product with no such doc pairs yet, is instead bootstrapped by reverse-engineering the codebase, screenshots, and demos — see §5 (Source & Provenance Conventions) for how that content is tagged differently from feature-driven content, so the two never get silently confused later.
>
> **Consumed by:** the `product-manager` skill (cross-checks new feature ideas against this before drafting), the `ux-designer` skill (reads it for context on existing product behavior), and `document-manager` itself on every subsequent update.
>
> **Real instance lives at:** `<docs_root>/functional-spec.md` (see `project_context_protocol.md` §3) as the permanent entry point, plus optional split-out files under `<docs_root>/functional/domains/`, `<docs_root>/functional/_global.md`, `_shared-components.md`, `_data-dictionary.md`, and `_screen-index.md` once the product grows (see §7 below).


> **Surface notation:** `Platform:` fields use the project's UI surfaces from `SDLC.md` (`surfaces`): `Web`, `Android`, `iOS`, `Mobile` (= Android and iOS behaving identically) or `All`. Only surfaces the project targets may appear.

---

## 1. File Layout

```
docs/
  functional-spec.md              <- entry point. Always exists, even if everything still lives here inline.
  functional/
    domains/
      <domain-slug>.md            <- one per domain, created only once a domain earns its own file
    _global.md                    <- cross-cutting concepts (roles, entitlements, product-wide business rules, global system behaviors)
    _shared-components.md         <- functionally-significant components used across 2+ domains
    _data-dictionary.md           <- shared entities/data concepts referenced across 2+ domains
    _screen-index.md              <- product-wide flat index of every screen/flow, split out of the entry file once it grows large
  changelog/
    <feature-id>_<feature-slug>_changelog.md <- one per feature update (see document-manager's assets/changelog_template.md)
```

`docs/functional-spec.md` is the default filename because it's a discoverable, conventional name other tooling in the project may already look for. It must **never stop existing or move**, even after every domain has been split into its own file — at that point it becomes a map (Domain Map, Navigation Structure, Screen & Flow Index, glossary, cross-cutting concepts, links) rather than the whole document, but anything that expects to find "the master doc" at this path must keep finding it there.

**When a single file is enough:** start with everything inline in `functional-spec.md`, using the domain structure from §3 below repeated under `##` headers, one per domain. Don't create the `functional/` folder preemptively — an empty scaffold with one domain in it is harder to navigate than one well-organized file. Same logic applies to the Screen & Flow Index (§2, entry file §5): skip it while there's only one or two domains and everything's still inline — it earns its keep once scanning past several domain files to find one screen gets annoying.

---

## 2. Entry File Structure (`functional-spec.md`)

This file always exists and always has this shape, whether or not any domains have been split out yet.

```markdown
# [Product Name] — Master Functional Documentation

> Project: `<project_id>`

> Entry point. While the product is small, this file may contain everything inline, using the
> domain structure (§3) repeated under `##` headers. As domains grow, they move to their own
> files under `docs/functional/domains/` — this file becomes a map plus the shared/cross-cutting
> reference point. Always start here regardless of how much has been split out.

## 1. Product Overview

[1-2 paragraphs: what the product is, who it's for, web vs. mobile at a glance. Source it from the
approved Product Vision (`product/product_vision.md` §2-§4), never inferred from a single feature. Do not restate
visual/design-system details here — that's ui_standards.md's job. This section answers "what is
this product," not "what does it look like."]

## 2. How to Read This Documentation

- **ID scheme:** `SCR-` for screens, `FLW-` for flows, `CMP-` for functionally-significant
  components. See §4 below for the full convention.
- **Platform notation:** every screen/flow states `Platform: Web / Android / iOS / Mobile / All`. A "Platform
  divergence" note appears only where functional behavior or content actually differs — its
  absence means there's no divergence, not that it was skipped.
- **Source & provenance:** every screen, component, and flow carries a Source field showing
  where it came from — either a feature's requirements/design-flow doc pair, or (for content
  that predates this documentation) "Reverse-engineered from codebase" with a
  Confirmed/Inferred confidence tag. See §5 below. Treat "Inferred" entries as provisional
  until a product owner confirms them — don't cite them as settled fact elsewhere in the doc.
- **Scope of this document:** describes *what the product does and why* — business rules, data,
  states' business meaning, user-facing behavior. It does not restate visual specs, component
  props, or design tokens — those live in ui_kit_registry.md / ui_standards.md and are only
  referenced here by name or link.

## 3. Domain Map

| Domain | One-line description | File | Status |
|---|---|---|---|
| [domain-slug] | [what it covers] | `docs/functional/domains/[domain-slug].md` or "inline below" | Active |

## 4. Navigation Structure

[The persistent navigation *shell* a user has access to at any time, per platform — distinct
from any one screen's own internal navigation (tabs within a screen stay documented on that
screen; see §6). This is the map that lets a reader go from "here are the domains" to "here's
how a user actually gets around the product" before diving into any one domain's detail.

- **Web:** [e.g. persistent left sidebar with entries X, Y, Z mapping to domains ...; top bar
  for ...]
- **Mobile:** [e.g. bottom tab bar with entries ...; anything not in the tab bar is reached via
  [drill-down path] instead]

Only describe the shell itself here — not every screen reachable from it. If web and mobile
organize domains differently (e.g. something is a top-level tab on mobile but nested under a
menu on web), say so; that's exactly the kind of divergence this section exists to surface.]

## 5. Screen & Flow Index

[A flat, product-wide table of every screen and flow, regardless of which domain file it lives
in — the fastest way to answer "does this exist, and where is it documented" once the product
spans many domains. Keep it to ID, name, domain, and platform; full detail always stays in the
domain file, this is a lookup table, not a second copy of the content. Skip this section
entirely while the product is small enough that the Domain Map already serves this purpose —
start it once domains begin splitting out (§7).]

**Screens**

| ID | Name | Domain | Platform |
|---|---|---|---|
| [SCR-xxx] | [Screen Name] | [domain-slug] | Web / Android / iOS / Mobile / All |

**Flows**

| ID | Name | Domain(s) | Platform |
|---|---|---|---|
| [FLW-xxx] | [Flow Name] | [domain-slug] or "cross-domain" | Web / Android / iOS / Mobile / All |

Move this whole section to `docs/functional/_screen-index.md` once it grows long enough to push
past a comfortable scroll of the entry file (same judgment-call threshold as §7) — link to it
here instead of leaving the full table inline.

## 6. Cross-Cutting Concepts

[Roles, entitlements, plan tiers, product-wide business rules ("Pro users get X"), and global
system behaviors (what happens product-wide on session expiry, offline mode, maintenance
windows) referenced by multiple domains. Move to `docs/functional/_global.md` once this section
grows large enough to warrant it; link here instead. This section is for *rules and behaviors*
— if you're describing a *thing* with its own lifecycle (a Subscription, an Order), that's
§8 (Shared Data Entities) instead.]

## 7. Shared Functional Components

[Components with product-specific behavior used across 2+ domains. Move to
`docs/functional/_shared-components.md` once this grows; link here instead. Purely visual/atomic
components stay in ui_kit_registry.md only — they don't belong here at all.]

## 8. Shared Data Entities

[Entities/data concepts referenced by 2+ domains (e.g. "Subscription," "Order," "Team") — their
business meaning and lifecycle, defined once instead of drifting across several domains'
"Data & business rules" bullets. Not a technical schema: no field types, no column names, that's
an engineering doc's job. Move to `docs/functional/_data-dictionary.md` once this grows past a
handful of entities; link here instead.]

## 9. Cross-Domain Flows

[Flows that span multiple domains, written in full using the Flow format from §3.3 below. A
domain file's own Flows section should only contain flows that stay entirely within that domain —
anything crossing domain boundaries lives here (or in a dedicated file if this section grows
large).]

## 10. Global Glossary

[Domain-agnostic terms used product-wide. Domain-specific terms stay in that domain's own file.]

## 11. Recent Changes

[A short rolling list of the last several changelog entries with links — enough to orient a
reader, not a full history. Full history lives in docs/changelog/.]

- [date] — [Domain]: [one-line summary] (see `changelog/[feature-id]_[feature-slug]_changelog.md`)

---

[If domains haven't been split out yet, their content goes below this line, each under its own
`##` header using the domain structure from §3 directly.]
```

---

## 3. Domain File Structure (repeats once per domain)

Whether a domain lives inline under a `##` header in `functional-spec.md` or in its own file at `docs/functional/domains/[domain-slug].md`, it always has this internal shape:

```markdown
# Domain: [Domain Name]

> Project: `<project_id>`

> Part of the Master Functional Documentation. See docs/functional-spec.md for the product-wide
> overview, navigation structure, glossary, and cross-cutting concepts — don't repeat those here.

## Overview

[What this domain covers, its boundaries, and how it relates to neighboring domains.]

## Screens / Pages

Repeat this block once per screen. Do not compress multiple screens into one block, and do not
include a "Platform divergence" bullet at all when there isn't one — its absence is the signal
that both platforms behave the same way here. See §6 below for what qualifies as a distinct
screen versus a modal, wizard step, or tab of another screen.

### [SCR-xxx] [Screen Name]

- **Platform:** Web / Android / iOS / Mobile / All
- **Purpose:** one sentence — what this screen accomplishes for the user.
- **Parent / tab-of:** *(omit if this is a standalone top-level destination)* [SCR-xxx] — only
  when this screen is a distinct-but-related tab or sub-view of another screen that shares its
  route/shell (see §6).
- **Entry points:** how a user reaches this screen (link to the relevant Flow ID(s)).
- **Functional composition:** functionally-significant components used here, by ID (link to this
  domain's Components section or _shared-components.md). Describe their functional role on this
  screen only — not their visual/prop details, which live in ui_kit_registry.md.
- **Data & business rules:** what data drives this screen and what rules govern what's shown,
  available, or enabled. Link to `_data-dictionary.md` entries (§8) for any entity referenced
  here rather than redefining it.
- **States (business meaning):** each state a user can encounter and what it *means*, not how
  it's rendered — e.g. "Empty — user has never saved a payment method," not "shows an EmptyState
  component."
- **Platform divergence:** *(omit this bullet entirely if there is none)* only when this screen's
  functionality or content — not layout — differs between web and mobile.
- **Related flows:** [FLW-xxx links]
- **Source:** `[feature-id]_[feature-slug]_prd.md` + `[feature-id]_[feature-slug]_ux_flow.md` (most recent feature that
  defined or changed this screen), **or** `Reverse-engineered from codebase, [date] —
  confidence: Confirmed/Inferred` for content that predates this documentation. See §5.

## Functionally-Significant Components

> Only components carrying product-specific behavior (business logic, conditional states with
> business meaning, data dependencies) belong here. Purely visual/atomic components live only in
> ui_kit_registry.md — don't duplicate them just because they appear on a screen. If a component
> here is used in 2+ domains, move it to docs/functional/_shared-components.md and link to it
> instead of keeping a local copy.

### [CMP-xxx] [Component Name]

- **Design system reference:** name/import path in ui_kit_registry.md (link only — don't restate
  its props or visual variants here). If this component is new and not yet formalized in the
  design system, say so plainly instead of linking to a registry entry that doesn't exist yet —
  e.g. "Not yet in ui_kit_registry.md — introduced as a new component for this feature; needs
  formalizing before/at ship time." Once it's formalized, update this field to a normal reference.
- **Functional role:** what business purpose this serves, wherever it appears.
- **Behavior rules:** conditional logic, states with business meaning, data dependencies.
- **Used on:** [SCR-xxx links]
- **Platform notes:** *(omit if none)* only if functional behavior — not visuals — differs by
  platform.
- **Source:** same convention as the Screens section above (feature doc pair, or
  reverse-engineered + confidence tag). See §5.

## Flows

Only flows that stay entirely within this domain. Flows crossing domain boundaries belong in the
entry file's Cross-Domain Flows section instead.

### [FLW-xxx] [Flow Name]

- **Goal / trigger:** why this flow happens and what starts it.
- **Screens involved (in sequence):** [SCR-xxx] → (triggering action) → [SCR-xxx] → ...
- **Business rules governing the flow:** eligibility, branching conditions, what determines which
  path a user takes.
- **Platform divergence:** *(omit if none)* only if the flow itself — not just a screen within
  it — differs by platform.
- **Edge cases / error handling:** summarized here; full detail lives on the relevant screen's
  States.
- **Source:** same convention as above. See §5.

## Domain Glossary

[Terms specific to this domain only. Product-wide terms belong in the entry file's Global
Glossary instead.]
```

---

## 4. ID Scheme

Stable IDs let screens, components, and flows reference each other without restating each other's content:

- **Screens:** `SCR-<domain-slug>-<screen-slug>` (e.g. `SCR-checkout-review`). A screen that's a tab/sub-view of another screen still gets a normal ID in this scheme — the relationship is captured by its **Parent / tab-of** field (§3), not by a different ID format.
- **Functionally-significant components:** `CMP-<component-slug>` (domain prefix only if the component is domain-specific rather than shared)
- **Flows:** `FLW-<flow-slug>` (domain prefix if it stays within one domain; no prefix for cross-domain flows, which live in the entry file)

Once an ID is assigned, treat it as **permanent** — other entries link to it. If a screen/flow/component is renamed, keep the ID and update the display name, rather than minting a new ID and orphaning old links.

---

## 5. Source & Provenance Conventions

Every screen, component, and flow entry ends with a **Source** field. There are two valid forms — never assert a fact in this document without one of them:

**Feature-driven** (the normal ongoing case, once this documentation exists): `[feature-id]_[feature-slug]_prd.md` + `[feature-id]_[feature-slug]_ux_flow.md` — the most recent feature whose requirements/design-flow doc pair defined or changed this entry.

**Reverse-engineered** (for content that predates this documentation, or was bootstrapped from an already-shipped product with no PRD/UX-flow pair to point to): `Reverse-engineered from codebase, [date]`, plus a required confidence tag:

- **Confirmed** — directly observed in code, a screenshot, or a demo. The *what* and the *how* are both grounded in something real.
- **Inferred** — the *what* was observable (a conditional exists, a state renders) but the *why* — business rationale, intended edge-case handling, the reasoning behind a rule — was not visible in code and is a best guess. Flag it as Inferred rather than writing it as settled fact, and surface it to the product owner for confirmation rather than letting it quietly become "truth" just because it's written down.

Never blend the two silently. If a screen was originally tagged "Reverse-engineered" and a later feature touches it, update its Source to that feature's doc pair — don't leave a stale reverse-engineered tag on content that's since been properly specified. Likewise, once a person confirms an "Inferred" entry, change the tag to "Confirmed" rather than leaving it Inferred indefinitely.

---

## 6. What Counts as a Screen

At the scale of a full multi-domain product this stops being obvious, so pin it down once rather than letting each domain file invent its own convention:

- **A Screen (`SCR-`)** is a distinct, independently-navigable destination — it has its own route on web, or its own place in the navigation stack on mobile. If a user can reach it directly (deep link, a back button lands on it, it shows up as its own entry in navigation history), it's a screen.
- **Modals, dialogs, and bottom sheets** that open over a screen and don't have their own route are usually *not* their own screen — document them as part of the triggering screen's Functional composition and States. Give one its own screen entry only if it's genuinely complex enough that folding it into the parent would force that screen's entry to carry a second, unrelated set of business rules and states.
- **Multi-step wizards** (checkout, onboarding, a multi-page form) are a **Flow** (`FLW-`) with a sequence of screens, not one screen with internal "steps." Each step that carries real, distinct data or business rules gets its own `SCR-`, so the flow's screens-involved sequence can reference them individually — a step that's just "page 2 of the same form with no new rules" doesn't need one.
- **Tabs within one screen** (e.g. a Profile screen with Overview / Activity / Settings tabs): if the tabs are just content filters with no distinct business rules, keep them as one `SCR-` entry, with the tab options noted as part of its own behavior. If a tab carries genuinely distinct data, business rules, or states, give it its own `SCR-` and set its **Parent / tab-of** field (§3) to the shell screen.

The test in ambiguous cases: would documenting this as part of its parent screen force that screen's entry to carry two unrelated sets of business rules and states? If yes, it earns its own `SCR-`. If the honest answer is "it's the same screen, just a different view of the same rules," it doesn't.

---

## 7. When to Split a Domain Out

Split a domain into its own file under `docs/functional/domains/` when either becomes true:

- The section covering it in `functional-spec.md` is pushing past roughly 300-400 lines, or
- It has accumulated enough screens/flows (roughly 8-10+) that scanning past it to find other domains is getting annoying.

Whichever comes first — this is a judgment call, not a hard trigger. Splitting a domain changes file paths, so any links to the moved content must be updated in the same approved change (file paths follow the conventions, so nothing in `SDLC.md` changes). The same threshold logic applies to starting the Screen & Flow Index (entry file §5) and to splitting `_shared-components.md`, `_data-dictionary.md`, or a large Screen & Flow Index out into `_screen-index.md`.

---

## 8. Functionally-Significant Components vs. Everything Else

Not every component that appears in a design/flow document's component tree deserves an entry in this document. A component earns one only if it carries product-specific behavior: conditional states with business meaning, data dependencies, or business rules governing when/how it appears. A `Button` or generic `Card` with no such logic doesn't need an entry here — it's fully covered by `ui_kit_registry.md` already. Rule of thumb: if describing the component functionally would just repeat "it's a button that does X" where X is already obvious from the screen's own Interactions section, it probably doesn't need its own entry.

---

## 9. Shared Components (Used Across Domains)

If a functionally-significant component appears in 2+ domains (e.g. a "Cart Summary" widget used in both a Shopping domain and a Checkout domain), define it once in `docs/functional/_shared-components.md` and have every domain file that uses it link to that single entry instead of re-describing it. The first time a component crosses this line, move its existing per-domain entry into the shared file and replace it with a link — don't leave the old copy behind as a stale duplicate.

---

## 10. Shared Data Entities

Parallel mechanism to §9, but for the data/business concepts multiple domains talk about rather than the components that render them. If two or more domains would each need to explain "what a Subscription is" in their own words, that's the signal it belongs here instead of inside any one domain's "Data & business rules" bullets.

### [Entity Name]

- **Business definition:** what this thing is, in plain terms — not a database schema. No field types, no column names; that's an engineering doc's job.
- **Key states/lifecycle:** e.g. a Subscription might move `trialing → active → past_due → canceled` — describe what each state means for the user, not how it's stored or computed.
- **Owned by:** which domain is the source of truth for this entity (creates/mutates it).
- **Referenced by:** [domain links] — every other domain whose screens depend on this entity's state, without owning it.
- **Source:** same convention as §5.

The first time an entity crosses the 2-domain line, move its definition here from wherever it was first described and replace that with a link — same discipline as §9. Move this section out into `docs/functional/_data-dictionary.md` once it grows past a handful of entities (same threshold logic as §7).

---

## 11. Global / Cross-Cutting Concepts

Concepts referenced by many domains but not really "screens," "flows," or "entities" themselves — user roles, entitlements/plan tiers, global business rules ("Pro users get X"), and global system behaviors (what happens product-wide on session expiry, offline mode, maintenance windows) — belong in the entry file's Cross-Cutting Concepts section, moved to `docs/functional/_global.md` once that section grows large. Domain files should link to these definitions rather than re-explaining "what a Pro user is" every time it's relevant. If what you're describing is a *thing* with its own lifecycle rather than a *rule*, it belongs in §10 (Shared Data Entities) instead.

---

## 12. Platform Divergence Notation

Every screen and flow entry carries a `Platform: Web / Android / iOS / Mobile / All` field. Only add a "Platform divergence" bullet when the *functional* behavior or *content* genuinely differs (a different feature is available, a different data field shows, a step is skipped on one platform) — not for purely visual differences (those belong in `ui_standards.md`'s platform conventions, not here). If every screen in a domain says "Both, no divergence," that's a sign of padding rather than documentation — omit the bullet entirely instead of writing "same on both." The entry file's Navigation Structure (§2, entry file §4) is where platform-level *navigation shell* divergence lives — a screen's own Platform divergence bullet is only for that screen's internal behavior.

---

## 13. Handling Approved Deviations from a PRD

When a design/flow document records that shipped behavior diverged from its originating requirements doc, this document reflects **what shipped** — that's current truth. Don't re-litigate the deviation in the domain file itself; a one-line note plus a pointer to the feature's changelog (which carries the full "PRD said / we shipped instead / why" record) is enough. This document describes the product as it is, not the history of how it got there.

---

## 14. Worked Example (entry file + one inline domain)

```markdown
# Acme Boards — Master Functional Documentation

## 1. Product Overview

Acme Boards is a kanban-style task board for small teams, available on web and iOS/Android. Teams
organize work into boards, each containing columns and cards.

## 2. How to Read This Documentation
...

## 3. Domain Map

| Domain | One-line description | File | Status |
|---|---|---|---|
| checkout | Cart, payment, order confirmation | inline below | Active |
| boards | Board/column/card CRUD and collaboration | inline below | Active |

## 4. Navigation Structure

**Web:** persistent left sidebar — Boards, Billing, Settings. Boards is the default landing destination.
**Mobile:** bottom tab bar — Boards, Notifications, Settings. Billing is reached via Settings
(no dedicated tab) — a genuine navigation divergence between platforms.

## 5. Screen & Flow Index

| ID | Name | Domain | Platform |
|---|---|---|---|
| SCR-boards-detail | Board Detail | boards | Both |
| SCR-boards-guest-invite-form | Guest Invite Form | boards | Both |

| ID | Name | Domain(s) | Platform |
|---|---|---|---|
| FLW-boards-invite-guest | Invite a Guest Collaborator | boards | Both |

## 6. Cross-Cutting Concepts

**Plan tiers:** Free (3 boards max), Pro (unlimited boards, guest collaborators).
**Session expiry:** an expired session redirects to SCR-auth-login with a "Session expired"
banner, product-wide, both platforms.

## 7. Shared Functional Components

None yet.

## 8. Shared Data Entities

### Board

- **Business definition:** a named collection of columns belonging to one team.
- **Key states/lifecycle:** Active → Archived (read-only, hidden from default list) → Deleted
  (soft-deleted, recoverable for 30 days).
- **Owned by:** boards
- **Referenced by:** boards
- **Source:** Reverse-engineered from codebase, 2026-07-24 — confidence: Confirmed.

## 9. Cross-Domain Flows

None yet.

## 10. Global Glossary

**Board** — a named collection of columns belonging to one team.

## 11. Recent Changes

- 2026-06-02 — Boards: guest collaborator invites (see `changelog/012_guest-invites_changelog.md`)

---

# Domain: Boards

## Overview

Covers board creation, column/card management, and guest collaboration.

## Screens / Pages

### [SCR-boards-detail] Board Detail

- **Platform:** Both
- **Purpose:** lets a user view and manage a single board's columns and cards.
- **Entry points:** FLW-boards-open, from the board list.
- **Functional composition:** CMP-guest-invite-banner
- **Data & business rules:** guest collaborators can view and move cards but not delete
  columns. References the Board entity (Shared Data Entities).
- **States (business meaning):** Empty — board has no columns yet, first-run state.
- **Related flows:** FLW-boards-invite-guest
- **Source:** 012_guest-invites_prd.md, 012_guest-invites_ux_flow.md

## Functionally-Significant Components

### [CMP-guest-invite-banner] Guest Invite Banner

- **Design system reference:** `components/banners/InviteBanner` in ui_kit_registry.md
- **Functional role:** prompts a Pro-tier board owner to invite a guest collaborator.
- **Behavior rules:** only shown to board owners on Pro tier with fewer than 5 active guests.
- **Used on:** SCR-boards-detail
- **Source:** 012_guest-invites_prd.md

## Flows

### [FLW-boards-invite-guest] Invite a Guest Collaborator

- **Goal / trigger:** board owner wants a non-team-member to collaborate on one board.
- **Screens involved:** SCR-boards-detail → (owner taps "Invite guest") → SCR-boards-guest-invite-form
- **Business rules governing the flow:** capped at 5 active guests per board on Pro tier; not
  available on Free tier.
- **Source:** 012_guest-invites_prd.md

## Domain Glossary

**Guest collaborator** — a user with board-scoped access who is not a full team member.
```

---

## 15. Authoring Checklist

Before treating a write to this document as final:

- [ ] Every fact traces to a requirements doc + design/flow doc pair, **or** is explicitly tagged "Reverse-engineered from codebase" with a Confirmed/Inferred confidence marker (§5) — nothing asserted without one of these two provenances.
- [ ] No visual/design-system detail (colors, spacing, props, variants) appears anywhere in this document — only names/links into `ui_kit_registry.md` / `ui_standards.md`.
- [ ] Every screen/flow/component has a stable ID, assigned once and never recycled.
- [ ] Every screen is either a standalone top-level destination or explicitly marked as a modal/step/tab of a parent screen (§6) — never left ambiguous between the two.
- [ ] "Platform divergence" bullets appear only where genuine functional divergence exists — not as padding.
- [ ] A component only gets its own entry if it's functionally significant (§8) — otherwise it's covered by the UI kit registry alone.
- [ ] Shared components (2+ domains) live in `_shared-components.md`, not duplicated per-domain (§9).
- [ ] Entities referenced by 2+ domains live in Shared Data Entities / `_data-dictionary.md` (§10), not redefined per screen.
- [ ] The Screen & Flow Index (entry file §5) is current whenever a screen or flow is added, renamed, or removed — once the product is large enough to have one.
- [ ] `docs/functional-spec.md` still exists and is still the entry point, even if most content has moved into split domain files.
