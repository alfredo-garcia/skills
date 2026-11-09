# Input Contract

This defines what the skill needs from its two inputs as **information categories**, not as a specific file format, template, or tool. Any two documents that cover these categories, in whatever structure they use, are valid input. This skill does not care what produced them — a dedicated requirements/design workflow, a PM writing directly in Markdown, an exported ticket, or a hand-written doc all work identically as long as the content is there.

Read this file whenever an input doesn't obviously map onto the categories below — that's the signal to extract by content rather than by assumed structure.

## Document A: the requirements-shaped input (a "PRD," ticket, or similar)

Must cover, somewhere, in some form:

1. **Feature identity** — a name and a one-line statement of what it's for.
2. **Scope** — what's included, and ideally what's explicitly excluded (non-goals). This helps prevent documenting things that were considered but didn't actually ship.
3. **Functional behavior** — the user-facing behavior/requirements: what the feature lets a user do.
4. **Data model** — what data fields/entities are involved and where they come from.
5. **Business rules / constraints** — the conditions, eligibility, and limits governing the behavior (e.g. "available only under X condition").
6. **Edge cases** — known edge cases and their intended handling.
7. **Dependencies** — what existing parts of the product this touches or depends on. This is the main input to Step 3's domain-assignment decision.
8. **Open questions / assumptions** — anything not yet resolved at the time this document was written.

## Document B: the design/flow-shaped input (screens, states, navigation)

Must cover, somewhere, in some form:

1. **Screens/pages** — every screen introduced or changed, and which platform(s) — web, mobile, or both — each applies to.
2. **Per-screen purpose and entry point** — what it's for and how a user reaches it.
3. **Component composition** — which UI components appear, and specifically which ones carry product-specific behavior as opposed to purely visual/generic ones — flagged however this particular document distinguishes "new / not yet in the design system" from "existing, reused" components (a prefix, an explicit note, a separate list — the mechanism varies, the distinction is what matters).
4. **States** — every state a screen or flow can be in, described with enough detail to infer *why* it's in that state, not just what renders when it is.
5. **Navigation / sequencing** — how screens connect, in order, with the triggering action between them.
6. **Approved deviations from the requirements document** — anywhere the shipped/approved behavior ended up differing from what Document A originally said, if that happened.
7. **Open items** — anything still unresolved.

## If an input is missing a category

Don't guess or invent to fill the gap.
- If the missing category would change what gets written into the master doc (e.g. no data model is given for a field you'd need to describe), ask the user before drafting that piece.
- If it wouldn't change anything load-bearing (a nice-to-have that just isn't there), note the gap in the changelog's open-items list and proceed with the rest.

## Using structure when it happens to be there

If Document A or B is already organized into clear, consistently-numbered sections, use that structure as a shortcut — it's faster than scanning for categories by content. But treat any specific section numbering as incidental to *this* document, never as a rule to expect from the next one. The categories above are the actual requirement; section numbers, if present, are just a convenience this time.
