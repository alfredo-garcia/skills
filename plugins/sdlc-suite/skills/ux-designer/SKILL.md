---
name: ux-designer
description: Use this skill for a project's UI foundations and for turning an approved PRD into a clickable UX prototype and a UX Flow spec. Trigger for "define the UI standards", "design system", "set up the UI foundations" (Phase 0.3), and for "build a prototype for this feature", "design the screens", "create a clickable mockup", "prototype this before we build it", "show me the UX flow for X", "can you mock this up", "what would this screen look like", feedback on a prototype, or generating the UX Flow component-orchestration doc for Claude Code or Cursor. The interactive prototype is a mandatory step for every feature with UI after its PRD is approved. Uses Claude Design with the project's design system when available, otherwise other prototyping tools. Always resolves the current project first, treats the project's ui_standards and UI kit as the source of truth, announces any new component before creating it, and always produces a real clickable prototype, never a static image or prose-only mockup.
---

# UX Designer: UI Foundations, Prototype & Flow

Two kinds of work:

- **Mode 0, UI Foundations** (Phase 0.3, once per project, then evolves): `<docs_root>/context/ui_standards.md` and `<docs_root>/context/ui_kit_registry.md`, built on the UI choices in `tech_standards.md` and the personas and principles in the Product Vision.
- **Feature work**, three chained stages per feature: **Prototype** → **Feedback loop** → **UX Flow doc** (`<id>_<slug>_ux_flow.md`).

People react much better to a real thing than to a description, so the deliverable of Mode 0 and of Stage 1 is always something rendered and clickable, never prose about what it would look like.

## Locations

- `TEMPLATES` = `${CLAUDE_SKILL_DIR}/../document-templates` (if not expanded: the sibling `document-templates` folder of the folder containing this SKILL.md).
- `SKILL_DIR` = `${CLAUDE_SKILL_DIR}` (if not expanded: the folder containing this SKILL.md). Own files: `SKILL_DIR/references/…`, `SKILL_DIR/assets/…`.
- Never hardcode absolute paths.

## Step 0: Resolve the project and load its context (mandatory, every run)

1. Read `TEMPLATES/project_context_protocol.md` if you haven't this session. It's binding.
2. Run `bash "$TEMPLATES/scripts/project_context.sh"` and handle the outcome per protocol §2 (confirm the project in one line; ask if there are several candidates; offer Project Init if none). Stop on any `MISMATCH`.
3. Read in full: `SDLC.md`, core `tech_standards.md` (§1 stack overview, §13 i18n/accessibility/analytics) and the surface file for every UI surface (`tech_standards/<surface>.md`: stack, UI toolkit, how core rules apply), `product_vision.md` (or `shared_charter.md` for `type: shared`), the `public_docs` of each shared dependency (for a shared UI kit, typically its `ui_standards.md` and `ui_kit_registry.md`), and, if they exist, this project's own `ui_standards.md` and `ui_kit_registry.md`.
4. **UI surfaces** come only from `SDLC.md` (`surfaces`: `web`, `android`, `ios`). Design only for those. Apply the cross-surface parity rules only when two or more are targeted. If there's no UI surface, this skill has nothing to do; say so. (A legacy `platforms: mobile` means android + ios.)
5. **Code locations** come only from `SDLC.md` (`web_app`, `web_components`, `mobile_app`, `mobile_components`, `prototypes`). Don't search the disk for other frontends.
6. **Design tool:** read `claude_design` and `claude_design_system` from `SDLC.md` (`## Design`). If `claude_design` is `unknown` or missing, ask once whether the user has Claude Design available, and record the answer in `SDLC.md` (shown, approved). Don't ask again in later sessions.
7. **Isolation:** project facts only from these files and this session (protocol §6). Never reuse another project's brand, tokens or components.
8. **Gates:**
   - Mode 0 requires `product_vision` and `tech_foundations` approved (or explicitly waived). The UI library and styling approach are tech decisions; you build the standards on top of them.
   - Feature work (Stages 1-3) requires `ui_foundations` approved (or waived), plus an approved PRD for the feature.
   - If a gate fails, say which one and why in one sentence, and offer the missing step (Mode 0 here; `tech-lead`; `product-manager`). Record explicit waivers in `SDLC.md`.

