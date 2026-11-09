# Template: UI Kit / Component Registry

> **What this is:** the canonical, authoritative list of every existing UI component in the
> product's design system — its name, props/variants, platform availability, and where it lives
> in code. This is the single most important input for visual consistency: it's the difference
> between a prototype (or a shipped screen) that looks like it belongs in the product and one that
> quietly invents its own parallel visual language.
>
> **What this is not:** a description of what components *do* functionally in the product (that's
> the Master Functional Documentation's job — it references components here by name/link and adds
> only the business-logic layer on top, e.g. "this badge shows the unread count," never repeating
> this file's visual/prop details).
>
> **Produced/maintained by:** typically the design system/frontend engineering team, generated
> from or kept in sync with the actual component library's source code. If a project has none yet,
> the `ux-designer` skill can bootstrap a first draft from this template — clearly marked as a
> starting point for engineering to review and correct against the real source, not a substitute
> for it.
>
> **Consumed by:** the `ux-designer` skill (checked before creating any new UI element — reuse an
> existing entry before inventing something new) and, indirectly, `document-manager` (links to
> entries here by name, never restates them).
>
> **Real instance lives at:** `<docs_root>/context/ui_kit_registry.md` (see
> `project_context_protocol.md` §3). Bootstrapped by `ux-designer` Mode 0 (Phase 0.3) from the
> component library or toolkit chosen in each UI surface's `tech_standards/<surface>.md` (it may start nearly empty, listing that
> library's components the project actually uses). A real instance starts with a header block:
> `# UI Kit Registry: [Product Name]`, then `> Project: \`<project_id>\``, then
> `> Status: Draft / Approved (YYYY-MM-DD)`. If web and mobile component sets diverge enough to
> warrant separate files, a project may split this into `ui_kit_registry.md` (web) and
> `ui_kit_registry_mobile.md`, noting the split in `SDLC.md` § Notes.


> **Surface notation:** `Platform:` fields use the project's UI surfaces from `SDLC.md` (`surfaces`): `Web`, `Android`, `iOS`, `Mobile` (= Android and iOS behaving identically) or `All`. Only surfaces the project targets may appear.

---

## 1. How to Read This Registry

- **Category taxonomy:** [the top-level groupings used below, e.g. Layout, Navigation, Inputs, Feedback/Overlays, Data Display. Keep this list stable — recategorizing later breaks nothing structurally, but it does make the registry harder to scan consistently over time.]
- **Platform notation:** every entry states `Platform: Web / Android / iOS / Mobile / All`. Where a component exists on both platforms but with a different implementation (e.g. a native bottom sheet vs. a web modal serving the same functional role), give each its own entry and cross-reference them under "Related components" rather than forcing one entry to describe two different implementations.
- **Status labels:** `Stable` (safe to use as-is), `Beta` (usable, but API may still change), `Deprecated` (don't use in new work; see its migration note for the replacement).

## 2. Component Index

A flat table for fast scanning — one row per component, linking down to its full entry in §3.

| Component | Category | Platform | Status | Import path |
|---|---|---|---|---|
| `Button` | Inputs | Both | Stable | `components/inputs/Button` |
| `Card` | Layout | Both | Stable | `components/layout/Card` |
| `BottomSheet` | Feedback/Overlays | Mobile | Stable | `components/overlays/BottomSheet` |
| `Modal` | Feedback/Overlays | Web | Stable | `components/overlays/Modal` |

## 3. Component Entry Structure (repeat per component)

### [Component Name]

- **Category:** [one of the categories from §1]
- **Platform:** Web / Android / iOS / Mobile / All
- **Import path(s):** [import path per surface where it differs]
- **Status:** Stable / Beta / Deprecated *(if Deprecated, add a one-line migration note: what replaces it and why)*
- **Description:** one or two sentences — what it is and its primary purpose.

**Props / variants**

| Prop | Type | Default | Description |
|---|---|---|---|
| `variant` | `"primary" \| "secondary" \| "ghost"` | `"primary"` | Visual emphasis level |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Physical size |
| `disabled` | `boolean` | `false` | Disables interaction |

**Visual states covered**

[Purely visual/interaction states this component itself renders — default, hover, focus, active, disabled, loading. Not business states; a component's *business* meaning when in a given state belongs in the Master Functional Documentation, not here, e.g. this file says "supports a `loading` prop that shows a spinner," the functional doc says "shown loading while awaiting payment confirmation."]

**Usage guidance**

- When to use this component vs. a similar-looking alternative.
- When *not* to use it (common misuse to avoid).

**Composition notes**

[What this component is commonly composed with, e.g. "typically wrapped by `<FormField>` for label/error handling rather than styled standalone."]

**Accessibility notes**

[Keyboard interaction, ARIA role/labeling requirements, focus management — anything component-specific beyond the general standards in `ui_standards.md` §8.]

**Do's and Don'ts**

[Concrete, component-specific rules — e.g. "Don't override this component's padding via a wrapper; use the `size` prop."]

**Related components**

[Names of similar or commonly-paired components, including the other-platform equivalent if this entry is platform-specific.]

## 4. Temporary / Not-Yet-Formalized Components

Prototypes and in-flight features sometimes introduce a component that doesn't exist here yet (conventionally prefixed `Tmp` in code, e.g. `TmpInlineRatingWidget`, and flagged as such wherever it's referenced). Such a component does **not** get a §3 entry in this registry until it's formally reviewed and adopted into the design system. When it is adopted:

1. Give it a real §3 entry here (drop the `Tmp` prefix, fill in all fields properly).
2. Update every place that referenced it as "not yet in the design system" (e.g. a Master Functional Documentation component entry's "Design system reference" field) to link to the new real entry instead.
3. Note the addition in this file's §6 versioning log.

## 5. Cross-Surface Parity Notes

[If the registry is split across separate web/mobile files, or if some components exist on only one platform, note the general parity approach here — e.g. "every web component has a React Native equivalent unless explicitly noted as web-only (e.g. `HoverCard`, which has no meaningful touch equivalent — see `ui_standards.md` §9 for the general hover-to-touch mapping principle)."]

## 6. Versioning

- **Last updated:** [date]
- **Owner:** [team/person who approves new entries and deprecations]
- Recent additions/deprecations worth flagging to consumers.
