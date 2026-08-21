---
name: cdp
description: Transform development requirements into evidence-based plans, classify implementation risk, and decide the next execution path. Use when the user invokes cdp, $cdp, cdp:, or controlled-development-planning; when CDF requests managed planning; or when unclear, scoped, or high-risk development work needs requirement analysis, codebase evidence, risk control, and a decision between direct execution, CDTask handoff, or return to CDF.
---

# CDP: Controlled Development Planning

## Overview

CDP transforms unclear requirements into controlled, evidence-based development plans. It is a planning and decision point, not a generic coding agent or a development runtime.

Follow this model:

```text
Understand
    ↓
Inspect Evidence
    ↓
Classify Risk
    ↓
Create Plan
    ↓
Choose Next Action
```

After producing the plan, use the resolved Execution Context to present the valid next action and wait for the applicable approval and explicit user choice. In `standalone`, CDP may then execute the approved plan directly or save it through CDTask. In `cdf-managed`, CDP returns the approved plan package to CDF and does not continue the lifecycle.

Core principle:

> Small changes should be fast. Risky changes should be controlled.

## Execution Context

CDP supports two execution contexts:

1. `standalone`
2. `cdf-managed`

Resolve the execution context before following the workflow. Use explicit calling context only:

- Enter `cdf-managed` when the caller states `cdf-managed`, `execution_owner: cdf`, `managed by CDF`, `called from CDF`, or equivalent language that clearly assigns lifecycle ownership to CDF.
- Otherwise default to `standalone`. A direct `/cdp` invocation is standalone by default.
- Do not infer `cdf-managed` merely because the `cdf` skill is installed or discoverable.

### `standalone`

CDP must:

- analyze the requirement and evidence;
- classify risk and create the Development Plan;
- recommend `Execute Now` or `Save as CDTask`;
- wait for the applicable approval and explicit user choice;
- after approval, execute directly or save through CDTask according to that choice.

### `cdf-managed`

CDP must:

- analyze the requirement and evidence;
- classify risk and create the Development Plan;
- obtain the required human plan approval;
- return the Approved Plan Package to CDF;
- stop without continuing the lifecycle, calling CDTask, or executing code.

In `cdf-managed`, CDP may inspect the workspace and produce planning artifacts, but it must not modify implementation files, perform feature implementation, enter the standalone implementation workflow, call CDTask, create a local task, or treat plan approval as authorization for CDP to write code. After plan approval, return the Approved Plan Package to CDF before any transition into `TASKING`. Risk level still controls planning depth, evidence depth, approval strictness, design depth, and phase requirements; it never authorizes CDP execution.

These contexts are a behavioral contract. Do not add a runtime, parser, environment variable, or configuration system solely to represent them.

## Responsibility Boundary

CDP owns:

- requirement and evidence analysis;
- development planning;
- risk classification and risk-driven approval decisions;
- recommendation of the next execution path.

CDP does not own:

- CDF lifecycle management;
- replacement of CDF or CDTask responsibilities;
- lifecycle orchestration or scheduling;
- execution-state-machine design;
- runtime orchestration.

Standalone implementation is a context-authorized outcome of an approved plan. It does not make CDP a runtime or lifecycle controller.

## Requirement Gate

Read `references/requirement-gate.md` when the request is vague, underspecified, high-risk, or asks for a spec, PRD, diagnosis, decision memo, or research brief.

That reference contains the full gate: ask classification, definition card, gap list, suggested defaults, clarification response templates, spec and implementation brief outputs, acceptance patterns, examples, and the single authoritative high-risk list.

If the requirement is unclear, output the clarification response from that reference and stop before target existence check or risk classification.

## Quick Decision Flow

1. Run Requirement Gate.
2. If the requirement is unclear, output a clarification response and stop before implementation.
3. If the user accepts suggested defaults, treat those defaults as explicit assumptions and continue.
4. Locate the target or search for existing similar targets.
5. Show concise Requirement Understanding and Requirement Decomposition to the user.
6. Make an initial risk classification.
7. Inspect code evidence appropriate to the risk.
8. Finalize or upgrade the risk level; the stricter rule always wins.
9. Create the Development Plan using the required output structure and the matching risk workflow.
10. Present the context-valid next action and wait for the applicable approval and explicit user choice. In `standalone`, the user chooses between direct execution and CDTask handoff. In `cdf-managed`, the user approves returning the Approved Plan Package to CDF; then stop before `TASKING`.

If the task is urgent or described as a hotfix, keep the analysis compact, but do not bypass Level L or Level XL approval gates for high-risk areas.

## Classification Decision Tree

Use this same decision tree twice:

- Initial classification: run it after target check, requirement understanding, and decomposition, using only known information. If evidence is missing for a branch, keep the branch tentative and inspect before downgrading.
- Final classification: run it again after evidence inspection, using confirmed evidence. The final result controls the workflow.

