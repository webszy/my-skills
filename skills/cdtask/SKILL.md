---
name: cdtask
description: Convert approved development plans into scoped task definitions and executor handoff information. Use when CDF provides an approved plan for managed tasking, when standalone CDP hands off approved work for persistence, or when the user asks to split a stable requirement or plan into dependency-aware tasks. CDTask may optionally persist designated task documents, but it does not execute, schedule, or manage the development lifecycle.
---

# Controlled Development Task

## Purpose

CDTask is the task-definition and handoff skill that converts an approved development plan into scoped, dependency-aware, verifiable task definitions and executor handoff information.

```text
Approved Plan
  -> Scope Lock
  -> Dependency Analysis
  -> Task Compilation
  -> Task Readiness Gate
  -> Executable Task Definitions
```

This skill has three first-class inputs:

* an approved `cdf-cdtask/v1` planning result from CDF for managed tasking,
* an approved `cdp-cdtask/v1` package that must be saved for deferred execution,
* a stable manual requirement document, PRD, technical proposal, or implementation plan that must be reviewed and split into tasks.

The `cdf-cdtask/v1` and `cdp-cdtask/v1` contracts, their `Approval-State` fields, and the related handoff structures are internal formats for CDF v0.1 skill coordination. Preserve and validate them as defined below. They are not a public runtime protocol and do not imply runtime, scheduler, or executor capabilities.

The CDF path preserves prior human plan approval and returns executable task definitions to CDF. The standalone CDP path preserves prior scope approval and local deferred-task behavior. The manual path remains a planning artifact until CDP or an equivalent risk and approval workflow authorizes implementation.

The goal is not just to create a task list.

The goal is to create a handoff-ready task section that:

* preserves the confirmed requirement boundary,
* prevents scope creep,
* protects explicit non-goals,
* splits work into dependency-aware tasks,
* gives every task clear acceptance criteria,
* states what must not change,
* gives the applicable executor strict handoff rules,
* performs a task-definition readiness pass before declaring tasks ready.

This skill does not implement code.

This skill does not invoke an executor.

This skill describes dependency and conflict facts but does not schedule tasks or decide whether execution is sequential, parallel, or mixed.

This skill does not perform independent implementation review.

This skill does not create a full lightweight spec system.

This skill prepares task breakdown and handoff sections that can be returned in chat, appended to an existing requirement document, or saved as a designated local task document.

It directly accepts the managed `cdf-cdtask/v1` contract from CDF and the existing `cdp-cdtask/v1` handoff contract produced when a user chooses `Save as CDTask` / `同意并保存为本地 task` at a standalone CDP approval gate.

---

# Core Principle

A task breakdown is valid only if it is constrained by the requirement boundary.

The assistant must not expand the requirement, add new architecture, add extra features, or convert future notes into current implementation tasks unless the user explicitly includes them in the current scope.

When in doubt, preserve the smaller scope.

The output is not complete until the Task Readiness Gate passes.

---

# Responsibility Boundary

CDTask v0.1 is responsible for:

* converting approved plans into scoped task definitions,
* preserving approved scope and explicit non-goals,
* defining dependencies and bounded write areas,
* defining acceptance criteria and verification requirements,
* preparing executor handoff information.

This skill may:

* review an existing requirement document,
* validate a `cdf-cdtask/v1` managed planning handoff,
* validate a `cdp-cdtask/v1` handoff package,
* extract in-scope and out-of-scope boundaries,
* identify non-goals,
* split the requirement into implementation tasks,
* declare task dependencies as a directed acyclic graph,
* declare write scope and shared contracts,
* define task-level acceptance criteria,
* define task-level verification steps,
* append a scope guard checklist,
* append Codex handoff rules,
* produce an executor-neutral managed Execution Contract,
* perform a Task Readiness Gate for ambiguity, conflict, and scope creep,
* optionally create or update the single task document explicitly selected by the user, CDF, or the CDP handoff contract.

This skill must not:

* implement code,
* modify source code, schemas, migrations, runtime configuration, generated files, tests, or other implementation files,
* invoke an executor,
* manage executor processes, sessions, or runtime statuses,
* schedule tasks or decide the final sequential/parallel/mixed execution strategy,
* manage the development lifecycle or CDF flow,
* execute implementation verification,
* perform independent implementation code review, run the fix loop, or declare final lifecycle completion,
* plan requirements, redesign approved architecture, or define CDF approval policy and flow transitions outside `TASKING`,
* claim an executor has executed anything,
* rewrite the whole requirement unless the user explicitly asks,
* invent missing architecture,
* silently resolve major ambiguity,
* include non-goals as current tasks,
* mark a document as ready when unresolved ambiguity or conflict remains.

CDP owns planning and the Next Action decision. CDF owns flow coordination, human decision points, and component handoff. Execution, scheduling, runtime management, and implementation review are outside CDTask v0.1. In managed mode, CDTask stops after producing task definitions that pass the Task Readiness Gate and returning them to CDF.

---

# Optional Role in the Flow

CDTask is optional. Not every CDP plan must become a CDTask.

Use CDTask when:

* work needs a durable task record,
* work will be resumed later,
* work needs explicit task decomposition or dependency metadata,
* execution should be separated from planning.

In standalone CDP, the user may choose `Execute Now` instead and bypass CDTask. Create or persist task definitions only when the selected path, input contract, or explicit user request requires it. Readiness alone never authorizes execution.

---

# When To Use This Skill

Use this skill when the user asks for any of the following:

* split this requirement into tasks,
* break this PRD into implementation tasks,
* create a task list for Codex,
* append tasks to this requirement document,
* prepare this document for Codex,
* create a scoped execution plan,
* convert this clarified requirement into actionable tasks,
* save an approved CDP scope as a local task for deferred execution,
* prevent Codex from over-implementing,
* add Codex handoff rules,
* review whether this task breakdown is ready for handoff.

Also use this skill when the user has a technical requirement and wants to hand it off to Codex, Claude Code, Cursor, or another coding agent.

Use the CDP handoff path without asking the user to restate the requirement when the input contains a valid `CDP Task Handoff Package` with `Contract-Version: cdp-cdtask/v1`.

Use CDF Managed Tasking Mode without asking the user to restate approved information when CDF supplies a valid `CDF Tasking Handoff` with `Contract-Version: cdf-cdtask/v1`.

---

# Do Not Use This Skill For

Do not use this skill when the user is still brainstorming and has not provided a reasonably stable requirement.

Do not use this skill to directly write or modify code.

Do not use this skill to create a full product roadmap.

Do not use this skill to design a full spec management system.

Do not use this skill to expand a requirement into future phases unless the user explicitly asks for future-phase planning.

---

# Input Routing Decision Tree

Choose the path before producing tasks:

```text
Valid cdf-cdtask/v1 package?
  -> Yes: Mode G, source = cdf, approval state = plan-approved.
  -> No: Valid cdp-cdtask/v1 package?
       -> Yes: Mode F, source = cdp, approval state comes from the package.
       -> No: Is the manual requirement stable enough to split?
            -> Yes: Mode A, B, C, or D, source = manual.
            -> No: Mode E and recommend CDP when risk classification or approval is still needed.
```

Manual input must never be labeled `source: cdp` and must never use `approval_state: scope-approved-execution-deferred`.

Manual input must also never be labeled `source: cdf`, use `approval_state: plan-approved`, or inherit managed execution authorization.

---

# CDF Managed Tasking Input Contract

`cdf-cdtask/v1` is distinct from `cdp-cdtask/v1`. Do not reuse, reinterpret, or modify the standalone deferred-task contract for managed tasking.

The canonical managed input begins with:

