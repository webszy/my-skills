# CDTask: Controlled Development Task

## Quick Understanding

CDTask is the task-definition and handoff layer of the CDF Suite. It converts an approved plan into verifiable tasks without changing the approved meaning or scope.

> Small changes should be fast. Risky changes should be controlled.

CDTask is optional. It creates task definitions and textual handoff information, and may persist a resumable task document. It is not a task engine, scheduler, executor, runtime, or review system.

## Position in the CDF Suite

```text
Requirement
 ↓
CDF assessment
 ↓
CDP planning + Scope Lock
 ↓
Human Plan Approval (run by CDP)
 ↓
CDTask: validate → decompose → guard scope → prepare handoff
 ↓
Execution, outside CDF v0.1
```

| Skill | Role | CDTask relationship |
|---|---|---|
| `cdf` | Control plane and return routing | Sends an approved managed package and receives task-definition readiness |
| `cdp` | Risk-aware planning, Scope Lock, and approval materials | Sends an optional approved deferred-execution package |
| `cdtask` | Approved-plan conversion into verifiable task definitions | Preserves meaning and prepares external handoff |

## Responsibilities and Boundaries

CDTask is responsible for:

- validating input readiness and approval metadata;
- copying and enforcing the canonical Scope Lock;
- defining dependencies and task boundaries;
- preserving acceptance criteria and protected areas;
- preparing executor-neutral handoff information;
- optionally persisting a resumable task document;
- reporting `READY`, `NOT_READY`, or `BLOCKED` for managed tasking.

CDTask is not responsible for:

- requirement analysis or technical replanning;
- plan approval;
- scope expansion;
- implementation or code modification;
- execution, scheduling, or parallel-work decisions;
- runtime or lifecycle control;
- implementation verification or review.

`READY` means the task definition is ready to return to CDF for a separately authorized handoff. It does not mean CDTask executed or verified anything.

## When to Use CDTask

Use CDTask when approved work needs persistence or later resumption, needs explicit decomposition, is large or phased or multi-contributor, or should separate planning from implementation.

Do not create a CDTask for every change, and do not use it to discover requirements, resolve product decisions, approve a plan, or repair a semantically incomplete plan.

## Input Routes

Exactly one route is chosen before tasking.

| Route | Required contract | Approval state | Lifecycle owner |
|---|---|---|---|
| CDF-managed | `cdf-cdtask/v1` | `plan-approved` | CDF |
| CDP deferred handoff | `cdp-cdtask/v1` | `scope-approved-execution-deferred` | External caller after resume through CDP |
| Manual requirement | `cdtask/v1` when persisted | `not-approved-by-cdp` | User / external caller |

Missing, invalid, or contradictory metadata is `BLOCKED`. CDTask never infers approval.

Manual input is not CDP-approved: the goal, scope, non-goals, acceptance criteria, and constraints are confirmed with the user first, and the persisted output is labelled accordingly. A requirement that needs substantial analysis or product decisions is routed through CDP instead.

These are internal CDF v0.1 Skill handoff formats, not public runtime protocols.

## Workflow

```text
Input route validation
  → Requirement readiness
  → Canonical Scope Lock validation
  → Dependency analysis
  → Task breakdown
  → Scope Guard
  → Handoff rules / Execution Contract
  → Task Readiness Gate
  → Optional persistence
  → Return to lifecycle owner
```

The canonical `cdp-scope/v1` block is copied verbatim from the received package. It is never derived, rebuilt, summarized, normalized, or rewritten. A readable projection may be added, but it cannot replace or alter the canonical block, and any projection that contradicts it is `BLOCKED`.

## Task Rules

- One primary outcome per task.
- Explicit dependency and completion criteria.
- Concrete write scope without fabricated paths.
- Verification appropriate to risk.
- Protected areas copied into `Must Not Change`.
- No task silently absorbs another task or an unapproved outcome.

`DRAFT` and `READY` are definition states only. Runtime states such as assigned, running, retrying, or completed are never introduced.

Dependencies describe constraints only — CDTask does not schedule work, assign workers, or choose parallel execution. A cycle caused only by task structure is `NOT_READY` and is repaired inside approved scope; a cycle revealing a plan contradiction is `BLOCKED`.

## Task Readiness Gate

| Status | Meaning | Required action |
|---|---|---|
| `READY` | Task definitions are complete, consistent, and within approved scope | Return or persist according to the selected route |
| `NOT_READY` | A CDTask-owned definition defect can be repaired without changing approved meaning | Repair and rerun the gate |
| `BLOCKED` | Approval, scope, requirement meaning, or source-plan authority is missing or contradictory | Stop and return to user, CDP, or CDF |

Every `BLOCKED` return carries a `Blocked-Reason-Class` — `approval`, `scope-lock`, `ambiguity`, `requires-new-scope`, or `partial-remainder` — so CDF can route the return without reading the explanation.

A `READY` managed return also carries `Task Count`, which must be greater than zero, plus the `Execution Owner: CDF` and `Next Owner: CDF` attestations. Both attestations are constants: CDTask returns the flow rather than continuing it.

## Scope Guard

After decomposition, CDTask confirms that every task maps to approved `in_scope` or `will_change`; that no task maps to `out_of_scope`, `non_goals`, `will_not_change`, or an unapproved remainder; that Scope Lock and approval wording are preserved verbatim; that dependencies add no new product or architecture decision; that acceptance criteria are preserved rather than broadened; that stop conditions are visible to the future executor; and that no implementation, scheduling, runtime, or review action was performed.

For partial approval, `Approved Items` must match the approved-subset `in_scope` verbatim, every unapproved item stays verbatim and explicitly excluded, and no task, write scope, note, acceptance criterion, or verification step may map to an unapproved item.

## Persistence

Persistence happens only when requested or required by the selected handoff path. The default path is:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md
```

An existing task document is never silently overwritten: a colliding default name is suffixed, and an explicit path is confirmed first. Only the required parent directory is created, and no implementation file is modified. After saving, the file is read back and verified against the route-specific document contract; success is not claimed if verification fails.

## Quick Start

Typical CDF-managed invocation:

```text
Convert this approved CDF plan into dependency-aware task definitions.
Preserve the canonical Scope Lock verbatim and return task readiness to CDF.
```

Typical standalone deferred invocation:

```text
Convert this approved CDP package into a resumable CDTask. Do not execute it.
```

## References

- [Task Templates](references/task-templates.md) — dependency, task-breakdown, and handoff output formats.
- [Persistence](references/persistence.md) — route-specific task-document contracts and save verification.

Read Task Templates before decomposition and Persistence before writing a file. CDTask remains the source of truth if a reference is unavailable.

## Installation

Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -g -y
```

Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a claude-code -g -y
```

Both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

## Non-Negotiable Rules

- Do not implement or modify code.
- Do not execute, schedule, assign, monitor, or review work.
- Do not infer or grant approval.
- Do not replan or invent implementation-affecting decisions.
- Do not expand approved scope.
- Do not rewrite the canonical Scope Lock or Approval Record.
- Do not create tasks for unapproved partial-approval items.
- Do not convert readiness statuses into runtime states.
