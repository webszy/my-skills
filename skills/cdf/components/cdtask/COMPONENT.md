# CDTask: Internal Post-Approval Task Compiler

CDTask is an internal instruction component of CDF. CDF loads it only after CDF has completed requirement analysis, repository-evidence inspection, risk classification, development planning, Scope Lock, human approval, and an explicit **Save as Task** decision.

CDTask has no direct invocation, installation, or public input surface. It compiles an approved CDF package into dependency-aware task definitions, persists the result, verifies the saved document, returns its path to CDF, and stops.

## Authority Boundary

CDTask owns only:

- validation of the approved tasking handoff;
- byte-for-byte preservation and enforcement of the canonical Scope Lock;
- dependency analysis and task decomposition inside approved scope;
- task-definition consistency and Scope Guard checks;
- persistence of the task document and read-back verification;
- a structured compilation result returned to CDF.

CDTask does not:

- accept a raw requirement, PRD, development request, or direct user instruction;
- inspect evidence to determine requirement meaning;
- plan or replan implementation;
- select a technical approach or make product or architecture decisions;
- classify or change risk;
- request, infer, grant, or renew approval;
- modify the Scope Lock, acceptance criteria, or approved phase boundary;
- implement, execute, schedule, assign, monitor, or review work;
- verify an implementation or claim that planned checks were run.

Task-definition validation is not implementation review. A saved task is not execution authorization.

## The Only Accepted Input

Accept input only from CDF in this form:

```text
# CDF Task Handoff

Contract-Version: cdf-cdtask/v1
Handoff-Type: approved-tasking
Approval-State: approved
Risk-Level: <Level S | Level M | Level L | Level XL>
Workspace: <absolute path or Unavailable>
Source-Branch: <branch or Unavailable>
Source-Commit: <commit or Unavailable>
Source-Worktree-State: <clean | dirty | Unavailable>
```

CDF may additionally provide persistence metadata:

```text
Task-Title: <short approved title>
Requested-Task-Path: <absolute path or Workspace-relative path>
```

Both fields are optional. They are routing and naming metadata only and cannot change approved task meaning. If `Task-Title` is absent, derive a filesystem-safe slug mechanically from the first approved `in_scope` entry; if it has no usable characters, use `task`. If `Requested-Task-Path` is absent, use the default destination under `Workspace`.

The handoff must also contain:

- Requirement Understanding;
- Evidence Summary, including material evidence gaps recorded by CDF;
- Development Plan;
- the canonical `cdf-scope/v1` Scope Lock;
- Approval Record covering that plan and Scope Lock and selecting **Save as Task**;
- Acceptance Criteria;
- Verification Strategy;
- Risks;
- Rollback Plan when applicable;
- Approved Phase Boundary when applicable;
- Partial Approval Result when approval covers only a safely separable subset;
- enough approved repository evidence or affected-area detail to create concrete write scopes without guessing.

`Risk-Level` is inherited metadata. CDTask must not reinterpret or recalculate it.

Reject every other input route. Do not translate an unsupported input into this contract, ask the user planning questions, or construct missing approval evidence. Return the defect to CDF.

## Input Validation

Before decomposition, verify all of the following:

1. The contract version, handoff type, approval state, and risk value exactly match the supported values.
2. Workspace, branch, commit, and worktree-state traceability are present, using `Unavailable` only where the contract permits it.
3. The Approval Record unambiguously binds the approved Development Plan and canonical Scope Lock and records **Save as Task** as the approved next action.
4. The package has no contradiction among Requirement Understanding, Development Plan, Scope Lock, Acceptance Criteria, Verification Strategy, phase boundary, and partial-approval material.
5. The approved evidence is sufficient to define tasks and write scopes without inventing paths, interfaces, modules, dependencies, or behavior.

Missing or contradictory authority is `BLOCKED`; it is never an invitation for CDTask to complete the planning package.

## Canonical Scope Lock

The handoff must contain one canonical block beginning with:

```yaml
Scope-Lock-Version: cdf-scope/v1
in_scope: []
out_of_scope: []
non_goals: []
assumptions: []
stop_conditions: []
will_change: []
will_not_change: []
acceptance_criteria: []
```

All eight fields must exist and must be arrays. Empty arrays are valid; do not invent filler prose.

