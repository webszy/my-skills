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
2. Else if any Mandatory Escalation Signal or High-Risk Areas item is present, classify as at least Level L.
3. Else if every Level S condition and the S/M Reverse Check pass, classify as Level S.
4. Else if every Level M condition and the S/M Reverse Check pass, classify as Level M.
5. Otherwise do not finalize S or M. Follow Evidence Gap and Evidence Conflict Handling, using the highest risk supported by available evidence.

## Mandatory Escalation Signals

Upgrade an initial Level S or Level M classification to at least Level L when any signal below is present. Upgrade to Level XL instead when the work also requires new architecture, a new module or service, a cross-system redesign, or phased delivery.

- shared components, shared UI primitives, theme systems, design tokens, or global state;
- conditional rendering, feature gating, entitlement checks, or permission-related behavior;
- caches or cache invalidation;
- analytics, telemetry, tracking, or business metrics;
- localization or i18n behavior;
- application, deployment, environment, or production configuration;
- scheduled jobs, queues, retries, background work, events, webhooks, or message consumers;
- data creation, mutation, deletion, migration, or backfill;
- billing, payments, subscriptions, IAP, pricing, authentication, or authorization;
- evidence that is insufficient to rule out a higher-risk path;
- evidence sources that materially conflict about scope, behavior, ownership, or impact.

Do not downgrade merely because the visible UI change is small or the file count is low.

For insufficient or conflicting evidence, Level L is a provisional control floor, not permission to finalize the plan. Follow the dedicated evidence path and remain `BLOCKED` when the unresolved item changes plan meaning.

Why: these signals commonly hide cross-cutting behavior or blast radius behind a locally visible change.

## S/M Reverse Check

Before finalizing Level S or Level M, answer every item below from inspected evidence:

- [ ] The target is not shared across components, routes, modules, themes, or global state.
- [ ] The change does not alter conditional rendering, permissions, entitlements, feature gates, or user-specific behavior.
- [ ] The change does not touch cache, tracking, analytics, i18n, configuration, jobs, queues, retries, events, or webhooks.
- [ ] The change does not read, create, mutate, delete, migrate, or backfill persistent data.
- [ ] The change does not affect billing, authentication, authorization, security, privacy, compliance, or production configuration.
- [ ] Relevant evidence is sufficient and internally consistent.
- [ ] The proposed scope is bounded, reversible, and does not require architecture, a new module/service, or phased delivery.

If any answer is `No`, upgrade to at least Level L. If any answer is `Unknown`, do not finalize S/M; follow Evidence Gap Handling. If inspected sources disagree, follow Evidence Conflict Handling.

Why: S/M is permitted only after the agent actively disproves hidden high-risk impact.

## Bundled References

For Requirement Gate details, read `references/requirement-gate.md` when the request is vague, underspecified, high-risk, or asks for a spec, PRD, diagnosis, decision memo, research brief, or implementation brief.

For Level M, Level L, and Level XL tasks, read `references/karpathy-guidelines.md` before producing a plan, design, or implementation. Use it to prevent generic planning, overbuilding, scope creep, unrelated edits, and weak verification.

For Level S tasks, do not read this reference by default. After the target check/search, read it for Level S only if at least one objective signal is true:

- A previous attempt in the current task failed, produced the wrong target, or required rework.
- The agent needs the additional minimal-change guardrails after the S/M Reverse Check has passed.

Shared targets, multiple affected modules, design tokens, shared styles, generated code, common configuration, or overlap with a Level L/XL area are not reasons to remain Level S and read more guidance. They are reclassification signals; rerun the decision tree and upgrade before continuing.

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

## Evidence Gap Handling

Use this path when required evidence is missing, unavailable, or too weak to rule out a higher-risk impact:

1. Record exactly what evidence is missing and which classification or scope decision depends on it.
2. Continue safe read-only inspection when the repository or supplied artifacts can resolve the gap.
3. If only the user or an external owner can resolve it, ask the smallest targeted question and stop before final classification, approval, implementation, or CDTask handoff.
4. If the gap leaves a Mandatory Escalation Signal possible, use provisional Level L controls; do not label the work S or M.
5. In `cdf-managed`, return `Planning Status: BLOCKED` when the missing evidence affects scope, architecture, behavior, risk, acceptance criteria, or approval meaning.