```md
# CDF Tasking Handoff

Contract-Version: cdf-cdtask/v1
Handoff-Type: managed-tasking
Approval-State: plan-approved
Execution-Owner: cdf
Risk-Level: <Level S | Level M | Level L | Level XL>
Workspace: <absolute path or Unavailable>
Source-Branch: <branch or Unavailable>
Source-Commit: <commit or Unavailable>

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
...

## Requirement Decomposition
...

## Confirmed Evidence
...

## Open Assumptions
...

## Change Scope

### Will Change
...

### Will Not Change
...

## Proposed Design
...

## Data Model / API / State Flow
...

## Approved Phase Boundary
...

## Implementation Plan / Phases
...

## Risks
...

## Acceptance Criteria
...

## Verification Strategy
...

## Rollback Plan
...

## Approval Record
- Approval Type: <full | conditional | partial>
- Approved Items: <all in_scope items or exact approved subset>
- Conditions Added To Scope Lock: <none or exact conditions>
- Unapproved Items: <none or exact remaining items>
- Scope Approved: Yes
```

Within this internal handoff format, `Execution-Owner: cdf` records the component that receives control after task definition. It does not mean that CDF or CDTask executes code, and it does not define a runtime executor.

## Managed Field Requirements

Require for every risk level:

* `Contract-Version: cdf-cdtask/v1`,
* `Handoff-Type: managed-tasking`,
* `Approval-State: plan-approved`,
* `Execution-Owner: cdf`,
* `Risk-Level: Level S | Level M | Level L | Level XL`,
* `Scope Lock` with `Scope-Lock-Version: cdp-scope/v1` and all eight required fields,
* `Requirement Understanding`,
* `Change Scope` with `Will Change` and `Will Not Change`,
* `Acceptance Criteria`,
* `Verification Strategy`,
* `Approval Record` confirming human plan approval, approval type, approved items, conditions, and any unapproved items.

Require when available or relevant: `Requirement Decomposition`, `Confirmed Evidence`, `Open Assumptions`, `Risks`, and workspace/branch/commit metadata. Missing optional metadata must be reported as `Unavailable`; do not invent it.

For Level L and Level XL, require stronger scope boundaries, risk details, and rollback considerations where applicable. For Level XL, require substantive `Proposed Design`, `Data Model / API / State Flow`, `Approved Phase Boundary`, and `Implementation Plan / Phases`.

Do not require Level S or Level M to fill architecture-only sections with meaningless placeholders. Do not upgrade Level S or Level M merely to satisfy the protocol.

## Managed Package Validation

When this contract is present:

1. Validate the exact contract version, handoff type, approval state, execution owner, and supported risk level.
2. Confirm the Approval Record shows prior human plan approval.
3. Validate required fields according to risk without weakening higher-risk controls.
4. Reuse the approved plan as the source of truth. Do not ask the user to repeat approved information.
5. Validate the Scope Lock verbatim and run Scope Lock Consistency Validation before decomposition.
6. Validate consistency and task readiness, but do not silently redesign, expand, narrow, or remove constraints from the approved plan.
7. If task decomposition exposes a blocking conflict, missing required decision, or invalid approved premise, return `Tasking Status: BLOCKED` to CDF. Do not independently replan; CDF may return the flow to CDP.
8. If a task definition can be repaired without changing approved scope, return it to draft, repair it, and rerun the Task Readiness Gate.
9. Run Scope Lock, DAG Dependency Analysis, Managed Task Breakdown, Scope Guard Checklist, Execution Contract, and Task Readiness Gate.
10. By default return the structured result to CDF without saving a file.

In CDF managed mode, do not introduce new implementation-affecting assumptions. If missing information would materially affect behavior, scope, architecture, API or data contracts, shared contracts, acceptance criteria, verification strategy, risk, product behavior, or implementation direction, return `Tasking Status: BLOCKED` to CDF. Do not guess, choose a default, or silently normalize the gap. CDF may return the flow to CDP for replanning or renewed approval.

The canonical Scope Lock in an approved input is never derived or reconstructed: copy it verbatim into every required artifact location. CDTask may derive only task-definition details that are fully implied by the approved Plan and introduce no new implementation decision. Allowed derivations include assigning stable task IDs, making already-implied dependency edges explicit, normalizing non-canonical headings, creating readable projections from the copied Scope Lock, deriving conservative task Write Scope from `will_change` and confirmed evidence, listing Shared Contracts already present in the approved Plan or evidence, and formatting approved Acceptance Criteria as task-level checklists.

## Scope Lock Consistency Validation

Run this validation for every `cdf-cdtask/v1` or `cdp-cdtask/v1` input before task decomposition and again before the Task Readiness Gate.

### Contract Validation

1. Require `Scope-Lock-Version: cdp-scope/v1`.
2. Require arrays named exactly `in_scope`, `out_of_scope`, `non_goals`, `assumptions`, `stop_conditions`, `will_change`, `will_not_change`, and `acceptance_criteria`.
3. Reject missing fields, placeholders, scalar replacements, or ambiguous catchalls such as `etc.`, `as needed`, or `unrelated changes` in restrictive fields.
4. Treat the received Scope Lock as immutable approved data. Copy it into outputs verbatim; do not paraphrase, merge, reorder, omit, weaken, or broaden list items.
5. Validate every readable projection, including `Change Scope`, `Scope Lock`, plan prose, phase boundaries, and high-level Acceptance Criteria, against the canonical block. A projection may add task-definition detail only when fully implied; it may not change meaning.
6. Validate `Approval Type: full | conditional | partial`. Conditional approval must have its conditions represented in the Scope Lock.
7. For partial approval, require `Approved Items` to match the approved-subset Scope Lock `in_scope` items one-for-one and verbatim. Require every `Unapproved Items` entry to remain verbatim and explicitly excluded; no task may be created for it.

### Task-to-Scope Validation

For every proposed task, verify:

- its Goal and Scope map to one or more `in_scope` items;
- its Write Scope and affected contracts map to `will_change`;
- it does not implement anything in `out_of_scope`, `non_goals`, or `will_not_change`;
- its Implementation Notes do not turn `assumptions` into confirmed facts or new decisions;
- its stop/escalation behavior preserves every applicable `stop_conditions` item;
- its task-level acceptance criteria refine, and never replace or weaken, the high-level `acceptance_criteria`.
- for partial approval, none of its Goal, Scope, Write Scope, Shared Contracts, Implementation Notes, or Acceptance Criteria maps to an `Unapproved Items` entry.

Do not allow `non_goals` to be summarized as generic prose. Preserve each item as an explicit prohibition in Scope Guard and `Must Not Change` checks.

### Validation Outcomes

- `READY`: every task maps to the Scope Lock, all prohibitions are preserved, and no scope item changed meaning.
- `NOT_READY`: CDTask introduced a task-definition-only defect, such as an extra task, omitted prohibition, or mismatched derived field, and can remove or repair it without changing the approved plan. Repair and rerun validation.
- `BLOCKED`: the Scope Lock is missing, invalid, internally conflicting, inconsistent with the approved plan, or too narrow for the requested task breakdown; a new impact area, assumption, decision, or scope extension would be required.

For `BLOCKED`, return the exact conflict to CDF for managed input or direct the standalone user back to CDP. Any scope expansion requires CDP replanning, a new `cdp-scope/v1` block, and renewed human approval. CDTask has no authority to expand scope.

Why: task decomposition is allowed to add structure, not implementation meaning.

## CDF-to-Scope-Lock Mapping

Apply this mapping without expanding the approved plan:

* `In Scope` <- `Scope Lock / in_scope`
* `Out Of Scope` <- `Scope Lock / out_of_scope`
* `Non-Goals That Must Not Be Implemented` <- `Scope Lock / non_goals`
* `Assumptions` <- `Scope Lock / assumptions`
* `Stop Conditions` <- `Scope Lock / stop_conditions`
* allowed task write areas <- `Scope Lock / will_change`
* protected areas and behavior <- `Scope Lock / will_not_change`
* high-level task coverage <- `Scope Lock / acceptance_criteria`

Do not turn future notes into current tasks. Do not invent architecture or remove approved constraints.

---

