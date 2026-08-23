# CDF: Controlled Development Flow

## Quick Understanding

CDF is the control plane of the CDF Suite. It decides whether a development request enters the controlled flow, routes each component return on contract fields, and refuses any handoff that lacks completed approval evidence.

> Small changes should be fast. Risky changes should be controlled.

CDF v0.1 ends at a handoff. It is not a runtime, scheduler, executor, verification system, or review system, and it holds no persistent state.

## Position in the CDF Suite

```text
Requirement
 ↓
CDF assessment
 ↓
CDP planning + human plan approval
 ↓
CDF handoff preconditions
 ↓
CDTask definition, when selected
 ↓
Handoff-ready Task Definition, or the Approved Plan Package
```

| Skill | Role | Output |
|---|---|---|
| `cdf` | Control plane, return routing, handoff preconditions | Approved flow handoff |
| `cdp` | Evidence-based planning, risk classification, Scope Lock, and the human approval gate | Approved Plan Package |
| `cdtask` | Approved-plan compilation into verifiable tasks | Handoff-ready Task Definition |

CDF coordinates the flow. It does not replace CDP planning, the CDP approval gate, or CDTask decomposition.

## Responsibilities and Boundaries

CDF is responsible for:

- flow assessment and coordination;
- component handoff and return routing;
- handoff preconditions and approval-evidence enforcement;
- preservation of approved scope.

CDF is not responsible for:

- requirement analysis or technical planning (`cdp`);
- the human approval gate itself, including plan display, approval-wording judgement, and re-asking (`cdp`);
- detailed task decomposition (`cdtask`);
- implementation, execution, or scheduling;
- implementation verification or review;
- runtime or lifecycle-state management.

CDF routes on contract fields. It never reads plan prose, task prose, or a reason string to decide what happens next.

## Routing

Every decision is a field comparison, never a judgement about wording or intent.

| `Planning Status` from CDP | CDF action |
|---|---|
| `APPROVED` | Continue to the handoff preconditions |
| `NOT_APPROVED` | Report `Reason`, produce no handoff, end the round as terminated |
| `BLOCKED` | Report `Reason` verbatim and end the round |
| missing or unrecognized | Treat as blocked, name the missing field, end the round |

| `Tasking Status` from CDTask | CDF action |
|---|---|
| `READY` | Produce the terminal handoff |
| `NOT_READY` | Return for repair inside approved scope, then re-evaluate |
| `BLOCKED` | Route on `Blocked-Reason-Class`: approval and scope-lock defects re-run the preconditions; `requires-new-scope`, `partial-remainder`, and `ambiguity` return to CDP |

## Handoff Preconditions

Before invoking CDTask, CDF confirms by field check that:

- `Contract-Version: cdp-cdf/v1` is present and recognized;
- `Planning Status` is `APPROVED`;
- every attestation field carries its required constant;
- an Approval Record exists with `Scope Approved: Yes` and `Code Changes Authorized In This Turn: No`;
- a canonical `cdp-scope/v1` block exists with all eight arrays populated;
- `Risk Level` is one of Level S, M, L, or XL;
- a Partial Approval Result is present when `Approval Type` is `partial`;
- `Phase` and `Remaining-Phases` are present or `Not applicable`;
- workspace, branch, and commit metadata are present or explicitly `Unavailable`.

Any failed condition returns the package to CDP. CDF never repairs a package, supplies a missing field, or proceeds on one that is merely close enough.

Approval confirms direction and scope. It does not authorize CDF to implement or execute anything.

## Attestation Fields

Some contract fields are constants rather than variables. A wrong value means the sending component acted outside its managed contract, so CDF reports it and ends the round instead of continuing:

| Field | Contract | Required value |
|---|---|---|
| `Lifecycle Owner` | `cdp-cdf/v1` | `CDF` |
| `Execution by CDP` | `cdp-cdf/v1` | `Not authorized` |
| `Code Changes by CDP` | `cdp-cdf/v1` | `None` |
| `Execution Owner` | `cdf-cdtask/v1` | `CDF` |

`Next Owner` must be `CDF` on an `APPROVED` return; `Human approver` alongside `APPROVED` means the approval gate never closed. `Task Count` must be present and greater than zero on a `READY` return.

## Scope Lock Preservation

The canonical `cdp-scope/v1` block travels from CDP through CDF to CDTask as an opaque payload, copied byte for byte. CDF does not paraphrase, reorder, merge, omit, weaken, expand, re-indent, normalize quoting, or re-wrap a line, and it reads the copy back to compare it against the source before handing off.

For partial approval, only the canonical approved-subset Scope Lock is passed. Every unapproved item stays explicitly excluded, no task is prepared for the remainder, and the terminal report states that the remainder was not carried forward.

## Risk Levels and CDTask Selection

| Risk Level | Coordination depth | CDTask default |
|---|---|---|
| Level S | Pass CDP's compact package through with minimal coordination | Not selected |
| Level M | Brief coordination summary | Not selected |
| Level L | Full package with risks, rollback, and verification | Selected |
| Level XL | Full package plus phase tracking | Selected |

Risk level never changes the approval requirement. Every level requires a completed CDP approval gate and a valid Approval Record before handoff.

CDTask is optional. It is selected when the approved work needs persistence, explicit decomposition, phasing, multiple contributors, or a separation between planning and implementation. Otherwise the Approved Plan Package is the terminal output.

If CDTask is selected but unavailable, CDF outputs the install command and stops. It never fabricates a task definition, writes a fallback file, or installs anything itself.

## Quick Start

Invoke with `cdf`, `/cdf`, `$cdf`, `cdf:`, or `controlled-development-flow`:

```text
Use CDF to assess this requirement, obtain an approved CDP plan, and prepare
a CDTask handoff.
```

CDF prints a Flow State block before and after every handoff so a human can resume an interrupted session. The block is a readable checkpoint, not a state file.

## References

- [Flow Contracts](references/flow-contracts.md) — field definitions for the four handoff directions, status semantics, and the Flow State block.

Read it when composing or validating a handoff. CDF remains the source of truth if the reference is unavailable.

## Installation

Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

Both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

## Non-Negotiable Rules

- Do not implement, modify, execute, or review code.
- Do not skip CDP, and do not hand off without a valid Approval Record.
- Do not judge whether a user reply is valid approval; that gate belongs to CDP.
- Do not route on plan prose, task prose, or a reason string.
- Do not expand approved scope or supply a missing contract field.
- Do not accept an attestation field that carries the wrong value, and do not correct one.
- Do not claim runtime, event-system, public schema-protocol, CLI, executor, verification, or review capability.