Do not convert an evidence gap into an assumption when being wrong would expand scope or change behavior.

## Evidence Conflict Handling

Use this path when inspected files, contracts, documentation, user statements, or runtime-facing configuration disagree materially:

1. List the conflicting claims and their sources.
2. Use the highest risk level supported by any credible source; never choose the lower-risk interpretation for convenience.
3. Ask for an authoritative decision when the conflict changes scope, behavior, ownership, contracts, or acceptance criteria.
4. Mark the plan `BLOCKED` until the material conflict is resolved. In `cdf-managed`, return the conflict to CDF for CDP replanning or renewed approval.
5. After resolution, update the evidence record, rerun classification, regenerate the Scope Lock, and invalidate any earlier approval whose meaning changed.

Why: missing evidence may be recoverable by inspection, while conflicting evidence requires an explicit authority decision; treating both as generic uncertainty causes unsafe defaults.

## Final Risk Classification

After evidence inspection, finalize or upgrade the risk level before planning or editing.

If evidence reveals a higher-risk area than the initial classification, reclassify immediately and switch to the stricter workflow.

Examples:

- A visible UI field that depends on payment, IAP, ROI, report, permission, or database logic must upgrade to Level L.
- A scoped change that requires a new service, new module, major data-flow redesign, or phased rollout must upgrade to Level XL.
- If evidence is insufficient to decide whether the task is high-risk, follow Evidence Gap Handling.
- If evidence materially conflicts, follow Evidence Conflict Handling and do not finalize the plan.

## Scope Lock Contract

Every Development Plan that may be approved, returned to CDF, or handed to CDTask must contain one canonical Scope Lock block using `Scope-Lock-Version: cdp-scope/v1`.

```yaml
Scope-Lock-Version: cdp-scope/v1
in_scope:
  - <approved outcome or capability>
out_of_scope:
  - <explicitly excluded adjacent area>
non_goals:
  - <specific behavior or deliverable that must not be implemented>
assumptions:
  - <approved assumption that does not conceal a blocking evidence gap>
stop_conditions:
  - <condition that requires stopping and returning to CDP or the user>
will_change:
  - <approved component, contract, behavior, or artifact>
will_not_change:
  - <protected component, contract, behavior, or artifact>
acceptance_criteria:
  - <high-level observable success condition>
```

All eight fields are required arrays. Use an explicit empty array `[]` only when the plan intentionally has no item for that field. Never use `TBD`, `etc.`, `as needed`, `unrelated changes`, or similarly unbounded language in `non_goals`, `will_not_change`, or `stop_conditions`.

Field meanings are fixed:

- `in_scope`: approved outcomes and capabilities;
- `out_of_scope`: adjacent areas excluded from this approval;
- `non_goals`: specific work that must not be implemented;
- `assumptions`: disclosed premises accepted for planning; blocking evidence gaps do not belong here;
- `stop_conditions`: evidence or change conditions that invalidate continuation;
- `will_change`: concrete affected behavior, components, contracts, or artifacts;
- `will_not_change`: concrete protected behavior, components, contracts, or artifacts;
- `acceptance_criteria`: high-level observable conditions for the approved scope.

The Scope Lock is the canonical scope source. Any `Change Scope`, plan prose, phase description, or task handoff section must be consistent with it. When handing off:

1. Copy the complete Scope Lock block verbatim, preserving version, field names, list items, ordering, and meaning.
2. Do not paraphrase, merge, weaken, omit, or broaden any field.
3. Do not promote an assumption into approved scope or an implementation fact.
4. If scope must expand, return to CDP, regenerate the plan and Scope Lock, and obtain approval again before handoff.

Why: one structured, immutable scope source prevents semantic drift between planning, approval, and task decomposition.

## Development Plan Output

Use this structure whenever CDP presents a plan for approval, next-action selection, or managed handoff. Keep each section proportional to the risk; Level S may use one concise line per section, while Level L and Level XL must include the detailed sections required by their workflows.