# CDP Handoff Input Contract

The canonical CDP input begins with:

```md
# CDP Task Handoff Package

Contract-Version: cdp-cdtask/v1
Handoff-Type: deferred-local-task
Title: ...
Workspace: ...
Requested-Task-Path: ...
Risk-Level: <Level S | Level M | Level L | Level XL>
Approval-State: scope-approved-execution-deferred
Source-Branch: ...
Source-Commit: ...

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
```

It must also contain these sections with the exact headings:

1. `Scope Lock` containing `Scope-Lock-Version: cdp-scope/v1` and all eight required fields
2. `Requirement Understanding`
3. `Requirement Decomposition`
4. `Confirmed Evidence`
5. `Open Assumptions`
6. `Change Scope`, including `Will Change` and `Will Not Change`
7. `Proposed Design`
8. `Data Model / API / State Flow`
9. `Approved Phase Boundary`
10. `Implementation Plan / Phases`
11. `Risks`
12. `Acceptance Criteria`
13. `Test Plan / Test Strategy`
14. `Rollback Plan`
15. `Approval Record`
16. `Handoff Execution Paths`
17. `Resume Rules`

For Level XL, `Proposed Design`, `Data Model / API / State Flow`, and `Approved Phase Boundary` must contain the approved design content. For Level S, Level M, and Level L, these headings remain present with `Not applicable for <risk level>.` when they have no approved content, so the interface stays structurally stable without inventing architecture.

## CDP Package Validation

When this contract is present:

1. Confirm that `Contract-Version` is exactly `cdp-cdtask/v1`.
2. Confirm that `Handoff-Type` is `deferred-local-task`.
3. Confirm that `Approval-State` is `scope-approved-execution-deferred`.
4. Confirm that the approval record says scope is approved and code changes are not authorized in the current turn.
5. Confirm that every required heading is present and that no blocking placeholder or unresolved conflict remains.
6. Confirm the Scope Lock block was copied verbatim from the approved CDP plan and run Scope Lock Consistency Validation.
7. Reuse the approved CDP content as the source of truth. Do not ask the user to repeat already confirmed scope, evidence, risks, or acceptance criteria.
8. Normalize approval-display labels into the exact package headings before validation. For example, `Will change:` maps to `Will Change`; do not reject a valid package because the prior chat template used different capitalization. Never normalize or rewrite the canonical Scope Lock block.
9. Run the normal Scope Lock, Task Breakdown, Scope Guard, Codex Handoff Rules, and Task Readiness Gate using that content.

If a required field or section is missing, ask only for the missing information. If the package conflicts with itself, mark it `Not Ready` and do not save a ready task.

The CDP approval authorizes creation of the local task document only. It does not authorize implementation changes in the current turn.

## CDP-to-Scope-Lock Mapping

Use the canonical `cdp-scope/v1` block directly. Do not reconstruct it from `Change Scope`, `Open Assumptions`, `Resume Rules`, or plan prose.

* `In Scope` <- `Scope Lock / in_scope`
* `Out Of Scope` <- `Scope Lock / out_of_scope`
* `Non-Goals That Must Not Be Implemented` <- `Scope Lock / non_goals`
* `Assumptions` <- `Scope Lock / assumptions`
* `Stop Conditions` <- `Scope Lock / stop_conditions`
* allowed task write areas <- `Scope Lock / will_change`
* protected areas and behavior <- `Scope Lock / will_not_change`
* high-level task coverage <- `Scope Lock / acceptance_criteria`

Do not invent additional scope, non-goals, assumptions, stop conditions, or acceptance meaning while mapping.

## Handoff Execution Paths

A saved CDP task supports two legal execution paths:

* Path A — Same-stack resume: the user requests `Continue local task: <path>`. CDP revalidates the target, evidence, risk, branch, and commit before implementation.
* Path B — External coding agent: the user explicitly gives the local task to another coding agent and instructs it to implement only the Task Breakdown under the Scope Guard and Codex Handoff Rules.

The task document alone is not execution authorization for either path. External execution is not automatically considered completed by CDP; bring the result back to CDP for verification or closure when CDP-managed completion is required.

---

# Required Workflow

Follow this workflow strictly:

```text
Requirement Readiness Check
  -> Scope Lock
  -> Dependency Analysis
  -> Task Breakdown
  -> Scope Guard Checklist
  -> Codex Handoff Rules (standalone/manual) OR Execution Contract (CDF managed)
  -> Task Readiness Gate
  -> Optional Task Persistence (only when requested or required by standalone CDP handoff)
  -> Return To CDF (CDF managed) OR Finish Standalone/Manual Path
```

The Task Readiness Gate is mandatory. It is the canonical name for the task-definition quality gate formerly called the Final Review Gate; it is not implementation review and does not inspect implementation code.

When reading an existing standalone/manual task document, accept the legacy `Final Review Gate` heading as the same compatibility gate. New output must use `Task Readiness Gate`.

Do not skip it.

The task breakdown is complete only if the Task Readiness Gate passes.

---

# Phase 1: Requirement Readiness Check

Before task breakdown, check whether the existing requirement is ready to be split into tasks.

Evaluate the requirement against these questions:

1. Is the implementation goal clear?
2. Is the current version scope clear?
3. Are non-goals or exclusions clear?
4. Are affected modules, APIs, tables, files, user flows, or data flows identified?
5. Are success paths described?
6. Are failure paths described?
7. Are data model changes clear?
8. Are migration requirements clear?
9. Are compatibility requirements clear?
10. Are acceptance criteria clear?
11. Are testing or verification expectations clear?
12. Is it clear whether backend, frontend, shared schema, OpenAPI, client code, tests, or migrations are in scope?
13. Is it clear what must not be changed?
14. Is there enough information for the intended executor to implement without inventing decisions?

If the requirement is ready, continue to Scope Lock.

If the requirement is partially ready but the missing information is minor, make conservative assumptions and label them for standalone/manual input.

For `cdf-cdtask/v1`, do not apply that conservative-assumption rule to any implementation-affecting gap. Derive only task-definition details fully implied by the approved Plan. If the missing information would materially affect implementation or approved semantics, return `BLOCKED` to CDF without guessing or selecting a default.

If standalone/manual input has blocking ambiguity, stop and ask for confirmation before producing the final task breakdown. If managed input has blocking ambiguity that affects implementation or approved semantics, return `BLOCKED` to CDF instead.

Use this format for standalone/manual input when the requirement is not ready. For managed input, return `Tasking Status: BLOCKED` and the exact missing approved decision to CDF instead of asking the user directly:

```markdown
# Requirement Readiness Check

## Ready To Split?
No / Partially

## Clear Points
- ...

## Blocking Ambiguities
- ...

## Required User Confirmations
1. ...
2. ...

## Why This Cannot Be Finalized Yet
- ...

## Suggested Next Step
Please confirm the points above, then I can produce the scoped task breakdown.
```

Do not produce a final task breakdown when blocking ambiguity remains.

For a valid `cdp-cdtask/v1` package, treat CDP's Requirement Gate and scope approval as prior readiness evidence. Still perform this readiness check as validation, but do not repeat questions unless a required field is missing, a placeholder remains, or the package conflicts with the current document.

For a valid `cdf-cdtask/v1` package, treat CDP planning and human plan approval as prior readiness evidence. Validate the approved plan without repeating resolved questions. If the plan itself is missing, conflicting, or invalid, return `BLOCKED` to CDF rather than asking CDTask to replan it.

---

# Phase 2: Scope Lock

Before producing tasks, extract and restate the implementation boundary.

For `cdf-cdtask/v1` and `cdp-cdtask/v1`, first reproduce the received canonical block verbatim:

```yaml
Scope-Lock-Version: cdp-scope/v1
in_scope: [...]
out_of_scope: [...]
non_goals: [...]
assumptions: [...]
stop_conditions: [...]
will_change: [...]
will_not_change: [...]
acceptance_criteria: [...]
```

