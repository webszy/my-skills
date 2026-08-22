---
name: cdf
description: Assess and coordinate a controlled AI development flow through CDP planning, human approval, and CDTask handoff. Use when the user invokes cdf, /cdf, $cdf, cdf:, or controlled-development-flow, or when a development request needs explicit planning and scope control. CDF v0.1 ends at task-definition handoff, or at approved plan handoff when CDTask is not selected, and does not implement, execute, verify, or review code.
---

# CDF: Controlled Development Flow

## Quick Understanding

> CDF is the control plane for the CDF Suite: it decides whether a development request enters the controlled flow, routes each component return, and refuses any handoff that lacks completed approval evidence.

**Small changes should be fast. Risky changes should be controlled.**

AI can develop quickly, but the development process must remain controlled. CDF reduces uncontrolled behavior through explicit stages, preserved scope, and human decisions.

CDF v0.1 ends after it hands off a CDTask definition or an approved plan package. It is not a runtime, scheduler, executor, verification system, or review system.

## Position in the CDF Suite

```text
Requirement
    ↓
CDF Assessment
    ↓
CDP Planning + Human Plan Approval
    ↓
CDF Handoff Preconditions
    ↓
CDTask Definition, when selected
    ↓
Execution (outside CDF v0.1)
```

| Skill | Role | Output |
|---|---|---|
| `cdf` | Control plane, return routing, handoff preconditions | Approved flow handoff |
| `cdp` | Evidence-based, risk-aware planning, Scope Lock, and the human approval gate | Approved Plan Package |
| `cdtask` | Approved-plan compilation into verifiable tasks | Handoff-ready Task Definition |

CDF coordinates the flow. It does not replace CDP planning, the CDP approval gate, or CDTask decomposition.

## Responsibilities and Boundaries

CDF owns:

- flow assessment and coordination;
- component handoff and return routing;
- handoff preconditions and approval-evidence enforcement;
- preservation of approved scope.

CDF does not own:

- requirement analysis or technical planning (`cdp`);
- the human approval gate itself, including plan display, approval-wording judgement, and re-asking (`cdp`);
- detailed task decomposition (`cdtask`);
- implementation or code modification;
- execution or scheduling;
- implementation verification or review;
- runtime or lifecycle-state management.

CDF routes on contract fields. It never reads plan prose, task prose, or a reason string to decide what happens next.

## Workflow

1. Receive the development requirement and available context.
2. Decide whether controlled planning is needed.
3. Send the requirement, constraints, known scope, `Context: cdf-managed`, and `Lifecycle-Owner: cdf` to CDP.
4. Route the CDP return on `Planning Status`. Only `APPROVED` continues.
5. Verify every Handoff Precondition. A failed precondition returns the package to CDP.
6. Apply CDTask Selection. If CDTask is selected, confirm it is available and send the approved package; otherwise go to step 8.
7. Route the CDTask return on `Tasking Status`.
8. Return the handoff-ready Task Definition, or the approved plan package, to a human or another authorized agent.
9. If `Remaining-Phases` is greater than zero, return to step 3 for the next phase. Otherwise stop and state that execution is outside CDF v0.1.

Do not enter the controlled flow for a purely informational request or a request that needs no development planning. Route or answer it normally.

### CDP Return Routing

| `Planning Status` | CDF action |
|---|---|
| `APPROVED` | Continue to the Handoff Preconditions |
| `NOT_APPROVED` | Report `Reason`, produce no handoff, and end the round as terminated rather than completed |
| `BLOCKED` | Report `Reason` verbatim and end the round. Do not send it back to CDP; CDP issued it |
| missing, unreadable, or unrecognized | Treat as blocked, name the missing field, and end the round |

If `Risk Level` differs from the previous round for the same requirement, CDP has reclassified. Discard the previously displayed plan and any approval obtained for it, and treat the return as a fresh round.

### CDTask Return Routing

