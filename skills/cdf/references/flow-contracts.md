# CDF Flow Contracts

Read this file when composing or validating a handoff. The gates, routing tables, and preconditions stay in `../SKILL.md`; this file defines the fields they route on.

These are internal CDF v0.1 Skill handoff formats, not public runtime protocols.

## Table of Contents
- CDF to CDP
- CDP to CDF
- CDF to CDTask
- CDTask to CDF
- Flow State Block

## CDF to CDP

```text
Context: cdf-managed
Lifecycle-Owner: cdf
```

Send these with the requirement, user constraints, and known scope boundaries. They remove the ambiguity that would otherwise make CDP ask who owns the lifecycle.

CDP runs the human approval gate inside this context and returns its outcome. CDF does not display the plan, judge an approval reply, or re-ask.

## CDP to CDF

```text
# Approved Plan Package

Contract-Version: cdp-cdf/v1
Planning Status: <APPROVED | NOT_APPROVED | BLOCKED>
Lifecycle Owner: CDF
Execution by CDP: Not authorized
Code Changes by CDP: None
Risk Level: <Level S | Level M | Level L | Level XL>
Phase: <n of N | Not applicable>
Remaining-Phases: <count or 0>
Reason: <plain text; required for NOT_APPROVED and BLOCKED>
Next Owner: <Human approver | CDF>
```

| `Planning Status` | Meaning | Required content |
|---|---|---|
| `APPROVED` | The CDP approval gate completed with valid approval | Development Plan, canonical Scope Lock, Approval Record, and the applicable Locked Scope Summary or Partial Approval Result |
| `NOT_APPROVED` | The user declined, or the gate ended without valid approval | `Reason` only; no Approval Record |
| `BLOCKED` | CDP could not produce a safe plan or a bounded Scope Lock | `Reason` only; no Approval Record |

`Planning Status` is the only routing field. `Reason` is human-readable text with no routing meaning.

`Phase` and `Remaining-Phases` describe the approved phase only. `Remaining-Phases: 0` ends the flow; a positive count means another phase follows and requires its own approval.

## CDF to CDTask

```text
# CDF Tasking Handoff

Contract-Version: cdf-cdtask/v1
Handoff-Type: managed-tasking
Approval-State: plan-approved
Execution-Owner: cdf
Risk-Level: <Level S | Level M | Level L | Level XL>
Workspace: <absolute path or Unavailable>
Source-Branch: <branch or Unavailable>
Source-Commit: <commit or Unavailable>
```

Carry the canonical Scope Lock byte for byte, the Approval Record, and the applicable Locked Scope Summary or Partial Approval Result.

## CDTask to CDF

```text
Tasking Status: <READY | NOT_READY | BLOCKED>
Contract-Version: cdf-cdtask/v1
Blocked-Reason-Class: <approval | scope-lock | requires-new-scope | ambiguity | partial-remainder | Not applicable>
Execution Owner: CDF
Task Count: <N when available>
Next Owner: CDF
```

| `Blocked-Reason-Class` | Source defect | Where the repair belongs |
|---|---|---|
| `approval` | Missing or invalid approval | CDF preconditions, then CDP |
| `scope-lock` | Missing or contradictory canonical Scope Lock, including a projection that contradicts it | CDF preconditions, then CDP |
| `ambiguity` | Implementation-affecting ambiguity in a managed package | CDP |
| `requires-new-scope` | Tasking would require new scope, architecture, behavior, or acceptance criteria | CDP replanning and renewed approval |
| `partial-remainder` | The partial-approval remainder cannot be separated safely | CDP replanning and renewed approval |

`Blocked-Reason-Class` is `Not applicable` unless the status is `BLOCKED`.

## Flow State Block

Print this before and after every handoff:

```text
Flow State
- Stage: <assessment | planning | handoff preconditions | tasking | terminal>
- Round: <CDP n of 3 | CDTask n of 2 | not applicable>
- Risk Level: <level or unknown>
- Approval: <none | APPROVED | NOT_APPROVED | BLOCKED>
- Phase: <n of N | Not applicable>
- Contract: <cdp-cdf/v1 | cdf-cdtask/v1 | none>
```

The block is a readable checkpoint for a human resuming an interrupted session. CDF holds no persistent state: do not write it to disk and do not treat it as runtime state.