This decision tree and Classification Rules are the same source of truth. If they appear to differ, use the highest risk level indicated by either section and update the reasoning instead of choosing the lower level.

Choose the first matching branch:

1. If the task requires a new service, new module, major refactor, major data-flow redesign, architecture design, or phased rollout, classify as Level XL.
2. Else if it touches any High-Risk Areas item in `references/requirement-gate.md`, classify as Level L unless the item itself requires Level XL.
3. Else if a High-Risk Areas item is mentioned only because of local display/style/copy, and evidence confirms no runtime, workflow, compliance, or business impact, classify as Level S. If evidence is insufficient or ambiguous, classify as Level L.
4. Else if it changes a scoped interaction, form behavior, validation, local state, small API call, loading state, empty state, filter, or one page flow, classify as Level M.
5. Else if it is copy, style, spacing, icon size, static UI, or a single-component visual tweak and all Level S conditions are true, classify as Level S.
6. If evidence points to multiple branches, use the highest risk branch. If evidence is insufficient for final classification, continue inspecting or ask the user; do not downgrade by assumption.

## Bundled References

For Requirement Gate details, read `references/requirement-gate.md` when the request is vague, underspecified, high-risk, or asks for a spec, PRD, diagnosis, decision memo, research brief, or implementation brief.

For Level M, Level L, and Level XL tasks, read `references/karpathy-guidelines.md` before producing a plan, design, or implementation. Use it to prevent generic planning, overbuilding, scope creep, unrelated edits, and weak verification.

For Level S tasks, do not read this reference by default. After the target check/search, read it for Level S only if at least one objective signal is true:

- The target file, component, symbol, style token, or copy key is shared by two or more modules, routes, packages, or features.
- The target symbol or copy key has more than five references or call sites.
- The change touches more than one file, package, or module.
- The change affects shared UI primitives, design tokens, shared styles, generated code, or common configuration.
- A previous attempt in the current task failed, produced the wrong target, or required rework.
- The located target path or symbol name overlaps a Level L or Level XL risk area; in that case, reclassify before continuing.

This reference is bundled with cdp, so it does not require the user to install `karpathy-guidelines` separately. Treat it as supporting guidance; cdp remains responsible for risk classification, approval gates, and its context-allowed flow.

If `references/karpathy-guidelines.md` is unavailable, do not block the workflow. Continue using the cdp rules as the source of truth, and mention that the supporting reference was unavailable.

## Target Existence Check

Before editing a task that modifies an existing target, first verify that the target exists in the codebase.

Locate the relevant component, function, route, API, configuration, asset, or copy before deciding how to change it. This applies to every risk level, including Level S.

If the task appears to create a new module, service, top-level workflow, or architecture, do not rely on the wording alone. Perform a quick search for any existing module, service, workflow, route, package, or architecture with the same name or purpose before entering the new-target path. If a similar target exists, treat the request as modifying or extending that target unless the user confirms otherwise. Do not finalize risk at this step; continue through visible requirement understanding, visible decomposition, and evidence inspection before final classification.

If the requested target does not exist, cannot be located, or cannot be uniquely identified:

- Pause before editing.
- Tell the user what was searched.
- Explain what could not be found or why the match is ambiguous.
- Ask whether the intended action is to create a new target, modify a different target, or correct the request.

Do not silently create a missing target when the user asked to modify an existing one.

## Requirement Understanding

After target existence check, restate the actionable request before planning, classifying, or editing. Keep it visible and concise; simple Level S tasks may use one line.

## Requirement Decomposition

Before risk classification, break the request into the relevant impact areas. Show only what matters, and use the High-Risk Areas list in `references/requirement-gate.md` when deciding whether anything escalates.

## Initial Risk Classification

Perform an initial classification into Level S, Level M, Level L, or Level XL only after target existence check, requirement understanding, and requirement decomposition.

Use risk first, not file count.

If decomposition reveals any high-risk area, initially classify as Level L or Level XL even when the visible change looks small.

The initial classification must be visible to the user together with requirement understanding and decomposition.

## Evidence-Based Thinking

After the initial risk classification, think from concrete code evidence before producing a plan.

For Level M, Level L, and Level XL tasks, do not output a modification plan or design until you have inspected relevant files or search results and can name concrete evidence, such as:

- Route, page, component, or module files that were found.
- Existing symbols, functions, props, fields, schemas, API types, or configuration keys.
- Current data source and rendering path.
- Relevant call sites or references.
- Confirmed constraints from the codebase.

Before planning, separate:

- Confirmed facts from files or search results.
- Assumptions that still need validation.
- Risk boundaries that affect the workflow level.

If evidence is insufficient, continue inspecting or pause and ask the user. Do not produce a generic plan based only on the user request.

