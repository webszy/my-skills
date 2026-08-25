# CDTask: Internal Post-Approval Task Compiler

CDTask is an internal instruction component of CDF. CDF loads it only after CDF has completed requirement analysis, repository-evidence inspection, risk classification, development planning, Scope Lock, human approval, and an explicit **Save as Task** decision.

CDTask has no direct invocation, installation, or public input surface. It compiles an approved CDF package into dependency-aware task definitions, persists the result, verifies the saved document, returns its path to CDF, and stops. It accepts the latest traceability metadata produced by CDF's pre-save drift preflight; it does not repeat repository planning or decide whether drift is material.

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

Task-definition validation is not implementation review. The saved Approval Record proves the approved scope and authorization to persist it. Neither that record nor the saved task is future execution authorization.

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
Source-Worktree-Changes: <[] | [Unavailable] | [' M src/foo.ts', '?? src/new-file.ts']>
Save-Drift-Preflight: <matched | non-material-drift>
Save-Drift-Notes: <none | concise evidence-backed explanation>
```

`Source-Worktree-Changes` is one flow-style YAML array and a stable, path-scoped projection of relevant `git status --short` entries. Use `[]` when there are no relevant changes, including a clean worktree. Quote every dirty entry, preserving both `XY` status characters including a leading space. Use `[Unavailable]` only when the status evidence cannot be obtained. Preserve repository-relative paths and sort entries deterministically by path, then status. Do not dump unrelated dirty paths from a large repository. A dirty worktree is a drift signal, not proof of material drift.

CDF may additionally provide persistence metadata:

```text
Task-Title: <short approved title>
Requested-Task-Path: <absolute path or Workspace-relative path>
```

Both fields are optional. They are routing and naming metadata only and cannot change approved task meaning. If `Task-Title` is absent, derive a filesystem-safe slug mechanically from the first approved `in_scope` entry; if it has no usable characters, use `task`. If `Requested-Task-Path` is absent, use the default destination under `Workspace`.

The handoff must also contain:

- the approved Development Plan copied verbatim, without splitting, renaming, or regenerating its sections;
- one canonical `cdf-scope/v1` Scope Lock inside that plan's `### Scope Lock` section;
- the immutable Approval Record covering that plan and Scope Lock and selecting **Save as Task**;
- Approved Phase Boundary when applicable;
- Partial Approval Result in the stable format below when approval covers only a safely separable subset;
- enough approved repository evidence or affected-area detail in the plan to create concrete write scopes without guessing.

The approved Development Plan carries these headings in this order:

```markdown
## Development Plan

### Requirement Understanding
### Evidence Summary
### Risk Gate Result
### Scope Lock
### Technical Approach
### Implementation Plan
### Risks
### Rollback Plan
### Acceptance Criteria
### Verification Strategy
### Next Action
```

Carry the content under every heading verbatim. Do not create parallel `Evidence`, `Risks and Rollback`, Acceptance Criteria, Verification Strategy, or other planning sections during handoff. For Level S or M, `### Rollback Plan` may be a concise reversible action or `None` when rollback is genuinely not applicable; do not manufacture filler.

`Risk-Level` is inherited metadata. CDTask must not reinterpret or recalculate it.

Reject every other input route. Do not translate an unsupported input into this contract, ask the user planning questions, or construct missing approval evidence. Return the defect to CDF.

## Input Validation

Before decomposition, verify all of the following:

1. The contract version, handoff type, approval state, and risk value exactly match the supported values.
2. Workspace, branch, commit, worktree state, a legal `Source-Worktree-Changes` array, `Save-Drift-Preflight`, and `Save-Drift-Notes` are present, using `Unavailable` only where the contract permits it. Require `matched` with `none`, or `non-material-drift` with concise supporting notes. Treat them as the latest metadata from CDF's pre-save drift preflight; do not perform a second repository-planning pass.
3. The Approval Record unambiguously binds the approved Development Plan and canonical Scope Lock and records **Save as Task** as the approved next action.
4. The Development Plan has the canonical headings in the required order and has not been split, renamed, or regenerated.
5. Canonical `in_scope` and `acceptance_criteria` are both non-empty, and the plan's `### Acceptance Criteria` is an item-for-item, same-order, verbatim projection of canonical `cdf-scope/v1.acceptance_criteria`.
6. The package has no contradiction among the Development Plan, Scope Lock, phase boundary, Approval Record, and partial-approval material.
7. The approved evidence is sufficient to define tasks and write scopes without inventing paths, interfaces, modules, dependencies, or behavior.

