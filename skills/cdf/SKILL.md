---
name: cdf
description: Controlled Development Flow orchestrator for AI-assisted software development. Use when the user invokes cdf, /cdf, $cdf, cdf:, or controlled-development-flow, or when a development request should move through a controlled lifecycle of planning, approval, tasking, execution, verification, review, fixing, and completion.
---

# CDF: Controlled Development Flow

CDF is the orchestration layer for controlled AI-assisted software development.

CDF does not replace planning, task definition, execution, or review capabilities.

CDF controls how work moves between them.

Core principle:

> Let AI move fast, but never let development move uncontrolled.

Or more formally:

> Every meaningful state transition must be governed by an explicit rule, validated outcome, or approval gate.

---

# 1. Purpose

CDF turns a software-development request into a controlled lifecycle.

The standard lifecycle is:

```text
Requirement
    ↓
Planning
    ↓
Plan Approval
    ↓
Tasking
    ↓
Execution
    ↓
Verification
    ↓
Review
    ↓
Fix if required
    ↓
Completion
```

CDF owns:

- flow state;
- state transitions;
- component handoff;
- role assignment;
- execution strategy;
- approval gates;
- verification gates;
- review gates;
- escalation;
- final lifecycle status.

CDF does not duplicate the internal behavior of CDP, CDTask, CDRunner, or CDReview.

---

# 2. Core Model

CDF separates development into two conceptual layers.

## 2.1 Control Plane

The Control Plane decides:

- what state the work is currently in;
- what may happen next;
- which component owns the next action;
- which agent or human owns the decision;
- whether the current result is sufficient to continue;
- whether execution must stop;
- whether replanning is required;
- whether escalation to the user is required.

Possible controllers include:

- Human
- Planner
- Reviewer
- Executor
- Verification result
- Policy
- Risk rule
- Flow rule

Controlled does not mean that every transition requires human approval.

Controlled means that no important transition happens without a governing reason.

---

## 2.2 Execution Plane

The Execution Plane performs development work.

Typical components are:

```text
CDP
Planning

CDTask
Task Definition

CDRunner
Execution + Verification

CDReview
Independent Review
```

CDF orchestrates these components but should not copy their detailed internal rules.

---

# 3. Component Responsibilities

## 3.1 CDP — Controlled Development Planning

CDP owns planning.

Responsibilities may include:

- requirement understanding;
- requirement clarification;
- repository inspection;
- target existence checks;
- evidence gathering;
- risk classification;
- assumptions;
- unknowns;
- alternatives;
- implementation design;
- scope definition;
- acceptance criteria;
- verification strategy;
- task strategy;
- planning output.

When invoked by CDF, CDP runs in managed mode.

In managed mode, CDP must not independently take ownership of the complete development lifecycle.

Its output returns control to CDF.

---

## 3.2 CDTask — Controlled Development Task

CDTask owns executable task representation.

Responsibilities may include:

- task decomposition;
- task identifiers;
- task scope;
- dependencies;
- affected areas;
- constraints;
- acceptance criteria;
- verification requirements;
- task status;
- execution metadata.

CDTask converts an approved plan into executable work units.

---

## 3.3 CDRunner — Controlled Development Runner

CDRunner owns managed execution.

Responsibilities may include:

- launching the assigned executor;
- providing task context;
- maintaining the execution session;
- enforcing approved task scope;
- collecting execution output;
- running verification;
- collecting changed-file information;
- producing an execution report;
- detecting when the approved plan is no longer valid.

CDRunner must not silently redesign the approved plan.

When execution requires a material scope, architecture, risk, or contract change, return control to CDF.

---

## 3.4 CDReview — Controlled Development Review

CDReview owns independent implementation review.

Typical review inputs:

```text
Approved Plan
+ Task Definition
+ Git Diff
+ Execution Report
+ Verification Result
```

Typical outcomes:

```text
APPROVED
```

or:

```text
CHANGES_REQUESTED
```

or:

```text
BLOCKED
```

CDReview should evaluate whether the implementation satisfies the approved requirement and task scope.

Review is not a new implementation-planning phase unless the current plan has been invalidated.

---

# 4. Roles

CDF recognizes four logical roles.

```yaml
roles:
  planner:
  executor:
  reviewer:
  human:
```

Roles are logical responsibilities, not fixed models.

Examples:

```yaml
planner: codex
executor: grok
reviewer: codex
human: user
```

or:

```yaml
planner: codex
executor: claude
reviewer: grok
human: user
```

The user may specify roles using natural language.

Examples:

