# Repository audit guide

## Discover the app and its build context

Read applicable repository instructions (CLAUDE.md, AGENTS.md) and inspect working-tree status. Identify the app's documented build command, app targets, schemes, configurations, dependencies, and source roots. Include Objective-C, storyboards, and XIBs in legacy UIKit apps. For React Native, Flutter, or other cross-platform apps, trace layout and state through the framework and native host.

Start with tracked/nonignored project files; include relevant ignored configuration only when necessary. Do not dump credentials or signing secrets from configuration files.

```sh
git status --short
rg --files -g 'CLAUDE.md' -g 'AGENTS.md' -g '*.xcodeproj/project.pbxproj' -g '*.xcworkspace/contents.xcworkspacedata' -g '*.xcscheme' -g '*.xcconfig' -g '*Info.plist' -g 'Package.swift' -g 'Package.resolved' -g 'Podfile*' -g 'Cartfile*' -g 'project.yml' -g 'Tuist.swift' -g 'Project.swift' -g 'package.json' -g 'pubspec.yaml'
xcodebuild -version
xcodebuild -showsdks
xcrun simctl list devices available
```

Inspect `SDKROOT`, `IPHONEOS_DEPLOYMENT_TARGET`, `TARGETED_DEVICE_FAMILY`, supported orientations, scene configuration, launch screen, and any full-screen compatibility settings. Resolve settings for the actual app target/configuration, including generated Info.plist values and xcconfig overrides. Treat these as context: do not require iPad support, new scenes, a newer deployment target, or every orientation merely because Duo support is requested.

Use the repository's build workflow. If it has none, list schemes for the identified project/workspace, choose an app scheme and an installed destination, and run a simulator build with DerivedData in a temporary directory. Avoid guessing scheme names or installing runtimes as part of the audit. A listing or dependency-resolution error is an environment limitation, not a Duo defect. Report the exact command and outcome; if compilation is blocked, complete the source review.

## Search leads, then trace behavior

Run searches in app-owned source directories once discovered. Exclude generated output and vendored dependencies from initial findings; inspect dependency integration when it owns affected UI. These commands are examples for native sources, not a completeness test. `rg` exit status 1 means no matches.

```sh
# D01–D06: geometry, traits, state, insets, reserved regions
rg -n -g '*.{swift,m,mm,h}' 'UIScreen|mainScreen|nativeBounds|userInterfaceIdiom|UI_USER_INTERFACE_IDIOM|UIDeviceOrientation|UIInterfaceOrientation|horizontalSizeClass|verticalSizeClass|safeAreaInsets|ignoresSafeArea|edgesIgnoringSafeArea|reservedRegions' .
rg -n -g '*.swift' 'NavigationPath|NavigationStack|NavigationSplitView|@State|@StateObject|\.id\(|onAppear|onChange|GeometryReader|\.frame\(' .
rg -n -g '*.{swift,m,mm,h}' 'viewWillTransition|traitCollectionDidChange|registerForTraitChanges|viewDidLayoutSubviews|layoutSubviews|preferredContentSize' .

# D07–D15: containers, bars, actions, presentations
rg -n -g '*.{swift,m,mm,h}' 'UINavigationController|UISplitViewController|UITabBarController|UIToolbar|UINavigationBar|UITabBar|UIBarButtonItem|toolbar|ToolbarItem|TabView|sheet\(|popover\(|presentation|ArrangementView|UIArrangementViewController' .
rg -n -g '*.{storyboard,xib}' 'navigationController|splitViewController|tabBarController|toolbar|barButtonItem|constraint|autoresizingMask|safeArea' .

# D16–D17: conditional camera/rendering paths
rg -n -g '*.{swift,m,mm,h}' 'AVCapture|UIImagePickerController|ARSession|MTKView|CAMetalLayer|SKView|SCNView|GLKView' .
```

Trace the containing scene/view, callers, and affected journey before classifying a match. An icon frame, a cached image size, or a non-layout idiom check is not a defect. A system container's presence also does not prove its content adapts. Check how custom wrappers constrain it and where selection, navigation, drafts, scroll position, and ongoing operations live.

For each suspected issue, identify the trigger and follow the code path that produces the symptom. A source-level gap needs a concrete causal argument; otherwise mark it for runtime verification. Capture file/line or symbol references from the actual checkout. Consolidate shared constants and containers into one proposed change with all affected screens listed.

## Verify platform details at the point of use

Read the linked Apple preparation/HIG pages and the exact symbol documentation needed for proposed changes. If Apple's HTML only returns a JavaScript shell, try the documentation page's linked Markdown representation; DocC JSON can also expose HIG content. Do not interpret a failed fetch as evidence that the feature does not exist. If sources remain unavailable, disclose that the catalog could not be revalidated and continue with source-backed app findings.

Use `xcrun --sdk iphonesimulator --show-sdk-path` to locate the selected SDK. Inspect relevant UIKit headers or SwiftUI interfaces for declarations and availability when proposing APIs. Distinguish an API missing from an older local SDK from an API absent from current Apple documentation. Never guess availability annotations or fabricate a fold angle, device model identifier, or simulator control. Preserve older-OS behavior when implementation is requested.

## Turn the audit into actionable work

Map representative journeys to the applicable rule IDs. Include entry points, navigation depth, editing, sheets/popovers, custom bars, and domain-specific UI actually present. For each proposed fix, supply its owner, dependencies, observable acceptance check, and evidence basis. Keep optional redesigns separate from work needed to resolve an actual gap.

Use the runtime matrix in the rule catalog. Ordinary simulator rotation/resizing can establish general adaptive-layout behavior, but it does not verify Duo fold regions, camera occlusion, display transitions, or vertical bars. If a Duo runtime/device is unavailable, explicitly leave those checks pending. Verify transitions with an in-progress task and assert retained state and reachable actions; static screenshots alone cannot establish either.

Report tools/environments used and checks actually executed. Do not silently turn an audit into app edits, dependency upgrades, signing changes, or a deployment-target migration. If fixes were also requested, implement the scoped findings and verify them using the same acceptance checks.
