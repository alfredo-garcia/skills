# Surface Lens: Android

Evaluate together with `ios.md` when both are targets. The native vs cross-platform decision is usually made once for both, and the reasoning must cover both.

## Decisions to make (with real alternatives)
1. **Approach:**
   - **Native** (Kotlin + Jetpack Compose): best platform fidelity and API access, the platform's first-class tooling. Costs a second codebase if iOS is also native.
   - **Shared logic, native UI** (e.g. Kotlin Multiplatform): share domain, networking and data layers while keeping native UIs. A good fit when the logic is substantial and the UI must feel native.
   - **Cross-platform UI** (e.g. React Native, Flutter): one UI codebase. A good fit for small teams, UI-consistent products, or web-skilled teams (React Native). Costs bridging for deep platform features and dependence on the framework's cadence.
   Decide from: team skills and size, UI fidelity needs, depth of platform APIs (background work, Bluetooth, widgets, payments), offline complexity, performance needs, and the 2-3 year maintenance cost.
2. **Minimum SDK** (from the vision's audience and markets; check current Google Play target-API requirements at decision time).
3. **Architecture pattern:** e.g. MVVM/MVI with unidirectional data flow, modularization strategy, DI.
4. **Local data & offline:** e.g. Room/SQLite/DataStore, sync strategy.
5. **Background work:** WorkManager vs foreground services, respecting platform restrictions.
6. **Push:** FCM, token lifecycle, notification channels.

## Questions to ask
- Target markets and device range (low-end devices, which matters a lot in some markets)?
- Which platform features are essential (camera, location, background sync, widgets, wearables)?
- Who builds it: an Android specialist, a mobile generalist, or a web team?

## Production must-haves
- Crash reporting with release tagging; R8/ProGuard mapping upload.
- Play App Signing; build flavors per environment; secrets never in the APK.
- Encrypted storage for tokens (Keystore-backed).
- Accessibility (TalkBack, font scaling); baseline profiles/startup performance budget.
- Play Data safety form kept consistent with actual data collection.
- Minimum supported version + forced-update path (agreed with release-manager).

## Red flags
Choosing cross-platform only because "it's one codebase" when the product depends on deep native features; choosing native for both platforms with one developer and a tight timeline without acknowledging the cost.

## Testing options to evaluate (Mode A step 3b)
- Local unit tests (JVM) for view models and domain logic.
- UI tests with the toolkit's testing APIs (e.g. Compose testing) or the platform's UI testing framework; screenshot tests for visual regression.
- Instrumented tests on emulators for PRs; a device farm (hosted or in-house) for the release matrix.
- Specific scenarios: process death, permissions denied, offline, low memory, different screen sizes and font scales.
- Cross-platform frameworks: their own unit/UI test runners, plus a platform-level e2e tool.
