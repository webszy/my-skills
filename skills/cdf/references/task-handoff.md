# Internal Task Handoff

Read this reference only when CDF is about to **Save as Task** or resume a task previously saved by CDF. The component that compiles and persists tasks is internal to CDF; its detailed compilation rules live in [CDTask Component](../components/cdtask/COMPONENT.md).

`cdf-cdtask/v1` is the sole tasking contract. It is an internal handoff format, not a public runtime protocol or a user-facing entry point.

## Entry boundary

CDF may create the handoff only after all of the following are true:

1. requirement meaning is sufficiently clear;
2. relevant repository evidence has been inspected;
3. risk has been classified from impact, blast radius, reversibility, uncertainty, sensitivity, and coordination needs;
4. the Development Plan and canonical `cdf-scope/v1` Scope Lock are complete;
5. a valid Approval Record identifies the approved scope or approved subset;
6. the user explicitly selected **Save as Task**.

Raw requirements, PRDs, unapproved plans, ambiguous acknowledgements, and manual task requests are not valid inputs. Route them through the normal CDF requirement, evidence, planning, and approval stages first.

## Handoff header

Use exactly this contract identity and lifecycle state:

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

`Unavailable` is an explicit evidence state, not a guessed value. Record the reason when missing workspace metadata affects persistence or later drift checks.

CDF may also supply naming and destination metadata:

```text
Task-Title: <short approved title>
Requested-Task-Path: <absolute path or Workspace-relative path>
```

Both fields are optional and cannot change approved task meaning. Without `Requested-Task-Path`, use the default `_cdtask` destination. Without `Task-Title`, derive the slug mechanically from the first approved `in_scope` item, falling back to `task` when it has no filesystem-safe characters.

## Required payload

Carry these sections in the handoff:

1. Requirement Understanding;
2. Evidence Summary and material evidence gaps, if any;
3. Development Plan;
4. canonical Scope Lock;
5. Approval Record;
6. Acceptance Criteria;
7. Verification Strategy;
8. Risks;
9. Rollback Plan when required by the risk or change type;
10. Approved Phase Boundary when approval covers one phase or subset.

The canonical Scope Lock uses this schema:

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

Every field must exist. Empty arrays are valid. Do not manufacture assumptions, non-goals, or stop conditions just to populate a field.

Treat the canonical Scope Lock as immutable data. Preserve its canonical block verbatim. The internal compiler must not paraphrase, rewrite, expand, weaken, reorder, normalize away distinctions, or silently add scope. Task-level scope may quote or map to canonical entries, but it cannot replace them.

## Handoff validation

Before compilation, verify:

- the contract version, handoff type, and approval state are exact;
- the risk level is supported and matches the approved plan;
- the Approval Record identifies the approver statement, approved boundary, timestamp or session context, approval type, and **Save as Task** action;
- the canonical Scope Lock has all eight fields and is internally consistent;
- plan steps and acceptance criteria fit inside the Scope Lock;
- any partial approval contains only the approved subset and keeps the remainder excluded;
- the handoff contains enough repository traceability to perform a later drift check;
- rollback and phase boundaries are present when applicable.

Task compilation must become `BLOCKED` if safe decomposition would require:

- a new module, interface, behavior, dependency, or affected area;
- broader write scope or changed protected areas;
- changed acceptance criteria or verification obligations;
- a new architecture or technical decision not contained in the approved plan;
- resolution of a material planning ambiguity;
- inclusion of an unapproved partial-approval remainder;
- modification of the canonical Scope Lock.

On `BLOCKED`, return the reason and evidence to CDF planning. CDF must reinspect as needed, revise the Development Plan and Scope Lock, and request renewed approval. The compiler must not resolve the defect by expanding or rewriting scope.

## Persistence invariant

The default task path remains:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<slug>.md
```

The persisted document must retain `cdf-cdtask/v1`, source traceability, the canonical Scope Lock verbatim, Approval Record, dependency-aware task definitions, Scope Guard, verification and rollback obligations, and resume rules. It must also store SHA-256 digests of the exact canonical Scope Lock and Approval Record bytes. After writing, read the document back, recompute both digests, and verify every invariant before reporting success. If save or read-back verification fails, do not report the task as ready.

Task readiness is not execution and does not expand the approved boundary.

## Resume entry

Resume through CDF, for example:

```text
$cdf continue task <path>
```

or an equivalent natural-language request. There is no separate user-facing task compiler command.

Before continuing:

1. read the persisted task from the requested path;
2. validate `cdf-cdtask/v1` and required sections;
3. validate the canonical `cdf-scope/v1` block and Approval Record by recomputing and matching their persisted SHA-256 digests;
4. compare the recorded workspace, branch, commit, relevant worktree state, evidence, assumptions, stop conditions, planned write scope, shared contracts, and target code with current repository state;
5. determine whether drift is material to plan correctness, risk, scope, acceptance, verification, or rollback;
6. confirm that the current user request authorizes continuation and that approval remains applicable.

A saved task proves what scope was approved when it was created; it is not perpetual permission to execute regardless of current intent or repository state. An explicit continue request initiates resume validation. Code changes may begin only after the checks above pass.

## Drift rules

Treat branch or commit mismatch as a drift signal, not automatic proof of material drift. Inspect the relevant delta.

Drift is **material** when it can change any of:

- requirement meaning or an approved assumption;
- target existence, file ownership, interfaces, or dependencies;
- impact, blast radius, sensitivity, reversibility, or risk level;
- canonical scope or protected areas;
- acceptance criteria, verification feasibility, or rollback safety;
- task dependency order or the ability to keep a partial approval isolated.

For material drift:

```text
Stop
-> return to CDF planning
-> update evidence and risk
-> revise the Development Plan and Scope Lock where needed
-> obtain renewed approval
-> regenerate or update the task through cdf-cdtask/v1
```

For demonstrably non-material drift, record what changed, why it does not affect the approved boundary, and which checks support that conclusion. Then continue within the existing canonical Scope Lock.

Do not bypass drift validation because the task is recent, the diff is small, or the saved task is marked ready.
