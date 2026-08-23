# Internal CDTask Task Templates

Read this reference before compiling dependency data or tasks. It defines the only task format emitted from an approved `cdf-cdtask/v1` handoff.

These are task-definition formats, not runtime state, scheduling data, implementation instructions beyond the approved plan, or execution authorization. The authority boundary, Scope Guard, and blocking rules remain in [COMPONENT.md](../COMPONENT.md).

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
- <verbatim approved criterion mapped to this task>

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
- **Acceptance Criteria:** copy the applicable approved criteria verbatim. Do not add task-local product acceptance criteria. Mechanical completion details belong in Planned Verification only when the approved strategy entails them.
- **Must Not Change:** preserve relevant `out_of_scope`, `non_goals`, `will_not_change`, partial-approval exclusions, and protected behavior.
- **Planned Verification:** describe checks to be run later by an authorized CDF execution flow. Never mark them passed or performed.
- **Assumptions and Stop Conditions:** keep applicable canonical wording verbatim so a resumed CDF flow can revalidate it.
- **Definition Status:** use only `DRAFT` while compiling and `READY` after the Compilation Gate passes. Do not add assigned, running, retrying, completed, reviewed, or verified runtime states.

If a task cannot be completed using these fields without adding meaning, scope, architecture, risk judgement, or acceptance criteria, return `BLOCKED` under the applicable reason class.

## Scope Guard Output

Include the completed Scope Guard after all task definitions:

```markdown
## Scope Guard
- [x] Every task maps to approved `in_scope` or `will_change` content.
- [x] No task treats `out_of_scope`, `non_goals`, `will_not_change`, or an unapproved remainder as positive scope or work; those entries appear only as protective constraints.
- [x] The canonical Scope Lock is byte-for-byte unchanged.
- [x] The Approval Record and approved phase boundary are preserved.
- [x] Dependencies and tasks introduce no product, technical, or architecture decision.
- [x] Acceptance criteria are preserved and are not broadened, weakened, or replaced.
- [x] Planned verification maps to the approved Verification Strategy and is not reported as performed.
- [x] Assumptions, stop conditions, and protected areas are visible to a future CDF resume.
- [x] No implementation, execution, scheduling, approval, risk classification, or implementation review occurred.
```

Do not check an item unless it was actually validated. Any unchecked item prevents persistence and is handled by the Compilation Gate.

## Future CDF Execution Constraints

Include these constraints in the saved document. They constrain a future CDF resume but do not authorize execution:

```markdown
## Future CDF Execution Constraints
- Resume only through CDF.
- Treat the canonical Scope Lock, approved phase boundary, and partial-approval exclusions as hard limits.
- Work only within task Write Scope and approved dependencies.
- Re-check repository drift, assumptions, stop conditions, task applicability, and approval validity before implementation.
- Stop and return to CDF planning if implementation requires new scope, a changed technical decision, changed acceptance criteria, or work from an unapproved remainder.
- Report only verification checks actually performed during a separately authorized execution.
- Do not infer execution authorization from this task document or its `READY` definition state.
```