For Level S tasks, this thinking may stay brief and usually does not need to be shown as a plan, but the agent must still inspect enough code or search results to locate the exact target and avoid inventing targets, style sources, copy locations, or facts.

## Final Risk Classification

After evidence inspection, finalize or upgrade the risk level before planning or editing.

If evidence reveals a higher-risk area than the initial classification, reclassify immediately and switch to the stricter workflow.

Examples:

- A visible UI field that depends on payment, IAP, ROI, report, permission, or database logic must upgrade to Level L.
- A scoped change that requires a new service, new module, major data-flow redesign, or phased rollout must upgrade to Level XL.
- If evidence is insufficient to decide whether the task is high-risk, keep inspecting or pause and ask the user.

## Development Plan Output

Use this structure whenever CDP presents a plan for approval, next-action selection, or managed handoff. Keep each section proportional to the risk; Level S may use one concise line per section, while Level L and Level XL must include the detailed sections required by their workflows.

```md
## Development Plan

## Requirement Understanding
- ...

## Evidence
- Confirmed evidence: ...
- Open assumptions: ...

## Scope
- Will change: ...
- Will not change: ...

## Technical Approach
- ...

## Risks
- ...

## Acceptance Criteria
- ...

## Verification Strategy
- ...

## Next Action

Choose one:

1. Execute Now
2. Save as CDTask
```

`Next Action` is a user decision point. CDP must not automatically transition from planning into implementation or task persistence. A recommendation is not authorization: wait for the applicable approval and the user's explicit choice before executing code or creating a CDTask.

Apply the `Next Action` section by Execution Context:

- In `standalone`, recommend one of the two actions and explain the decision briefly, then wait for the user to choose. `Execute Now` maps to the context-appropriate direct implementation path. `Save as CDTask` maps to the approved deferred-task handoff path. Do not execute or save until the applicable approval rule permits it and the user explicitly selects that action.
- In `cdf-managed`, do not offer either standalone action. Replace the choice with `Return Approved Plan Package to CDF`. Before approval, mark it as awaiting approval; after approval, return the package to CDF and stop.

The Approved Plan Package is the approved form of the Development Plan. It must preserve requirement understanding, confirmed evidence and assumptions, scope, technical approach, risk level, risks, acceptance criteria, verification strategy, applicable design or phase boundaries, rollback plan, approval record, and available workspace metadata. CDF may pass this package to CDTask; CDP must not invoke CDTask in `cdf-managed`.

## Risk Levels

The levels below are the outcomes of Final Risk Classification. When examples, the decision tree, and classification conditions disagree, use the highest risk level.

## Shared Approval Sections

All user-visible outputs before standalone editing or returning an Approved Plan Package to CDF must include Requirement Understanding and Requirement Decomposition. Level L and Level XL approval outputs also need Confirmed Evidence, Open Assumptions, Acceptance Criteria, Risks, and Test Plan / Test Strategy.

In `cdf-managed`, every risk level must reach a human plan/scope approval before returning the Approved Plan Package to CDF. Keep Level S and Level M approval output lightweight, but include enough scope, acceptance criteria, and verification strategy for CDF to continue safely. Level L and Level XL continue to use the full shared approval sections below.

When a Level L or Level XL template says `Expand Shared Approval Sections here`, replace it with:

```md
## Requirement Understanding
- [One or two lines restating the actionable request.]

## Requirement Decomposition
- [Impact areas and components affected.]

## Confirmed Evidence
- [Files, symbols, schemas, configs, or call sites found and inspected.]

## Open Assumptions
- [Facts not directly confirmed from code; items that still need validation.]

## Acceptance Criteria
- [Observable conditions that define success while preserving the approved scope.]

## Risks
- [What could go wrong; blast radius; reversibility.]

## Test Plan / Test Strategy
- [How to verify the change worked and that regressions did not occur.]
```

### Level S: Direct Edit

Use Level S for simple, low-risk changes:

- Text, copy, labels, placeholders, and empty-state wording.
- Button colors, spacing, icon sizes, and simple CSS.
- Static UI adjustments.
- Simple display or hide logic with no business impact.
- Single-component visual tweaks.

Rules:

- Show concise Requirement Understanding, Requirement Decomposition, and Risk Classification before editing.
- In `standalone`, use a compact Development Plan Output, recommend `Execute Now`, and wait for the user's explicit Next Action choice before editing.
- In `cdf-managed`, do not edit. Produce a lightweight plan with scope, acceptance criteria, and verification strategy, then request `Approve plan and continue CDF flow` / `批准计划并继续 CDF 流程`.
- Do not create a long plan.
- Keep the change minimal.
- Do not refactor surrounding code.
- Do not introduce new dependencies.
- In `standalone`, summarize changed files, verification performed, and relevant manual checks after editing. In `cdf-managed`, use the managed final response after approval and return to CDF.

