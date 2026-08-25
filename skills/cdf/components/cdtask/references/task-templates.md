# Internal CDTask Task Templates

Read this reference before compiling dependency data or tasks. It defines the only task format emitted from an approved `cdf-cdtask/v1` handoff.

These are task-definition formats, not runtime state, scheduling data, implementation instructions beyond the approved plan, or execution authorization. The authority boundary, Scope Guard, and blocking rules remain in [COMPONENT.md](../COMPONENT.md).

## Approved Planning Inputs

Compile from the approved Development Plan exactly as received. It must retain these headings, in order, with no splitting, renaming, or regeneration:

```markdown
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

The plan's `### Scope Lock` contains the only canonical `cdf-scope/v1` block. Canonical `in_scope` and `acceptance_criteria` must each contain at least one non-empty entry. `cdf-scope/v1.acceptance_criteria` is the only canonical acceptance source. The plan's readable `### Acceptance Criteria` must repeat every canonical entry once, in the same order and verbatim. Do not compile from a plan whose projection adds, deletes, weakens, broadens, reinterprets, merges, or splits an entry.

When present, preserve the partial-approval projection defined in [Human Approval](../../../SKILL.md#6-human-approval) exactly, and do not treat it as a second scope authority.

Approved items must quote canonical `in_scope` entries. Unapproved items remain protective exclusions only and can never produce a task, positive write scope, acceptance mapping, or verification obligation. If the subsets cannot be separated safely, return `BLOCKED` with `partial-separation`.

## Dependency Graph

Use stable task IDs and a directed acyclic graph. List only dependency constraints supported by the approved Development Plan.

```markdown
## Dependency Graph
- TASK-001 -> TASK-003
- TASK-002 -> TASK-003

## Dependency Data
| Task ID | Depends On | Approved reason |
|---|---|---|
| TASK-001 | none | <reason derived from the approved plan> |
| TASK-002 | none | <reason derived from the approved plan> |
| TASK-003 | TASK-001, TASK-002 | <reason derived from the approved plan> |
```

For independent tasks, use `none` in `Depends On`; do not invent an edge to make the graph look sequential. Do not assign workers, choose parallel execution, add scheduling fields, or infer coordination policy.

Task IDs must be unique and stable within the saved document. Every dependency must resolve to a defined task. A task must not depend on itself, and the graph must be acyclic.

## Task Definition

Keep every field. Use `None` only when the approved package establishes that the field is not applicable; do not create filler content.

```markdown
## TASK-001: <Task Name>

### Goal
<one approved outcome>

### Dependencies
- <stable task ID or none>

### Approved Scope Mapping
- `in_scope`: <verbatim approved entry>
- `will_change`: <verbatim approved entry>

### Write Scope
- <approved path or affected area supported by repository evidence>

### Shared Contracts
- <approved interface, invariant, or none>

### Implementation Notes
- <direction already present in the approved Development Plan>

### Acceptance Criteria
- <applicable canonical cdf-scope/v1.acceptance_criteria entry, verbatim>

### Must Not Change
- <verbatim exclusion, non-goal, protected area, or approved invariant>

### Planned Verification
- <unperformed check mapped to the approved Verification Strategy>

### Assumptions and Stop Conditions
- <verbatim relevant assumption or stop condition, or none>

### Definition Status
READY
```

### Field Rules

- **Goal:** one outcome already approved by CDF. Do not combine unrelated outcomes.
- **Dependencies:** match the Dependency Data exactly.
- **Approved Scope Mapping:** quote the relevant canonical entries verbatim. Do not summarize or normalize them.
- **Write Scope:** use only paths or areas supported by approved evidence. Never fabricate a path to make the task look concrete.
- **Shared Contracts:** carry only contracts or invariants already present in the Development Plan or Scope Lock.
- **Implementation Notes:** decompose approved direction; do not select a new approach.
- **Acceptance Criteria:** select only applicable canonical `cdf-scope/v1.acceptance_criteria` entries, retain their canonical order, and copy them verbatim. Each task must map to at least one existing canonical entry. Do not add, delete, weaken, broaden, reinterpret, merge, or split criteria. Mechanical completion details belong in Planned Verification only when the approved strategy entails them. If a new criterion would be needed, return `BLOCKED` with `acceptance-change` so CDF can refresh planning and obtain renewed approval.
- **Must Not Change:** preserve relevant `out_of_scope`, `non_goals`, `will_not_change`, partial-approval exclusions, and protected behavior. An unapproved item may appear only here as a protective exclusion, never as positive work.
- **Planned Verification:** describe checks to be run later by an authorized CDF execution flow. Never mark them passed or performed.
- **Assumptions and Stop Conditions:** keep applicable canonical wording verbatim so a resumed CDF flow can revalidate it.
- **Definition Status:** use only `DRAFT` while compiling and `READY` after the Compilation Gate passes. Do not add runtime states to the immutable task definition. A later authorized CDF execution records `pending`, `in_progress`, `verified`, or `blocked` only in the separate [Execution Progress](../../../references/execution-progress.md) sidecar.

If a task cannot be completed using these fields without adding meaning, scope, architecture, risk judgement, or acceptance criteria, return `BLOCKED` under the applicable reason class. CDF must produce refreshed planning and obtain renewed approval before task compilation resumes.

## Scope Guard Output

Include the completed Scope Guard after all task definitions:

```markdown
## Scope Guard
- [x] Every task maps to approved `in_scope` or `will_change` content.
- [x] No task treats `out_of_scope`, `non_goals`, `will_not_change`, or an unapproved remainder as positive scope or work; those entries appear only as protective constraints.
- [x] The canonical Scope Lock is byte-for-byte unchanged.
- [x] The Development Plan is carried verbatim with its canonical headings and sole Scope Lock block.
- [x] The Development Plan Acceptance Criteria is an item-for-item, same-order, verbatim projection of canonical `cdf-scope/v1.acceptance_criteria`.
- [x] Canonical `in_scope` and `acceptance_criteria` are both non-empty.
- [x] Every task-level criterion is an applicable canonical entry quoted verbatim and in canonical order; no task requires a new criterion.
- [x] The immutable Approval Record, stable Partial Approval Result when applicable, and approved phase boundary are preserved without creating a second scope authority.
- [x] Dependencies and tasks introduce no product, technical, or architecture decision.
- [x] Planned verification maps to the approved Verification Strategy and is not reported as performed.
- [x] Assumptions, stop conditions, and protected areas are visible to a future CDF resume.
- [x] Source worktree state, the path-scoped stable changes array, and CDF's save-drift preflight result and notes are preserved; dirty state was not treated as automatically material.
- [x] No implementation, execution, scheduling, approval, risk classification, or implementation review occurred.
```

Do not check an item unless it was actually validated. Any unchecked item prevents persistence and is handled by the Compilation Gate.

## Future CDF Execution Constraints

Include these constraints in the saved document. They constrain a future CDF resume but do not authorize execution:

```markdown
## Future CDF Execution Constraints
- Resume only through CDF.
- Follow CDF's authoritative Integrity Verification, Resume a Saved Task, and Repository Drift rules.
- Treat the canonical Scope Lock, Approval Record, approved phase boundary, partial-approval exclusions, task Write Scope, and dependencies as immutable limits.
- Stop and return to CDF planning if current evidence requires new scope, a changed technical decision, changed acceptance criteria, or work from an unapproved remainder.
- After explicit current authorization, record runtime state only in the separate `cdf-execution-progress/v1` sidecar; never write it into this task.
- Skip only sidecar tasks whose `verified` evidence remains applicable. Inspect `in_progress` or `blocked` work before continuing it.
- Report only checks actually performed. An inspect, review, summarize, or validate request authorizes no code change or progress mutation.
```

After successful validation of an explicit continue request, CDF uses the runtime-only authorization format defined in [Resume a Saved Task](../../../SKILL.md#resume-a-saved-task), then follows [Execution Progress](../../../references/execution-progress.md). Neither action modifies the saved task or its Approval Record.