```text
这个交给 Grok 做。
Claude 执行。
让 Codex 自己实现。
Grok 做，Codex review。
```

If the user specifies only the executor, preserve the current environment as planner unless another role is explicitly assigned.

Default reviewer should be independent from the executor when a suitable reviewer is available.

Prefer:

```text
executor != reviewer
```

This is a preference, not an absolute invariant.

---

# 5. Flow States

CDF v0.1 defines the following lifecycle states:

```text
REQUIREMENT

PLANNING

PLAN_READY

PLAN_APPROVED

TASKING

READY_TO_EXECUTE

EXECUTING

VERIFYING

REVIEWING

FIXING

REPLANNING

BLOCKED

DONE

FAILED
```

---

# 6. Standard State Flow

The default flow is:

```text
REQUIREMENT
    ↓
PLANNING
    ↓
PLAN_READY
    ↓
Human Plan Gate
    ↓
PLAN_APPROVED
    ↓
TASKING
    ↓
READY_TO_EXECUTE
    ↓
EXECUTING
    ↓
VERIFYING
    ↓
REVIEWING
   ↙       ↘
FIXING     DONE
   ↓
EXECUTING
```

If a critical assumption, approved scope, architecture, or execution premise becomes invalid:

```text
EXECUTING
    ↓
REPLANNING
    ↓
PLANNING
```

If CDF cannot safely decide how to continue:

```text
Any State
    ↓
BLOCKED
    ↓
Human Escalation
```

---

# 7. Transition Rules

Every meaningful transition requires a valid transition condition.

Examples:

```text
REQUIREMENT
→ PLANNING

Condition:
The requested development goal is understood well enough to begin planning.
```

```text
PLANNING
→ PLAN_READY

Condition:
A concrete plan exists with enough evidence, scope, risks, assumptions,
acceptance criteria, and execution strategy for the task's risk level.
```

```text
PLAN_READY
→ PLAN_APPROVED

Condition:
The required approval gate has passed.
```

```text
PLAN_APPROVED
→ TASKING

Condition:
The approved plan is stable enough to convert into executable tasks, and CDF
has normalized it into a `cdf-cdtask/v1` handoff for CDTask.
```

```text
TASKING
→ READY_TO_EXECUTE

Condition:
CDTask returned `Tasking Status: READY`, its Task Readiness Gate passed,
executable task definitions exist, and CDF verified the required dependencies,
write scopes, shared contracts, acceptance criteria, verification expectations,
and absence of blocking task-definition issues.
```

```text
READY_TO_EXECUTE
→ EXECUTING

Condition:
The selected executor is available and execution is authorized by the
approved plan.
```

```text
EXECUTING
→ VERIFYING

Condition:
The executor reports implementation completion for the current execution unit.
```

```text
VERIFYING
→ REVIEWING

Condition:
Required verification has completed successfully or any unavailable checks
have been explicitly recorded with sufficient alternative evidence.
```

```text
REVIEWING
→ DONE

Condition:
Review outcome is APPROVED.
```

```text
REVIEWING
→ FIXING

Condition:
Review outcome is CHANGES_REQUESTED and the required fix remains inside
the approved scope.
```

```text
FIXING
→ VERIFYING

Condition:
The requested fixes have been applied.
```

No transition may be treated as successful merely because an agent claims
that the previous stage is complete.

Use the relevant gate or evidence.

---

# 8. Human Gates

CDF v0.1 defines two primary human gates.

## 8.1 Plan Approval Gate

Before managed execution begins, the user must be given the implementation plan.

The approval output should contain enough information for a meaningful decision.

At minimum, show:

```text
Goal

Requirement Understanding

Proposed Approach

Scope

Important Assumptions

Important Unknowns

Risks

Tasks / Phases

Execution Strategy

Executor

Reviewer

Verification Strategy
```

The amount of detail should match the risk.

Do not force large approval documents for trivial changes.

The human gate approves the development direction and scope.

It does not imply that the plan can never change.

If later evidence materially invalidates the plan, enter REPLANNING.

---

## 8.2 Escalation Gate

CDF should avoid unnecessary human interruption after plan approval.

Do not escalate merely because an executor encountered an ordinary implementation issue.

Escalate when human judgment is materially useful or required.

Examples include:

- a key approved assumption is false;
- implementation requires material scope expansion;
- architecture must change;
- a new high-risk area appears;
- a destructive operation becomes necessary;
- two valid approaches have materially different product implications;
- executor and reviewer cannot resolve an issue safely;
- repeated fix loops fail;
- external information or credentials required for continuation are unavailable;
- CDF cannot determine a safe transition.

