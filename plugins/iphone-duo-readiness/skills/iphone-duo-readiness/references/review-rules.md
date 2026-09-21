# Review rules and implementation map

HIG and preparation article rechecked September 21, 2026. The HIG page lists September 9, 2026 as its initial publication date. Linked symbol pages and videos require further consultation before implementation. Recheck current guidance during an audit; this catalog is a dated starting point, not an API availability guarantee.

Sources:

- [HIG: Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) — design intent.
- [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo) — implementation guidance.

The review targets and acceptance checks below are engineering translations, not quotations or Apple certification requirements.

## A. Geometry, continuity, and occlusion

| ID | Rule / basis | Review targets and implementation guidance | Acceptance evidence |
|---|---|---|---|
| D01 | Use available container geometry. Preparation: resizing considerations. | Inspect screen-bound calculations, cached launch dimensions, fixed root frames, device-model branches, `userInterfaceIdiom`, and orientation-driven layout. Replace layout assumptions with containing view/scene bounds and responsive constraints or traits where needed. | Main journeys remain operable through resizing, including narrow multitasking widths. |
| D02 | Preserve the user's task through layout changes. HIG: best practices. | Inspect conditional view identity, navigation paths, selected IDs, draft ownership, and initialization triggered by layout changes. Make state independent of transient presentation structure. | Enter a draft, select an item, and navigate deeply; resize and return without losing work or changing selection. |
| D03 | Evaluate compact and regular layouts as one hierarchy. HIG: dynamic layouts. | Review master/detail navigation, collapse selection, back behavior, empty detail states, and deep links. Expand useful context where appropriate without introducing different features for each display. | The same destination survives collapse/expansion; all previously available actions remain reachable. |
| D04 | Account for changing reserved regions. Preparation: reserved regions. | Inventory custom drawing, centered controls, floating buttons, overlays, and custom presentations. Separate fold divisions from camera occlusions; inspect active-region geometry in the correct coordinate space. Avoid duplicating adjustments already supplied by system containers. | Important content and hit targets remain usable while the fold activates/deactivates and the inner camera turns on/off. |
| D05 | Check asymmetric insets and bar edges. Preparation: vertical presentation. | Inspect symmetric-padding assumptions, ignored safe areas, manual edge offsets, and custom overlays. Query the system's actual bar edge when required. Background extension and interactive-content placement need separate treatment. | Test both multitasking positions; content and custom controls avoid whichever edge contains system bars. |
| D06 | Keep adaptation restrained. HIG: reserved regions. | Review grid changes and animated rearrangements. Consider even column counts where a fold divides a grid; do not impose them universally. | Repeated folding does not cause confusing control jumps or hide selected content. |

Relevant source sections: [HIG dynamic layouts](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Dynamic-layouts), [preparation resizing](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations), [reserved regions](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Adapt-to-reserved-regions-in-your-views).

## B. Containers and presentations

| ID | Rule / basis | Review targets and implementation guidance | Acceptance evidence |
|---|---|---|---|
| D07 | Prefer existing adaptive system containers. Preparation: resizing. | Inspect navigation/split/tab container ownership, Auto Layout conflicts, and custom replacements. First test existing system behavior; introducing a new container is justified by a specific gap. | Shared containers resize without broken constraints, duplicated navigation, or lost state. |
| D08 | Consider arrangement views for suitable paired content. Preparation: arrangement views. | Inventory paired horizontal/vertical panels and layered primary/secondary content. Evaluate split versus overlay semantics, axis limits, and secondary-content accessibility before replacing stacks. Keep navigation responsibility separate. Observe the documentation tension below. | Each panel remains reachable and useful in full and folded layouts, including any permitted secondary collapse. |
| D09 | Audit each presentation context independently. Preparation: vertical presentation. | Inspect inspectors, sheets, popovers, and split-view panes. Do not assume every toolbar becomes vertical. Review sheet placement overrides and custom anchors only where the observed result is unsuitable. | Open each presentation before a transition; dismiss, confirm, and interact afterward without clipping or unreachable controls. |

