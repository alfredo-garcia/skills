# UI Foundations Guide (Mode 0)

How to build a project's `ui_standards.md` and `ui_kit_registry.md` without over-designing, especially for a small team or a solo builder.

## Principle: customize a library, don't invent a design system

The per-surface tech standards (`tech_standards/<surface>.md` §2-§3; core §1 for the overview) already name the component library or native toolkit and styling approach for each platform (e.g. a headless or styled component library plus a utility CSS approach on web, or a React Native UI kit on mobile). Your job is to:
1. Take that library's defaults as the base.
2. Decide the small set of things that make the product feel like itself: palette, typography, radius, density/spacing, voice and tone, iconography (from the library's or the stack's approved icon set).
3. Write those down as tokens and rules an agent can apply literally.

If §7 is empty or says "n/a" while the project has a UI, that's a tech_standards gap. Send it to `tech-lead`; don't pick a library yourself.

## Inputs to collect (ask only for what's missing)

- Existing brand assets: logo, colors, fonts. If there are none, propose them.
- 2-3 reference products whose feel the user likes, and one they dislike.
- Light mode, dark mode, or both.
- Accessibility needs beyond the baseline (WCAG AA contrast, visible focus, minimum touch targets).
- Voice: derive a first proposal from the vision's personas and principles, then confirm.

## Order of work and source of truth

Write `ui_standards.md` and `ui_kit_registry.md` as drafts first; they're the source of truth. When Claude Design is available, the project's design system there is built *from* them and from the UI kit code (`claude_design_handoff.md` §1), and anything approved in Claude Design flows back into these files as an approved diff. Otherwise, the style guide below is built with the project's stack or the sandbox scaffold.

## What to show (Mode 0 deliverable)

A rendered, clickable style guide built with the project's stack (or the sandbox scaffold as a labeled approximation):
- The color palette with token names and contrast checks against text.
- Type scale and spacing scale.
- The core components in all their states (default, hover/pressed, focus, disabled, error, loading): button, input, select, card, modal/sheet, toast/alert, empty state, list item.
- One realistic sample screen from the vision's main use case, so the user can judge the feel.

## Writing the documents

- `ui_standards.md`: follow the template section by section. Tokens use the naming convention from template §10 and map 1:1 to the library's theme mechanism. Platform conventions only for the UI surfaces in `SDLC.md` (`surfaces`).
- `ui_kit_registry.md`: list only components the project will actually use, each with its import path from the library or the project's own wrappers (`web_components` / `mobile_components` in `SDLC.md`). It's fine to start small; it grows as features need things.

## Approval

Every choice is `[PROPOSED]` with a rationale until the user confirms it. Remove the tags before saving. Update `ui_foundations` in `SDLC.md` only after explicit approval.