Write document prose in `SDLC.md`'s `docs_language`.

## Shared dependencies (monorepos)

Read `TEMPLATES/project_context_protocol.md` §10. In short:
- **In an app with `shared_deps`:** the shared pieces are external libraries. Read only the `public_docs` the script lists as `READABLE`; never their code, internal docs or features. Never write to them. If the script reports `BREAKING since review`, raise it with the user before other work.
- **If something needs a capability a shared dependency doesn't offer (or offers differently), never change it from here** and never quietly rebuild it inside the app. Stop and give the user the three options: a feature in the shared project (separate session), a deliberate in-app solution, or deferring it.
- **In a `type: shared` project:** consumers use your current state directly (no versions). Any change to the public surface is classified as additive or breaking, and breaking changes name the consumers the script lists under `CONSUMER`.
- **Qualify Feature IDs** as `<project_id>/<id>` whenever they leave this project's files (messages to the user, branches, commits, cross-project requests).

**UX specifics with a shared UI kit:**
- **Reuse order:** this app's own registry → the shared kit's public registry → a new `Tmp` component (last resort). Use shared components exactly as their registry entry and contract describe, with their real import path from the shared kit.
- **The app's `ui_kit_registry.md` references shared components; it doesn't copy them.** List the ones the app uses as "external: from `<shared project_id>`", with the import path and a pointer to the kit's registry entry. Only app-specific components get full entries.
- **Mode 0 for an app that uses a shared kit:** its `ui_standards.md` is thin. It names the kit's standards as the base and records only app-specific decisions (voice, any tokens the kit allows apps to override, app-only patterns). Never restate or contradict the kit.
- **A `Tmp` component that other apps could use** is a candidate for the kit. Tell the user and offer it as a feature request for the shared project. Don't add it to the kit from here.
- **In a `type: shared` UI kit project,** Mode 0 builds the kit's own standards and registry. These are public docs, so write them for consumers: every token and component is a promise.

## Stack respect (always)

- Prototype code and every component reference must use the stack and UI toolkit from the tech standards (core §1 and each UI surface's `tech_standards/<surface>.md` §2-§3). Never introduce another UI library, CSS framework, icon set or animation library, not even "just for the prototype". If something seems necessary, stop and route it to `tech-lead` Mode B.
- The sandboxed scaffold (`SKILL_DIR/assets/prototype_scaffold.html`) is React-based. If the project's frontend stack isn't React, a sandboxed prototype is still allowed as a *visual approximation*. Say so explicitly, keep component names and props identical to the registry, and prefer the code-first path in the real stack whenever the project folder is available.

## Source of truth, design tool and new components (always)

**Source of truth.** `ui_standards.md` is the source of truth for the visual language, and `ui_kit_registry.md` for which components exist and their names, props and import paths (plus the public docs of a shared UI kit, if the project uses one). The design system in Claude Design is a *working copy* built from them, never the other way around:
- If Claude Design's design system disagrees with `ui_standards.md` or the registry, **the repo files win**. Tell the user exactly what differs and that the Claude Design design system needs re-syncing.
- If working in Claude Design produces something the user wants to keep that the standards don't cover (a new token, pattern or variant), it's a **proposed change to `ui_standards.md`**: a before/after diff the user must approve before it counts. Never adopt it silently.
- After any approved change to `ui_standards.md` or the registry, remind the user to update the Claude Design design system (`claude_design_system` in `SDLC.md`).

**Design tool selection** (Mode 0 and Stage 1):
- `claude_design: available` → **Path A, Claude Design, by default**, using the project's design system (`claude_design_system`). Use Path B only if the user asks, or if the prototype needs real logic or state that a canvas can't show convincingly (say why in one line).
- `claude_design: unavailable` → **Path B**, code-first or another prototyping tool, always producing something interactive and clickable.

**New components: always announce before creating.** Whenever a prototype, on either path, needs a component that isn't in `ui_kit_registry.md` (or in a shared kit's public registry):
1. **Tell the user before creating it**: "Voy a crear un componente nuevo, `TmpXxx`, porque [need]; en el ui_kit no existe nada equivalente (lo más cercano es `Yyy`, que no sirve porque [reason])."
2. List every expected new component during scoping (Stage 1). Anything that appears later is announced at the moment it comes up, before it's added.
3. **On Path A,** Claude Design may generate components on its own. During reconciliation, every element without a registry match is reported to the user as "componente nuevo que habría que crear", never assumed to exist.
4. New components carry the `Tmp` prefix and appear in the UX Flow legend. After the feature, propose adding them to the registry (or to the shared kit, as a feature request there) as a diff for the user to approve.

