# Test Design Playbook

## 1. Testability: what a good acceptance criterion looks like

A criterion is testable when it has **concrete inputs, a single observable outcome, and an unambiguous pass/fail.**

| Not testable | Testable rewrite |
|---|---|
| "Search is fast" | "Given 10,000 recipes, when the user searches a 3-letter term, results appear within 500 ms at p95" |
| "Shows an error if something goes wrong" | "Given the payment provider times out after 10 s, when the user confirms payment, the order stays `pending` and the user sees the retry message" |
| "Users can share lists" | "Given a list owner, when they invite a registered email, the invitee sees the list within 1 minute and can edit items" |

Always check that the PRD specifies:
- the negative paths (invalid input, missing permission, empty state);
- the behavior when each third party fails, is slow, or returns something malformed;
- differences between surfaces, where they exist;
- measurable thresholds for NFRs.

Report anything missing as a finding for product-manager: the criterion, the problem, and a suggested rewrite.

## 2. Deriving test cases

For each criterion and requirement, consider:
- **Positive:** the happy path.
- **Negative:** invalid inputs, unauthorized users, missing data.
- **Boundaries:** limits (0, 1, max, max+1), empty and very long strings, time zones, dates at month or year ends.
- **Equivalence classes:** one representative per class of input that should behave the same.
- **State transitions:** every allowed transition, plus the forbidden ones.
- **Concurrency & idempotency:** double submit, retries from mobile clients, two devices editing at once.
- **Failure of each dependency:** timeout, error, malformed response, partial success.
- **Compatibility:** the oldest supported app version against the new backend.
- **Accessibility & localization:** where the PRD or the standards require them.

## 3. Choosing the level (the pyramid)

Test each behavior **once, at the cheapest level that can prove it:**
- **Unit:** business rules, calculations, validation, state machines. Most tests live here.
- **Integration:** persistence, queries, messaging, adapters to third parties (against doubles or sandboxes).
- **Contract:** that the backend honors what clients expect, and that clients only rely on what the backend promises.
- **UI / component:** rendering of each state in the UX Flow; interactions within one screen.
- **End-to-end:** only the critical journeys, across surfaces. Slow and brittle, so keep them few.
- **Visual regression:** key screens and components against approved baselines, where the strategy uses it.

## 4. Surfaces: what's special

- **Backend:** run integration tests against a real instance of the database engine (e.g. in containers), not a different engine; test migrations forward against realistic data.
- **Web:** component tests for states; browser e2e for critical journeys; accessibility checks automated in CI.
- **Android / iOS:** unit tests for view models and domain logic; UI tests for the UX Flow states; a defined device/OS matrix (real devices or a farm for releases, emulators/simulators for PRs); tests for process death, permissions denied, offline.
- **Cross-platform frameworks:** test shared logic once; still test each platform's integration points (permissions, push, deep links, storage).

## 5. Integrations

- **Backend ↔ clients:** contract tests on every PR that changes the API or a client's use of it; a compatibility check against the oldest supported client versions.
- **Third parties:** test doubles or recorded responses for fast PR suites; the provider's sandbox on a schedule (e.g. nightly) to catch drift; explicit tests for each failure mode the PRD specifies. Never call production third-party accounts from tests.

## 6. Tagging & traceability

Every test carries the qualified feature ID and the criterion it proves (e.g. a tag or annotation `recetas/004 AC-3`), following the convention in tech_standards §14. The traceability matrix can then be verified from the test results, not by hand.

## 7. Flaky tests

Typical causes are timing and waits, shared state between tests, order dependence, unseeded randomness, real network or clock, and animations in UI tests. Quarantine with a ticket and a deadline; fix the cause rather than adding retries; a retry that hides a real race condition is a bug, not a fix.