| `Tasking Status` | `Blocked-Reason-Class` | CDF action |
|---|---|---|
| `READY` | — | Continue to step 8 |
| `NOT_READY` | — | Return to CDTask for repair inside approved scope, then re-evaluate |
| `BLOCKED` | `approval` or `scope-lock` | A precondition CDF must enforce has failed. Re-run the Handoff Preconditions, and return the package to CDP if the defect is in the package |
| `BLOCKED` | `requires-new-scope` or `partial-remainder` | Return to CDP for replanning and renewed approval, then restart at step 4 |
| `BLOCKED` | `ambiguity` | Return the package to CDP for correction and report the blocker to the user |
| `BLOCKED` | missing or unrecognized | Report to the user and end the round |

## Operating Context

CDF invokes CDP in `cdf-managed` context. This means:

- CDP may inspect evidence and prepare planning artifacts;
- CDP runs the human approval gate and returns its outcome to CDF;
- CDP must not call CDTask or implement code in this context;
- CDF decides whether the approved plan proceeds to CDTask.

CDF invokes CDTask only with an approved managed handoff. CDTask returns task-definition readiness to CDF and does not continue into execution.

## Key Gates and Contracts

### Handoff Preconditions

CDP owns the approval gate. CDF enforces it at the handoff boundary through field checks only, never through a judgement about wording or intent. Before step 6, confirm:

- `Contract-Version: cdp-cdf/v1` is present and recognized;
- `Planning Status` is `APPROVED`;
- an Approval Record exists with `Scope Approved: Yes`;
- the Approval Record states `Code Changes Authorized In This Turn: No`;
- a canonical `cdp-scope/v1` block exists with all eight arrays populated;
- `Risk Level` is Level S, Level M, Level L, or Level XL;
- a Partial Approval Result is present when `Approval Type` is `partial`;
- `Phase` and `Remaining-Phases` are present or `Not applicable`;
- workspace, branch, and commit metadata are present or explicitly `Unavailable`.

Any failed condition returns the package to CDP. Do not repair it, do not supply a missing field, and do not proceed on a package that is merely close enough.

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

Treat the canonical block as an opaque payload. Copy it byte for byte from CDP to CDTask: do not paraphrase, reorder, merge, omit, weaken, expand, re-indent, normalize quoting, or re-wrap a line. After copying, read the copy back and compare it with the source. If they differ, discard the copy and repeat. Never hand off a block that failed comparison, and never rely on CDTask to detect the difference.

For partial approval:

- preserve CDP's Partial Approval Result;
- pass only the canonical approved-subset Scope Lock;
- require `Approved Items` to match `in_scope` verbatim;
- keep every `Unapproved Items` entry explicitly excluded;
- prepare no task for the unapproved remainder.

The unapproved remainder has no owner in this round. State it in the terminal report, mark it as not carried forward, and require a new CDP round for any part of it.

If Scope Lock is missing, conflicting, inconsistent, or too narrow for the requested tasking, do not invoke CDTask. Return to CDP for replanning and renewed approval.

### Risk-Level Routing

Route on the `Risk Level` field, never on how small a change looks.

| Risk Level | Coordination depth | CDTask default |
|---|---|---|
| Level S | Pass CDP's compact package through with minimal coordination | Not selected |
| Level M | Brief coordination summary | Not selected |
| Level L | Full package with risks, rollback, and verification | Selected |
| Level XL | Full package plus phase tracking | Selected |

Risk level never changes the approval requirement. Every level requires a completed CDP approval gate and a valid Approval Record before handoff.

### CDTask Selection

CDTask is optional. Select it when the approved work:

- needs persistence or later resumption;
- needs explicit task decomposition;
- is large, phased, or multi-contributor;
- should separate planning from implementation.

Otherwise the Approved Plan Package is the terminal output. Do not create a task definition for work that gains nothing from one.

If CDTask is selected but unavailable, do not fabricate a task definition, write a fallback file, or install anything. Output this command verbatim and stop until the user confirms installation:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

The command must name `--skill cdtask`. Never invent a repository, package name, or path.

### Phased Delivery

A Level XL plan may be approved one phase at a time. `Phase` and `Remaining-Phases` in the CDP return say where the flow is. Each phase is a separate round with its own plan display, approval, Scope Lock, and handoff.