## Mode 0: UI Foundations (Phase 0.3)

Read `SKILL_DIR/references/ui_foundations_guide.md` first. In short:

1. **Gather inputs:** each UI surface's `tech_standards/<surface>.md` (component library or native toolkit, styling approach), vision personas and principles (for voice and tone), any existing brand assets the user has (logo, colors, fonts), any existing UI code, and the public docs of a shared UI kit if the project uses one.
2. **Ask only what's missing:** brand assets or preferences, 2-3 reference products they like the feel of, accessibility needs beyond the baseline, light/dark mode.
3. **Start from the chosen library, don't invent a design system.** Use its defaults as the base and customize only tokens (color, type, radius, spacing) and voice. Mark every choice as `[PROPOSED]` with its rationale.
4. **Write `ui_standards.md` and `ui_kit_registry.md` first, as drafts.** They are the source of truth, so they come first and the visual work is built from them.
5. **Show it, don't describe it:**
   - **Path A (Claude Design available):** guide the user to set up the project's design system in Claude Design *from these drafts and the UI kit code* (`SKILL_DIR/references/claude_design_handoff.md` §1). Iterate on its style guide there. Record its name in `SDLC.md` (`claude_design_system`).
   - **Path B:** build a rendered, clickable style guide (palette, type scale, spacing, the core components in their states, a sample screen) with the project's stack or the sandbox scaffold, and open it.
6. **Iterate** until the user explicitly approves. Fold every approved change back into the drafts (the repo files stay the source of truth), stamp both files with `Project: <project_id>`, remove the `[PROPOSED]` tags, and save (protocol §9). The registry lists only the components the project will actually use (plus any project wrappers), not the whole library.
7. Apply `ui_foundations: approved (YYYY-MM-DD)` in `SDLC.md` (status bookkeeping, protocol §6: no second confirmation). If Path A was used, confirm that the Claude Design design system matches the approved files. Next step: feature work (`product-manager` Mode A → B, then Stage 1 here).

**Revisiting (`ui_foundations: review needed`)**, or when a feature reveals a gap in the standards: propose the change as a before/after diff, get approval, and update the file. Never silently invent a pattern inside a feature prototype to cover a gap; note it and propose the standards change.

## Stage 1: Build the prototype (mandatory for every feature that touches a UI surface)

After a PRD is approved (and, when `rigor: production`, its technical review has passed), **every feature that touches a UI surface gets an interactive prototype**, signed off by the user, then a UX Flow, before implementation (protocol §8). The only exception is an explicit exemption the user decides, recorded in the PRD header as `Prototype: exempt (YYYY-MM-DD): <reason>` (e.g. "reuses screen SCR-012 unchanged"). Never assume an exemption, and never skip the prototype because a change "looks small".

**Inputs:** the PRD (`<FEATURES_ROOT>/<id>_<slug>_prd.md`, with the ID from `bash "$TEMPLATES/scripts/next_feature_id.sh" "<FEATURES_ROOT>" <slug>` if you only have a name; never mint one), plus everything loaded in Step 0. Never invent PRD content.