Missing or contradictory authority is `BLOCKED`; it is never an invitation for CDTask to complete the planning package.

CDF owns the pre-save drift preflight. Immediately before constructing this handoff, CDF re-checks workspace, branch, commit, and relevant dirty worktree evidence against the approved planning evidence. Material drift returns to CDF planning before CDTask is entered. Demonstrably non-material drift is recorded in the latest handoff metadata. CDTask validates and persists that metadata; it does not inspect the repository to reinterpret the requirement, risk, plan, or drift result.

## Canonical Scope and Acceptance Authority

The approved Development Plan must contain exactly one canonical block, in `### Scope Lock`, beginning with:

```yaml
Scope-Lock-Version: cdf-scope/v1
in_scope:
  - <approved outcome or impact>
out_of_scope: []
non_goals: []
assumptions: []
stop_conditions: []
will_change: []
will_not_change: []
acceptance_criteria:
  - <observable result>
```

All eight fields must exist and must be arrays. `in_scope` and `acceptance_criteria` must each contain at least one non-empty entry; the other arrays may be empty. Do not invent filler prose. A partial or conditional result with no approved `in_scope` item is `BLOCKED`. This is the only canonical scope block in the handoff and saved task; do not copy it into a second scope section.

Treat the complete canonical block as an immutable opaque payload. Copy it verbatim. Do not paraphrase, rewrite, expand, weaken, normalize, re-indent, reorder, re-wrap, merge, omit, or reserialize it. Readable mappings elsewhere in the task document are secondary and must not conflict with the canonical block.

`cdf-scope/v1.acceptance_criteria` is the sole canonical acceptance source. The Development Plan's `### Acceptance Criteria` section must project every canonical entry once, in the same order and with exactly the same wording. It may not add, delete, weaken, broaden, reinterpret, merge, or split an entry. Task-level Acceptance Criteria may select only the entries applicable to that task, keep their canonical order, and quote them verbatim. If any task needs a criterion that does not already exist in the canonical array, return `BLOCKED` with `acceptance-change`; CDF must produce refreshed planning and obtain renewed approval.

## Integrity Verification