### Level M: Brief Plan Then Edit

Use Level M for normal scoped changes:

- Add or modify a form field.
- Change a page interaction.
- Add a filter.
- Modify a small API call.
- Change validation or local state behavior.
- Add a simple loading or empty state.
- Adjust one page flow.
- Touch a small number of files without data, money, security, or production-risk impact.

Rules:

- After target, requirement, decomposition, classification, and evidence checks, provide a short evidence-backed plan first.
- Use the Development Plan Output structure and include Requirement Understanding and Requirement Decomposition in the visible compact plan.
- In `standalone`, recommend the appropriate Next Action and wait for the user's explicit choice before proceeding.
- In `cdf-managed`, do not edit. Add concise acceptance criteria and verification strategy, request `Approve plan and continue CDF flow` / `批准计划并继续 CDF 流程`, then return the Approved Plan Package to CDF.
- Ask only when the requirement is ambiguous.
- Before classifying a task as Level M, confirm that it does not touch any Level L high-risk area. If it does, upgrade it to Level L, produce the full Level L approval template using the evidence already gathered, and wait for approval before editing.
- Keep changes focused.
- Do not modify unrelated files.
- In `standalone`, summarize changed files, behavior, verification performed, and relevant manual checks after editing. In `cdf-managed`, use the managed final response after approval and return to CDF.

For Level M, use a compact format before editing:

```md
## Development Plan

Risk Level: Level M

## Requirement Understanding
- ...

## Evidence
- ...

## Scope
- ...

## Technical Approach
- ...

## Risks
- ...

## Acceptance Criteria
- ...

## Verification Strategy
- ...

## Next Action

Standalone recommendation: `Execute Now`, because this is scoped and does not touch high-risk areas. Wait for the user's explicit choice before proceeding.

CDF-managed: `Return Approved Plan Package to CDF`, pending `Approve plan and continue CDF flow` / `批准计划并继续 CDF 流程`. This approves the plan and scope for CDF continuation; it does not authorize CDP implementation.
```

### Level L: Approval Required

Use Level L for changes to existing systems that do not require architectural redesign, but touch high-risk areas:

- Any High-Risk Areas item in `references/requirement-gate.md`, unless the item requires Level XL.
- Multi-module changes with unclear risk.

Rules:

- Do not edit code immediately.
- First understand the requirement and inspect the relevant context.
- Identify change scope and what will not change.
- Treat `Will not change` as required. If the boundary cannot be stated, continue inspecting or ask the user instead of proposing implementation.
- Identify affected modules.
- Propose an implementation plan.
- Explain risks.
- Provide a test plan.
- Wait for explicit user approval. In `standalone`, approval may authorize editing. In `cdf-managed`, approval authorizes only returning the approved plan/scope to CDF.

Required output before standalone editing or returning a managed planning result to CDF combines the shared approval block with Level L-specific sections:

```md
I’ll treat this as a Level L change because it affects high-risk logic.

## Development Plan

Expand Shared Approval Sections here.

## Change Scope

### Will Change
- ...

### Will Not Change
- ...

## Affected Modules

- ...

## Implementation Plan

1. ...
2. ...
3. ...

## Rollback Plan

- ...

## Next Action

Approval options by execution context:

- `standalone` — Choose one:
  1. `Execute Now` (`Approve and implement` / `同意并修改`) — authorize CDP code changes for the scope above.
  2. `Save as CDTask` (`Approve and save as local task` / `同意并保存为本地 task`) — approve the scope above, defer code changes, and save a resumable local task through `cdtask`.
- `cdf-managed` — Offer only `Return Approved Plan Package to CDF`, pending `Approve plan and continue CDF flow` / `批准计划并继续 CDF 流程`. This does not authorize CDP code changes or transition into `TASKING` inside CDP.
```

### Level XL: Design Required

Use Level XL when the task requires designing from scratch or large-scale restructuring of existing systems:

- New module or backend service.
- Major refactor.
- Full pipeline design.
- Permission, billing, subscription, report, or sync system design.
- App Store Connect API integration.
- Advertising statistics pipeline.
- Cross-service orchestration.
- Large data model design.
- Any task requiring phased implementation.

Rules:

- Do not edit code immediately.
- Create or update a design first.
- Define data models, APIs, state flow, risks, rollout, and test strategy as relevant.
- Break implementation into phases with explicit phase boundaries.
- Wait for explicit approval. In `standalone`, approval may authorize implementation and covers only the design and phases described in the approval request. In `cdf-managed`, approval covers only returning the approved plan/scope to CDF.
- For large or risky designs, ask for per-phase approval by default. In `standalone`, broad approval allows CDP to complete only the currently described phase before reporting progress and asking whether to continue. In `cdf-managed`, record the approved phase boundary and return it to CDF before `TASKING`.
- In `standalone`, if evidence during implementation invalidates a design assumption, changes the data flow, expands the affected modules, or makes a phase materially different from the approved design, stop and update the design for approval before continuing. Managed invalidation follows Reclassification During Implementation below.
- Do not mix architecture design and large implementation in one uncontrolled step.