```md
## Development Plan

## Requirement Understanding
- ...

## Evidence
- Confirmed evidence: ...
- Open assumptions: ...

## Scope Lock

Scope-Lock-Version: cdp-scope/v1
in_scope: [...]
out_of_scope: [...]
non_goals: [...]
assumptions: [...]
stop_conditions: [...]
will_change: [...]
will_not_change: [...]
acceptance_criteria: [...]

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

All user-visible outputs before standalone editing or returning an Approved Plan Package to CDF must include Requirement Understanding, Requirement Decomposition, and the canonical Scope Lock. Level L and Level XL approval outputs also need Confirmed Evidence, Open Assumptions, Acceptance Criteria, Risks, and Test Plan / Test Strategy.

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

## Scope Lock

Scope-Lock-Version: cdp-scope/v1
in_scope: [...]
out_of_scope: [...]
non_goals: [...]
assumptions: [...]
stop_conditions: [...]
will_change: [...]
will_not_change: [...]
acceptance_criteria: [...]

## Acceptance Criteria
- [Observable conditions that define success while preserving the approved scope.]

## Risks
- [What could go wrong; blast radius; reversibility.]

## Test Plan / Test Strategy
- [How to verify the change worked and that regressions did not occur.]
```

### Level S: Lightweight Plan and Decision

Use Level S for simple, low-risk changes:

- Text, copy, labels, placeholders, and empty-state wording.
- Button colors, spacing, icon sizes, and simple CSS.
- Static UI adjustments.
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

### Level M: Brief Plan and Decision

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

## Scope Lock

Scope-Lock-Version: cdp-scope/v1
in_scope: [...]
out_of_scope: [...]
non_goals: [...]
assumptions: [...]
stop_conditions: [...]
will_change: [...]
will_not_change: [...]
acceptance_criteria: [...]

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

This is a readable projection of the canonical Scope Lock and must not add or weaken scope.

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

- the change is limited to local copy, spacing, color, icon size, or static presentation;
- exactly one non-shared target is identified from evidence;
- no conditional behavior, state transition, API call, persistent data, contract, configuration, or generated artifact changes;
- no Mandatory Escalation Signal or High-Risk Areas item is present;
- evidence is sufficient and consistent;
- the S/M Reverse Check passes completely.

Classify as Level M only when all are true:

- the behavior change is bounded to one feature or user flow;
- affected modules, inputs, outputs, failure behavior, and verification are known;
- the change is reversible without migration, rollout coordination, or contract redesign;
- no shared/global surface and no Mandatory Escalation Signal or High-Risk Areas item is present;
- evidence is sufficient and consistent;
- the S/M Reverse Check passes completely.

Classify as Level L when any are true and Level XL does not apply:

- any Mandatory Escalation Signal or High-Risk Areas item is affected;
- the change crosses module boundaries or shared contracts but does not require architectural redesign;
- persistent data, money, identity, permissions, configuration, background processing, integrations, compliance, or observability-sensitive behavior may change;
- evidence gaps prevent proving S/M but the work can still be responsibly planned with explicit unknowns and an approval gate.

Classify as Level XL when any are true:

- a new module, service, subsystem, or top-level workflow is required;
- architecture, public contracts, or major data flow must be designed or redesigned;
- rollout, migration, or implementation must be split into approval-controlled phases;
- multiple high-risk systems interact and need a coordinated design;
- the requested outcome cannot be achieved inside the existing approved boundaries without material redesign.

Level S and M are all-conditions classifications. Level L and XL are any-condition classifications. When rules overlap, use the highest level.

## Reclassification During Implementation

This section applies only when `execution_owner = self` in `standalone` mode.

If implementation reveals a higher-risk area than originally classified, stop editing immediately.

