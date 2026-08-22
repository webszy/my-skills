---
name: cdf
description: Assess and coordinate a controlled AI development flow through CDP planning, human approval, and CDTask handoff. Use when the user invokes cdf, /cdf, $cdf, cdf:, or controlled-development-flow, or when a development request needs explicit planning and scope control. CDF v0.1 ends at task-definition handoff and does not implement, execute, verify, or review code.
---

# CDF: Controlled Development Flow

## Quick Understanding

> CDF is the control plane for the CDF Suite: it decides whether a development request enters the controlled flow, coordinates component handoffs, and enforces the human plan-approval gate.

**Small changes should be fast. Risky changes should be controlled.**

AI can develop quickly, but the development process must remain controlled. CDF reduces uncontrolled behavior through explicit stages, preserved scope, and human decisions.

CDF v0.1 ends after it hands off a CDTask definition. It is not a runtime, scheduler, executor, verification system, or review system.

## Position in the CDF Suite

```text
Requirement
    ↓
CDF Assessment
    ↓
CDP Planning
    ↓
Human Plan Approval
    ↓
CDTask Definition
    ↓
Execution (outside CDF v0.1)
```

| Skill | Role | Output |
|---|---|---|
| `cdf` | Control plane, flow coordination, human gates | Approved flow handoff |
| `cdp` | Evidence-based, risk-aware planning and Scope Lock | Approved Plan Package |
| `cdtask` | Approved-plan compilation into verifiable tasks | Handoff-ready Task Definition |

CDF coordinates the flow. It does not replace CDP planning or CDTask decomposition.

## Responsibilities and Boundaries

CDF owns:

- flow assessment and coordination;
- component handoff;
- human decision points;
- preservation of approved scope.

CDF does not own:

- requirement analysis or technical planning (`cdp`);
- detailed task decomposition (`cdtask`);
- implementation or code modification;
- execution or scheduling;
- implementation verification or review;
- runtime or lifecycle-state management.

## Workflow

1. Receive the development requirement and available context.
2. Decide whether controlled planning is needed.
3. If yes, send the requirement, constraints, and known scope to CDP.
4. Present CDP's decision-ready plan and wait for valid human approval.
5. If the user requests changes, return the feedback to CDP and repeat planning and approval.
6. After approval, pass the Approved Plan Package to CDTask.
7. Return the handoff-ready Task Definition to a human or another authorized agent.
8. Stop. State that execution is outside CDF v0.1.

Do not enter the controlled flow for a purely informational request or a request that needs no development planning. Route or answer it normally.

## Operating Context

CDF invokes CDP in `cdf-managed` context. This means:

- CDP may inspect evidence and prepare planning artifacts;
- CDP returns control to CDF after approval;
- CDP must not call CDTask or implement code in this context;
- CDF decides whether the approved plan proceeds to CDTask.

CDF invokes CDTask only with an approved managed handoff. CDTask returns task-definition readiness to CDF and does not continue into execution.

## Key Gates and Contracts

### Human Plan Approval

Before CDTask handoff, show a concise plan containing:

- proposed direction;
- canonical Scope Lock;
- material risks and assumptions;
- acceptance criteria;
- the action being approved.

Approval must identify both the action and the approved plan, Scope Lock, phase, task, or subset. Silence and acknowledgements such as `ok`, `继续`, `可以`, or `嗯` are not approval.

Approval confirms direction and scope. It does not authorize CDF to implement or execute anything.

### Scope Lock Preservation

The approved plan must contain `Scope-Lock-Version: cdp-scope/v1` with:

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

Copy the complete block verbatim from CDP to CDTask. Do not paraphrase, reorder, merge, omit, weaken, or expand any item.

For partial approval:

- preserve CDP's Partial Approval Result;
- pass only the canonical approved-subset Scope Lock;
- require `Approved Items` to match `in_scope` verbatim;
- keep every `Unapproved Items` entry explicitly excluded;
- prepare no task for the unapproved remainder.

If Scope Lock is missing, conflicting, inconsistent, or too narrow for the requested tasking, do not invoke CDTask. Return to CDP for replanning and renewed approval.

### Internal Handoff Formats

- CDP → CDF: Approved Plan Package with the canonical Scope Lock and Approval Record.
- CDF → CDTask: `Contract-Version: cdf-cdtask/v1`, `Handoff-Type: managed-tasking`, `Approval-State: plan-approved`, `Execution-Owner: cdf`, supported `Risk-Level`, and available workspace/branch/commit metadata.

These are internal CDF v0.1 Skill handoff formats, not public runtime protocols.

## Outputs and Handoffs

CDF sends CDP:

- original requirement and relevant context;
- user constraints and known scope boundaries;
- `cdf-managed` lifecycle ownership.

CDF expects CDP to return:

- requirement understanding and technical analysis;
- evidence-backed implementation plan;
- risk level, material risks, and assumptions;
- acceptance criteria and verification strategy;
- canonical approved Scope Lock;
- Approval Record and the applicable Locked Scope Summary or Partial Approval Result.

CDF sends CDTask only the approved package. CDTask determines task structure and dependencies without changing implementation meaning.

The CDF v0.1 terminal output is a handoff-ready Task Definition plus an explicit statement that execution remains outside CDF.

## Usage

Use CDF when a development request needs controlled planning, explicit scope, or a human plan decision. A typical invocation is:

```text
Use CDF to assess this requirement, obtain an approved CDP plan, and prepare a CDTask handoff.
```

Keep coordination concise. Let CDP provide technical depth and CDTask provide task-definition detail.

## Non-Negotiable Rules

- Do not implement or modify code.
- Do not execute development tasks.
- Do not review implementation.
- Do not skip CDP or the human plan-approval gate.
- Do not invoke CDTask while material decisions remain unresolved.
- Do not expand approved scope.
- Do not invent missing planning decisions.
- Do not replace CDP or CDTask responsibilities.
- Do not claim runtime, event-system, public schema-protocol, CLI, executor, verification, or review capability.
- End after task-definition handoff.

## Future Extensions

These are not CDF v0.1 capabilities. Do not invoke, simulate, or depend on them.

### Near Future

- CDRunner
- CDReview

### Long Term

- CDF Runtime
- public or runtime Protocol Schema
- event-driven coordination
- CLI support
