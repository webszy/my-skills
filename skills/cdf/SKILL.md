---
name: cdf
description: Coordinate a controlled AI development flow from requirement intake through planning approval and task definition. Use when the user invokes cdf, /cdf, $cdf, cdf:, or controlled-development-flow, or when a development request needs explicit planning and human approval before task handoff. CDF does not implement, execute, or review code.
---

# CDF: Controlled Development Flow

## Overview

CDF is the top-level flow-control skill for AI-assisted software development.

AI can develop quickly, but the development process must remain controlled. CDF reduces uncontrolled behavior by moving work through explicit stages, preserving scope, and requiring a human decision before a plan becomes executable work.

CDF v0.1 coordinates CDP and CDTask. It is not a development runtime and does not perform implementation.

## Responsibility

CDF owns:

- flow coordination;
- component handoff;
- human decision points;
- preservation of the approved direction and scope.

CDF does not own:

- requirement analysis or technical planning, which belong to CDP;
- detailed task decomposition, which belongs to CDTask;
- implementation or code changes;
- code execution or verification;
- code review.

## Workflow

Follow this flow:

```text
Requirement
    ↓
CDF
    ↓
CDP
    ↓
Plan Review
    ↓
CDTask
    ↓
Execution (outside CDF v0.1)
```

1. Receive the development requirement.
2. Decide whether the request should enter the controlled flow. Use CDF when the work requires development planning, scope control, or an explicit plan decision. For simple informational questions or requests that do not require development planning, do not force CDF.
3. Send the requirement and available context to CDP.
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
- acceptance criteria.

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

## Human Gate

### Plan Approval

Before invoking CDTask, show the user a concise, decision-ready plan containing the proposed direction, scope, important risks, and acceptance criteria.

Wait for explicit approval. Approval confirms the direction and scope; it does not authorize CDF to implement or execute the tasks.

Do not treat silence, partial feedback, or approval of only one section as approval of the complete plan.

## Rules

- Do not directly implement or modify code.
- Do not execute code or development tasks.
- Do not review implementation.
- Do not skip CDP or the plan-approval gate.
- Do not enter CDTask while material requirements or plan decisions remain unclear.
- Do not expand the user's requested or approved scope.
- Do not replace CDP's planning responsibilities.
- Do not replace CDTask's task-definition responsibilities.
- Do not claim runtime, execution, verification, review, event, schema, or CLI capabilities.
- End the v0.1 flow after producing and handing off the executable task definition.

## Future Extensions

The following are possible future capabilities, not CDF v0.1 behavior:

- CDRunner for managed implementation and execution;
- CDReview for implementation review;
- CDF Runtime, including runtime control or state-machine execution;
- Protocol Schema for structured component contracts;
- execution and verification gates;
- event-driven coordination;
- CLI support.

Do not invoke, simulate, or depend on these extensions in the v0.1 flow.
