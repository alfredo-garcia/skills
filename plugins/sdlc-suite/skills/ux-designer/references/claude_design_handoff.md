# Claude Design (Path A)

Detail behind Path A in `SKILL.md`, used by default when `SDLC.md` says `claude_design: available`. Claude Design is a separate Anthropic product with its own canvas. This skill can't drive it directly: the user works there, and this skill prepares the inputs, then brings the results back and reconciles them with the repo.

Claude Design is in research preview. Treat the specifics below as "how it works today". If what you see differs, trust what you see, adapt, and tell the user about the discrepancy.

## 0. The rule that governs everything here

**`ui_standards.md` (visual language) and `ui_kit_registry.md` (components) in the repo are the source of truth.** The design system in Claude Design is a working copy built from them. When they disagree, the repo wins. A change discovered in Claude Design becomes a proposed diff to the repo files, and only counts once the user approves it.

## 1. How Claude Design is organized, and setting it up (Mode 0, or the first time a project uses Claude Design)

**Structure** (recorded in `SDLC.md`, `## Design`):

| Piece | How many | What it holds | `SDLC.md` key |
|---|---|---|---|
| Shared design system | One per family of apps that share a UI kit (none for a standalone app) | The shared kit: tokens, components, patterns, voice. Source of truth: the shared kit's `ui_standards.md`, registry and code | `claude_design_shared_system` |
| App design system | One per app | Only what's specific to the app (its theme or overrides, its own components), built on the shared one | `claude_design_system` |
| Screens canvas `<App> · Screens` | One per app (a Design canvas with both design systems installed) | One page per screen or flow; each page has the screen's artboards in all its states and formats (sizes, light/dark). Always the **current shipped state**. Temporary `Propuesta <id> · <title>` pages while a feature is in progress | `claude_design_screens` |

Never create a canvas per feature. Each design system's README links its app's Screens canvas (or, for the shared one, says the rule: one Screens canvas per app, pages per screen, temporary proposal pages per feature).

**Setting up the design systems:**

1. Prepare the inputs for the user:
   - `ui_standards.md` (tokens, typography, spacing, voice, platform conventions), as the main reference;
   - the UI kit **code**: the project's component folders from `SDLC.md` (`web_components` / `mobile_components`), and the shared UI kit's code location if the project consumes one. Claude Design can derive components and styles from a codebase during onboarding, which keeps it aligned with what developers actually import;
   - `ui_kit_registry.md`, so names match the kit;
   - brand assets (logo, fonts) if any.
2. The user creates or updates the design system in Claude Design from those inputs.
   With a shared UI kit, set up (or reuse) the shared design system from the kit first, then the app's design system on top of it with only the app's own tokens, overrides and components.
3. Record names and URLs in `SDLC.md`: `claude_design_shared_system` (several apps point to the same one) and `claude_design_system` (shown, approved).
4. **Verify alignment:** compare the design system's tokens and components with `ui_standards.md` and the registry. Report any difference; the repo files win, and the design system gets corrected.
5. **Re-sync triggers:** any approved change to `ui_standards.md` or the registry, or a breaking change in a shared UI kit. When one happens, remind the user to update the design system.

## 2. Handing off a feature's prototype (Stage 1)

The prototype lives in a new page `Propuesta <id> · <title>` of the app's Screens canvas (`claude_design_screens`). It may start from copies of artboards in the current screen pages, then modify them. If the canvas doesn't exist yet, the prompt first tells the user to create it: a Design canvas named `<App> · Screens` with the shared and the app design systems installed; once it exists, record its URL in `SDLC.md` (shown, approved).

Hand the user **one ready-to-paste prompt**, built with `SKILL_DIR/assets/claude_design_prompt_template.md`. It must be self-contained (Claude Design hasn't seen the PRD) and carry:
- the PRD content in scope (goal, what's out of scope, the screens and flows, every UI state and edge case, real copy and example data);
- the agreed scope list from Stage 1, **including the new components already announced and accepted**, with their `Tmp` names;
- the surfaces and formats to cover and the platform conventions and voice from `ui_standards.md`;
- an explicit instruction to use only design-system components, and to flag anything new instead of improvising it;
- what to deliver (navigable prototype, every state visible, a list of components used and new ones flagged).

Save it at `<prototypes>/<id>_<slug>_claude_design_prompt.md` and show it in chat in a single fenced code block, followed by the steps to use it (open a project with the design system, paste, iterate, bring the result back). For feedback during Stage 2, hand over follow-up prompts the same way.

The user iterates there, with or without you present. Your role resumes when they bring the result back.

## 3. Bringing the result back

Accept whatever the user has: a share link, an export (HTML, PDF, PPTX), screenshots, or a handoff bundle in Claude Code. Treat it as the current prototype for the Stage 2 feedback loop. Don't build a parallel code version unless the user explicitly asks for one.

## 4. Reconciling against the registry (before Stage 3, and whenever a new version comes back)

1. Match every element to `ui_kit_registry.md` (and a shared kit's public registry) by name and apparent props. A visual match isn't a prop-level match; you're working from pixels or an export, not source.
2. **Every element without a registry match is reported to the user explicitly as a new component that would have to be created** (proposed name `TmpXxx`, why it's needed, the closest existing component and why it doesn't fit). Never silently map it to a guessed existing component, and never let it into the UX Flow without the user knowing it's new.
3. **Every disagreement between the prototype and the standards** (a different color, spacing, variant or pattern) is reported. Default resolution: the repo's `ui_standards.md` wins and the prototype gets corrected. If the user prefers the prototype's version, that's a proposed `ui_standards.md` change (a diff), approved before it counts.

## 5. Feeding Stage 3

The UX Flow needs real component names and import paths, not visual descriptions. Use registry names for matched components and `Tmp` names for the announced new ones. Anything you couldn't reconcile with confidence goes in as an open item (UX Flow §7) rather than a guessed name, because an implementation agent trusting a wrong guess is worse than an explicit "confirm this component" flag. The UX Flow header records the Screens canvas URL, the proposal page and the screen pages the feature touches.

## 6. Integrating into the Screens canvas (Stage 4, after merge)

The screen pages show the shipped app, so a feature's screens move there only once it's merged: from the proposal page plus any deviations approved during implementation. Hand the user the integration prompt (template), listing per screen page which artboards are replaced or added; then the proposal page is deleted. Pages for new screens or flows are created with the same structure as the others (all states, all formats).
