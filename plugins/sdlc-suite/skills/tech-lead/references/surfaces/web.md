# Surface Lens: Web

## Decisions to make (with real alternatives)
1. **Rendering model:** SSR/hybrid (SEO, fast first paint, authenticated apps with server sessions), SSG (content sites), SPA (app-like experience behind login, no SEO needs). Decide from the vision: public discoverability, personas' devices and networks.
2. **Framework:** what the team knows. Check fit with the rendering model and the hosting options (decided with platform-engineer).
3. **Styling & components:** the component library/approach. This is the base for ux-designer's UI foundations. If a shared ui-kit exists in the repo, evaluate consuming it (Mode B ADR).
4. **Data fetching & state:** server state vs client state, cache strategy, and how generated API clients are used.
5. **Auth in the browser:** HttpOnly secure cookies + CSRF protection (preferred for first-party), vs tokens. Never long-lived tokens in localStorage.
6. **Is web the admin/backoffice too?** If so, decide whether it's the same app or a separate surface.

## Questions to ask
- Does any part need SEO or social sharing previews?
- Browsers and devices to support? Accessibility obligations?
- Offline or PWA needs (a real requirement, not "nice to have")?
- Internationalization at launch?

## Production must-haves
- CSP, secure headers, dependency scanning.
- Core Web Vitals budget; bundle-size budget enforced in CI.
- Error reporting with source maps uploaded per release.
- Analytics with consent gating; WCAG AA accessibility testing.

## Red flags
Micro-frontends for one team; a custom design system from scratch when a library fits; client-side-only rendering for SEO-critical pages.

## Testing options to evaluate (Mode A step 3b)
- Unit and component tests with the framework's recommended runner and a DOM testing library.
- End-to-end in real browsers (pick one framework; define the browser matrix for PR vs release).
- Visual regression on key screens and components (hosted service vs self-hosted snapshots).
- Accessibility checks automated in component and e2e tests.
- API mocking for component tests generated from the API schema, so mocks can't drift from the contract.