Then produce the readable projection below. The projection must map one-to-one to the canonical fields and cannot replace them.

Always include:

```markdown
## Scope Lock

### In Scope
- ...

### Out Of Scope
- ...

### Non-Goals That Must Not Be Implemented
- ...

### Assumptions
- ...

### Stop Conditions
- ...

### Will Change
- ...

### Will Not Change
- ...

### High-Level Acceptance Criteria
- ...
```

## Scope Lock Rules

1. Anything listed as a non-goal must not appear as a current implementation task.
2. Future work may be documented only under "Future / Not In This Version".
3. Do not turn future sorting rules, dashboards, frontend display, provider-level stats, daily aggregation, or architecture improvements into current tasks unless explicitly requested.
4. If the user says "第一版", "暂时不做", "不要扩大", "只做写入", "先不做展示", or similar phrases, treat those as hard boundaries.
5. If the requirement says not to modify a module, do not include that module in "Files Likely Touched".
6. If the requirement says not to add a table, do not propose a table.
7. If the requirement says not to add a service method, do not propose a service method.
8. If the requirement says not to modify sorting, do not include sorting implementation as a current task.
9. If the requirement says sorting should only be documented for future work, include it only as documentation or future-note content.
10. If the requirement says only backend write logic is in scope, do not include frontend, shared schema, OpenAPI, or display tasks.
11. For `cdf-cdtask/v1`, copy the received canonical Scope Lock verbatim. Derive only readable projections and task-definition details from it; never reconstruct it from plan prose.
12. If managed decomposition reveals a contradiction in the approved plan, return `BLOCKED` to CDF; do not independently replan.
13. For either approved contract, preserve every canonical Scope Lock list item verbatim in the stored or returned artifact.
14. If CDTask itself introduces an out-of-scope task or drops a prohibition, use `NOT_READY`, repair the task definition, and rerun validation.
15. If satisfying the requested breakdown requires new scope, changed assumptions, or weakened prohibitions, use `BLOCKED` and return to CDP for replanning and renewed approval.

---

# Phase 3: Dependency Analysis

Before listing tasks, identify explicit logical dependencies. Do not infer ordering solely from task numbering.

For standalone/manual compatibility, the existing linear presentation remains valid when the work is actually linear:

````markdown
## Dependency Order

```text
Task 1 -> Task 2 -> Task 3 -> Task 4
```

### Dependency Notes

* Task 2 depends on Task 1 because ...
* Task 4 must happen after Task 3 because ...

````

Rules:

1. Database migration should usually come before code that depends on new fields.
2. Resolver or helper return-shape changes should come before route integration.
3. Shared helpers should come before endpoint-specific use.
4. Endpoint integrations should be separated when they have different behavior.
5. Tests or verification should come after implementation tasks.
6. Documentation-only future rules should not become implementation dependencies.

For CDF managed mode, use stable task IDs and DAG-style dependency data:

````markdown
## Dependency Graph

```text
TASK-001
├── TASK-002
└── TASK-003
     ↓
  TASK-004
```

## Dependency Data

```yaml
TASK-001:
  depends_on: []
TASK-002:
  depends_on:
    - TASK-001
TASK-003:
  depends_on:
    - TASK-001
TASK-004:
  depends_on:
    - TASK-002
    - TASK-003
```

### Dependency Notes

* `TASK-002` and `TASK-003` each depend on `TASK-001` because ...
* No explicit dependency is detected between `TASK-002` and `TASK-003`; this is not an instruction to run them in parallel.
````

Managed dependency rules:

1. Use stable IDs `TASK-001`, `TASK-002`, and so on.
2. Represent every task in dependency data, including tasks with `depends_on: []`.
3. Support branches and joins; do not force a linear chain when evidence supports a DAG.
4. Reject cycles as `NOT_READY` when task-definition repair can resolve them inside approved scope; use `BLOCKED` when the approved plan itself is cyclic or contradictory.
5. Declare only logical dependencies supported by scope, interfaces, data flow, or implementation order.
6. CDTask may report that no explicit dependency is detected, but it must not command parallel execution.

## Parallelism Boundary

CDTask supplies `Dependencies`, `Write Scope`, `Shared Contracts`, and `Risk`. CDTask does not decide whether later execution is `SEQUENTIAL`, `PARALLEL`, or `MIXED`; that decision belongs to the execution process outside CDTask v0.1.

Parallel eligibility requires CDF to evaluate at least:

```text
No dependency
AND
No overlapping write scope
AND
No conflicting shared contract
```

CDTask must produce accurate metadata for a later execution decision but must not schedule or select parallelism.

---

# Phase 4: Task Breakdown

Break the requirement into small, dependency-aware tasks.

Tasks must be implementation-sized and reviewable.

Use this exact template for each task unless the user requests another format:

```markdown
## Task N: <Task Name>

### Goal
Describe the specific outcome of this task.

### Dependency
- Depends on: Task X / None

### Files Likely Touched
- `path/to/file`

### Implementation Notes
- Concrete implementation constraints.
- Important order of operations.
- Known edge cases.

### Acceptance Criteria
- [ ] Observable condition 1.
- [ ] Observable condition 2.
- [ ] Existing behavior remains unchanged.

### Must Not Change
- [ ] Do not change unrelated behavior.
- [ ] Do not implement excluded scope.
- [ ] Do not modify unrelated files.

### Verification
- Manual verification or test case.
````

For CDF managed mode, use this schema for every task:

```markdown
## TASK-001: <Task Name>

### Goal
- ...

### Dependencies
- None
```

or list stable IDs:

```markdown
### Dependencies
- TASK-001
- TASK-002
```

Then include:

```markdown
### Scope
- ...

### Write Scope
- `path/...`
- `path/...`

### Shared Contracts
- <API / schema / type / state / config / shared interface>
- None

### Implementation Notes
- ...

### Acceptance Criteria
- [ ] ...

### Must Not Change
- [ ] ...

### Verification
- ...

### Risk
- Level S / Level M / Level L / Level XL

### Status
- <DRAFT | READY>
```

Managed field rules:

* `Dependencies`: list explicit logical task dependencies. Use `None` only when there are none.
* `Write Scope`: list concrete files, directories, modules, or bounded implementation areas supported by evidence. If exact files are unknown, write `unresolved` or use a conservative confirmed module boundary; never invent paths.
* `Shared Contracts`: list API contracts, database schema, shared types, state models, shared configuration, common interfaces, generated contracts, or protocol definitions. Write `None` only when evidence supports no shared contract; never omit the field.
* `Risk`: inherit the approved Plan risk unless a narrower task-specific risk is known. Never silently downgrade a higher-risk approved Plan in a way that weakens controls.
* `Status`: keep tasks as draft definitions until the Task Readiness Gate passes. Set every managed task to `READY` only after the gate returns `READY`.
* Do not use runtime statuses such as `RUNNING`, `COMPLETED`, or `FAILED`; runtime lifecycle state is outside CDTask v0.1.

## Task Design Rules

1. Do not combine unrelated work into one task.
2. Separate database migration from business logic.
3. Separate resolver or shared helper changes from route integration.
4. Separate each affected API route when possible.
5. Separate tests from implementation when the implementation is non-trivial.
6. Each task must have clear acceptance criteria.
7. Each task must state what must not change.
8. The task order must respect dependencies.
9. If a task depends on another task, state the dependency.
10. Avoid vague tasks such as "implement feature" or "update logic".
11. Avoid tasks that require Codex to infer hidden decisions.
12. Do not include future work in current tasks.
13. Do not include optional improvements unless the user explicitly requests them.
14. Do not include broad refactors unless the requirement is explicitly a refactor.
15. Do not include "cleanup unrelated code" as a task.
16. Do not add frontend, schema, OpenAPI, or generated-file tasks unless the requirement explicitly includes them.
17. Do not add extra tests beyond the requested scope if the user explicitly says only manual verification is required.
18. Do not omit verification for high-risk changes.
19. In managed mode, give every task a stable ID, Dependencies, Scope, Write Scope, Shared Contracts, Acceptance Criteria, Must Not Change, Verification, Risk, and Status.
20. Resolve Write Scope from approved evidence when possible. An explicit `unresolved` value may pass only when the task remains conservatively bounded and the uncertainty is disclosed to CDF; otherwise use `NOT_READY` for a repairable task-definition gap or `BLOCKED` when required evidence or scope authority is missing.

---

# Phase 5: Scope Guard Checklist

After the task list, output a scope guard checklist.

Use this format:

```markdown
# Scope Guard Checklist

