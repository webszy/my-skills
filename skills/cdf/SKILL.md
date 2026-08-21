---
name: cdf
description: Assess and coordinate a controlled AI development flow through CDP planning, human approval, and CDTask handoff. Use when the user invokes cdf, /cdf, $cdf, cdf:, or controlled-development-flow, or when a development request needs explicit planning and scope control. CDF v0.1 ends at task-definition handoff and does not implement, execute, verify, or review code.
---

# CDF: Controlled Development Flow

## Overview

CDF is the top-level flow-coordination skill for AI-assisted software development.

AI can develop quickly, but the development process must remain controlled. CDF reduces uncontrolled behavior by moving work through explicit stages, preserving scope, and requiring a human decision before a plan becomes executable work.

CDF v0.1 coordinates CDP and CDTask. It is not a runtime or an executor. It ends after producing and handing off the CDTask definition and does not perform implementation, execution, verification, or review.

## Responsibility

CDF owns:

- flow coordination;
- component handoff;
- human decision points;
- approved scope preservation.

CDF does not own:

- requirement analysis or technical planning, which belong to CDP;
- detailed task decomposition, which belongs to CDTask;
- implementation;
- execution;
- verification;
- review.

## Workflow

Follow this flow:

```text
Requirement
    ↓
CDF Assessment
    ↓
CDP Planning
    ↓
Human Plan Approval
    ↓
CDTask
    ↓
Execution (outside CDF v0.1)
```

1. Receive and assess the development requirement.
2. Decide whether the request should enter the controlled flow. Use CDF when the work requires development planning, scope control, or an explicit plan decision. For simple informational questions or requests that do not require development planning, stop the CDF flow and handle or route the request normally.
3. If the request enters the flow, send the requirement and available context to CDP.
4. Present CDP's plan to the user and wait for explicit approval.
5. If the user requests changes, return the feedback to CDP and present the revised plan for approval.
6. After approval, send the approved plan to CDTask.
7. Return the executable task definition for handoff to a human or another execution agent. State clearly that execution is outside CDF v0.1.

## CDP Integration

Use CDP for analysis and planning. Provide the original requirement, relevant context, user constraints, and known scope boundaries.

CDF expects CDP to return:

- requirement understanding;
- technical analysis;
- implementation plan;
- risks and material assumptions;
- acceptance criteria;
- an approved `Scope-Lock-Version: cdp-scope/v1` block;
- an Approval Record identifying full, conditional, or partial approval and any unapproved items;
- the applicable Locked Scope Summary or Partial Approval Result shown to the user.

Do not rewrite CDP's technical design as if CDF produced it. If the output is incomplete or the requirement remains materially ambiguous, keep the work in planning and ask CDP to resolve the gap before tasking.

## CDTask Integration

Invoke CDTask only after the user approves the plan.

Input:

```text
Approved Plan
```

Output:

```text
Executable Task Definition
```

Preserve the approved plan's scope, constraints, risks, and acceptance criteria in the handoff. Let CDTask determine the task structure and decomposition details. If task creation exposes a missing implementation decision or a conflict with the approved plan, return to CDP or the user as appropriate; do not invent the decision.

For the existing internal `cdf-cdtask/v1` handoff, copy the complete approved `cdp-scope/v1` block verbatim. Do not paraphrase, reorder, merge, omit, weaken, or expand `in_scope`, `out_of_scope`, `non_goals`, `assumptions`, `stop_conditions`, `will_change`, `will_not_change`, or `acceptance_criteria`.

Do not invoke CDTask when the Scope Lock is missing, internally conflicting, or inconsistent with the approved plan. Any scope extension must return to CDP for replanning and renewed human approval.

For partial approval, preserve CDP's Partial Approval Result and pass only its canonical approved-subset Scope Lock to CDTask. `Approved Items` must match `in_scope` verbatim, every `Unapproved Items` entry must remain explicitly excluded, and no task may be prepared for the unapproved remainder.

These versioned values are internal Skill handoff formats for CDF v0.1, not a public runtime protocol.

## Human Gate

### Plan Approval

Before invoking CDTask, show the user a concise, decision-ready plan containing the proposed direction, scope, important risks, and acceptance criteria.

Wait for explicit approval. Approval confirms the direction and scope; it does not authorize CDF to implement or execute the tasks.

Do not treat silence or acknowledgements such as `ok`, `继续`, `可以`, or `嗯` as approval. Conditional or partial approval applies only to the normalized approved Scope Lock returned by CDP; unapproved items remain excluded.

## Rules

- Do not directly implement or modify code.
- Do not execute code or development tasks.
- Do not review implementation.
- Do not skip CDP or the plan-approval gate.
- Do not enter CDTask while material requirements or plan decisions remain unclear.
- Do not expand the user's requested or approved scope.
- Do not replace CDP's planning responsibilities.
- Do not replace CDTask's task-definition responsibilities.
- Do not claim runtime, execution, verification, review, event-system, public schema-protocol, or CLI capabilities.
- End the v0.1 flow after producing and handing off the executable task definition.

## Future Extensions

These extensions are not CDF v0.1 capabilities. Do not invoke, simulate, or depend on them in the v0.1 flow.

### Near Future

- CDRunner for managed implementation and execution;
- CDReview for implementation review;

### Long Term

- CDF Runtime;
- public or runtime Protocol Schema;
- event-driven coordination;
- CLI support.
