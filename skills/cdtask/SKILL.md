---
name: cdtask
description: Convert approved development plans into scoped, dependency-aware, verifiable task definitions and executor handoff information. Use when CDF provides an approved managed plan, standalone CDP hands off approved work for persistence, or a user asks to split a stable requirement into tasks. CDTask may persist designated task documents, but it does not execute, schedule, or manage a lifecycle.
---

# CDTask: Controlled Development Task

## Quick Understanding

> CDTask is the task-definition and handoff layer of the CDF Suite: it converts an approved plan into verifiable tasks without changing the approved meaning or scope.

**Small changes should be fast. Risky changes should be controlled.**

CDTask is optional. It creates task definitions and textual handoff information; it is not a task engine, scheduler, executor, runtime, or review system.

## Position in the CDF Suite

```text
Requirement
    ↓
CDF Assessment
    ↓
CDP Planning + Scope Lock
    ↓
Human Plan Approval
    ↓
CDTask: Validate → Decompose → Guard Scope → Prepare Handoff
    ↓
Execution (outside CDF v0.1)
```

| Skill | Role | CDTask relationship |
|---|---|---|
| `cdf` | Control plane and human-gate coordination | Sends an approved managed package and receives task-definition readiness |
| `cdp` | Risk-aware planning, Scope Lock, and approval materials | Sends an optional approved deferred-execution package |
| `cdtask` | Approved-plan conversion into verifiable task definitions | Preserves meaning and prepares external handoff |

## Responsibilities and Boundaries

CDTask owns:

- validating input readiness and approval metadata;
- copying and enforcing the canonical Scope Lock;
- defining dependencies and task boundaries;
- preserving acceptance criteria and protected areas;
- preparing executor-neutral handoff information;
- optionally persisting a resumable task document;
- reporting `READY`, `NOT_READY`, or `BLOCKED` for managed tasking.

CDTask does not own:

- requirement analysis or technical replanning;
- plan approval;
- scope expansion;
- implementation or code modification;
- execution, scheduling, or parallel-work decisions;
- runtime or lifecycle control;
- implementation verification or review.

`READY` means the task definition is ready to return to CDF for a separately authorized handoff. It does not mean CDTask executed or verified the work.

## When to Use CDTask

Use CDTask when approved work:

- needs persistence or later resumption;
- needs explicit task decomposition;
- is large, phased, or multi-contributor;
- should separate planning from implementation.

Do not create CDTask for every change. Keep small, immediate, approved standalone work in CDP when durable tasking adds no value.

Do not use CDTask to discover requirements, resolve product decisions, approve a plan, or repair a semantically incomplete plan.

## Input Routes

Choose exactly one route before tasking.

| Route | Required contract | Approval state | Lifecycle owner |
|---|---|---|---|
| CDF-managed | `cdf-cdtask/v1` | `plan-approved` | CDF |
| CDP deferred handoff | `cdp-cdtask/v1` | `scope-approved-execution-deferred` | External caller after resume through CDP |
| Manual requirement | `cdtask/v1` when persisted | `not-approved-by-cdp` | User / external caller |

These are internal CDF v0.1 Skill handoff formats, not public runtime protocols.

### CDF-Managed Input

Require:

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

The package must also contain:

- canonical `cdp-scope/v1` Scope Lock;
- `Change Scope`, the readable projection of `will_change` and `will_not_change`;
- requirement understanding and decomposition;
- confirmed evidence and open assumptions;
- technical approach or proposed design;
- approved phase boundary, when applicable;
- implementation plan or phases;
- risks, acceptance criteria, verification strategy, and rollback;
- Approval Record;
- Locked Scope Summary or Partial Approval Result.

Reject missing, invalid, or contradictory metadata as `BLOCKED`. Do not infer approval.

Require `Requirement Understanding`, `Change Scope` with `Will Change` and `Will Not Change`, `Acceptance Criteria`, `Verification Strategy`, and `Approval Record` for every risk level. Require stronger boundaries, risk, and rollback detail for Level L/XL; require substantive design, data/API/state flow, phase boundary, and phases for Level XL. Do not force meaningless architecture placeholders into managed Level S/M packages.