- [ ] Does not implement any non-goal.
- [ ] Does not modify unrelated modules.
- [ ] Does not add unrequested tables or services.
- [ ] Does not add unrequested queues, cron jobs, workers, or background processing.
- [ ] Does not change frontend unless explicitly in scope.
- [ ] Does not change API response structures unless explicitly in scope.
- [ ] Does not change generated OpenAPI files unless explicitly in scope.
- [ ] Does not alter existing sorting behavior unless explicitly in scope.
- [ ] Does not add provider/platform/date dimensions unless explicitly in scope.
- [ ] Preserves existing behavior for requests that are outside the new feature path.
- [ ] Keeps future work separate from current implementation tasks.
```

Customize the checklist based on the requirement.

If the requirement contains explicit non-goals, include each non-goal in the checklist.

For managed mode, also include checks that every task has stable Dependencies, a bounded or explicitly unresolved Write Scope, a Shared Contracts declaration, inherited-safe Risk metadata, and no undisclosed write-scope/shared-contract conflict.

---

# Phase 6: Codex Handoff Rules

Preserve this compatibility handoff format for standalone CDP and manual paths when the user intends to give the document to Codex or another coding agent. Do not use it as the CDF managed contract.

This section is not an instruction for the assistant to execute code.

This section is only text that will be appended to the requirement document.

Use the heading:

```markdown
# Codex Handoff Rules
```

Do not call it "Codex Execution Result".

Do not imply that Codex has already executed anything.

Use this format:

```markdown
# Codex Handoff Rules

These rules govern Path B only after the user explicitly instructs the external coding agent to execute this task. Possession of the document alone is not implementation authorization.

1. Execute tasks strictly in the order listed.
2. Only implement the content explicitly listed in the task breakdown.
3. Do not implement anything from the non-goals section.
4. Do not expand the scope, redesign architecture, or perform unrelated cleanup.
5. Do not modify unrelated files.
6. If current code conflicts with the requirement document, stop and report the conflict before inventing a solution.
7. After each task, self-check against that task's acceptance criteria.
8. After all tasks, check the reported result against the task acceptance criteria and Scope Lock. Do not perform an independent code review or automatic fix loop as part of this handoff.
9. After all tasks, output:
   - changed files,
   - completed tasks,
   - skipped tasks, if any,
   - tests or verification performed,
   - any behavior intentionally not changed,
   - any remaining risks.
```

Add project-specific prohibitions when relevant.

Examples:

* Do not modify `apps/web`.
* Do not modify `packages/shared`.
* Do not regenerate OpenAPI.
* Do not add a new statistics table.
* Do not add service-layer abstractions.
* Do not change existing list sorting logic.
* Do not modify frontend display.
* Do not modify API response structure.
* Do not add provider/platform/date dimensions.
* Do not perform unrelated refactors.

## CDF Managed Execution Contract

For `cdf-cdtask/v1`, produce an executor-neutral section with this heading:

```markdown
# Execution Contract
```

This contract prepares constraints for a separately authorized executor handoff. CDTask produces the handoff information but does not enforce it, manage execution, or invoke an executor.

Use this minimum contract:

```markdown
# Execution Contract

1. Execute only the assigned current task.
2. Stay inside the task's Scope and Write Scope.
3. Obey every Must Not Change item.
4. Do not implement future, optional, or excluded work.
5. Do not redesign architecture without escalation through CDF.
6. Do not modify unrelated files.
7. If code evidence materially conflicts with the approved task or Plan, stop and report the conflict.
8. Perform the task's required Verification.
9. Report changed files.
10. Report verification performed and actual results.
11. Report every unmet Acceptance Criterion.
12. Report any newly discovered assumption, scope expansion, architecture change, shared-contract impact, or risk escalation.
```

Add plan-specific constraints where needed. Keep the language executor-neutral: the executor may be Codex, Grok, Claude, or another coding agent selected by CDF.

An authorized executor may later self-check its assigned work and report verification evidence. Independent implementation review and any fix loop remain outside CDTask v0.1.

---

# Phase 7: Task Readiness Gate (formerly Final Review Gate)

After appending the task breakdown, scope guard checklist, and applicable handoff contract, review the entire resulting document from a task-definition quality perspective.

This gate is mandatory. It checks task definitions, not implementation code, and must not be confused with implementation review.

The assistant must check whether the final document contains:

1. unclear requirements,
2. hidden assumptions,
3. conflicting instructions,
4. missing acceptance criteria,
5. vague task boundaries,
6. task items that violate non-goals,
7. future work accidentally included as current work,
8. implementation steps that exceed the confirmed scope,
9. missing failure-path decisions,
10. missing verification or testing requirements,
11. inconsistent terminology,
12. ambiguity about affected files or modules,
13. ambiguity about whether frontend, backend, schema, OpenAPI, migration, or tests are in scope,
14. contradiction between "Non-Goals" and "Task Breakdown",
15. contradiction between "Scope Lock" and the applicable handoff contract,
16. contradiction between "first version" constraints and proposed tasks,
17. missing stop conditions for the executor,
18. missing rules for handling code/document conflicts.

For approved `cdf-cdtask/v1` and `cdp-cdtask/v1` handoffs also check:

- missing or changed `Scope-Lock-Version: cdp-scope/v1`;
- any missing, reordered, paraphrased, weakened, or broadened Scope Lock item;
- vague or collapsed `non_goals` instead of item-by-item prohibitions;
- tasks, write areas, contracts, or acceptance criteria that do not map to approved Scope Lock fields;
- any required scope expansion that has not returned to CDP and passed renewed approval.

For managed tasks also check:

19. missing or unstable task IDs,
20. missing or invalid DAG dependencies, including cycles,
21. missing or unsafely unresolved Write Scope,
22. missing Shared Contracts declarations,
23. write-scope overlap or shared-contract conflicts that are not disclosed,
24. missing task Risk or draft/READY state errors,
25. managed instructions that assign scheduling, execution, or final independent review to CDTask or the executor.

Use this format:

```markdown
# Task Readiness Gate

## Tasking Status
READY / NOT_READY / BLOCKED

## Readiness Findings

### Confirmed Clear
- ...

### Potential Ambiguities
- ...

### Potential Conflicts
- ...

### Scope Creep Risks
- ...

### Missing Decisions
- ...

## Required User Confirmations
1. ...
2. ...

## Final Status
Ready for task handoff / Not ready yet / Blocked; return to CDF
```

Use the managed outcomes precisely:

* `READY`: task definitions pass the gate and may return to CDF as handoff-ready task definitions. Only after this verdict may managed tasks use `Status: READY`.
* `NOT_READY`: CDTask can repair task-definition defects inside the approved scope, then rerun the gate.
* `BLOCKED`: the approved Plan is missing, conflicting, or invalid; an implementation-affecting decision or assumption is missing; or repair would require replanning or new approval. Return the gap or conflict to CDF; do not guess, choose a default, silently normalize it, or independently replan.

---

# Task Readiness Rules

## If the document is clear

If no meaningful ambiguity, conflict, or missing decision remains, mark the document as ready:

```markdown
## Final Status

