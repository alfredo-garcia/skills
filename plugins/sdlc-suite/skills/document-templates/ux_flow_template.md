# Template: UX Flow Doc

> **What this is:** the strict, image-free component-orchestration spec produced once a prototype
> is signed off — written so an implementation agent (Claude Code, Cursor) can build the real
> screens without guessing at rendering logic. Every line should resolve to a concrete rendering
> or data instruction; no subjective visual description ("modern," "clean") anywhere in it.
>
> **What this is not:** a visual spec. It references `ui_kit_registry.md` and `ui_standards.md`
> by name for anything about how a component looks — this document is about which components
> appear, in what order, under what conditions, and what happens when the user interacts with
> them, never about color/spacing/type.
>
> **Produced by:** the `ux-designer` skill's Stage 3, only once the user has explicitly signed off
> on a prototype (Stage 1-2). Built almost entirely by transcription from what already exists in
> the approved prototype — not new design work. If drafting this doc surfaces a state or component
> that never appeared in the prototype, that's a signal to go back and add it to the prototype
> first, not to invent it here.
>
> **Consumed by:** an implementation agent (alongside the PRD) to build the feature, and by
> `document-manager` as "Document B" — see that skill's `references/input_contract.md` for the
> content categories it extracts from this document (screens/platforms, per-screen purpose and
> entry point, component composition, states, navigation/sequencing, approved deviations, open
> items). `document-manager` is format-agnostic, so any document covering those categories is
> valid input even if it doesn't follow this template's exact section numbers — but following it
> is the fastest path to a clean extraction.
>
> **Real instance filename:** `<feature-id>_<feature-slug>_ux_flow.md` — same ID and slug as the
> source PRD. Saved alongside it by default. Never mint a new Feature ID here — look up the
> existing one if it isn't already in hand (see the `ux-designer` skill's Step 0).


> **Surface notation:** `Platform:` fields use the project's UI surfaces from `SDLC.md` (`surfaces`): `Web`, `Android`, `iOS`, `Mobile` (= Android and iOS behaving identically) or `All`. Only surfaces the project targets may appear.

---

## Structure

Seven sections, in this order:

```markdown
# UX Flow: [Feature Name]

> Project: `<project_id>`
> Source PRD: `<feature-id>_<feature-slug>_prd.md`
> UI Standards referenced: `docs/context/ui_standards.md`
> UI Kit Registry referenced: `docs/context/ui_kit_registry.md`
> Prototype: `[path or description of the approved, signed-off prototype]`
> Status: Approved by user on [date]

This document is strict component-orchestration instructions for an implementation agent
(Claude Code, Cursor). No images. No subjective visual description ("modern", "clean") — every
line should resolve to a concrete rendering or data instruction.

## 1. Flow Summary

One short paragraph plus a linear list of the screens in this flow, in sequence, with the
triggering action between them. Example:

- `ScreenA` → (user taps "Continue") → `ScreenB` → (user submits form) → `ScreenC`

## 2. Screens

Repeat this block once per screen. Do not compress multiple screens into one block.

### 2.[N]. [Screen Name]

- **Platform**: Web / Android / iOS / Mobile / All (if both, note any divergence inline in the component tree or
  state matrix below)
- **Purpose**: one sentence.
- **Route / entry point**: [where this screen is reached from]

**Data required**
List every field this screen needs, its type, and where it comes from (API response, prior
screen's state, global store). This should trace back to the PRD's Data Model and API sections.

| Field | Type | Source |
|---|---|---|
| `example.field` | string | GET /api/example |

**Component tree**
Nested list of every component used on this screen, in layout order. For each: its exact name,
whether it's reused from the kit (with import path) or new-temporary (flagged), and the key props
it's given.

- `<ScreenContainer>` (kit: `components/layout/ScreenContainer`)
  - `<Header title="..." />` (kit)
  - `<TmpInlineRatingWidget value={x} onChange={...} />` (**NEW — temporary**, prototype-only,
    needs proper design-system treatment before shipping)

**Conditional rendering states**
Every state this screen can be in, as an explicit if/then, using this exact style — condition,
then the exact component call:

- If `isLoading === true`, render `<LoadingSpinner fullScreen />`
- If `error !== null`, render `<ErrorBanner message={error.message} onRetry={...} />`
- If `data.length === 0`, render `<EmptyState message="..." />`
- Otherwise, render the normal component tree above with `data`.

Include every state that appeared in the prototype and every state the PRD's UI/UX Requirements
or Edge Cases sections call for — cross-check both before finalizing this screen's block.

**Interactions / transitions**
For each interactive element: the action, what happens locally (state change), and what it
navigates to (if anything).

- Tap/click `[element]` → [local state change, if any] → navigates to `[ScreenX]` / stays on
  screen

## 3. Navigation Map

A simple text/arrow diagram of the full flow across all screens (not just the linear happy path —
include branches for error/empty/edge states reached from any screen).

## 4. Data Requirements Summary

Consolidated list of every data field used anywhere in this flow, deduplicated, with type and
source — a quick reference for whoever wires up the API/state layer, without needing to re-read
every screen block.

## 5. Component Legend

Two tables: components reused from the kit, and new temporary components introduced by this
feature.

**Reused from `ui_kit_registry.md`**

| Component | Import path | Used on screens |
|---|---|---|

**New — temporary (needs formalizing before/at ship time)**

| Component | Purpose | Used on screens | Notes |
|---|---|---|---|

## 6. Deviations from PRD (Approved)

Anything that came out of the feedback loop where the user explicitly chose to diverge from the
original PRD. If none, state that explicitly rather than omitting the section.

| PRD said | We shipped instead | Why / who approved |
|---|---|---|

## 7. Open Items

Anything still unresolved that implementation should flag back rather than guess on. If none,
state that explicitly.
```

