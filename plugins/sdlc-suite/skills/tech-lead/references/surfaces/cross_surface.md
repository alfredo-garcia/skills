# Cross-Surface Lens

Read whenever a project has 2+ surfaces. These decisions belong to no single surface, so they're where heterogeneous platforms usually fail. Each one ends up in core `tech_standards.md`.

1. **One contract, many clients.** A single API schema (e.g. OpenAPI) as the source of truth; generated clients for web/android/ios; contract tests in CI; breaking-change detection on the schema.
2. **Deployed clients can't be recalled.** Mobile apps in users' hands run old code for months. Decide with release-manager:
   - the compatibility window (e.g. "the backend supports the last N app versions / X months");
   - additive-only changes by default; expand → migrate → contract for anything breaking;
   - minimum supported version + forced/optional update mechanism;
   - server-driven kill switches for risky features.
3. **Identity across surfaces:** one identity provider; session models per surface (cookies on web, tokens in secure storage on mobile); logout and revocation everywhere; account linking.
4. **Shared domain logic:** where business rules live. Default: server-side, with clients thin. If offline requires client-side rules, decide how they stay in sync (shared code via KMP, a rules schema, or duplication with contract tests).
5. **Notifications & deep links:** one routing scheme across web, Android App Links and iOS Universal Links; push payloads that carry deep links; per-platform channel/category mapping.
6. **Analytics identity & taxonomy:** one event taxonomy for all surfaces, the same names and properties; cross-device identity stitching; consent per platform.
7. **Feature flags across surfaces:** the same flag evaluated consistently; server-driven where possible; clients with cached defaults when offline.
8. **Observability across surfaces:** trace context propagated from client to backend; the same correlation ID in client logs and server logs; release/version tags on every event and crash.
9. **Localization:** shared string keys or a shared translation pipeline; server-sent texts vs client strings.
10. **Design consistency vs platform conventions:** agree with ux-designer which patterns are shared and which follow Material / Human Interface Guidelines.
11. **Release coordination:** backend first, then clients; flags to decouple deploy from release; record it in release_process §7.
12. **Integration testing across surfaces** (decided in Mode A step 3b, recorded in core tech_standards §14):
    - Contract approach between backend and every client, run on every PR that touches the API or its use.
    - Compatibility: the new backend tested against the oldest supported app versions (recorded fixtures of their requests, or contract versions), per release_process §7.
    - Third parties: one approach per provider (sandbox, doubles, recorded responses), plus explicit failure-mode tests; never production accounts from tests.
    - End-to-end across surfaces only for the critical journeys; everything else at lower levels.
    - One tagging convention for every surface, so the traceability matrix is computed the same way everywhere.

