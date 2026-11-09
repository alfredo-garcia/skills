# Template: UI Standards / Design & Brand Guidelines

> **What this is:** the single source of truth for the product's visual language and platform
> conventions — brand tone, color, type, spacing, motion, accessibility minimums, and how web and
> mobile idioms map to each other. It owns **how things look and feel**, never **what they do** —
> that's the Master Functional Documentation's job (see `master_functional_spec_template.md`).
>
> **Produced/maintained by:** typically the design/brand team, hand-authored or exported from a
> design tool. If a project has none yet, the `ux-designer` skill can bootstrap a first draft from
> this template (see that skill's `SKILL.md` Step 0) — clearly marked as a starting point for the
> design team to review, not a substitute for their sign-off.
>
> **Consumed by:** the `ux-designer` skill (loaded in full before designing a single screen; drives
> both the prototype's visual tokens and its web/mobile parity checklist) and, indirectly, anyone
> reading `ui_kit_registry.md` entries that reference tokens defined here.
>
> **Never referenced by:** `document-manager`'s output — the Master Functional Documentation links
> to this file by name only and never restates its contents.
>
> **Real instance lives at:** `<docs_root>/context/ui_standards.md` (see
> `project_context_protocol.md` §3). Built by `ux-designer` Mode 0 (Phase 0.3) on top of the UI
> implementation choices in the per-surface tech standards (`tech_standards/<surface>.md` §2-§3). A real instance starts with a header block:
> `# UI Standards: [Product Name]`, then `> Project: \`<project_id>\``, then
> `> Status: Draft / Approved (YYYY-MM-DD)`. Prose in the project's `docs_language`.


> **Surface notation:** `Platform:` fields use the project's UI surfaces from `SDLC.md` (`surfaces`): `Web`, `Android`, `iOS`, `Mobile` (= Android and iOS behaving identically) or `All`. Only surfaces the project targets may appear.

---

## 1. Brand Voice & Tone

- **Personality:** [3-5 adjectives that describe how the product should feel, e.g. "confident, warm, unfussy." Avoid vague marketing language — each adjective should be specific enough to rule something out.]
- **Voice in UI copy:** [how the product talks to users — formal vs. casual, first-person vs. second-person, how errors/empty-states are worded. Give one good and one bad example sentence.]
- **What to avoid:** [tonal anti-patterns — e.g. "never use exclamation points in error messages," "no jokes in destructive-action confirmations."]

## 2. Color Tokens

Every color used anywhere in the product should trace to a named token here, not a raw hex value picked ad hoc in a screen or component.

| Token | Value (light) | Value (dark, if applicable) | Usage |
|---|---|---|---|
| `color.primary.500` | `#...` | `#...` | Primary actions, brand accents |
| `color.neutral.100` | `#...` | `#...` | Backgrounds |
| `color.danger.500` | `#...` | `#...` | Destructive actions, error states |
| `color.success.500` | `#...` | `#...` | Confirmation states |

- **Contrast requirements:** [minimum contrast ratio for text on background, e.g. WCAG AA 4.5:1 for body text, 3:1 for large text — see §8.]
- **Semantic vs. raw tokens:** [if the system distinguishes raw palette tokens (`blue.500`) from semantic ones (`color.primary.500`), explain the mapping and state which one components/prototypes should reference.]

## 3. Typography

- **Font families:** [primary typeface, fallback stack, and platform-specific equivalents if web/iOS/Android use different system fonts.]

| Style name | Size | Weight | Line height | Usage |
|---|---|---|---|---|
| `display` | ... | ... | ... | Hero/marketing headers |
| `heading-1` | ... | ... | ... | Screen titles |
| `body` | ... | ... | ... | Default paragraph/UI text |
| `caption` | ... | ... | ... | Secondary/metadata text |

- **Platform-specific stacks:** [web font-family declaration vs. iOS/Android system font names, if they differ.]

## 4. Spacing & Layout Scale

- **Base unit:** [e.g. 4px/8px base grid.]
- **Scale:** [named steps, e.g. `space.xs = 4px`, `space.sm = 8px`, `space.md = 16px`, `space.lg = 24px`, `space.xl = 32px` — enough steps to cover every real layout decision without needing an arbitrary in-between value.]
- **Breakpoints (web):** [named breakpoints and their pixel widths, e.g. `mobile <640px`, `tablet 640-1024px`, `desktop >1024px`.]
- **Grid:** [column count, gutter width, margin, per breakpoint if it varies.]

## 5. Iconography

- **Icon set/library:** [name of the icon library or custom set in use.]
- **Sizing:** [standard icon sizes, e.g. 16/20/24px, and when each is used.]
- **Stroke/fill style:** [outline vs. filled, consistent stroke width.]

## 6. Elevation, Shadow & Radius

| Token | Value | Usage |
|---|---|---|
| `radius.sm` | ... | Small controls (chips, tags) |
| `radius.md` | ... | Cards, inputs |
| `elevation.1` | ... | Resting cards |
| `elevation.3` | ... | Modals, popovers |

## 7. Motion & Animation Principles

- **Duration scale:** [named durations, e.g. `duration.fast = 100ms`, `duration.base = 200ms`, `duration.slow = 320ms`.]
- **Easing curves:** [named easing functions and when each applies — entrance vs. exit, e.g. ease-out for entrances, ease-in for exits.]
- **When to animate vs. not:** [principles, e.g. "state changes that affect layout should animate; purely cosmetic hover changes should not," "respect `prefers-reduced-motion`."]

## 8. Accessibility Standards

- **Contrast minimums:** [WCAG level targeted, e.g. AA; specific ratios for text sizes.]
- **Minimum touch target size:** [e.g. 44x44pt iOS / 48x48dp Android / 44x44px web — this is a hard constraint the `ux-designer` skill holds mobile prototypes to even when the web version is visually denser.]
- **Focus states:** [what a keyboard-focus indicator must look like; never rely on color alone.]
- **Screen reader conventions:** [labeling patterns for icon-only buttons, image alt-text conventions, live-region usage for dynamic content.]
- **Motion sensitivity:** [reduced-motion fallback behavior.]

## 9. Platform Conventions (Web vs. Mobile)

This section is read directly by the `ux-designer` skill's cross-surface parity checklist — where this section is silent on a point, that checklist falls back to its own defaults, so filling this in precisely prevents guessed parity decisions.

- **Primary interaction model:** [hover-and-click on web vs. touch-only on mobile — state explicitly how hover-revealed affordances (tooltips, hover-to-show buttons) should degrade on touch: always-visible, long-press, or a swipe action.]
- **Navigation container:** [web pattern (e.g. top tab bar / sidebar) and its mobile equivalent (e.g. bottom tab bar / stack navigation) — state which maps to which.]
- **Overlays:** [web modal/dialog pattern and its mobile equivalent (bottom sheet, full-screen takeover) — state when each is used on each platform.]
- **Gestures (mobile-only):** [swipe-to-dismiss, pull-to-refresh, long-press, and any other native gesture patterns in use, with no web equivalent expected.]
- **Divergence is the exception:** platform differences should be called out only where they're real; don't pad every convention with "same on both platforms."

## 10. Design Token Naming Convention

- **Token naming pattern:** [e.g. `category.variant.step`, such as `color.primary.500`, `space.md`, `radius.sm`.]
- **CSS custom property mapping:** [how a token name maps to a CSS variable, e.g. `color.primary.500` → `--color-primary-500`. This mapping is read directly by prototyping tools (e.g. `ux-designer`'s scaffold) to translate tokens into a working stylesheet.]
- **Platform-native equivalents:** [if iOS/Android use a different token format (e.g. asset catalogs, XML resources), note the mapping or the source of truth for each platform.]

## 11. Do's and Don'ts

A short list of concrete, product-specific rules that don't fit neatly into the categories above but matter enough to call out explicitly (e.g. "never use pure black `#000` for text — use `color.neutral.900`," "destructive actions are always `color.danger.500`, never a plain red picked ad hoc").

## 12. Versioning

- **Last updated:** [date]
- **Owner:** [team/person who approves changes to this file]
- Note any recent breaking changes (e.g. a token rename) that consumers should be aware of.