When escalation is required:

```text
State: BLOCKED

Reason:
...

Evidence:
...

Decision required:
...

Options:
A. ...
B. ...

Recommended:
...

Why:
...
```

Keep the decision surface narrow.

Do not ask the user to redo analysis that CDF can perform itself.

---

# 9. Planning Integrity

A polished plan is not automatically a correct plan.

Before plan approval, CDF should prefer plans that expose:

```text
Confirmed Facts
Assumptions
Unknowns
Alternatives
Risks
Acceptance Criteria
Verification Strategy
```

High-impact uncertainty should not be hidden.

If a critical unknown prevents responsible planning, CDF may introduce a research or spike step before final approval.

Example:

```text
Requirement
    ↓
Initial Planning
    ↓
Critical Unknown
    ↓
Research / Spike
    ↓
Evidence
    ↓
Replan
    ↓
PLAN_READY
```

The purpose of a spike is to reduce decision uncertainty, not to silently implement the full feature.

---

# 10. Plan Critique

CDF should support independent challenge of a proposed plan.

A plan critique may check for:

- incorrect assumptions;
- misunderstood requirements;
- unnecessary complexity;
- simpler approaches;
- missing edge cases;
- hidden architectural changes;
- scope creep;
- unverified dependencies;
- weak acceptance criteria;
- weak verification;
- unnecessary new abstractions;
- risky irreversible decisions.

A critic does not automatically own the final plan.

The planner may revise the plan using valid critique.

The final plan shown to the user should reflect important resolved findings.

Plan critique depth should match risk.

Do not turn trivial tasks into multi-agent planning exercises without value.

---

# 11. Risk-Aware Control

CDF should use risk to determine control depth.

Risk does not exist merely to label tasks.

Risk changes how much control is required.

Conceptually:

```text
Low Risk
→ lightweight control

Medium Risk
→ evidence-backed planning

High Risk
→ explicit assumptions + risks + approval

Architecture / systemic risk
→ design + critique + phases + stronger gates
```

Exact risk classification may be delegated to CDP.

CDF consumes the classification to determine flow behavior.

---

# 12. Execution Strategy

CDF supports:

```text
SEQUENTIAL

PARALLEL

MIXED
```

Default:

```text
SEQUENTIAL
```

CDF should prefer correctness and isolation over theoretical maximum throughput.

---

## 12.1 Sequential Execution

Use sequential execution when:

- tasks depend on previous tasks;
- write scopes overlap;
- tasks modify shared contracts;
- tasks affect the same data model;
- execution order matters;
- the conflict risk is uncertain.

Example:

```text
TASK-001
    ↓
TASK-002
    ↓
TASK-003
```

---

## 12.2 Parallel Execution

Parallel execution is allowed only when CDF has sufficient evidence that tasks are safely independent.

At minimum:

```text
No dependency
AND
No overlapping write scope
AND
No shared contract ordering risk
```

Shared contracts may include:

- API definitions;
- schemas;
- types;
- state models;
- database structures;
- shared configuration;
- shared interfaces;
- common generated artifacts.

If independence is uncertain, use sequential execution.

Do not parallelize merely because multiple executors are available.

---

## 12.3 Mixed Execution

Mixed execution may combine dependency stages.

Example:

```text
TASK-001
    ↓
    ├───────────────┐
    ↓               ↓
TASK-002         TASK-003
    └───────┬───────┘
            ↓
         TASK-004
```

The parallel branch may begin only after its required predecessor has completed.

The successor may begin only after all required predecessor tasks have satisfied their gates.

---

# 13. Execution Scope Guard

Execution is bounded by the approved plan and current task.

Executors must not silently:

- add unrelated features;
- redesign unrelated modules;
- refactor surrounding code without necessity;
- change public contracts outside approved scope;
- introduce speculative architecture;
- expand data models without approval;
- change high-risk behavior merely because it appears convenient.

Small implementation details necessary to complete an approved task do not require replanning.

Material changes do.

When uncertain, evaluate whether the change alters:

```text
Scope
Architecture
Contract
Risk
Acceptance Criteria
Product Behavior
```

If yes, consider REPLANNING or escalation.

---

# 14. Verification Gate

Execution completion is not equivalent to task completion.

Before review, required verification must be performed.

Verification may include:

- tests;
- type checks;
- builds;
- linting;
- targeted behavior checks;
- schema validation;
- API contract checks;
- fixture checks;
- integration checks;
- manual verification instructions when automation is unavailable.

Never report a check as passed unless it was actually performed.

If the ideal verification cannot be performed:

1. record why;
2. perform the strongest available alternative;
3. preserve the limitation for review.

A verification failure inside the approved scope may return the task to FIXING.

A verification failure that exposes a planning problem should trigger REPLANNING.

---

# 15. Review Gate

Review should be independent from execution when practical.

CDReview determines whether the implementation satisfies:

```text
Approved Requirement
Approved Scope
Task Acceptance Criteria
Verification Requirements
Regression Expectations
```

Valid outcomes:

```text
APPROVED

CHANGES_REQUESTED

BLOCKED
```

If APPROVED:

```text
REVIEWING
→ DONE
```

If CHANGES_REQUESTED:

```text
REVIEWING
→ FIXING
```

If BLOCKED:

```text
REVIEWING
→ BLOCKED
```

---

# 16. Fix Loop

Normal review findings should not require user intervention.

Default loop:

```text
CDReview
    ↓
CHANGES_REQUESTED
    ↓
CDRunner / Executor
    ↓
Fix
    ↓
Verification
    ↓
CDReview
```

Continue until:

```text
APPROVED
```

or:

```text
BLOCKED
```

CDF should define a reasonable protection against uncontrolled fix loops.

If repeated review cycles indicate that the original plan or architecture is incorrect, stop patching symptoms and enter REPLANNING.

---

# 17. Replanning

Replanning is required when execution evidence materially invalidates the approved plan.

Typical triggers:

- a confirmed assumption becomes false;
- required architecture differs materially from the approved design;
- a new service or module becomes necessary;
- task scope expands substantially;
- a new high-risk area appears;
- the approved contract cannot satisfy the requirement;
- implementation evidence proves that the proposed approach is unsuitable.

Flow:

```text
Current State
    ↓
REPLANNING
    ↓
CDP
    ↓
Revised Plan
    ↓
PLAN_READY
```

A revised plan that materially changes approved direction must pass the relevant approval gate again.

Do not use replanning for trivial implementation details.

---

# 18. Managed CDP Context

When CDF invokes CDP, treat the planning session as CDF-managed.

Conceptually:

```yaml
execution_context: cdf-managed
execution_owner: cdf
```

CDF-managed planning means:

- CDP owns planning;
- CDF owns lifecycle continuation;
- CDP returns planning results to CDF;
- approved plans continue through CDTask / CDRunner / CDReview;
- CDP must not silently switch into standalone lifecycle ownership.

Standalone `/cdp` behavior is not changed by this rule.

---

# 19. Task Handoff

After plan approval, CDF is the adapter and orchestrator between the approved CDP planning result and CDTask.

The required dependency direction is:

```text
CDF → CDP
CDP → CDF

CDF → CDTask
CDTask → CDF
```

The managed planning-to-tasking flow is:

```text
PLAN_APPROVED
→ CDF constructs cdf-cdtask/v1
→ TASKING
→ CDTask
→ Task Readiness Gate
→ CDTask returns READY | NOT_READY | BLOCKED
→ CDF evaluates the next transition
```

CDP does not construct or invoke `cdf-cdtask/v1`. After human approval, CDP returns the approved planning result to CDF. CDF preserves that result, constructs the versioned handoff, enters `TASKING`, invokes CDTask, and consumes the tasking result.

## 19.1 CDF Tasking Adapter

CDF must normalize the approved planning result into this contract without silently changing approved meaning:

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
...
```

CDF owns adapter fidelity, not task compilation. It must preserve the approved planning content, risk level, human approval, assumptions and unknowns, scope, acceptance criteria, verification strategy, and available workspace metadata. It must not reconstruct the requirement from memory, invent missing implementation decisions, or copy CDTask's detailed validation rules into CDF.

CDTask remains the source of truth for `cdf-cdtask/v1` validation, Scope Lock, dependency analysis, Task Compilation, and the Task Readiness Gate.

## 19.2 CDTask Outcomes

CDF must recognize these managed outcomes while in `TASKING`:

### READY

Expected result:

```text
Tasking Status: READY
Contract-Version: cdf-cdtask/v1
Execution Owner: CDF
Task Count: N
Next Owner: CDF
```

Before entering `READY_TO_EXECUTE`, CDF must verify that:

- the Task Readiness Gate passed;
- executable task definitions exist;
- Dependencies are declared;
- Write Scope is declared or acceptably bounded;
- Shared Contracts are declared;
- Acceptance Criteria are defined;
- Verification requirements are defined;
- no blocking task-definition issue remains.

Only after these guards pass may CDF perform:

```text
TASKING → READY_TO_EXECUTE
```

### NOT_READY

`NOT_READY` means CDTask can repair a task-definition defect wholly inside the approved scope. CDF remains in `TASKING` while CDTask repairs the definition and reruns the Task Readiness Gate.

```text
Tasking Status: NOT_READY
```

Do not require renewed human plan approval, enter `REPLANNING`, or begin execution for a repair that introduces no new implementation decision. If repair would change approved meaning, treat the result as `BLOCKED` instead.

### BLOCKED

`BLOCKED` means the approved Plan is missing or conflicts on an implementation-affecting decision, or tasking exposed a scope, architecture, contract, acceptance, verification, or risk issue that cannot be repaired inside approved meaning.

```text
Tasking Status: BLOCKED
```

CDTask must not call CDP or independently replan. CDF owns the next transition, normally:

```text
TASKING → REPLANNING → CDP
```

When human judgment is required, CDF may instead use:

```text
TASKING → BLOCKED → Human Escalation
```

## 19.3 Readiness State Separation

These are distinct concepts:

```text
Tasking Status: READY
= CDTask readiness verdict