Do not stop while `Remaining-Phases` is greater than zero, and do not carry one phase's approval into the next.

### Loop Budgets

- CDP replanning: at most 3 rounds for the same requirement.
- CDTask repair or replanning: at most 2 rounds for the same defect.

Record what changed each round. The same problem returning twice goes to the user with the difference between rounds, regardless of remaining budget. A round that changes nothing is a stall, not a round.

### Repository Drift

`Source-Branch` and `Source-Commit` arrive with the approved package. Compare them with the current repository state before step 6. If either differs, the approval was made against different code: return to CDP for revalidation instead of handing off. If they are `Unavailable`, state that drift could not be checked.

### Flow State

Print the Flow State block from [references/flow-contracts.md](references/flow-contracts.md) before and after every handoff so a human can resume an interrupted session.

CDF holds no persistent state. The block is a readable checkpoint, not a state file. Do not write it to disk and do not treat it as runtime state.

### Internal Handoff Formats

- CDF → CDP: `Context: cdf-managed` and `Lifecycle-Owner: cdf`.
- CDP → CDF: `Contract-Version: cdp-cdf/v1` with `Planning Status`, `Risk Level`, `Phase`, `Remaining-Phases`, and `Reason`.
- CDF → CDTask: `Contract-Version: cdf-cdtask/v1`, `Handoff-Type: managed-tasking`, `Approval-State: plan-approved`, `Execution-Owner: cdf`, supported `Risk-Level`, and available workspace/branch/commit metadata.
- CDTask → CDF: `Contract-Version: cdf-cdtask/v1` with `Tasking Status` and, when blocked, `Blocked-Reason-Class`.

[references/flow-contracts.md](references/flow-contracts.md) holds the full field definitions. If a required field is missing or unrecognized, treat the return as blocked, name the field, and stop.

These are internal CDF v0.1 Skill handoff formats, not public runtime protocols.

## Outputs and Handoffs

CDF sends CDP:

- original requirement and relevant context;
- user constraints and known scope boundaries;
- `cdf-managed` lifecycle ownership.

CDF expects an `APPROVED` CDP return to contain:

- requirement understanding and technical analysis;
- evidence-backed implementation plan;
- risk level, material risks, and assumptions;
- acceptance criteria and verification strategy;
- canonical approved Scope Lock;
- Approval Record and the applicable Locked Scope Summary or Partial Approval Result.

A `NOT_APPROVED` or `BLOCKED` return carries `Reason` and no plan content. Absent sections are expected there, not a defect.

CDF sends CDTask only the approved package. CDTask determines task structure and dependencies without changing implementation meaning.

The CDF v0.1 terminal output is a handoff-ready Task Definition, or the Approved Plan Package when CDTask is not selected, plus an explicit statement that execution remains outside CDF.

## References and Usage

- [Flow Contracts](references/flow-contracts.md) — full field definitions for the four handoff directions, status semantics, and the Flow State block.

Read it when composing or validating a handoff. If it is unavailable, continue with this Skill as the source of truth and mention the missing supporting reference.

Use CDF when a development request needs controlled planning, explicit scope, or a human plan decision. A typical invocation is:

```text
Use CDF to assess this requirement, obtain an approved CDP plan, and prepare a CDTask handoff.
```

Keep coordination concise. Let CDP provide technical depth and CDTask provide task-definition detail.

## Non-Negotiable Rules

- Do not implement or modify code.
- Do not execute development tasks.
- Do not review implementation.
- Do not skip CDP, and do not hand off without a valid Approval Record.
- Do not judge whether a user reply is valid approval; that gate belongs to CDP.
- Do not route on plan prose, task prose, or a reason string; route only on contract fields.
- Do not invoke CDTask while material decisions remain unresolved.
- Do not expand approved scope.
- Do not invent missing planning decisions or supply a missing contract field.
- Do not replace CDP or CDTask responsibilities.
- Do not claim runtime, event-system, public schema-protocol, CLI, executor, verification, or review capability.
- End after task-definition handoff, or after the approved plan package when CDTask is not selected.

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
