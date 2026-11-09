# Surface Lens: iOS

Evaluate together with `android.md` when both are targets.

## Decisions to make (with real alternatives)
1. **Approach:** native (Swift + SwiftUI, UIKit where needed), shared logic with native UI (e.g. Kotlin Multiplatform), or cross-platform UI (e.g. React Native, Flutter). Same criteria as Android: team, fidelity, platform API depth, offline, performance, long-term cost.
2. **Minimum iOS version** (from the audience; check current App Store submission requirements at decision time).
3. **Architecture pattern:** e.g. MVVM / The Composable Architecture / clean layering; modularization with Swift Packages; DI.
4. **Concurrency model:** Swift concurrency (async/await, actors) conventions.
5. **Local data & offline:** e.g. SwiftData/Core Data/SQLite, Keychain for secrets, sync strategy.
6. **Push & background:** APNs, background modes and their review implications, notification categories.

## Questions to ask
- Essential platform features (HealthKit, Apple Pay, widgets, Live Activities, Sign in with Apple)? Some carry App Review obligations (e.g. offering Sign in with Apple alongside other third-party logins, in-app purchase rules for digital goods).
- iPad, Mac (Catalyst), or watchOS too?
- Who builds it?

## Production must-haves
- Crash reporting with dSYM upload per build.
- Certificates and provisioning managed reproducibly (platform-engineer); TestFlight for beta.
- Keychain for tokens; App Transport Security; privacy manifest and App Store privacy details consistent with real data collection.
- Accessibility (VoiceOver, Dynamic Type).
- Minimum supported version + forced-update path (agreed with release-manager).
- Phased release policy (release-manager).

## Red flags
Ignoring App Review rules that affect architecture (payments, login options, background modes); assuming web-view wrappers will pass review for core functionality.

## Testing options to evaluate (Mode A step 3b)
- Unit tests with the platform's frameworks (XCTest / Swift Testing).
- UI tests with XCUITest; snapshot tests for visual regression.
- Simulators for PRs; real devices or a device farm for the release matrix.
- Specific scenarios: permissions denied, background/foreground transitions, offline, Dynamic Type, VoiceOver.
- Cross-platform frameworks: their own runners plus a platform-level e2e tool.