artifact status: tasking_ready
= optional persisted CDTask artifact state

READY_TO_EXECUTE
= CDF lifecycle state
```

CDF must not enter `READY_TO_EXECUTE` solely because an artifact says `status: tasking_ready`. The `TASKING → READY_TO_EXECUTE` transition remains owned by CDF and requires all transition guards above.

The handoff is part of the control boundary. Information must not silently disappear between planning and tasking.

---

# 20. Flow State Integrity

CDF must always know the current lifecycle state.

Do not pretend a stage was completed if its required output is unavailable.

Examples:

```text
No approved plan
→ cannot be PLAN_APPROVED

No valid task definition
→ cannot be READY_TO_EXECUTE

Execution not completed
→ cannot be VERIFYING

Required verification failed
→ cannot be REVIEWING as successful verification

No review result
→ cannot be DONE
```

State should describe reality, not desired progress.

---

# 21. Failure vs Blocked

Use `FAILED` for an execution or system failure that ended the current attempt.

Use `BLOCKED` when continuation requires a decision, missing dependency, or intervention.

Examples:

```text
Executor process crashes irrecoverably
→ FAILED
```

```text
Database migration requires user decision
→ BLOCKED
```

```text
Required credential is unavailable
→ BLOCKED
```

```text
Reviewer discovers architecture must change
→ REPLANNING or BLOCKED
```

Prefer recovery or replanning when possible.

Do not mark a recoverable issue as permanent failure.

---

# 22. Final Result

CDF owns the final lifecycle report.

When the flow reaches DONE, report a concise summary.

Suggested structure:

```md
# CDF Completed

Status: DONE

## Requirement
- ...

## Plan
- ...

## Execution
- Executor:
- Tasks completed:
- Execution strategy:

## Changed
- ...

## Verification
- ...

## Review
- Reviewer:
- Review rounds:
- Final outcome: APPROVED

## Fixes
- [If applicable.]

## Remaining Risks / Manual Checks
- ...

## Traceability
- ...
```

Do not flood the final response with internal orchestration logs.

Surface information useful for understanding what changed and whether the result is trustworthy.

---

# 23. Invariants

The following are CDF invariants.

1. Never allow managed implementation to begin before the required planning gate has passed.

2. Never silently expand approved scope.

3. Never hide material assumptions or newly discovered uncertainty.

4. Never treat agent confidence as verification.

5. Never report verification that was not actually performed.

6. Never mark review as approved without a valid review outcome.

7. Never continue blindly when a critical planning assumption has been invalidated.

8. Never parallelize tasks whose independence has not been established.

9. Never require human intervention for ordinary issues that can be safely resolved inside the approved flow.

10. Never allow automation to remove meaningful control.

11. Prefer the smallest safe transition that moves the work forward.

12. State must reflect the actual lifecycle condition.

---

# 24. CDF v0.1 Scope

CDF v0.1 defines the orchestration model.

It does not require all runtime capabilities to exist yet.

Initial implementation may support only:

```text
CDP
→ Human Plan Approval
→ CDTask
→ Sequential Execution
→ Verification
→ Review
→ Fix
→ Done
```

Features such as:

```text
parallel workers
worktrees
advanced scheduling
persistent runtime recovery
automatic DAG optimization
multi-executor load balancing
cross-machine execution
```

are future execution capabilities.

Do not complicate the initial CDF implementation merely to support hypothetical future scale.

The first goal is:

> A user describes a requirement, confirms a trustworthy plan once, and CDF controls the remaining development flow until completion or meaningful escalation.