- Stop implementation or task-persistence preparation at the first newly discovered Mandatory Escalation Signal.
- Record the new evidence, the previous classification, the required new classification, and the affected Scope Lock fields.
- Level S or Level M must upgrade to at least Level L when a Mandatory Escalation Signal or high-risk area is discovered.
- Level L must upgrade to Level XL when architecture, a new module/service, phased rollout, coordinated migration, or major data-flow redesign becomes necessary.
- Mark the previous Next Action choice and approval stale when the new evidence changes risk, scope, approach, acceptance criteria, or stop conditions.
- Re-enter the stricter workflow using the evidence already gathered, regenerate the Development Plan and Scope Lock, and obtain the required approval again.
- If edits were already made before the discovery, disclose them, do not continue editing, and do not revert user or unrelated changes unless the user approves or the revert is required to leave the workspace coherent.
- Workspace coherence means the agent's own partial edits should not leave obvious syntax errors, type errors, broken imports, failed formatting caused by the edit, or tests/builds that fail solely because the edit is half-applied. If such breakage is discovered, first make the smallest repair or revert necessary to restore the pre-upgrade baseline, report it, and then wait for the stricter approval. Do not use coherence repair to implement additional scope or continue the high-risk change.
- Wait for the required approval before any further Level L or Level XL edits.

Why: reclassification is a control reset, not a warning appended to an already-authorized plan.

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

## Scope Lock

Scope-Lock-Version: cdp-scope/v1
in_scope: [...]
out_of_scope: [...]
non_goals: [...]
assumptions: [...]
stop_conditions: [...]
will_change: [...]
will_not_change: [...]
acceptance_criteria: [...]

## Requirement Understanding
- ...

## Requirement Decomposition
- ...

## Confirmed Evidence
- ...

## Open Assumptions
- ...

## Change Scope

- [Derived display only. It must exactly reflect `will_change` and `will_not_change` from the Scope Lock.]

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
- Approval Type: <full | conditional | partial>
- Approved Items: <all in_scope items or exact approved subset>
- Conditions Added To Scope Lock: <none or exact conditions>
- Unapproved Items: <none or exact remaining items>
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

For Level L and Level XL, before valid approval do not implement, create a `cdp-cdtask/v1` package, invoke CDTask, persist a task, or prepare executor-specific task instructions. Planning and the approval display are the only allowed outputs.

## Valid Approval Semantics

Approval is valid only when the reply unambiguously identifies both:

1. the authorized action for the current Execution Context; and
2. the approved plan, Scope Lock, phase, task, or explicitly named subset.

Exact offered action labels are valid when used as a direct reply to the displayed plan:

- standalone implementation: `Execute Now`, `Approve and implement`, `批准并实施`, `同意按此范围执行`, `同意并修改`;
- standalone persistence: `Save as CDTask`, `Approve and save as CDTask`, `批准此范围并保存为 CDTask`, `同意并保存为本地 task`;
- CDF-managed return: `Approve plan and continue CDF flow`, `批准计划并继续 CDF 流程`, `批准此 Scope Lock 并返回 CDF`.

A reply is not valid approval when it only acknowledges the message or leaves action/scope ambiguous. Invalid examples include:

- `ok`, `OK`, `好的`, `继续`, `Proceed`, `可以`, `嗯`, `yes`, `go ahead`;
- `sounds good`, `why not`, `I guess`, `そうですね`, `pourquoi pas`;
- a question, concern, alternative request, or new requirement without an explicit approval action.

For non-English replies, apply the same semantic test. Do not infer approval from tone, politeness, or conversational context alone.

Why: explicit action plus explicit scope prevents acknowledgement text from becoming implementation or persistence authorization.

## Approval Modes

Support exactly these modes:

### Full Approval

The user approves the displayed action and complete Scope Lock. Record `Approval Type: full` and `Approved Items: all in_scope items`.

### Conditional Approval

The user explicitly approves an action subject to one or more concrete conditions.

1. Normalize each condition into the applicable `in_scope`, `out_of_scope`, `non_goals`, `assumptions`, `stop_conditions`, `will_change`, or `will_not_change` field.
2. Reject conditions that are ambiguous, conflict with acceptance criteria, or require an unplanned scope expansion.
3. Record `Approval Type: conditional` and the exact normalized conditions in the Approval Record.
4. The conditional Scope Lock replaces the earlier Scope Lock for all later handoff.

Example: `批准并实施，但不得修改数据库 schema` is valid only after `database schema` appears in `will_not_change` or `non_goals`.

### Partial Approval

The user approves only explicitly named phases, tasks, or scope items.