Apply [Integrity Verification](../../SKILL.md#integrity-verification) at handoff validation, save, read-back, and resume. Text comparison is the authoritative check.

Before persistence, capture the received canonical payloads. After persistence, extract the saved payloads under the same boundaries and compare them with the received ones line for line. Any difference invalidates the saved task. A non-LF line ending, trailing whitespace on a payload line, a missing or ambiguous boundary, a reordered Scope Lock, or a duplicate canonical block is `BLOCKED`; CDTask must not repair the payload.

After the authoritative line-for-line comparison succeeds, compute a SHA-256 digest over each exact canonical payload and persist both as the durable resume baseline. Never write a digest that was not produced by an actual hashing command, and never treat a digest as a substitute for the pre-save text comparison. If either digest cannot be computed, return `BLOCKED` with `persistence-failure` rather than saving a document that cannot prove its later baseline.

## Approval and Partial Approval

Preserve the Approval Record verbatim. It is immutable historical evidence of the approved scope and the user's **Save as Task** persistence authorization. It does not authorize future code changes. Never edit it.

When approval is partial, require and preserve the projection defined in [Human Approval](../../SKILL.md#6-human-approval) exactly as received.

This result is audit information, not a second scope authority. It must not include another complete Scope Lock. Each Approved Items entry must correspond verbatim to an approved entry in canonical `in_scope`. Preserve each Unapproved Items entry verbatim and require it to remain protected by the canonical `out_of_scope`, `non_goals`, `will_not_change`, or another appropriate canonical exclusion. Create no task goal, positive scope, write operation, implementation obligation, acceptance mapping, or verification obligation for an unapproved item; carry it only as a protective prohibition or exclusion. If the approved and unapproved subsets cannot be separated without changing meaning, return `BLOCKED` with `partial-separation`; CDF must refresh the Development Plan and Scope Lock and obtain renewed approval.

## Compilation Workflow

```text
Validate Approved Handoff
        ↓
Freeze Approved Plan, Canonical Scope, and Approval Record
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
- task-level acceptance mappings that quote only applicable canonical `cdf-scope/v1.acceptance_criteria` entries verbatim and in canonical order, plus planned verification obligations;
- protected areas and exclusions carried into `Must Not Change`;
- assumptions and stop conditions visible to the future CDF execution flow.

Do not fabricate paths. If the approved package identifies only an area, keep the write scope at that supported level. Every task must map to at least one existing canonical acceptance criterion; do not create, delete, combine, split, or reinterpret criteria to make the mapping fit. If safe decomposition requires a new module, interface, dependency, behavior, affected area, acceptance criterion, or architecture decision, stop with `BLOCKED`.

`DRAFT` and `READY` are task-definition states only. They are not execution states.

### Scope Guard

After decomposition, complete the Scope Guard defined in [Task Templates](references/task-templates.md#scope-guard-output). Every item must be actually validated and checked before persistence.

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
| `acceptance-change` | compilation would add, remove, weaken, broaden, reinterpret, merge, or split canonical acceptance criteria | Return to CDF planning and obtain renewed approval |
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
Scope-Lock-Digest: <verified | not-verified>
Approval-Record-Digest: <verified | not-verified>
Document-Read-Back: <verified | not-verified>
Reason: <concise explanation | Not applicable>
```

`READY` requires an absolute saved path and all five read-back and digest fields set to `verified`. A result that has not been successfully persisted is not `READY`.

## Persistence

Persistence is mandatory for this component path because CDF enters it only for **Save as Task**. Use the destination and document contract in [Persistence](references/persistence.md).

The default destination remains:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md
```

Write only the task document and its required parent directory. Do not modify implementation files. Never silently overwrite an existing task document.

After saving, reopen the exact destination and verify the frontmatter, required sections, stable task IDs, dependency graph, Scope Guard, Compilation Gate, immutable Approval Record, sole canonical Scope Lock, acceptance projections, required payload digests, and traceability arrays. Compare both canonical payloads line for line and recompute both digests. Do not report success when read-back verification fails.

## Resume Semantics

Every saved task resumes through CDF; CDTask has no resume entry point and the document alone grants no execution authority. [Resume a Saved Task](../../SKILL.md#resume-a-saved-task), [Integrity Verification](../../SKILL.md#integrity-verification), and [Repository Drift](../../SKILL.md#repository-drift) are the sole authorities for later validation and authorization.

Only after those checks pass and the user explicitly requests continuation may CDF create the runtime-only Resume Authorization Record and enter [Execution Progress](../../references/execution-progress.md). Runtime status belongs only in the separate sidecar. Never append it to the saved task or modify the canonical Scope Lock or Approval Record. An inspect, review, summarize, or validate request authorizes no implementation or progress mutation.

## References

- [Task Templates](references/task-templates.md) — read before dependency analysis and task compilation.
- [Persistence](references/persistence.md) — read before choosing a destination or writing a task document.
- [Execution Progress](../../references/execution-progress.md) — owned by CDF after a later authorized resume, never by this compiler.

## Non-Negotiable Rules

- Accept only `cdf-cdtask/v1` with `Handoff-Type: approved-tasking` and `Approval-State: approved` from CDF.
- Preserve the canonical `cdf-scope/v1` block byte for byte.
- Treat `cdf-scope/v1.acceptance_criteria` as the only canonical acceptance source; projections and task mappings must be verbatim.
- Preserve the approved Development Plan headings and content without splitting or regeneration.
- Preserve the immutable Save Approval Record as historical scope and persistence authority, never as future execution authority.
- Do not accept or transform raw requirements or alternate handoff formats.
- Do not plan, classify risk, approve, implement, execute, schedule, monitor, or review implementation.
- Do not create tasks for unapproved work or silently change acceptance criteria.
- Send semantic blockers back to CDF planning for renewed approval.
- Persist, read back, return the verified path to CDF, and stop.