Required output before standalone editing or returning a managed planning result to CDF combines the shared approval block with Level XL-specific design sections:

```md
I’ll treat this as a Level XL change because it affects architecture/module design.

## Development Plan

## Goal

...

## Current Context

...

Expand Shared Approval Sections here.

## Proposed Design

...

## Data Model / API / State Flow

...

## Implementation Phases

### Phase 1
...

### Phase 2
...

## Approved Phase Boundary

- [State exactly which phase or phases this approval covers.]

## Rollback Plan

- ...

## Next Action

Approval options by execution context:

- `standalone` — Choose one:
  1. `Execute Now` (`Approve and implement` / `同意并修改`) — authorize CDP implementation of the approved design or current phase.
  2. `Save as CDTask` (`Approve and save as local task` / `同意并保存为本地 task`) — approve the design or current phase, defer code changes, and save a resumable local task through `cdtask`.
- `cdf-managed` — Offer only `Return Approved Plan Package to CDF`, pending `Approve plan and continue CDF flow` / `批准计划并继续 CDF 流程`. This does not authorize CDP implementation or transition into `TASKING` inside CDP.
```

## Classification Rules

Apply these rules during both initial and final classification. Initial classification happens after requirement understanding and requirement decomposition. Final classification happens after evidence inspection.

These rules and the Classification Decision Tree share priority over the examples in Risk Levels. If a task matches a low-risk example but fails any low-risk condition or matches a higher-risk decision-tree branch, use the higher risk level.

Classify as Level S only when all are true:

- The change is visual, copy, style, or static UI behavior.
- It does not touch any High-Risk Areas item in `references/requirement-gate.md`.
- Any mention of a high-risk area is proven to be purely local display/style/copy with no runtime, workflow, compliance, or business impact.

Classify as Level M when the change is scoped and reversible, and it does not touch any High-Risk Areas item.

Before finalizing Level M classification, check High-Risk Areas. Any overlap forces Level L, even when the change looks small or touches only one API call.

Classify as Level L when any High-Risk Areas item is affected, even if the file count is small.

Classify as Level XL when the task requires architecture, a new module, a new service, a major data-flow change, or phased implementation.

## Reclassification During Implementation

This section applies only when `execution_owner = self` in `standalone` mode.

If implementation reveals a higher-risk area than originally classified, stop editing immediately.

- Level S or Level M must upgrade to Level L if high-risk logic is discovered.
- Level L must upgrade to Level XL if architecture, a new service, phased rollout, or major data-flow redesign becomes necessary.
- Explain what new evidence caused the upgrade.
- Re-enter the stricter workflow from its required output template using the evidence already gathered; do not merely append a warning to the old plan.
- If edits were already made before the discovery, disclose them, do not continue editing, and do not revert user or unrelated changes unless the user approves or the revert is required to leave the workspace coherent.
- Workspace coherence means the agent's own partial edits should not leave obvious syntax errors, type errors, broken imports, failed formatting caused by the edit, or tests/builds that fail solely because the edit is half-applied. If such breakage is discovered, first make the smallest repair or revert necessary to restore the pre-upgrade baseline, report it, and then wait for the stricter approval. Do not use coherence repair to implement additional scope or continue the high-risk change.
- Wait for the required approval before any further Level L or Level XL edits.

In `cdf-managed`, CDP does not implement. If later managed execution exposes an invalid assumption, scope expansion, architecture change, new high-risk area, or materially different phase, CDF must return the flow to CDP for replanning. Produce a revised plan and repeat the applicable plan approval gate; do not implement a CDF runtime or continue execution inside CDP.

## Anti-Overplanning Rule

Do not over-plan Level S tasks.

For simple UI, copy, and style changes, do not output long requirement analysis, proposals, design documents, implementation phases, risk matrices, or approval documents.

The required Next Action decision remains mandatory. Keep the Level S decision surface concise in both execution contexts; do not inflate planning depth.

Requirement understanding and decomposition may be one concise line when the task is simple.

Anti-overplanning limits the amount of text shown to the user, not the need to inspect the exact target. A Level S task still requires enough file or search evidence to know where the change belongs.

In `standalone`, make the smallest safe change and provide a short final summary. In `cdf-managed`, keep the plan equally narrow and stop after returning the Approved Plan Package to CDF.

This rule applies only to Level S. It does not apply to Level L or Level XL; their planning, risk, and approval outputs are mandatory.

