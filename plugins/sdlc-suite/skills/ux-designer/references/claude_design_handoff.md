# Claude Design (Path A)

Detail behind Path A in `SKILL.md`, used by default when `SDLC.md` says `claude_design: available`. Claude Design is a separate Anthropic product with its own canvas. This skill can't drive it directly: the user works there, and this skill prepares the inputs, then brings the results back and reconciles them with the repo.

Claude Design is in research preview. Treat the specifics below as "how it works today". If what you see differs, trust what you see, adapt, and tell the user about the discrepancy.

## 0. The rule that governs everything here

**`ui_standards.md` (visual language) and `ui_kit_registry.md` (components) in the repo are the source of truth.** The design system in Claude Design is a working copy built from them. When they disagree, the repo wins. A change discovered in Claude Design becomes a proposed diff to the repo files, and only counts once the user approves it.

## 1. Setting up the project's design system (Mode 0, or the first time a project uses Claude Design)

1. Prepare the inputs for the user:
   - `ui_standards.md` (tokens, typography, spacing, voice, platform conventions), as the main reference;
   - the UI kit **code**: the project's component folders from `SDLC.md` (`web_components` / `mobile_components`), and the shared UI kit's code location if the project consumes one. Claude Design can derive components and styles from a codebase during onboarding, which keeps it aligned with what developers actually import;
   - `ui_kit_registry.md`, so names match the kit;
   - brand assets (logo, fonts) if any.
2. The user creates or updates the design system in Claude Design from those inputs.
3. Record its name or link in `SDLC.md` as `claude_design_system` (shown, approved). Several projects may point to the same one, e.g. the apps that consume the same shared UI kit.
4. **Verify alignment:** compare the design system's tokens and components with `ui_standards.md` and the registry. Report any difference; the repo files win, and the design system gets corrected.
5. **Re-sync triggers:** any approved change to `ui_standards.md` or the registry, or a breaking change in a shared UI kit. When one happens, remind the user to update the design system.

## 2. Handing off a feature's prototype (Stage 1)

Give the user what they need for a good first pass in a Claude Design project using the project's design system:
- the PRD sections in scope (goals, user stories, the screens and flows, every UI state from §9 and edge case from §10);
- the agreed scope list from Stage 1, **including the new components already announced and accepted**;
- the surfaces to cover (web / Android / iOS) and any platform conventions from `ui_standards.md`;
- an explicit instruction to use only design-system components, and to flag anything new instead of improvising it.

The user iterates there, with or without you present. Your role resumes when they bring the result back.

## 3. Bringing the result back

Accept whatever the user has: a share link, an export (HTML, PDF, PPTX), screenshots, or a handoff bundle in Claude Code. Treat it as the current prototype for the Stage 2 feedback loop. Don't build a parallel code version unless the user explicitly asks for one.

## 4. Reconciling against the registry (before Stage 3, and whenever a new version comes back)

1. Match every element to `ui_kit_registry.md` (and a shared kit's public registry) by name and apparent props. A visual match isn't a prop-level match; you're working from pixels or an export, not source.
2. **Every element without a registry match is reported to the user explicitly as a new component that would have to be created** (proposed name `TmpXxx`, why it's needed, the closest existing component and why it doesn't fit). Never silently map it to a guessed existing component, and never let it into the UX Flow without the user knowing it's new.
3. **Every disagreement between the prototype and the standards** (a different color, spacing, variant or pattern) is reported. Default resolution: the repo's `ui_standards.md` wins and the prototype gets corrected. If the user prefers the prototype's version, that's a proposed `ui_standards.md` change (a diff), approved before it counts.

## 5. Feeding Stage 3

The UX Flow needs real component names and import paths, not visual descriptions. Use registry names for matched components and `Tmp` names for the announced new ones. Anything you couldn't reconcile with confidence goes in as an open item (UX Flow §7) rather than a guessed name, because an implementation agent trusting a wrong guess is worse than an explicit "confirm this component" flag.