1. Create an approved-subset Scope Lock containing only the approved items and their necessary existing constraints.
2. List every remaining item under `Unapproved Items`; do not treat it as implicitly approved.
3. Record `Approval Type: partial` and the exact approved subset.
4. Do not prepare implementation or CDTask handoff information for unapproved items.

If a condition or partial selection adds new scope, changes architecture, introduces a Mandatory Escalation Signal, or changes acceptance meaning, treat the previous plan as stale, replan, rerun classification, and request approval again.

## Locked Scope Echo

After any valid full, conditional, or partial approval, immediately echo this concise summary before taking the authorized next action:

```md
## Locked Scope Summary

### In Scope
- ...

### Will Not Change
- ...

### Non-Goals
- ...

Approval Type: <full | conditional | partial>
Authorized Action: <Execute Now | Save as CDTask | Return Approved Plan Package to CDF>
```

Copy these items from the approved Scope Lock without paraphrasing. If the echo would differ from what the user approved, stop and ask for confirmation of the corrected Scope Lock instead of proceeding. A second approval is not required when the echo is an exact restatement and the user does not correct it.

## Ambiguous Approval Follow-Up

For an invalid or ambiguous reply, do not advance and do not repeat the entire plan. Use the user's language and ask:

```md
I need an explicit approval action for the locked scope before continuing.

Choose one:
1. `Execute Now` — approve implementation of the displayed Scope Lock.
2. `Save as CDTask` — approve persistence and task handoff only; no implementation now.
3. `Request changes` — revise the plan or Scope Lock.
```

In `cdf-managed`, replace options 1 and 2 with `Approve plan and continue CDF flow`; keep `Request changes`.

A deferred-task approval approves task persistence only. It never authorizes implementation in the current turn. A managed approval means `PLAN_APPROVED`; return the Approved Plan Package to CDF and stop before `TASKING`.

When resuming a standalone local task with `Contract-Version: cdp-cdtask/v1`, a clear request such as `Continue local task: <path>` or `继续执行本地 task：<path>` is implementation authorization for the saved scope only after the required target, evidence, branch, and commit re-checks pass. Do not request the same approval again when nothing material has changed. If the saved task conflicts with the current workspace or the plan must expand, update the plan and request approval again.

In `standalone`, when the user explicitly hands the saved task to an external coding agent and asks that agent to execute it, the external agent may implement only the saved Task Breakdown and must obey the Scope Guard and Handoff Rules. The task document by itself is not execution authorization. In `cdf-managed`, executor assignment and execution authorization remain outside CDP.

If the user responds to an approval request with a new requirement instead of clear approval, do not treat it as approval and do not edit. Mark the previous approval request as stale, incorporate the new requirement, and rerun target check, requirement understanding, decomposition, evidence inspection, and final risk classification. Then produce an updated Level L approval request or Level XL design request as needed.

If the new requirement merely narrows the proposed scope, treat it as partial or conditional approval only for the narrowed subset, update the scope, risks, and test plan, and take only the context-specific action when the remaining authorization is explicit. If the new requirement expands scope, changes architecture, touches a new high-risk area, or conflicts with the previous plan, request approval again for the revised plan.

## Final Response Rule

Branch the final response by Execution Context.

In `cdf-managed`, never use the standalone code-change final response. Before approval, report `Planning Status: PLAN_READY`; after approval, report `Planning Status: APPROVED`. Always state that CDF owns lifecycle continuation, execution by CDP is not authorized, and CDP made no code changes:

```md
# Approved Plan Package

Planning Status: <PLAN_READY | APPROVED>
Lifecycle Owner: CDF
Execution by CDP: Not authorized
Code Changes by CDP: None
Scope-Lock-Version: cdp-scope/v1
Approval Type: <pending | full | conditional | partial>
Handoff: <awaiting plan approval | ready for CDF tasking | blocked with reason ...>
Next Owner: <Human approver | CDF>
```

After managed approval, use `Handoff: ready for CDF tasking` and `Next Owner: CDF`, include the complete Development Plan, canonical Scope Lock, Approval Record, and Locked Scope Summary in the Approved Plan Package, and stop. Do not check CDTask availability, invoke CDTask, create a local task, offer CDP resume, or report implementation verification as completed.

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