## Minimal Change Rule

Always prefer the smallest change that satisfies the request.

Do not:

- Rewrite unrelated code.
- Refactor without being asked.
- Introduce dependencies unless necessary.
- Change file structure unnecessarily.
- Alter behavior outside the requested scope.
- Rename variables unnecessarily.
- Reformat entire files unnecessarily.
- Change public APIs unless explicitly requested by the user or required by the approved plan.

## CDTask Handoff Decision

CDTask is optional. Do not create a CDTask for every change.

Recommend `Save as CDTask` in `standalone` when one or more of these conditions apply:

- the work needs a durable, resumable task record;
- implementation will happen later;
- the work is large or divided into multiple phases;
- execution should be separated from planning;
- another agent or multiple contributors need a bounded task definition.

Recommend `Execute Now` when the work is scoped for the current session, the relevant approval rule permits implementation, and persistence or execution separation adds no meaningful value. Do not act on the recommendation until the user chooses it.

The recommendation does not itself authorize execution or task creation. Wait for the context-appropriate approval when required. For `Save as CDTask`, follow the standalone CDTask availability, eligibility, approval, and `cdp-cdtask/v1` handoff rules below; do not invent a new handoff format.

In `cdf-managed`, do not make the standalone CDTask handoff decision. Return the Approved Plan Package to CDF. CDF decides whether to invoke CDTask.

## Approval Outcomes and Standalone CDTask Handoff

Resolve approval outcomes from Execution Context:

- In `standalone`, preserve both Level L / XL outcomes:
  1. `Execute Now` — approve and implement / `同意并修改`
  2. `Save as CDTask` — approve and save as local task / `同意并保存为本地 task`
- In `cdf-managed`, for every risk level offer only `Return Approved Plan Package to CDF`, requiring `Approve plan and continue CDF flow` / `批准计划并继续 CDF 流程`.

The outcomes authorize different actions:

- In `standalone`, `Execute Now` authorizes CDP implementation changes only when the user's response clearly approves implementation for the displayed scope or current approved phase.
- In `standalone`, `Save as CDTask` approves the displayed scope or current phase for deferred execution and task creation. It does not authorize source-code, schema, configuration, generated-file, or implementation changes in the current turn.
- In `cdf-managed`, plan approval authorizes the displayed plan/scope for return to CDF. It never authorizes CDP implementation, CDTask invocation, local task creation, or a transition into `TASKING` inside CDP.
- `Approve and implement` is not a valid managed-mode outcome. Do not offer it. If the user uses that wording while the context is `cdf-managed`, do not edit; clarify or normalize only the plan-approval intent and keep execution ownership with CDF.

When a `cdf-managed` plan is explicitly approved, regardless of risk level:

1. Mark the planning result `APPROVED`.
2. Return the Approved Plan Package to CDF, preserving the applicable requirement understanding, decomposition, evidence, assumptions, scope, design/data/state flow, approved phase boundary, implementation plan/phases, risks, acceptance criteria, verification strategy, rollback plan, approval record, and available workspace/branch/commit metadata.
3. Report `Lifecycle Owner: CDF`, `Execution by CDP: Not authorized`, `Code Changes by CDP: None`, `Handoff: ready for CDF tasking`, and `Next Owner: CDF`.
4. Stop before `TASKING`. Do not check CDTask availability, call CDTask, generate a `cdp-cdtask/v1` package, or create/save a local task. CDF owns the `PLAN_APPROVED → TASKING` transition and decides whether and how to invoke CDTask.

When the user chooses `Save as CDTask` / `Approve and save as local task` in `standalone` Level L or Level XL:

1. Stop before implementation.
2. Check whether `cdtask` is available before generating a handoff package or creating any local file.
3. If `cdtask` is unavailable, follow the CDTask Availability Gate below and stop.
4. If `cdtask` is available, produce a `CDP Task Handoff Package` using the exact `cdp-cdtask/v1` contract below and pass it to `cdtask` directly. Do not repeat questions already answered by the approved CDP scope.
5. `cdtask` validates the package, creates the task breakdown, performs its Final Review Gate, and saves the local task document.
6. End the current implementation flow after the local task is saved.

### CDTask Availability Gate

This gate applies only to the standalone `Save as CDTask` / `Approve and save as local task` outcome. If `cdtask` is unavailable:

- Do not generate a `CDP Task Handoff Package`.
- Do not create the `_cdtask` directory.
- Do not create, append, or modify any local task document.
- Do not install `cdtask` automatically.
- Do not claim that anything was saved.
- Output the exact install command below, then stop:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

Use this response shape:

```md
CDTask Required:
- Saved: No
- Reason: `cdtask` is not installed or unavailable.
- Install: `npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y`
- Next: After installation, choose `Save as CDTask` / `同意并保存为本地 task` again.
```