Ready for task handoff.
```

Also include:

```markdown
Document readiness does not authorize implementation.
No blocking ambiguity found.
No scope conflict found.
No non-goal violation found.
```

## If the document has ambiguity

If there are unresolved ambiguities, do not mark it as ready.

For standalone/manual input, ask the user to confirm the missing decisions. For managed input, use `BLOCKED` when the approved Plan lacks the required decision or `NOT_READY` when CDTask can repair only the task definition inside approved scope, and return the result to CDF.

In managed mode, a repair is task-definition-only only when it is fully implied by the approved Plan and confirmed evidence and introduces no new implementation decision. Otherwise treat the ambiguity as `BLOCKED`.

For standalone/manual input, use direct questions.

Example:

```markdown
## Final Status

Not ready yet. User confirmation required before this document can be handed to Codex.

## Required User Confirmations

1. Should `success_count` write failure preserve the original success response?
2. Should this version modify backend tests, or only provide manual verification steps?
```

## If the document has conflicts

If the requirement contradicts itself, stop and report the conflict.

Do not silently choose one side. In managed mode, return `BLOCKED` to CDF rather than independently replanning.

Example:

```markdown
## Potential Conflicts

- The document says "do not modify OpenAPI", but Task 5 says "regenerate OpenAPI".
- The document says "first version only writes counters", but Task 4 includes backend list display changes.

## Final Status

Not ready yet. These conflicts must be resolved before handoff.
```

## If a task violates a non-goal

Remove or revise that task before marking the document ready.

Example:

```markdown
Non-goal violation found:
- Non-goal says "do not add a statistics table".
- Task 2 proposes `asset_binding_usage_stats`.

Resolution:
- Remove this task from the current version.
- Move it to "Future / Not In This Version" only if helpful.
```

---

# Phase 8: Optional Task Persistence

Run this phase only when:

* the user explicitly requests a local task,
* a valid CDP package has `Handoff-Type: deferred-local-task`, or
* CDF explicitly requests persistence for a valid managed result.

CDF managed persistence is optional. The default managed behavior is to return the structured task result to CDF without writing a file. Keep task definition separate from persistence.

## Storage Path

Choose the target path in this order:

1. Use `Requested-Task-Path` when it contains an explicit path.
2. Otherwise use `<Workspace>/_cdtask/YYYY-MM-DD-<slug>.md`.

Path rules:

* Resolve relative paths against `Workspace`.
* Create only the parent directory needed for the task document.
* Do not modify any implementation file while saving the task.
* Do not overwrite an existing file silently. When the default filename exists, add a numeric suffix. When an explicit user path exists, ask before replacing it.
* Store paths in the document relative to `Workspace` where practical; keep `Workspace` itself absolute.

## Local Task File Contract

For a validated CDP package, save the reviewed task document with this frontmatter:

```yaml
---
task_contract: cdp-cdtask/v1
status: ready_for_resume
source: cdp
approval_state: scope-approved-execution-deferred
risk_level: Level L
workspace: /absolute/workspace/path
source_branch: branch-or-Unavailable
source_commit: commit-or-Unavailable
created_at: YYYY-MM-DDTHH:mm:ssZ
---
```

Use `Level XL` when appropriate. Do not invent branch or commit values.

For a manual input saved locally, use this distinct frontmatter:

```yaml
---
task_contract: cdtask/v1
status: ready_for_review
source: manual
approval_state: not-approved-by-cdp
risk_level: Unclassified
workspace: /absolute/workspace/path
source_branch: branch-or-Unavailable
source_commit: commit-or-Unavailable
created_at: YYYY-MM-DDTHH:mm:ssZ
---
```

A manual task is ready for review or handoff planning, not implementation. Before source-code changes, run CDP or an equivalent risk and approval workflow. Never copy CDP approval state into a manual task.

For a managed CDF input saved only on explicit request, use this distinct frontmatter:

```yaml
---
task_contract: cdf-cdtask/v1
status: tasking_ready
source: cdf
approval_state: plan-approved
execution_owner: cdf
risk_level: Level M
workspace: /absolute/workspace/path
source_branch: branch-or-Unavailable
source_commit: commit-or-Unavailable
created_at: YYYY-MM-DDTHH:mm:ssZ
---
```

Use the approved managed risk level. Do not use `ready_for_resume`, do not add a standalone CDP resume command, and do not transfer execution ownership away from CDF.

`Tasking Status: READY` and persisted artifact `status: tasking_ready` are task-definition concepts, not runtime execution states. CDTask produces the readiness verdict and may persist the artifact state; it does not enter an execution lifecycle state.

For `source: cdp` and `source: manual`, use this document order after the frontmatter:

```md
# Local Task: <Title>

## Resume Contract
- Resume command: `Continue local task: <task-path>`
- Path A — Same-stack resume: use `cdp`.
- Path B — External coding agent: the user explicitly instructs that agent to execute only the Task Breakdown under the Scope Guard and Codex Handoff Rules.
- The task document alone is not execution authorization.
- For `source: manual`, run CDP or an equivalent approval workflow before any implementation.
- Revalidate the target, evidence, risk, branch, and commit before editing.
- For `source: cdp` only, if no material drift exists, the explicit resume request authorizes implementation of the saved scope.
- If material drift or conflict exists, stop and request approval for the revised plan.
- When all implementation and verification for the task are complete, update the frontmatter to `status: completed` and add `completed_at: YYYY-MM-DDTHH:mm:ssZ`.

## Approval Record
...

## Requirement Understanding
...

## Requirement Decomposition
...

## Confirmed Evidence
...

## Open Assumptions
...

## Proposed Design
...

## Data Model / API / State Flow
...

## Approved Phase Boundary
...

## Scope Lock
- [Include the complete canonical `cdp-scope/v1` block verbatim, followed by its readable projection.]

## Dependency Order
...

## Task Breakdown
...

## Risks
...

## Acceptance Criteria
...

## Test Plan / Test Strategy
...

## Rollback Plan
...

## Handoff Execution Paths
...

## Scope Guard Checklist
...

## Codex Handoff Rules
...

## Task Readiness Gate
...
```

For `source: cdf`, use this managed document order instead. Do not include the standalone/manual `Dependency Order` section:

```md
# Managed Task: <Title>

## CDF Continuation Contract
- Execution owner: CDF
- Next owner: CDF
- This document is a task definition, not standalone implementation authorization.
- Return this document to CDF; do not resume it through standalone CDP.

## Approval Record
...

## Requirement Understanding
...

## Requirement Decomposition
...

## Confirmed Evidence
...

## Open Assumptions
...

## Proposed Design
...

## Data Model / API / State Flow
...

## Approved Phase Boundary
...

## Scope Lock
- [Include the complete canonical `cdp-scope/v1` block verbatim, followed by its readable projection.]

## Dependency Graph
...

## Dependency Data
...

## Task Breakdown
...

## Risks
...

## Acceptance Criteria
...

## Test Plan / Test Strategy
...

## Rollback Plan
...

## Scope Guard Checklist
...

## Execution Contract
...