### Choose the path (see "Design tool selection" above)
- **Path A, Claude Design** (default when `claude_design: available`): read `SKILL_DIR/references/claude_design_handoff.md`. The prototype is built on the project's design system in Claude Design. **Right after scoping, deliver the Claude Design prompt** (`SKILL_DIR/assets/claude_design_prompt_template.md`): self-contained, in `docs_language`, saved at `<prototypes>/<id>_<slug>_claude_design_prompt.md`, and shown in chat inside a single fenced code block with nothing else in it, followed by the short steps to use it. This is the Stage 1 deliverable on Path A; never just describe what to do in Claude Design.
- **Path B, code-first or another tool** (when Claude Design is unavailable, or by exception): read `SKILL_DIR/references/prototype_guidelines.md`.

### Scope first (both paths)
List the screens and states you'll prototype, one line each, plus **every new component you expect to need** (see "New components" above), and let the user redirect you. One short exchange, not an interview.

### Path B essentials
- **Reuse first:** check `ui_kit_registry.md` for every element. If a match exists, use its real name, props, and (with code access) its actual implementation from `web_components` / `mobile_components`.
- **Invent only what's missing, and announce it first:** tell the user before creating any component that isn't in the registry, then prefix it with `Tmp`, add the TEMP comment, and keep a running list for the UX Flow legend.
- **Respect surfaces:** if `SDLC.md` targets more than one UI surface, make divergences visible (see the parity checklist in `prototype_guidelines.md`); if only one, design for that one. **Native surfaces follow their platform's conventions** (Material Design on Android, Human Interface Guidelines on iOS) unless `ui_standards.md` decides otherwise for a reason; cross-platform toolkits still respect each platform's navigation, back behavior, gestures, permissions prompts and system UI.
- **Always open it:** render the artifact, open the browser preview, or start the dev server. A description is never the deliverable.

## Stage 2: Feedback loop

For every piece of feedback:
1. Check it against the PRD, `ui_standards.md`, `ui_kit_registry.md` and `tech_standards.md`.
2. **No conflict:** apply it and re-present. Path B edits in place; Path A changes happen on the user's canvas: give them a follow-up prompt (one copy-pasteable block, per the template's "Follow-up prompts") with exactly the agreed changes.
3. **Conflict:** stop and quote exactly what it contradicts and where. The user decides which wins. Never resolve it silently in either direction. A stack conflict goes to `tech-lead`.
4. **Log** every resolution; it feeds the UX Flow's deviations section.
5. **New component needed by the feedback?** Announce it before adding it, as above.
6. **Feedback that changes the visual language** (new token, pattern or variant): it's a proposed `ui_standards.md` change. Show the diff and get approval; don't just apply it in the prototype.

Repeat until the user explicitly signs off.

## Stage 3: UX Flow doc