### CDP Deferred Input

Require:

```text
# CDP Task Handoff Package

Contract-Version: cdp-cdtask/v1
Handoff-Type: deferred-local-task
Title: <short title>
Workspace: <absolute path>
Requested-Task-Path: <user path or _cdtask/YYYY-MM-DD-<slug>.md>
Risk-Level: <Level S | Level M | Level L | Level XL>
Approval-State: scope-approved-execution-deferred
Source-Branch: <branch or Unavailable>
Source-Commit: <commit or Unavailable>
```

Require the canonical Scope Lock and these exact headings: `Requirement Understanding`, `Requirement Decomposition`, `Confirmed Evidence`, `Open Assumptions`, `Change Scope` with `Will Change` and `Will Not Change`, `Proposed Design`, `Data Model / API / State Flow`, `Approved Phase Boundary`, `Implementation Plan / Phases`, `Risks`, `Acceptance Criteria`, `Test Plan / Test Strategy`, `Rollback Plan`, `Approval Record`, `Handoff Execution Paths`, and `Resume Rules`.

For Level S/M/L, architecture-only headings remain present with `Not applicable for <risk level>.`; Level XL contains substantive approved content. This approval state approves the planning scope only; execution remains deferred.

### Manual Input

Accept a stable requirement or an existing requirements document. Manual input is not CDP-approved. Before producing final tasks:

- confirm the goal, scope, non-goals, acceptance criteria, and material constraints;
- ask focused questions for implementation-affecting ambiguity;
- create an explicit Scope Lock with the user;
- label persisted output `Approval-State: not-approved-by-cdp`.

If the requirement needs substantial analysis, risk classification, or product decisions, route it through CDP instead of inventing a plan.

## Workflow

```text
Input Route Validation
    ↓
Requirement Readiness
    ↓
Canonical Scope Lock Validation
    ↓
Dependency Analysis
    ↓
Task Breakdown
    ↓
Scope Guard
    ↓
Handoff Rules / Execution Contract
    ↓
Task Readiness Gate
    ↓
Optional Persistence
    ↓
Return to Lifecycle Owner
```

### 1. Requirement Readiness

Confirm that the package defines:

- the desired outcome and observable behavior;
- approved scope and explicit exclusions;
- affected areas and dependencies;
- material assumptions and stop conditions;
- acceptance criteria and verification strategy;
- approval state and lifecycle owner.

For manual input, ask the user about missing implementation-affecting details. For CDP or CDF input, do not create new assumptions. Return semantic gaps to the source owner as `BLOCKED`.

### 2. Scope Lock

For CDF or CDP input, copy the received canonical block verbatim:

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

Do not derive, rebuild, summarize, normalize, or rewrite the canonical block. A readable projection may be added elsewhere, but it cannot replace or alter the canonical block.

For manual input, use the same eight-field structure after the user confirms it.

### 3. Scope Consistency Validation

Validate the contract before decomposing tasks:

- all eight Scope Lock arrays exist and contain explicit values;
- Approval Record matches the canonical Scope Lock and selected action;
- `in_scope` maps only to approved plan outcomes;
- `out_of_scope`, `non_goals`, and `will_not_change` remain explicit constraints;
- `will_change` contains no unapproved affected area;
- every readable projection, including `Change Scope`, plan prose, and phase boundaries, matches the canonical block;
- high-level acceptance criteria match approved outcomes;
- assumptions and stop conditions are actionable;
- risk and phase metadata do not contradict the plan.

Then validate every task:

- goal, scope, write scope, notes, and acceptance criteria map to `in_scope` or `will_change`;
- `Must Not Change` preserves `out_of_scope`, `non_goals`, and `will_not_change`;
- no task introduces a new behavior, dependency, affected area, or acceptance criterion;
- verification proves approved outcomes without widening them.

For partial approval:

- `Approved Items` must match the canonical approved-subset `in_scope` entries verbatim;
- every `Unapproved Items` entry must remain verbatim and explicitly excluded;
- no task, write scope, note, acceptance criterion, or verification step may map to an unapproved item;
- include the Partial Approval Result in the handoff.

If tasking introduces an unapproved impact surface, report `BLOCKED` and return to CDP for replanning and renewed approval. CDTask has no authority to expand scope.

### 4. Dependency Analysis

Describe only dependency constraints. Do not schedule work, assign workers, choose parallel execution, or claim runtime coordination.

Use the dependency format for the selected input route from [references/task-templates.md](references/task-templates.md): a linear `Dependency Order` for manual or CDP-deferred input when dependencies are truly linear, or a stable-ID `Dependency Graph` with `Dependency Data` for CDF-managed input.

A cycle caused only by task-definition structure is `NOT_READY`; repair it inside approved scope. A cycle revealing a plan contradiction is `BLOCKED` and returns to the source owner.

### 5. Task Breakdown

Use the smallest independently verifiable tasks that preserve implementation meaning.

Read the task format for the selected input route in [references/task-templates.md](references/task-templates.md) before writing tasks, and keep every field it requires.

`DRAFT` and `READY` are definition states only. Do not add runtime states such as assigned, running, retrying, or completed.

Task rules:

- one primary outcome per task;
- explicit dependency and completion criteria;
- concrete write scope without fabricated paths;
- verification appropriate to risk;
- protected areas copied into `Must Not Change`;
- no task may silently absorb another task or an unapproved outcome.

### 6. Scope Guard

Complete this checklist after task decomposition:

```markdown
## Scope Guard Checklist
- [ ] Every task maps to approved `in_scope` or `will_change`.
- [ ] No task maps to `out_of_scope`, `non_goals`, `will_not_change`, or unapproved remainder.
- [ ] Scope Lock and approval wording are preserved verbatim.
- [ ] Dependencies add no new product or architecture decision.
- [ ] Acceptance criteria are preserved, not broadened.
- [ ] Stop conditions are visible to the future executor.
- [ ] No implementation, scheduling, runtime, or review action was performed.
```

Any failed item must be resolved through the Task Readiness Gate.

### 7. Handoff Information

Produce the handoff text for the selected route from [references/task-templates.md](references/task-templates.md): `Codex Handoff Rules` for manual or CDP-deferred output, or an executor-neutral `Execution Contract` for CDF-managed output.

These sections are handoff text only. CDTask does not select, invoke, monitor, or review an executor.

## Task Readiness Gate

Run this gate after the Scope Guard and before persistence or handoff. Legacy input titled `Final Review Gate` may be interpreted as this gate, but CDTask performs task-definition validation, not code review.

### Status Semantics

| Status | Meaning | Required action |
|---|---|---|
| `READY` | Managed task definitions are complete, internally consistent, within approved scope, and ready to return to CDF | Return or persist according to the selected route |
| `NOT_READY` | A CDTask-owned definition defect can be repaired without changing approved meaning | Repair the task definition and rerun the gate |
| `BLOCKED` | Approval, scope, requirement meaning, or source-plan authority is missing or contradictory | Stop and return to user, CDP, or CDF |

Use this output:

```markdown
## Task Readiness Gate

### Tasking Status
<READY | NOT_READY | BLOCKED>

### Confirmed Clear
- <validated item>

### Potential Ambiguities
- <none or issue>

### Potential Conflicts
- <none or issue>

### Scope Creep Risks
- <none or issue>

### Missing Decisions
- <none or issue>

### Required User Confirmations
- <none or focused question>

### Final Status
<concise reason and routing decision>
```

Examples of `NOT_READY`:

- duplicate or unstable task IDs;
- incomplete task fields;
- a task-only dependency cycle;
- acceptance wording not yet mapped to tasks but recoverable verbatim.

Examples of `BLOCKED`:

- missing or invalid approval;
- missing or contradictory canonical Scope Lock;
- a readable projection that contradicts the canonical Scope Lock;
- implementation-affecting ambiguity in a managed package;
- tasking would require new scope, architecture, behavior, or acceptance criteria;
- partial-approval remainder cannot be separated safely.

