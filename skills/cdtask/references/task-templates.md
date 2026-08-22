# CDTask Task Templates

Read this file before producing dependency data, task definitions, or handoff text. Use only the format that matches the input route selected in `../SKILL.md`.

These are output formats. The task rules, Scope Guard, status semantics, and Task Readiness Gate stay in `../SKILL.md`.

## Table of Contents
- Dependency Formats
- Task Breakdown Formats
- Handoff Formats

## Dependency Formats

Describe only dependency constraints. Do not schedule work, assign workers, choose parallel execution, or claim runtime coordination.

### Manual or CDP-Deferred Input

A linear order is acceptable only when dependencies are truly linear:

```markdown
## Dependency Order
1. <task or prerequisite>
2. <dependent task>

### Dependency Notes
- <why the dependency exists>
```

### CDF-Managed Input

Use stable IDs and a directed acyclic graph:

```markdown
## Dependency Graph
- TASK-001 -> TASK-003
- TASK-002 -> TASK-003

## Dependency Data
| Task ID | Depends On | Reason |
|---|---|---|
| TASK-001 | none | <reason> |
| TASK-002 | none | <reason> |
| TASK-003 | TASK-001, TASK-002 | <reason> |
```

## Task Breakdown Formats

Keep every field in the selected format. Do not add runtime fields.

### Manual or CDP-Deferred Input

```markdown
## Task N: <Task Name>

### Goal
<one outcome>

### Dependency
<task or prerequisite>

### Files Likely Touched
- <path or area>

### Implementation Notes
- <approved constraints and direction>

### Acceptance Criteria
- <observable result>

### Must Not Change
- <protected behavior or area>

### Verification
- <check>
```

### CDF-Managed Input

```markdown
## TASK-001: <Task Name>

### Goal
<one outcome>

### Dependencies
- <stable task ID or none>

### Scope
- <verbatim mapping to approved scope>

### Write Scope
- <allowed path or area>

### Shared Contracts
- <interface or invariant>

### Implementation Notes
- <approved constraints and direction>

### Acceptance Criteria
- <observable result>

### Must Not Change
- <protected behavior or area>

### Verification
- <check>

### Risk
<S|M|L|XL and task-specific note>

### Status
<DRAFT|READY>
```

## Handoff Formats

These sections are handoff text only. CDTask does not select, invoke, monitor, or review an executor.

### Manual or CDP-Deferred Output

Provide text rules for a future authorized coding agent:

```markdown
## Codex Handoff Rules
- Work only inside the canonical Scope Lock.
- Treat non-goals and Must Not Change as hard constraints.
- Respect dependencies and stop conditions.
- Stop and request replanning if scope must expand.
- Verify each task against its acceptance criteria.
- Do not infer execution authorization from task readiness.
```

### CDF-Managed Output

Provide an executor-neutral contract:

```markdown
## Execution Contract
- Lifecycle Owner: CDF
- Approval State: plan-approved
- Allowed Work: <verbatim approved scope mapping>
- Prohibited Work: <verbatim exclusions and non-goals>
- Stop Conditions: <verbatim stop conditions>
- Required Verification: <task verification obligations>
- Scope Expansion Path: return to CDP through CDF for replanning and approval
```