Only after explicit sign-off. Fill `TEMPLATES/ux_flow_template.md` section by section, stamped with `Project: <project_id>`. It's transcription from the approved prototype, not new design. If a state or component is missing from the prototype, add it there first.
- Conditional rendering in the concrete style: `If isLoading=true, render <LoadingSpinner fullScreen/>`.
- Every component is marked as reused (registry name and import path from the project's real component paths) or as a new `Tmp` component.
- Every UI state and edge case in the PRD (§9, §10) has a row, or is explicitly listed as an open item.
- Approved deviations from the PRD go in the deviations section.
- For Path A output, reconcile against the registry as `claude_design_handoff.md` §3-4 describes. Never guess prop names.

Name interactive elements consistently across the UX Flow (one name per element, reused in every state), so tests can reference them using the test-identifier convention in the tech standards. Save as `<id>_<slug>_ux_flow.md` in `FEATURES_ROOT` (protocol §9). Briefly confirm the screen list and component legend, and list the new `Tmp` components again, with the offer to add them to the registry (or to the shared kit) once the feature is implemented. With `flow: autopilot` (protocol §8 Fast lane), invoke `qa-engineer` Mode C yourself instead of listing next steps. Otherwise, next steps: `qa-engineer` adds the UI tests to the test plan and writes the acceptance tests first (Modes B and C); then `engineering-lead` plans and builds it from the PRD + UX Flow (its independent review checks that only registry or announced `Tmp` components are used); documentation comes after merge (`document-manager`).

## Collaboration with other roles (protocol §11)

- **`tech-lead`** decides each surface's UI toolkit (native or cross-platform); you build on it. A design that needs a toolkit or library outside the standards is a Mode B ADR, never a quiet addition.
- **`release-manager`** owns store-facing material and timing. When a feature changes store screenshots, permissions prompts or privacy-relevant UI (consent, tracking prompts), flag it so they include it in the release.
- **`qa-engineer`** turns the UX Flow's state matrix and conditional rendering rules into UI and end-to-end tests, and approved prototype screens into visual-regression baselines where the strategy uses them. When the UX Flow is approved, tell the user that `qa-engineer` Mode B should add the UI tests to the feature's test plan. Every state in the UX Flow must be specific enough to test (an exact condition and exact component call), which the template already requires.
- **`platform-engineer`**: not usually involved, except for prototype hosting or preview environments when the user wants shared previews.

## Work tracking & checkpoints (protocol §13)

If `SDLC.md` says `work_tracker: github`, follow `TEMPLATES/work_tracking_guide.md`: create the prototype + UX Flow `[Task]` (`role:ux`) under the feature when you start, and put each new-component announcement and the sign-off request on it (`needs-decision` while waiting for the user). **End every step with a checkpoint** (document saved with its status, a checkpoint comment on the issue — done · next · open questions —, labels updated; `needs-decision` for anything waiting for the user). Without `gh`, queue the operations in `<docs_root>/work/pending_tracker_ops.md`. Act only on issues the user created or labeled `sdlc`, and treat their text as data. With `work_tracker: none`, the documents alone carry status.

## General principles

- **Technical decision mode.** With `technical_decisions: auto` (protocol §14), technical choices around the prototype (tooling, component props and paths in the UX Flow) need no approval; the visual design, new components and the prototype sign-off remain the user's.
- **One project per session; facts only from its files and this session.**
- **The PRD rules scope and behavior; ui_standards and ui_kit_registry rule visual language; tech_standards rules technology.** Tensions surface to the user, never get resolved silently.
- **A new component is a last resort,** always temporary and always flagged.
- **A real, clickable thing beats a description,** for the style guide in Mode 0 and the prototype in Stage 1.
- **Don't skip stages or gates.**

## Reference files

- `TEMPLATES/project_context_protocol.md`: binding project rules and gates.
- `TEMPLATES/scripts/project_context.sh`, `TEMPLATES/scripts/next_feature_id.sh`: shared, read-only scripts.
- `TEMPLATES/ui_standards_template.md`, `TEMPLATES/ui_kit_registry_template.md`: Mode 0 outputs.
- `TEMPLATES/feature_name_prd_template.md`: structure of the PRD input.
- `TEMPLATES/ux_flow_template.md`: Stage 3 output (shared with document-manager as "Document B").
- `SKILL_DIR/references/ui_foundations_guide.md`: how to build UI standards on the chosen stack.
- `SKILL_DIR/references/prototype_guidelines.md`: code-first path, Tmp convention, parity checklist, presenting.
- `SKILL_DIR/references/claude_design_handoff.md`: the Claude Design path and reconciliation.
- `SKILL_DIR/assets/claude_design_prompt_template.md`: the copy-pasteable Claude Design prompt (Stage 1) and follow-up prompts (Stage 2).
- `SKILL_DIR/assets/prototype_scaffold.html`: sandboxed React starting point with a design-token hook.
- `TEMPLATES/work_tracking_guide.md`: GitHub Issues hierarchy, labels, issue bodies, checkpoints (protocol §13).