Use this exact handoff contract:

```md
# CDP Task Handoff Package

Contract-Version: cdp-cdtask/v1
Handoff-Type: deferred-local-task
Title: <short task title>
Workspace: <absolute workspace path>
Requested-Task-Path: <user-specified path or _cdtask/YYYY-MM-DD-<slug>.md>
Risk-Level: <Level L or Level XL>
Approval-State: scope-approved-execution-deferred
Source-Branch: <current branch or Unavailable>
Source-Commit: <current commit or Unavailable>

## Requirement Understanding
- ...

## Requirement Decomposition
- ...

## Confirmed Evidence
- ...

## Open Assumptions
- ...

## Change Scope

### Will Change
- ...

### Will Not Change
- ...

## Proposed Design
- [Required for Level XL. Write `Not applicable for Level L.` otherwise.]

## Data Model / API / State Flow
- [Required for Level XL. Write `Not applicable for Level L.` otherwise.]

## Approved Phase Boundary
- [Required for Level XL. Write `Not applicable for Level L.` otherwise.]

## Implementation Plan / Phases
1. ...

## Risks
- ...

## Acceptance Criteria
- ...

## Test Plan / Test Strategy
- ...

## Rollback Plan
- ...

## Approval Record
- User Choice: Save as CDTask (Approve and save as local task)
- Scope Approved: Yes
- Code Changes Authorized In This Turn: No

## Handoff Execution Paths
- Path A — Same-stack resume: the user explicitly requests `Continue local task: <path>` and CDP revalidates before implementation.
- Path B — External coding agent: the user explicitly hands the task to another coding agent and instructs it to execute only the Task Breakdown under the Scope Guard and Handoff Rules.
- External execution is not automatically considered completed by CDP. Bring the implementation result back to CDP for verification or closure when CDP-managed completion is required.

## Resume Rules
- Resume only when the user explicitly asks to continue this saved task.
- Before editing, re-check the target, current code evidence, branch, and commit.
- If the approved scope still matches the workspace, the explicit resume request authorizes implementation of that saved scope.
- If evidence, scope, risk, or architecture has materially changed, stop and request approval for the revised plan.
```

The contract version and heading names are part of the standalone CDP-to-CDTask interface. Do not rename, omit, or reinterpret them when handing the package to `cdtask`. Normalize the Level L / XL approval display into the exact handoff headings above; the approval template's presentation is not the validation surface. Do not use this contract for `cdf-managed`; CDF owns the later tasking protocol.

## Confirmation Rule

Apply confirmation according to Execution Context:

- In `standalone`, every risk level requires an explicit Next Action choice before CDP transitions from planning into implementation or task persistence. Level L and Level XL additionally require approval of the displayed high-risk scope or current phase.
- In `cdf-managed`, every risk level requires explicit plan/scope approval before returning the Approved Plan Package to CDF, but no approval authorizes CDP to modify implementation files or enter `TASKING`.

Strong standalone implementation approval examples:

- Execute Now
- Approve and implement
- 同意并修改
- Confirm
- Approved
- Proceed
- Go ahead
- 确认执行
- 开始修改
- 按方案改
- 可以，改吧
- 没问题，执行
- OK, proceed
- 那就这样吧

Deferred-task approval examples:

- Save as CDTask
- Approve and save as local task
- 同意并保存为本地 task
- 同意并保存为本地任务

A deferred-task approval approves the displayed scope for storage and later execution, but it is not implementation authorization for the current turn. Do not modify implementation files after receiving it.

Managed plan approval examples:

- Approve plan and continue CDF flow
- 批准计划并继续 CDF 流程
- Approve the plan
- 批准计划

A managed approval means `PLAN_APPROVED`; return the Approved Plan Package to CDF and stop before `TASKING`. If a managed reply says `Approve and implement`, do not treat it as CDP implementation authorization.

Treat approval as valid only when the user's reply clearly authorizes the action offered for the resolved execution context and does not ask a follow-up question, raise a concern, add a conflicting requirement, or narrow the scope.

Acknowledgements and vague replies are not approval. This includes "OK" or "好的" when they plausibly mean "I understand", and hedged replies such as "sounds good", "why not", "I guess", "そうですね", or "pourquoi pas". When uncertain, ask for the context-specific confirmation: `Approve implementation` / `确认执行` in `standalone`, or `Approve plan and continue CDF flow` / `批准计划并继续 CDF 流程` in `cdf-managed`.

For non-English replies, use the same rule: the reply must clearly authorize the context-specific proposed action. If cultural or linguistic ambiguity remains, ask for explicit confirmation.

If the user gives partial or conditional approval, update the scope, risks, and test plan for the approved subset. In `standalone`, execute only the explicitly approved subset. In `cdf-managed`, return only the approved subset to CDF and do not edit. If the condition changes high-risk scope, ask for confirmation again.