**Documentation tension:** The HIG says navigation containers belong outside arrangement views, and includes navigation split views as an example. The preparation article cautions against placing arrangement views inside navigation split views, lists, scroll views, or containers that can make content inaccessible. These statements do not establish a universally safe nesting recipe. Consult the current [ArrangementView](https://developer.apple.com/documentation/swiftui/arrangementview) or [UIArrangementViewController](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller) documentation and validate the specific composition before changing it. Do not automatically wrap every split-view pane in an arrangement view.

## C. Bars and actions

Apple describes side bars on the outer display and inner landscape, with horizontal bars on inner portrait. Side placement follows hardware even in RTL; multitasking can put controls on either outside edge. Prefer the system-selected placement. [HIG vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)

| ID | Review rule | Code review / implementation target | Acceptance evidence |
|---|---|---|---|
| D10 | Use container-managed bars. | Find detached `UIToolbar`, `UINavigationBar`, `UITabBar`, and custom SwiftUI bar stacks. Check navigation-container integration before adding vertical-layout code. | Bars use the expected system presentation in each context. |
| D11 | Express action semantics and grouping. | Inspect manual spacers, positional assumptions, custom Back/Close, and Done placement. Preserve logical groups and use semantic placements. | Navigation and completion actions stay discoverable; related actions retain sensible order. |
| D12 | Supply adaptable item representations. | Audit icon-only items lacking titles, text-only items, and custom-view toolbar items. Prefer title-plus-symbol where appropriate; preserve justified textual actions. | Horizontal, vertical, and overflow representations communicate the same action. |
| D13 | Define overflow priorities from actual task importance. | Map frequent actions and status badges before assigning visibility priority, first by group and then by item. | At constrained sizes, essential visible actions remain prominent and overflow actions remain accessible. |
| D14 | Choose compression according to the screen's purpose. | Evaluate destination-focused screens separately from task editors. Keep defaults unless the task benefits from prioritizing toolbar actions. | A person can both navigate and finish the current task when space is constrained. |
| D15 | Consolidate overflow and preserve action scope. | Inspect custom ellipsis menus and actions attached to the wrong pane. Route overflow into the system menu and keep pane-specific controls associated with their content. | No duplicate or missing overflow commands; each action affects the expected pane. |

Implementation basis: [bar presentation](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Optimize-bars-for-vertical-presentation), [bar items](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars). Search leads are not findings: customized bars and text actions may be intentional.

## D. Conditional work and compatibility

| ID | Applies when | Review and acceptance |
|---|---|---|
| D16 | Camera capture exists | Inspect camera selection and session handling through display transitions. Verify the intended facing direction after opening, closing, and rotation. Read [camera direction guidance](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces) before changing selection logic. Outer-display capture accessories are optional product work, not a prerequisite. |
| D17 | Game or immersive rendering exists | Review viewport/aspect updates and input-coordinate transforms. Test stable control/text sizing and reachable inputs through supported poses. Evaluate unavoidable padding as a design decision. Source: HIG best practices. |
| D18 | All apps | Record build SDK, Xcode, deployment target, and runtime coverage. The preparation guide notes different screen-space behavior for builds made with Xcode 26 or earlier. Verify the current toolchain and new-API availability; do not silently raise deployment targets. |
| D19 | All changed UI | Engineering extension: test large text, VoiceOver focus/order, long localized labels, RTL, keyboard-visible editing, and regressions on supported conventional iPhones/iPads. These checks supplement Duo guidance. |

## API lookup map

These symbols are referenced by the reviewed Apple pages. This map identifies where to investigate; it does not certify availability or provide compile-ready signatures.

| Concern | SwiftUI | UIKit |
|---|---|---|
| Fold/camera regions | `GeometryProxy.reservedRegions(kind:options:layoutDirectionBehavior:)`, `ReservedRegion` | `UIView.reservedRegions(kind:options:)`, `UIView.ReservedRegion` |
| Paired content | `ArrangementView` | `UIArrangementViewController` |
| Current vertical edge | `EnvironmentValues.toolbarVerticalEdge` | `UITraitCollection.verticalBarEdge` |
| Priority | `visibilityPriority(_:)` | `UIBarButtonItem.visibilityPriority` |
| Grouping | `ToolbarItemGroup` | `UIBarButtonItemGroup` |
| Overflow | `ToolbarOverflowMenu` | `UINavigationItem.additionalOverflowItems` |
| Compression policy | `ToolbarVerticalCompressionBehavior` | `UIVerticalBarCompressionBehavior` |

Follow the links from the preparation article or HIG to the exact declarations required by a proposed fix.

## Runtime verification matrix

Use representative journeys and risk-based combinations rather than mechanically multiplying every case. Cover:

- Closed outer display; fully open inner display in supported orientations; partially folded configurations available in Device Hub/simulator or hardware.
- Open → partially fold → close → reopen during navigation, editing, selection, and an active presentation.
- Split View multitasking in each side and representative available widths; repeat transitions that affect the changed components.
- Inner camera inactive → active → inactive where relevant; outer camera/Dynamic Island interference for affected custom UI.
- Dense toolbar content and overflow; task-focused versus destination-focused screens.
- Accessibility, localization, keyboard, and supported older-device regressions relevant to the change.

For each executed case record app build, OS/runtime, configuration, starting state, action sequence, result, and evidence. Capture unavailable cases as pending with the required environment. Use [Device Hub](https://developer.apple.com/documentation/xcode/device-hub) and [device-running guidance](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices) as needed. Screenshots demonstrate layout; interactive tests are needed to establish state continuity and action reachability.