## Section-by-Section Guidance

- **§2 (Screens):** one block per screen, never compressed. This is the section most likely to grow long — that's expected and correct; don't summarize multiple screens into one block to save space.
- **Component tree naming:** always use the component's real name and, if reused, its real import path from `ui_kit_registry.md` — never a description of what it looks like. A new, not-yet-formalized component is flagged unmistakably (conventionally a `Tmp` prefix, e.g. `TmpInlineRatingWidget`) so it can never be mistaken for an approved kit component later.
- **New components were announced:** every `Tmp` component in this doc must have been announced to the user before it was created (ux-designer "New components" rule), and they must all be listed together in the component legend with the reason no registry component fit. A component that isn't in the registry and isn't in that list must not appear.
- **Conditional rendering states:** must use the exact concrete style shown above — a condition and the exact component call, not a description of the condition. `"shows a spinner while loading"` is not acceptable; `If isLoading === true, render <LoadingSpinner fullScreen/>` is.
- **Cross-check against the PRD:** every state and edge case listed in the PRD's UI/UX Requirements and Edge Cases sections needs a corresponding row in this doc's state matrix. If the PRD names a state that was never actually built in the prototype, that's a gap — either build it now or explicitly flag it as an open item (§7), never omit it silently.
- **§6 (Deviations):** this is the paper trail for why the shipped UX doesn't match the original PRD line-for-line. Every approved deviation from the feedback loop belongs here, in the same "PRD said / we shipped instead / why" shape that `document-manager`'s changelog carries forward.

## Worked Example (one screen block)

```markdown
### 2.1. Quick Reorder Section

- **Platform**: Both
- **Purpose**: lets a repeat customer add a frequently-ordered item to their cart in one tap.
- **Route / entry point**: home screen, above the main catalog grid.

**Data required**

| Field | Type | Source |
|---|---|---|
| `frequentItems` | array of `{id, name, price, imageUrl}` | GET /api/users/me/frequent-items |
| `isLoading` | boolean | local state, true until the request above resolves |

**Component tree**

- `<Section title="Reorder">` (kit: `components/layout/Section`)
  - `<QuickAddCard>` (kit: `components/commerce/QuickAddCard`) — one per item in `frequentItems`

**Conditional rendering states**

- If `isLoading === true`, render `<SkeletonRow count={5} />`
- If `frequentItems.length === 0`, do not render this section at all (not even an empty state —
  first-time customers simply don't see it)
- Otherwise, render up to 5 `<QuickAddCard>` components from `frequentItems`

**Interactions / transitions**

- Tap `<QuickAddCard>`'s quick-add button → item added to cart (local cart state updates) → stays
  on home screen, cart icon badge count increments
```
