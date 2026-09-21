---
name: iphone-duo-readiness
description: Audit an iOS app for iPhone Duo (foldable iPhone) support and produce a prioritized, evidence-backed implementation plan covering resizing, state continuity, reserved regions, arrangement views, and vertical bars. Use whenever the user mentions iPhone Duo, a foldable or folding iPhone, fold/hinge layout, inner or outer display, reserved regions, or asks what the app needs in order to be ready for that form factor — including when they ask to implement those fixes. Not for general iOS code review or ordinary iPad/size-class adaptation work.
---

# iPhone Duo readiness

Review the existing app and produce an evidence-backed implementation map. Use [the rule catalog](references/review-rules.md) for applicability, search targets, acceptance checks, and source links.

Read [the repository audit guide](references/repository-audit.md) when inspecting a codebase; it provides discovery commands, search leads, and build/runtime evidence handling. Default to an audit when asked what needs to be done. Return the report in the conversation unless the user requests a file.

## Scope and evidence

- Determine whether the request is an audit, implementation, or both. An audit produces findings and a plan; it does not authorize a redesign.
- Identify app targets, UI frameworks, deployment targets, Xcode/SDK versions, reusable UI components, navigation/state ownership, and test capabilities. For a cross-platform app, inspect its native integration and framework support before proposing SwiftUI or UIKit changes.
- Read repository instructions. Inventory the main user journeys and their screens, presentations, and shared components. Include camera or game paths only if present.
- Recheck relevant Apple documentation and local SDK declarations before using new APIs. Verify signatures, availability, and fallbacks; do not invent OS versions, pose APIs, dimensions, hinge angles, or capability flags.
- Treat search matches as investigation leads. A fixed dimension for an icon is not evidence of an unresizable screen. Device-type checks outside layout are not automatically defects.
- Distinguish Apple guidance, project-specific acceptance criteria, and engineering recommendations. Recommendations to consider or prefer a design are not universal requirements or App Store rules.

## Audit workflow

1. Establish the target, baseline build, and available runtime environments using the project's documented build workflow. If a build cannot run, continue static inspection and record the reason. Record pre-existing failures separately.
2. Map applicable rule IDs to user journeys and source locations. Inspect shared abstractions before individual screens; one shared fix may resolve several findings.
3. Reproduce suspected failures when possible. Record the transition, app state, expected outcome, and observed outcome. Label static-only findings as unverified behavior.
4. Classify each rule per relevant component as **pass**, **gap**, **needs runtime verification**, **not applicable**, or **blocked**. Explain exclusions and blockers. State whether a pass is limited to source inspection or supported by runtime evidence. Absence of a new API is not itself a gap.
5. Prioritize demonstrated user impact: lost work, crashes, and inaccessible core actions first; navigation/layout failures next; refinements afterward. These priorities are engineering judgments, not Apple severity ratings.
6. Produce a dependency-ordered implementation map. Separate essential fixes from optional enhancements and unresolved design decisions.

## Implementation workflow

When implementation is requested, make the smallest coherent change that resolves the evidenced problem. Prefer repairing existing containers and shared components over adding a device-specific parallel UI. Keep navigation and model state stable through layout changes. Preserve supported older systems with verified availability handling.

Run relevant builds and behavioral checks after changes. Test transitions while a task is in progress, not only clean launches at different sizes. Use the verification matrix in the reference. Report unavailable simulator/device checks explicitly; never equate successful compilation with device readiness.

## Required report

For each finding include:

| Field | Content |
|---|---|
| ID / status / priority | Rule ID, evidence status, user-impact priority |
| Location | Actual file and line or symbol; owning screen/shared component |
| Trigger and evidence | Concrete pose/resize/presentation/state; observed or static-only evidence |
| Impact | What the person cannot see, reach, retain, or complete |
| Proposed change | Specific implementation action and dependencies |
| Acceptance check | Observable behavior proving the fix |
| Basis | Apple source or explicitly identified engineering inference |

Lead with the most consequential work and the limits of the assessment. Group repeated occurrences under their shared implementation owner, retaining representative source locations and affected journeys. Include coverage of all D01–D19 rules, including exclusions, so uninspected areas are visible. Order work by dependencies and user impact; identify verification-only tasks separately from code changes. Give effort estimates only with stated assumptions when useful or requested.

Finish with coverage, implementation order, completed changes if any, validation results, and remaining uncertainties. If no repository is available, deliver the review framework and state that no codebase findings have been established. Never label the whole app ready from source inspection or a successful build alone.