Treat the complete canonical block as an immutable opaque payload. Copy it verbatim. Do not paraphrase, rewrite, expand, weaken, normalize, re-indent, reorder, re-wrap, merge, omit, or reserialize it. Readable mappings elsewhere in the task document are secondary and must not conflict with the canonical block.

Before persistence, compute SHA-256 over the exact canonical Scope Lock bytes and the exact Approval Record bytes. Persist both digests. After persistence, extract both saved payloads, compare their bytes with the received payloads, recompute their digests, and require every comparison to match. Any difference invalidates the saved task.

For partial approval:

- preserve the Partial Approval Result;
- require approved items to map exactly to the canonical approved-subset Scope Lock;
- preserve unapproved items verbatim as exclusions;
- create no task goal, positive scope, write operation, implementation obligation, acceptance mapping, or verification obligation for an unapproved item; carry it only as a prohibition or exclusion;
- return `BLOCKED` if the approved subset cannot be separated safely.

## Compilation Workflow

```text
Validate Approved Handoff
        ↓
Freeze Canonical Scope and Approval Record
        ↓
Analyze Dependency Constraints
        ↓
Compile Stable-ID Tasks
        ↓
Run Scope Guard
        ↓
Run Compilation Gate
        ↓
Persist Task Document
        ↓
Read Back and Verify
        ↓
Return Path to CDF
        ↓
Stop
```

CDTask never continues into execution.

### Dependency Analysis

Describe dependency constraints only. Do not assign workers, choose concurrency, schedule tasks, or claim runtime coordination.

Use stable task IDs and a directed acyclic graph. A cycle caused only by task grouping is a CDTask-owned definition defect: repair the grouping without changing approved meaning. A cycle that exposes an ambiguity or contradiction in the Development Plan is `BLOCKED` and returns to CDF planning.

Read [Task Templates](references/task-templates.md) before compiling dependency data or tasks.

### Task Breakdown

Create the smallest independently verifiable tasks that preserve the approved implementation meaning:

- one primary outcome per task;
- stable ID and explicit dependencies;
- a direct mapping to approved `in_scope` or `will_change` entries;
- concrete write scope supported by the approved evidence;
- only implementation direction already present in the approved Development Plan;
- approved acceptance-criteria mappings and planned verification obligations;
- protected areas and exclusions carried into `Must Not Change`;
- assumptions and stop conditions visible to the future CDF execution flow.

Do not fabricate paths. If the approved package identifies only an area, keep the write scope at that supported level. If safe decomposition requires a new module, interface, dependency, behavior, affected area, acceptance criterion, or architecture decision, stop with `BLOCKED`.

`DRAFT` and `READY` are task-definition states only. They are not execution states.

### Scope Guard

Complete this guard after decomposition:

```markdown
## Scope Guard
- [ ] Every task maps to approved `in_scope` or `will_change` content.
- [ ] No task treats `out_of_scope`, `non_goals`, `will_not_change`, or an unapproved remainder as positive scope or work; those entries appear only as protective constraints.
- [ ] The canonical Scope Lock is byte-for-byte unchanged.
- [ ] The Approval Record and approved phase boundary are preserved.
- [ ] Dependencies and tasks introduce no product, technical, or architecture decision.
- [ ] Acceptance criteria are preserved and are not broadened, weakened, or replaced.
- [ ] Planned verification maps to the approved Verification Strategy and is not reported as performed.
- [ ] Assumptions, stop conditions, and protected areas are visible to a future CDF resume.
- [ ] No implementation, execution, scheduling, approval, risk classification, or implementation review occurred.
```

Every item must pass before persistence.

## Compilation Gate

Run this gate after the Scope Guard and before persistence.

| Status | Meaning | Action |
|---|---|---|
| `READY` | The task definitions are complete, internally consistent, and wholly inside approved scope | Persist and verify |
| `NOT_READY` | A mechanical CDTask-owned defect can be repaired without changing approved meaning | Repair the definition and rerun the gate |
| `BLOCKED` | Authority, approved meaning, scope, acceptance, or safe separability is missing or contradictory | Stop and return the package to CDF |

Mechanical defects include duplicate IDs, a missing task field, or a task-grouping-only dependency cycle. CDTask may repair only those defects whose correction is deterministic and does not alter the approved plan.

Use one blocking reason class:

| Reason class | Example | CDF route |
|---|---|---|
| `invalid-handoff` | unsupported or missing contract metadata | Restore a valid CDF handoff before tasking |
| `approval-invalid` | missing, contradictory, or non-tasking Approval Record | Return to the CDF approval gate |
| `scope-lock-invalid` | missing, malformed, changed, or contradictory canonical Scope Lock | Return to CDF planning and obtain renewed approval |
| `ambiguity` | task boundaries require an implementation-affecting assumption | Return to CDF planning and obtain renewed approval |
| `requires-new-scope` | compilation needs a new module, interface, dependency, behavior, or affected area | Return to CDF planning and obtain renewed approval |
| `acceptance-change` | compilation would add, remove, weaken, broaden, or reinterpret acceptance criteria | Return to CDF planning and obtain renewed approval |
| `verification-change` | compilation would add, remove, weaken, or materially reinterpret verification obligations | Return to CDF planning and obtain renewed approval |
| `partial-separation` | approved and unapproved work cannot be separated safely | Return to CDF planning and obtain renewed approval |
| `persistence-failure` | destination or read-back verification prevents a trustworthy save | Return to CDF for destination or I/O resolution; do not treat the artifact as resumable |

For `ambiguity`, `requires-new-scope`, `acceptance-change`, `verification-change`, or `partial-separation`, CDF must reinspect the relevant evidence, produce a refreshed Development Plan and canonical Scope Lock package, and request renewed human approval. This fresh planning and approval round is required even if re-analysis leaves the canonical Scope Lock text unchanged. CDTask must not propose or apply the resolution.

Return a structured result to CDF:

```text
# CDTask Compilation Result

Contract-Version: cdf-cdtask/v1
Compilation-Status: <READY | NOT_READY | BLOCKED>
Blocked-Reason-Class: <reason class | Not applicable>
Saved-Task-Path: <absolute path | Unavailable>
Task-Count: <number | Unavailable>
Scope-Lock-Read-Back: <verified | not-verified>
Approval-Record-Read-Back: <verified | not-verified>
Document-Read-Back: <verified | not-verified>
Reason: <concise explanation | Not applicable>
```

`READY` requires an absolute saved path and all three read-back fields set to `verified`. A result that has not been successfully persisted is not `READY`.

## Persistence

Persistence is mandatory for this component path because CDF enters it only for **Save as Task**. Use the destination and document contract in [Persistence](references/persistence.md).

The default destination remains:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md
```

Write only the task document and its required parent directory. Do not modify implementation files. Never silently overwrite an existing task document.

After saving, reopen the exact destination and verify the frontmatter, required sections, stable task IDs, dependency graph, Scope Guard, Compilation Gate, Approval Record, and canonical Scope Lock. Do not report success when read-back verification fails.

## Resume Semantics

Every saved task resumes through CDF; CDTask has no resume entry point and the document alone grants no execution authority.

Before CDF continues a saved task, CDF must:

1. read the task document;
2. validate `cdf-cdtask/v1` and the required saved-document structure;
3. validate the canonical `cdf-scope/v1` block and Approval Record;
4. compare the recorded workspace, branch, commit, relevant worktree state, and repository evidence with the current repository;
5. re-check assumptions and stop conditions;
6. confirm the tasks still match the current code and approved Development Plan;
7. determine whether material drift has invalidated the risk classification, Scope Lock, acceptance criteria, phase boundary, or approval;
8. confirm the current CDF action is explicitly authorized before any implementation.

Material drift, a failed assumption, an active stop condition, changed task meaning, or invalid approval returns to CDF planning and renewed approval. Never execute an old task blindly.

## References

- [Task Templates](references/task-templates.md) — read before dependency analysis and task compilation.
- [Persistence](references/persistence.md) — read before choosing a destination or writing a task document.

## Non-Negotiable Rules

- Accept only `cdf-cdtask/v1` with `Handoff-Type: approved-tasking` and `Approval-State: approved` from CDF.
- Preserve the canonical `cdf-scope/v1` block byte for byte.
- Do not accept or transform raw requirements or alternate handoff formats.
- Do not plan, classify risk, approve, implement, execute, schedule, monitor, or review implementation.
- Do not create tasks for unapproved work or silently change acceptance criteria.
- Send semantic blockers back to CDF planning for renewed approval.
- Persist, read back, return the verified path to CDF, and stop.