## Optional Persistence

Persist only when requested or required by the selected handoff path. Never silently overwrite an existing task document. Use the explicit path supplied by the user; otherwise use:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md
```

Resolve relative paths against `Workspace`. Do not overwrite silently: suffix a colliding default name, and ask before replacing an explicit path. Create only the required parent directory and modify no implementation file.

Read [references/persistence.md](references/persistence.md) before writing a file. It holds the route-specific document contract — frontmatter, required sections, and the save-verification checklist — for CDP deferred, manual, and CDF-managed output. Managed persistence occurs only when requested by CDF or the user.

After saving, read the file back and verify it against that contract. Do not claim success if verification fails.

Treat `READY`, `ready_for_resume`, `ready_for_review`, and `tasking_ready` as distinct task-definition states. Do not reinterpret them as runtime execution states.

## Resume and Return Rules

- A `cdp-cdtask/v1` file supports two handoff paths: same-stack resume through `Continue local task: <path>`, or explicit handoff to an external coding agent. In either case, the task document alone is not execution authorization.
- Same-stack resume goes through CDP, which revalidates approval, assumptions, evidence, Scope Lock, repository state, and Task Readiness before any action.
- An external agent may receive only an explicit user handoff and must stay inside the Task Breakdown, Scope Guard, and Codex Handoff Rules.
- A `cdtask/v1` manual file returns to the user or CDP for review and approval.
- A `cdf-cdtask/v1` file returns to CDF. CDTask must not continue the lifecycle.

Replanning, scope expansion, or changed acceptance criteria always return to CDP and require renewed approval.

For managed return, end with the current status and ownership:

```text
Tasking Status: <READY | NOT_READY | BLOCKED>
Contract-Version: cdf-cdtask/v1
Blocked-Reason-Class: <approval | scope-lock | requires-new-scope | ambiguity | partial-remainder | Not applicable>
Execution Owner: CDF
Task Count: <N when available>
Next Owner: CDF
```

`Blocked-Reason-Class` is required when the status is `BLOCKED` and `Not applicable` otherwise. It lets CDF route the return without reading the blocking explanation. Map every `BLOCKED` reason above to exactly one class:

| Class | Blocking reason |
|---|---|
| `approval` | missing or invalid approval |
| `scope-lock` | missing or contradictory canonical Scope Lock, including a projection that contradicts it |
| `ambiguity` | implementation-affecting ambiguity in a managed package |
| `requires-new-scope` | tasking would require new scope, architecture, behavior, or acceptance criteria |
| `partial-remainder` | the partial-approval remainder cannot be separated safely |

## Output Modes

Choose the smallest output that satisfies the request:

| Mode | Use |
|---|---|
| Review only | Report readiness and blockers without task decomposition |
| Task breakdown | Return Scope Lock, dependencies, tasks, Scope Guard, handoff rules, and readiness |
| Append | Add the tasking sections to an existing document without altering approved content |
| Full merged document | Combine requirement context and tasking while preserving the canonical blocks |
| Clarification needed | Return focused questions and `NOT_READY` or `BLOCKED` |
| CDP local save | Persist `cdp-cdtask/v1` deferred work |
| CDF managed tasking | Return or persist `cdf-cdtask/v1` managed tasks to CDF |

## References and Usage

Use the references progressively:

- [Task Templates](references/task-templates.md) — dependency, task-breakdown, and handoff output formats;
- [Persistence](references/persistence.md) — route-specific task-document contracts and save verification.

Read Task Templates before decomposition and Persistence before writing a file. If a reference is unavailable, continue with this Skill as the source of truth and mention the missing supporting reference.

Typical CDF-managed invocation:

```text
Convert this approved CDF plan into dependency-aware task definitions. Preserve the canonical Scope Lock verbatim and return task readiness to CDF.
```

Typical standalone deferred invocation:

```text
Convert this approved CDP package into a resumable CDTask. Do not execute it.
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
- Return managed outputs to CDF and deferred outputs through their declared resume path.
