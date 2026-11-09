# Prototype Guidelines

Detail behind Stage 1 of `SKILL.md`. Read this before you start building a prototype.

## 1. Deciding how to build it

The right approach depends on what kind of access you actually have this session — don't default to one approach out of habit, check.

> **New components:** before creating any component that isn't in `ui_kit_registry.md` (or a shared kit's public registry), tell the user what you're about to create and why nothing existing fits. See "New components" in `SKILL.md`.

### A. You have real access to the project's code

Use the project's own stack and UI library from `tech_standards.md`. Never add a dependency to the project for the prototype; anything not in `tech_standards.md` goes to `tech-lead` first.
 (Claude Code, Cowork with a connected repo)

Prefer building the prototype as an actual runnable piece of the real app, not a lookalike:
- Reuse the real component implementations from the component directories declared in `SDLC.md` (`web_components` / `mobile_components`) directly — import them, don't reimplement their visuals from memory.
- Wire the new screens into a throwaway route/entry point (under the `prototypes` directory declared in `SDLC.md`, e.g. `prototypes/<feature-id>_<feature-slug>/`) rather than into the real navigation, so it's obviously scratch work and easy to remove later, but still runs on the project's real dev server with its real styling pipeline (this is what actually guarantees brand/token accuracy — far more than any approximation you could hand-build).
- Start the dev server and open it in a browser tool if one is available. If no browser tool is available, still start the server, give the user the exact URL and command, and — if you have any way to render HTML/React content directly in the conversation as well — do that too as a backup so the user isn't blocked on running a command themselves.

### B. You don't have real project access (sandboxed claude.ai session, no connected repo)

Build a single self-contained artifact instead:
- Start from `assets/prototype_scaffold.html` — it already has React, a minimal client-side router/state simulation for multi-screen flows, and a CSS custom-property block you fill in from `ui_standards.md` (colors, spacing scale, type). Starting from this every time means every prototype speaks the same technical dialect instead of you inventing a new one-off setup per feature.
- Translate whatever `ui_kit_registry.md` describes into faithful React components inside this file (same names, same props/behavior) — even though this isn't the literal production code, the names and prop shapes should match exactly, so the eventual real implementation is a straightforward swap-in rather than a rewrite.
- Save it as a `.html` (or `.jsx` if your environment renders those directly) file to the outputs location your environment uses for artifacts, so it renders inline for the user automatically. This is the "open it" step — don't stop at having written the file, make sure it actually renders as a preview.

If you're unsure which situation you're in, check for filesystem/browser tools before deciding, rather than assuming.

## 2. Reuse first: how to check the registry properly

`ui_kit_registry.md` should tell you, for each component: its name, its props/variants, and (ideally) where it lives in code. Before building any piece of UI:
1. Search the registry for something that already covers this need — check for near-matches too (e.g. the registry's `Card` with a `variant="interactive"` prop might already cover what you were about to call a new `ClickableTile`).
2. If a real match exists and you have code access, import the actual component. If you don't have code access, recreate it faithfully (same name, same props) in the sandboxed artifact.
3. Only if genuinely nothing in the registry covers the need, create something new.

## 3. Temporary component convention

When you must create something new:
- Prefix the component name with `Tmp` (e.g. `TmpInlineRatingWidget`) so it can never be confused with an approved kit component, in the prototype code and in any doc that references it.
- Add a one-line comment at its definition: `// TEMP — prototype-only, not in ui_kit_registry.md. Needs a real design-system component before this ships.`
- Keep a running list as you build (component name, one-line purpose, which screen(s) use it). You'll transcribe this list directly into the UX Flow doc's component legend in Stage 3 — don't reconstruct it from memory later.
- Keep new components genuinely minimal — just enough to make the flow clickable and legible. The point is to unblock the prototype, not to design a polished new component; that design work belongs to whoever formalizes it into the kit afterward.

## 4. Web / mobile parity checklist

Apply this section only when `SDLC.md` lists two or more UI surfaces (`web`, `android`, `ios`). With a single surface, design for that surface's conventions only.

The prototype needs to make sense as a single UX that every targeted surface can implement with its own toolkit (as decided in `tech_standards/<surface>.md`: native Compose/SwiftUI, a cross-platform framework, or a web framework), not one platform's idiom stretched over all. Android and iOS are distinct surfaces: respect Material vs Human Interface Guidelines differences in navigation, back behavior, sheets/dialogs, and system permission prompts. Check `ui_standards.md` first — if it already defines platform conventions, those win over anything below. Where it's silent, watch for:

- **Primary interaction model**: hover-revealed affordances (tooltips, hover-to-show buttons) don't exist on touch. If a screen's web version relies on hover, show the mobile equivalent explicitly (always-visible affordance, long-press, or a swipe action) rather than leaving it implied.
- **Navigation container**: web tab bars / sidebars vs. mobile bottom tab bars / stack navigation — call out which maps to which if the PRD implies both platforms.
- **Overlays**: web modals/dialogs often become bottom sheets or full-screen takeovers on mobile. Don't assume the same overlay treatment works identically on both; show both if they diverge.
- **Touch targets**: mobile interactive elements need to be sized for a finger, not a cursor — if `ui_standards.md` gives a minimum tap target size, hold to it in the mobile version even if the web version is denser.
- **Gestures**: swipe-to-dismiss, pull-to-refresh, and similar mobile-native patterns have no web equivalent — don't invent a web analog for the sake of parity, just note the mobile-only behavior.

Where a genuine divergence exists, make it visible in the prototype (e.g. a toggle or side-by-side view between "Web" and "Mobile" for that screen) rather than picking one and hoping it's understood to generalize — this divergence, once approved, is exactly what Stage 3's UX Flow doc needs to capture per-platform.

## 5. Presenting the prototype (opening it for feedback)

Whichever build approach you used, the prototype must actually be opened/rendered for the user, not just described:
- **Real repo + browser tool available**: navigate the browser tool to the running dev server URL.
- **Real repo, no browser tool**: give the exact run command and URL, and if your environment can also render a standalone HTML/React artifact, produce one as a fallback so the user has something to react to immediately without leaving the chat.
- **Sandboxed artifact**: save the file to the artifact-rendering output location your environment uses, so it renders inline automatically — don't require the user to manually open a downloaded file if inline rendering is available.

After every revision in the Stage 2 feedback loop, re-render/re-open the updated version the same way — the user should always be looking at the current state, not a stale one.