## Task Readiness Gate
...
```

## Save Verification

After writing the file, read it back and verify:

1. CDP input uses `task_contract: cdp-cdtask/v1`, `source: cdp`, and `status: ready_for_resume`.
2. Manual input uses `task_contract: cdtask/v1`, `source: manual`, `approval_state: not-approved-by-cdp`, and `status: ready_for_review`.
3. Managed CDF input uses `task_contract: cdf-cdtask/v1`, `source: cdf`, `approval_state: plan-approved`, `execution_owner: cdf`, and `status: tasking_ready`.
4. The workspace and source traceability match the input.
5. Every required section exists.
6. Approved CDP/CDF input preserves the complete `cdp-scope/v1` block verbatim and passes Scope Lock Consistency Validation.
7. The Task Readiness Gate says the task is ready for its declared destination: resume for CDP input, review or handoff planning for manual input, or return to CDF for managed input.
8. A managed document contains no standalone resume command and names CDF as next owner.
9. A managed document contains `Dependency Graph` and `Dependency Data` and does not contain the standalone/manual `Dependency Order` section.
10. No implementation file changed as part of the save flow.

If verification fails, do not claim the task was saved successfully.

## Resume Behavior

When a later request explicitly says `Continue local task: <path>` or `继续执行本地 task：<path>`:

1. Read the entire task document.
2. Inspect `task_contract`, `source`, `approval_state`, and `status`.
3. For `source: cdp` with `status: ready_for_resume`, use CDP and re-check the target, current evidence, risk level, branch, and commit before editing.
4. If nothing material changed, treat the explicit resume request as authorization to implement only the saved CDP scope.
5. If scope, evidence, architecture, or risk changed materially, do not edit. Produce a revised CDP approval request.
6. For `source: manual` with `status: ready_for_review`, route through CDP's Requirement Gate, risk classification, evidence inspection, and required approval. The resume request is not implementation authorization.
7. For `source: cdf`, `execution_owner: cdf`, or `task_contract: cdf-cdtask/v1`, do not implement or route through standalone CDP resume behavior. Return the task to CDF for lifecycle continuation.

---

# Completion Definition

This skill is complete only when one of the following outcomes is reached.

## Outcome A: Ready

The final task breakdown contains:

* a complete canonical `cdp-scope/v1` Scope Lock for approved handoffs, preserved verbatim and validated against every task,
* non-goals,
* dependency order for standalone/manual input, or a Dependency Graph and Dependency Data for managed input,
* task breakdown,
* scope guard checklist,
* the applicable Codex Handoff Rules or managed Execution Contract,
* Task Readiness Gate result,
* no unresolved ambiguity,
* no unresolved conflict,
* no non-goal violation.

The assistant may say:

```text
This task breakdown is ready for task handoff. Document readiness does not authorize implementation.
```

This outcome means the task document passed the breakdown and handoff quality gates. It does not by itself authorize implementation.

When local saving was requested:

* CDP input is complete only after a verified `cdp-cdtask/v1` file has `status: ready_for_resume`.
* Manual input is complete only after a verified `cdtask/v1` file has `status: ready_for_review`.
* Managed CDF input is complete only after a verified `cdf-cdtask/v1` file has `status: tasking_ready`, `execution_owner: cdf`, and no standalone resume command.

For managed CDF input without persistence, completion means the structured result passed the Task Readiness Gate and was returned to CDF with:

```text
Tasking Status: READY
Contract-Version: cdf-cdtask/v1
Execution Owner: CDF
Task Count: N
Next Owner: CDF
```

plus Scope Lock, Dependency Graph, Dependency Data, managed Tasks, Execution Contract, and Task Readiness Result. CDTask stops there; it does not invoke an executor, perform implementation verification, or perform implementation review.

When persistence occurred, report the saved path, source, status, and applicable next action.

## Outcome B: Not Ready

The document still contains unresolved ambiguity, conflict, or missing decisions.

The assistant must not claim the document is complete.

For standalone/manual input, ask the user for confirmation. For managed input, return `NOT_READY` only when CDTask can repair the task definition within approved scope; otherwise return `BLOCKED` to CDF.

The assistant may say:

```text
This task breakdown is not ready to hand off yet. The following points need confirmation first.
```

## Outcome C: Blocked

Use for CDF managed input when the approved Plan itself is missing, conflicting, invalid, or requires new planning/approval authority.

Return:

```text
Tasking Status: BLOCKED
Contract-Version: cdf-cdtask/v1
Execution Owner: CDF
Next Owner: CDF
```

List the exact blocking conflicts and required CDF decision. Do not independently replan, invoke CDP, or begin execution.

---

# Output Modes

Choose one of the following output modes based on the user's request.

Modes A–D use `source: manual` unless their input is a validated CDP package routed to Mode F or a validated CDF package routed to Mode G. If a manual-mode result is saved locally, use `task_contract: cdtask/v1`, `approval_state: not-approved-by-cdp`, and `status: ready_for_review`.

---

## Mode A: Review Only

Use when the user asks whether the requirement can be split into tasks.

Output:

```markdown
# Requirement Task Readiness Review

## Verdict
Ready / Not Ready / Partially Ready

## Key Strengths
- ...

## Blocking Ambiguities
- ...

## Recommended Decisions Before Tasking
- ...

## Suggested Task Groups
- ...

## Next Step
- ...
```

Do not output a full task list unless the user asks.

---

## Mode B: Task Breakdown Only

Use when the user has a clear requirement and asks to split it into tasks.

Output:

```markdown
# Task Breakdown

## Scope Lock
...

## Dependency Order
...

## Tasks
...

# Scope Guard Checklist
...

# Codex Handoff Rules
...

# Task Readiness Gate
...
```

Do not rewrite the full requirement document.

---

## Mode C: Append-To-Document Version

Use when the user asks to append tasks to an existing requirement document.

Output only the sections that should be appended:

```markdown
---

# Task Breakdown

...

---

# Scope Guard Checklist

...

---

# Codex Handoff Rules

...

---

# Task Readiness Gate

...
```

Do not repeat the entire original document unless the user explicitly requests the full merged version.

---

## Mode D: Full Merged Requirement + Tasks

Use when the user explicitly asks for the full modified original document.

Output the complete requirement document with the task breakdown, scope guard checklist, Codex handoff rules, and Task Readiness Gate appended.

---

## Mode E: Not Ready, Clarification Needed

Use when the requirement is not ready for task breakdown.

Output:

```markdown
# Requirement Readiness Check

## Ready To Split?
No / Partially

## Clear Points
- ...

## Blocking Ambiguities
- ...

## Required User Confirmations
1. ...
2. ...

## Why This Cannot Be Finalized Yet
- ...

## Suggested Next Step
Please confirm the points above, then I can produce the scoped task breakdown.
```

Do not produce a final task breakdown in this mode.

---

## Mode F: CDP Local Task Save

Use when the input is a valid `CDP Task Handoff Package` and the user chose `Approve and save as local task` / `同意并保存为本地 task`.

Process:

1. Validate the `cdp-cdtask/v1` input contract.
2. Reuse the approved CDP scope without asking the user to restate it.
3. Produce the Scope Lock, dependency-aware Task Breakdown, Scope Guard Checklist, Codex Handoff Rules, and Task Readiness Gate.
4. Save the complete Local Task File Contract to the requested or default path.
5. Read the file back and run Save Verification.
6. Stop without implementing code.

Final response:

```md
Saved Task:
- Path: <workspace-relative or absolute task path>
- Contract-Version: cdp-cdtask/v1
- Source: cdp
- Status: ready_for_resume
- Code Changes: None
- Resume: Continue local task: <task path>
```

Do not claim success unless the file exists and Save Verification passes.

---

## Mode G: CDF Managed Tasking

Use when the input is a valid `CDF Tasking Handoff` with `Contract-Version: cdf-cdtask/v1`.

Process:

1. Validate the managed contract and prior plan approval without asking the user to repeat approved information.
2. Preserve the canonical Scope Lock verbatim and run Scope Lock Consistency Validation; derive task-definition details only when fully implied by the approved Plan and confirmed evidence.
3. Build the DAG Dependency Graph and managed task definitions with stable IDs, Dependencies, Write Scope, Shared Contracts, Acceptance Criteria, Must Not Change, Verification, Risk, and draft status.
4. Produce the Scope Guard Checklist and executor-neutral Execution Contract.
5. Run the Task Readiness Gate.
6. If `NOT_READY`, repair only task-definition defects fully implied by the approved Plan and confirmed evidence, then rerun the gate.
7. If `BLOCKED`, return the blocking Plan conflict or missing authority to CDF without replanning.
8. If `READY`, set every task to `Status: READY` and return the structured result to CDF.
9. Save a managed task document only when CDF or the user explicitly requests persistence, then run Save Verification.
10. Stop before execution. Do not invoke an executor.

If any missing information would introduce a new implementation decision or materially affect behavior, scope, architecture, contracts, acceptance, verification, risk, product behavior, or implementation direction, use `BLOCKED` at step 7. Do not supply a conservative default in managed mode.

Output:

```md
Tasking Status: READY
Contract-Version: cdf-cdtask/v1
Execution Owner: CDF
Task Count: <N>
Next Owner: CDF