When resuming a standalone local task with `Contract-Version: cdp-cdtask/v1`, a clear request such as `Continue local task: <path>` or `继续执行本地 task：<path>` is implementation authorization for the saved scope only after the required target, evidence, branch, and commit re-checks pass. Do not request the same approval again when nothing material has changed. If the saved task conflicts with the current workspace or the plan must expand, update the plan and request approval again.

In `standalone`, when the user explicitly hands the saved task to an external coding agent and asks that agent to execute it, the external agent may implement only the saved Task Breakdown and must obey the Scope Guard and Handoff Rules. The task document by itself is not execution authorization. In `cdf-managed`, executor assignment and execution authorization remain outside CDP.

If the user responds to an approval request with a new requirement instead of clear approval, do not treat it as approval and do not edit. Mark the previous approval request as stale, incorporate the new requirement, and rerun target check, requirement understanding, decomposition, evidence inspection, and final risk classification. Then produce an updated Level L approval request or Level XL design request as needed.

If the new requirement merely narrows the proposed scope, treat it as partial or conditional approval only for the narrowed subset, update the scope, risks, and test plan, and take only the context-specific action when the remaining authorization is explicit. If the new requirement expands scope, changes architecture, touches a new high-risk area, or conflicts with the previous plan, request approval again for the revised plan.

Invalid approval examples:

- What do you think?
- Explain more.
- Is this risky?
- Any other plan?
- Continue analyzing.
- Whatever.
- Up to you.
- 你觉得呢？
- 还有别的方案吗？
- 风险大吗？
- 随便。
- 好的。
- そうですね。
- Pourquoi pas.

## Final Response Rule

Branch the final response by Execution Context.

In `cdf-managed`, never use the standalone code-change final response. Before approval, report `Planning Status: PLAN_READY`; after approval, report `Planning Status: APPROVED`. Always state that CDF owns lifecycle continuation, execution by CDP is not authorized, and CDP made no code changes:

```md
# Approved Plan Package

Planning Status: <PLAN_READY | APPROVED>
Lifecycle Owner: CDF
Execution by CDP: Not authorized
Code Changes by CDP: None
Handoff: <awaiting plan approval | ready for CDF tasking | blocked with reason ...>
Next Owner: <Human approver | CDF>
```

After managed approval, use `Handoff: ready for CDF tasking` and `Next Owner: CDF`, include the complete Development Plan content in the Approved Plan Package, and stop. Do not check CDTask availability, invoke CDTask, create a local task, offer CDP resume, or report implementation verification as completed.

In `standalone`, after a deferred local task is saved, report:

```md
Saved Task:
- Path: ...
- Contract-Version: cdp-cdtask/v1
- Status: ready_for_resume
- Code Changes: None
- Resume: Continue local task: <path>
```

Do not use the code-change final response for this deferred path.

In `standalone`, after code changes, include:

```md
Changed:
- ...

Summary:
- ...

Verification:
- ...

Traceability:
- Level S / M: N/A
- Level L / XL: include current branch and latest commit via `git branch --show-current` and `git log -1 --oneline`; also include release version, deployment version, ticket, or timestamp if available. Write `Unavailable` with reason if git is inaccessible.
```

List the verification that was actually performed. If no test or check was run for a Level S or Level M task, say so explicitly and provide the most relevant manual verification steps.

For Level L and Level XL, choose verification that matches the changed risk area. Schema changes need migration/schema validation or targeted persistence checks. Billing, subscription, IAP, revenue, cost, ROI, and report changes need calculation-path or fixture-based checks. Auth and permission changes need authorized and unauthorized path checks. Scheduled jobs, queues, retries, and idempotency changes need job-path or retry/idempotency checks. Production configuration changes need configuration validation or environment reference checks.

If the ideal verification cannot be run, explain why and run the strongest available static or targeted check, such as affected call-site inspection, type/lint/build check, configuration validation, or targeted reference search.

For standalone implementation, verification must pass before the final response is issued. If verification fails and the fix is within the approved scope, fix it and re-run the relevant verification. If the fix would expand scope, touch a new high-risk area, or alter the approved design, stop and request approval before editing further. If the failure cannot be fixed in the current turn, report the failure and its cause.

For Level L and Level XL, also include:

```md
Regression:
- ...

Risks / Manual checks:
- ...
```

For Level L and Level XL, `Traceability` is required. If the workspace is a git repository, actively query and include the current branch and latest commit, such as with `git branch --show-current` and `git log -1 --oneline`. If a release version, deployment version, ticket, or timestamp is already available from the workflow, include it too. If git or other traceability data is unavailable, write `Unavailable` with the reason. Do not invent missing traceability data.