## Scope Lock
...

## Dependency Graph
...

## Dependency Data
...

## Tasks
...

# Scope Guard Checklist
...

# Execution Contract
...

# Task Readiness Gate
...
```

For `NOT_READY` or `BLOCKED`, replace the status and report exact readiness defects or approved-Plan conflicts. Do not mark draft tasks `READY` and do not cross into `EXECUTING`.

`Tasking Status: READY` means the task definitions are ready to return to CDF for handoff. It is not execution authorization, and CDTask does not choose the execution strategy.

---

# Task Quality Standards

A good task is:

* small enough to review,
* tied to a clear requirement,
* dependency-aware,
* limited in scope,
* testable,
* reversible where possible,
* explicit about what not to change,
* explicit about verification,
* clear enough for a coding agent to execute without inventing decisions.

A bad task is:

* vague,
* too broad,
* mixes database, API, frontend, and tests into one step,
* includes future work,
* silently expands scope,
* lacks acceptance criteria,
* lacks verification instructions,
* ignores non-goals,
* changes unrelated modules,
* requires hidden assumptions.

---

# Common Anti-Patterns To Prevent

Reject or revise task lists that include these problems:

1. Implementing future enhancements as current tasks.
2. Adding new tables when the requirement says not to.
3. Updating frontend when the first version is backend-only.
4. Regenerating OpenAPI when the response contract is unchanged.
5. Refactoring unrelated files.
6. Adding service methods when the requirement says local helper only.
7. Changing sorting logic when the requirement only asks to document future sorting.
8. Treating global resource data as app-specific behavior.
9. Counting by the wrong identifier.
10. Using JavaScript read-modify-write for counters that require atomic database updates.
11. Turning optional notes into mandatory implementation tasks.
12. Ignoring failure-path requirements.
13. Removing existing behavior that the requirement says should remain unchanged.
14. Expanding one endpoint change into broader API redesign.
15. Introducing background jobs when the requirement asks for synchronous write.
16. Introducing new schema layers when the requirement says first version only.
17. Modifying frontend types when backend response is unchanged.
18. Updating generated files without explicit scope.
19. Making assumptions about business logic without marking them.
20. Marking a document ready before the Task Readiness Gate.

---

# Requirement Review Checklist

Use this checklist during the Requirement Readiness Check and Task Readiness Gate.

```markdown
## Requirement Review Checklist

### Goal
- [ ] The implementation goal is explicit.
- [ ] The current version boundary is explicit.

### Scope
- [ ] In-scope items are explicit.
- [ ] Out-of-scope items are explicit.
- [ ] Non-goals are explicit.
- [ ] Future work is separated from current work.

### Data / Model
- [ ] Data model changes are explicit.
- [ ] Migration requirements are explicit.
- [ ] Backfill requirements are explicit or explicitly not required.
- [ ] Identifier and counting dimensions are clear.

### Behavior
- [ ] Success path is clear.
- [ ] Failure path is clear.
- [ ] No-op path is clear.
- [ ] Existing behavior preservation is clear.

### Affected Areas
- [ ] Backend scope is clear.
- [ ] Frontend scope is clear.
- [ ] Shared schema scope is clear.
- [ ] OpenAPI/generated file scope is clear.
- [ ] Client scope is clear.
- [ ] Test scope is clear.

### Handoff
- [ ] Tasks declare their dependencies.
- [ ] Each task has acceptance criteria.
- [ ] Each task has verification.
- [ ] Each task has "Must Not Change".
- [ ] The applicable Codex Handoff Rules or managed Execution Contract is included.
- [ ] Task Readiness Gate passes.

### CDF Managed Metadata
- [ ] Every task has a stable Task ID.
- [ ] Every task has Dependencies, Write Scope, Shared Contracts, Risk, and draft/READY status.
- [ ] Dependency data is acyclic and supports DAG branches and joins.
- [ ] The Execution Contract is executor-neutral.
- [ ] CDTask does not own scheduling or lifecycle continuation.
- [ ] Independent implementation review is outside CDTask and the task-definition gate.
```

---

# Handoff Document Structure

For standalone/manual appendable handoff sections, prefer this final structure:

```markdown
---

# Task Breakdown

## Scope Lock
...

## Dependency Order
...

## Tasks
...

---

# Scope Guard Checklist
...

---

# Codex Handoff Rules
...

---

# Task Readiness Gate
...
```

For CDF managed appendable handoff sections, use the DAG structure and do not include `Dependency Order`:

```markdown
---

# Task Breakdown

## Scope Lock
...

## Dependency Graph
...

## Dependency Data
...

## Tasks
...

---

# Scope Guard Checklist
...

---

# Execution Contract
...

---

# Task Readiness Gate
...
```

If the user asks to append to an existing document, output only the appended sections unless the user explicitly requests the full merged document.

---

# Final Response Rules

When using this skill:

1. Do not implement code.
2. Do not invoke an executor.
3. Do not claim an executor ran anything.
4. Do not claim the handoff task breakdown is ready until the Task Readiness Gate passes.
5. Always review the final appended sections for task-definition quality.
6. If ambiguity exists in standalone/manual input, ask the user to confirm. For managed input, return `NOT_READY` for repairable task-definition ambiguity or `BLOCKED` for a Plan-level decision gap.
7. If conflict exists, stop and report it. For managed input, return the conflict to CDF and do not independently replan.
8. If a task violates a non-goal, revise the task list before finalizing.
9. If the task breakdown is ready, explicitly say it is ready for task handoff and that document readiness does not authorize implementation.
10. If a standalone/manual task breakdown is not ready, explicitly say it is not ready and list required confirmations. For managed input, return `NOT_READY` or `BLOCKED` with the exact task-definition defects or missing approved decisions to CDF.
11. Keep future work separate from current tasks.
12. Make scope boundaries visible.
13. Prefer strictness over enthusiasm.
14. Prefer a smaller, safer task list over a broad, impressive one.
15. For a valid `cdp-cdtask/v1` package, do not re-ask questions already resolved by CDP.
16. For a valid `cdf-cdtask/v1` package, preserve prior plan approval and return `READY`, `NOT_READY`, or `BLOCKED` to CDF without replanning.
17. In managed mode, do not add implementation-affecting assumptions or defaults. Derive only task-definition details fully implied by the approved Plan; otherwise return `BLOCKED` to CDF.
18. For either approved contract, copy `cdp-scope/v1` verbatim, preserve each non-goal as an explicit prohibition, and run Scope Lock Consistency Validation before reporting readiness.
19. Modify only the designated task document when local saving is requested; do not modify implementation files.
20. Do not claim a local task was saved until Save Verification passes.
21. Never label manual input as `source: cdp` or `source: cdf`, or copy either approval state into it.
22. Treat `Tasking Status: READY` and artifact `status: tasking_ready` as task-definition readiness, not runtime execution state.
23. Treat "ready for handoff", `ready_for_resume`, `ready_for_review`, and `tasking_ready` as distinct states.
24. Do not decide scheduling or final sequential/parallel/mixed execution strategy.
25. Do not assign independent final implementation review as a CDTask responsibility.
26. Stop managed flow before `EXECUTING` and return it to CDF.
27. End with the current status:

    * Ready for task handoff; implementation is not authorized by document readiness alone.
    * Not ready yet; user confirmation required.
    * Saved locally as `ready_for_resume`.
    * Saved locally as `ready_for_review`.
    * Tasking `READY`, `NOT_READY`, or `BLOCKED`; next owner CDF.
    * Saved managed task as `tasking_ready`; next owner CDF.
