---

name: cdtask
description: Use this skill when the user wants to split an existing requirement document, PRD, technical proposal, or implementation plan into a scoped, reviewable task breakdown for Codex or another coding agent. This skill focuses on scope locking, non-goal protection, dependency-ordered tasks, acceptance criteria, Codex handoff rules, and a final reviewer pass. It does not create a full spec system, does not implement code, and does not execute Codex.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Scope Locked Task Breakdown

## Purpose

This skill converts an existing requirement document, PRD, technical proposal, or implementation plan into a scoped task breakdown for a coding agent.

The goal is not just to create a task list.

The goal is to create a handoff-ready task section that:

* preserves the confirmed requirement boundary,
* prevents scope creep,
* protects explicit non-goals,
* splits work into dependency-ordered tasks,
* gives every task clear acceptance criteria,
* states what must not change,
* gives Codex or another coding agent strict handoff rules,
* performs a final reviewer pass before declaring the document ready.

This skill does not implement code.

This skill does not invoke Codex.

This skill does not create a full lightweight spec system.

This skill only prepares the task breakdown and handoff sections that can be appended to an existing requirement document.

---

# Core Principle

A task breakdown is valid only if it is constrained by the requirement boundary.

The assistant must not expand the requirement, add new architecture, add extra features, or convert future notes into current implementation tasks unless the user explicitly includes them in the current scope.

When in doubt, preserve the smaller scope.

The output is not complete until the Final Review Gate passes.

---

# Responsibility Boundary

This skill may:

* review an existing requirement document,
* extract in-scope and out-of-scope boundaries,
* identify non-goals,
* split the requirement into implementation tasks,
* order tasks by dependency,
* define task-level acceptance criteria,
* define task-level verification steps,
* append a scope guard checklist,
* append Codex handoff rules,
* perform a final review for ambiguity, conflict, and scope creep.

This skill must not:

* implement code,
* modify project files,
* invoke Codex,
* claim Codex has executed anything,
* rewrite the whole requirement unless the user explicitly asks,
* invent missing architecture,
* silently resolve major ambiguity,
* include non-goals as current tasks,
* mark a document as ready when unresolved ambiguity or conflict remains.

---

# When To Use This Skill

Use this skill when the user asks for any of the following:

* split this requirement into tasks,
* break this PRD into implementation tasks,
* create a task list for Codex,
* append tasks to this requirement document,
* prepare this document for Codex,
* create a scoped execution plan,
* convert this clarified requirement into actionable tasks,
* prevent Codex from over-implementing,
* add Codex handoff rules,
* review whether this task breakdown is ready for handoff.

Also use this skill when the user has a technical requirement and wants to hand it off to Codex, Claude Code, Cursor, or another coding agent.

---

# Do Not Use This Skill For

Do not use this skill when the user is still brainstorming and has not provided a reasonably stable requirement.

Do not use this skill to directly write or modify code.

Do not use this skill to create a full product roadmap.

Do not use this skill to design a full spec management system.

Do not use this skill to expand a requirement into future phases unless the user explicitly asks for future-phase planning.

---

# Required Workflow

Follow this workflow strictly:

```text
Requirement Readiness Check
  -> Scope Lock
  -> Dependency Analysis
  -> Task Breakdown
  -> Scope Guard Checklist
  -> Codex Handoff Rules
  -> Final Review Gate
```

The Final Review Gate is mandatory.

Do not skip it.

The task breakdown is complete only if the Final Review Gate passes.

---

# Phase 1: Requirement Readiness Check

Before task breakdown, check whether the existing requirement is ready to be split into tasks.

Evaluate the requirement against these questions:

1. Is the implementation goal clear?
2. Is the current version scope clear?
3. Are non-goals or exclusions clear?
4. Are affected modules, APIs, tables, files, user flows, or data flows identified?
5. Are success paths described?
6. Are failure paths described?
7. Are data model changes clear?
8. Are migration requirements clear?
9. Are compatibility requirements clear?
10. Are acceptance criteria clear?
11. Are testing or verification expectations clear?
12. Is it clear whether backend, frontend, shared schema, OpenAPI, client code, tests, or migrations are in scope?
13. Is it clear what must not be changed?
14. Is there enough information for Codex to implement without inventing decisions?

If the requirement is ready, continue to Scope Lock.

If the requirement is partially ready but the missing information is minor, make conservative assumptions and label them.

If the requirement has blocking ambiguity, stop and ask for confirmation before producing the final task breakdown.

Use this format when the requirement is not ready:

```markdown
# Requirement Readiness Check

## Ready To Split?
No / Partially

## Clear Points
- ...

## Blocking Ambiguities
- ...

## Required User Confirmations
1. ...
2. ...

## Why This Cannot Be Finalized Yet
- ...

## Suggested Next Step
Please confirm the points above, then I can produce the scoped task breakdown.
```

Do not produce a final task breakdown when blocking ambiguity remains.

---

# Phase 2: Scope Lock

Before producing tasks, extract and restate the implementation boundary.

Always include:

```markdown
## Scope Lock

### In Scope
- ...

### Out Of Scope
- ...

### Non-Goals That Must Not Be Implemented
- ...

### Assumptions
- ...

### Stop Conditions
- ...
```

## Scope Lock Rules

1. Anything listed as a non-goal must not appear as a current implementation task.
2. Future work may be documented only under "Future / Not In This Version".
3. Do not turn future sorting rules, dashboards, frontend display, provider-level stats, daily aggregation, or architecture improvements into current tasks unless explicitly requested.
4. If the user says "第一版", "暂时不做", "不要扩大", "只做写入", "先不做展示", or similar phrases, treat those as hard boundaries.
5. If the requirement says not to modify a module, do not include that module in "Files Likely Touched".
6. If the requirement says not to add a table, do not propose a table.
7. If the requirement says not to add a service method, do not propose a service method.
8. If the requirement says not to modify sorting, do not include sorting implementation as a current task.
9. If the requirement says sorting should only be documented for future work, include it only as documentation or future-note content.
10. If the requirement says only backend write logic is in scope, do not include frontend, shared schema, OpenAPI, or display tasks.

---

# Phase 3: Dependency Analysis

Before listing tasks, identify the implementation order.

Use this format:

````markdown
## Dependency Order

```text
Task 1 -> Task 2 -> Task 3 -> Task 4
````

### Dependency Notes

* Task 2 depends on Task 1 because ...
* Task 4 must happen after Task 3 because ...

````

Rules:

1. Database migration should usually come before code that depends on new fields.
2. Resolver or helper return-shape changes should come before route integration.
3. Shared helpers should come before endpoint-specific use.
4. Endpoint integrations should be separated when they have different behavior.
5. Tests or verification should come after implementation tasks.
6. Documentation-only future rules should not become implementation dependencies.

---

# Phase 4: Task Breakdown

Break the requirement into small, dependency-ordered tasks.

Tasks must be implementation-sized and reviewable.

Use this exact template for each task unless the user requests another format:

```markdown
## Task N: <Task Name>

### Goal
Describe the specific outcome of this task.

### Dependency
- Depends on: Task X / None

### Files Likely Touched
- `path/to/file`

### Implementation Notes
- Concrete implementation constraints.
- Important order of operations.
- Known edge cases.

### Acceptance Criteria
- [ ] Observable condition 1.
- [ ] Observable condition 2.
- [ ] Existing behavior remains unchanged.

### Must Not Change
- [ ] Do not change unrelated behavior.
- [ ] Do not implement excluded scope.
- [ ] Do not modify unrelated files.

### Verification
- Manual verification or test case.
````

## Task Design Rules

1. Do not combine unrelated work into one task.
2. Separate database migration from business logic.
3. Separate resolver or shared helper changes from route integration.
4. Separate each affected API route when possible.
5. Separate tests from implementation when the implementation is non-trivial.
6. Each task must have clear acceptance criteria.
7. Each task must state what must not change.
8. The task order must respect dependencies.
9. If a task depends on another task, state the dependency.
10. Avoid vague tasks such as "implement feature" or "update logic".
11. Avoid tasks that require Codex to infer hidden decisions.
12. Do not include future work in current tasks.
13. Do not include optional improvements unless the user explicitly requests them.
14. Do not include broad refactors unless the requirement is explicitly a refactor.
15. Do not include "cleanup unrelated code" as a task.
16. Do not add frontend, schema, OpenAPI, or generated-file tasks unless the requirement explicitly includes them.
17. Do not add extra tests beyond the requested scope if the user explicitly says only manual verification is required.
18. Do not omit verification for high-risk changes.

---

# Phase 5: Scope Guard Checklist

After the task list, output a scope guard checklist.

Use this format:

```markdown
# Scope Guard Checklist

- [ ] Does not implement any non-goal.
- [ ] Does not modify unrelated modules.
- [ ] Does not add unrequested tables or services.
- [ ] Does not add unrequested queues, cron jobs, workers, or background processing.
- [ ] Does not change frontend unless explicitly in scope.
- [ ] Does not change API response structures unless explicitly in scope.
- [ ] Does not change generated OpenAPI files unless explicitly in scope.
- [ ] Does not alter existing sorting behavior unless explicitly in scope.
- [ ] Does not add provider/platform/date dimensions unless explicitly in scope.
- [ ] Preserves existing behavior for requests that are outside the new feature path.
- [ ] Keeps future work separate from current implementation tasks.
```

Customize the checklist based on the requirement.

If the requirement contains explicit non-goals, include each non-goal in the checklist.

---

# Phase 6: Codex Handoff Rules

Append a handoff protocol when the user intends to give the document to Codex or another coding agent.

This section is not an instruction for the assistant to execute code.

This section is only text that will be appended to the requirement document.

Use the heading:

```markdown
# Codex Handoff Rules
```

Do not call it "Codex Execution Result".

Do not imply that Codex has already executed anything.

Use this format:

```markdown
# Codex Handoff Rules

1. Execute tasks strictly in the order listed.
2. Only implement the content explicitly listed in the task breakdown.
3. Do not implement anything from the non-goals section.
4. Do not expand the scope, redesign architecture, or perform unrelated cleanup.
5. Do not modify unrelated files.
6. If current code conflicts with the requirement document, stop and report the conflict before inventing a solution.
7. After each task, self-check against that task's acceptance criteria.
8. After all tasks, output:
   - changed files,
   - completed tasks,
   - skipped tasks, if any,
   - tests or verification performed,
   - any behavior intentionally not changed,
   - any remaining risks.
```

Add project-specific prohibitions when relevant.

Examples:

* Do not modify `apps/web`.
* Do not modify `packages/shared`.
* Do not regenerate OpenAPI.
* Do not add a new statistics table.
* Do not add service-layer abstractions.
* Do not change existing list sorting logic.
* Do not modify frontend display.
* Do not modify API response structure.
* Do not add provider/platform/date dimensions.
* Do not perform unrelated refactors.

---

# Phase 7: Final Review Gate

After appending the task breakdown, scope guard checklist, and Codex handoff rules, review the entire resulting document again from a reviewer perspective.

This review is mandatory.

The assistant must check whether the final document contains:

1. unclear requirements,
2. hidden assumptions,
3. conflicting instructions,
4. missing acceptance criteria,
5. vague task boundaries,
6. task items that violate non-goals,
7. future work accidentally included as current work,
8. implementation steps that exceed the confirmed scope,
9. missing failure-path decisions,
10. missing verification or testing requirements,
11. inconsistent terminology,
12. ambiguity about affected files or modules,
13. ambiguity about whether frontend, backend, schema, OpenAPI, migration, or tests are in scope,
14. contradiction between "Non-Goals" and "Task Breakdown",
15. contradiction between "Scope Lock" and "Codex Handoff Rules",
16. contradiction between "first version" constraints and proposed tasks,
17. missing stop conditions for Codex,
18. missing rules for handling code/document conflicts.

Use this format:

```markdown
# Final Review Gate

## Review Verdict
Ready / Not Ready / Needs User Confirmation

## Reviewer Findings

### Confirmed Clear
- ...

### Potential Ambiguities
- ...

### Potential Conflicts
- ...

### Scope Creep Risks
- ...

### Missing Decisions
- ...

## Required User Confirmations
1. ...
2. ...

## Final Status
Ready to hand off to Codex / Not ready yet
```

---

# Final Review Rules

## If the document is clear

If no meaningful ambiguity, conflict, or missing decision remains, mark the document as ready:

```markdown
## Final Status

Ready to hand off to Codex.
```

Also include:

```markdown
No blocking ambiguity found.
No scope conflict found.
No non-goal violation found.
```

## If the document has ambiguity

If there are unresolved ambiguities, do not mark it as ready.

Ask the user to confirm the missing decisions.

Use direct questions.

Example:

```markdown
## Final Status

Not ready yet. User confirmation required before this document can be handed to Codex.

## Required User Confirmations

1. Should `success_count` write failure preserve the original success response?
2. Should this version modify backend tests, or only provide manual verification steps?
```

## If the document has conflicts

If the requirement contradicts itself, stop and report the conflict.

Do not silently choose one side.

Example:

```markdown
## Potential Conflicts

- The document says "do not modify OpenAPI", but Task 5 says "regenerate OpenAPI".
- The document says "first version only writes counters", but Task 4 includes backend list display changes.

## Final Status

Not ready yet. These conflicts must be resolved before handoff.
```

## If a task violates a non-goal

Remove or revise that task before marking the document ready.

Example:

```markdown
Non-goal violation found:
- Non-goal says "do not add a statistics table".
- Task 2 proposes `asset_binding_usage_stats`.

Resolution:
- Remove this task from the current version.
- Move it to "Future / Not In This Version" only if helpful.
```

---

# Completion Definition

This skill is complete only when one of the following outcomes is reached.

## Outcome A: Ready

The final task breakdown contains:

* scope lock,
* non-goals,
* dependency order,
* task breakdown,
* scope guard checklist,
* Codex handoff rules,
* final review result,
* no unresolved ambiguity,
* no unresolved conflict,
* no non-goal violation.

The assistant may say:

```text
This task breakdown is ready to hand off to Codex.
```

## Outcome B: Not Ready

The document still contains unresolved ambiguity, conflict, or missing decisions.

The assistant must not claim the document is complete.

The assistant must ask the user for confirmation.

The assistant may say:

```text
This task breakdown is not ready to hand off yet. The following points need confirmation first.
```

---

# Output Modes

Choose one of the following output modes based on the user's request.

---

## Mode A: Review Only

Use when the user asks whether the requirement can be split into tasks.

Output:

```markdown
# Requirement Task Readiness Review

## Verdict
Ready / Not Ready / Partially Ready

## Key Strengths
- ...

## Blocking Ambiguities
- ...

## Recommended Decisions Before Tasking
- ...

## Suggested Task Groups
- ...

## Next Step
- ...
```

Do not output a full task list unless the user asks.

---

## Mode B: Task Breakdown Only

Use when the user has a clear requirement and asks to split it into tasks.

Output:

```markdown
# Task Breakdown

## Scope Lock
...

## Dependency Order
...

## Tasks
...

# Scope Guard Checklist
...

# Codex Handoff Rules
...

# Final Review Gate
...
```

Do not rewrite the full requirement document.

---

## Mode C: Append-To-Document Version

Use when the user asks to append tasks to an existing requirement document.

Output only the sections that should be appended:

```markdown
---

# Task Breakdown

...

---

# Scope Guard Checklist

...

---

# Codex Handoff Rules

...

---

# Final Review Gate

...
```

Do not repeat the entire original document unless the user explicitly requests the full merged version.

---

## Mode D: Full Merged Requirement + Tasks

Use when the user explicitly asks for the full modified original document.

Output the complete requirement document with the task breakdown, scope guard checklist, Codex handoff rules, and Final Review Gate appended.

---

## Mode E: Not Ready, Clarification Needed

Use when the requirement is not ready for task breakdown.

Output:

```markdown
# Requirement Readiness Check

## Ready To Split?
No / Partially

## Clear Points
- ...

## Blocking Ambiguities
- ...

## Required User Confirmations
1. ...
2. ...

## Why This Cannot Be Finalized Yet
- ...

## Suggested Next Step
Please confirm the points above, then I can produce the scoped task breakdown.
```

Do not produce a final task breakdown in this mode.

---

# Task Quality Standards

A good task is:

* small enough to review,
* tied to a clear requirement,
* dependency-aware,
* limited in scope,
* testable,
* reversible where possible,
* explicit about what not to change,
* explicit about verification,
* clear enough for a coding agent to execute without inventing decisions.

A bad task is:

* vague,
* too broad,
* mixes database, API, frontend, and tests into one step,
* includes future work,
* silently expands scope,
* lacks acceptance criteria,
* lacks verification instructions,
* ignores non-goals,
* changes unrelated modules,
* requires hidden assumptions.

---

# Common Anti-Patterns To Prevent

Reject or revise task lists that include these problems:

1. Implementing future enhancements as current tasks.
2. Adding new tables when the requirement says not to.
3. Updating frontend when the first version is backend-only.
4. Regenerating OpenAPI when the response contract is unchanged.
5. Refactoring unrelated files.
6. Adding service methods when the requirement says local helper only.
7. Changing sorting logic when the requirement only asks to document future sorting.
8. Treating global resource data as app-specific behavior.
9. Counting by the wrong identifier.
10. Using JavaScript read-modify-write for counters that require atomic database updates.
11. Turning optional notes into mandatory implementation tasks.
12. Ignoring failure-path requirements.
13. Removing existing behavior that the requirement says should remain unchanged.
14. Expanding one endpoint change into broader API redesign.
15. Introducing background jobs when the requirement asks for synchronous write.
16. Introducing new schema layers when the requirement says first version only.
17. Modifying frontend types when backend response is unchanged.
18. Updating generated files without explicit scope.
19. Making assumptions about business logic without marking them.
20. Marking a document ready before final review.

---

# Requirement Review Checklist

Use this checklist during the Requirement Readiness Check and Final Review Gate.

```markdown
## Requirement Review Checklist

### Goal
- [ ] The implementation goal is explicit.
- [ ] The current version boundary is explicit.

### Scope
- [ ] In-scope items are explicit.
- [ ] Out-of-scope items are explicit.
- [ ] Non-goals are explicit.
- [ ] Future work is separated from current work.

### Data / Model
- [ ] Data model changes are explicit.
- [ ] Migration requirements are explicit.
- [ ] Backfill requirements are explicit or explicitly not required.
- [ ] Identifier and counting dimensions are clear.

### Behavior
- [ ] Success path is clear.
- [ ] Failure path is clear.
- [ ] No-op path is clear.
- [ ] Existing behavior preservation is clear.

### Affected Areas
- [ ] Backend scope is clear.
- [ ] Frontend scope is clear.
- [ ] Shared schema scope is clear.
- [ ] OpenAPI/generated file scope is clear.
- [ ] Client scope is clear.
- [ ] Test scope is clear.

### Handoff
- [ ] Tasks are ordered by dependency.
- [ ] Each task has acceptance criteria.
- [ ] Each task has verification.
- [ ] Each task has "Must Not Change".
- [ ] Codex handoff rules are included.
- [ ] Final Review Gate passes.
```

---

# Handoff Document Structure

When producing appendable handoff sections, prefer this final structure:

```markdown
---

# Task Breakdown

## Scope Lock
...

## Dependency Order
...

## Tasks
...

---

# Scope Guard Checklist
...

---

# Codex Handoff Rules
...

---

# Final Review Gate
...
```

If the user asks to append to an existing document, output only the appended sections unless the user explicitly requests the full merged document.

---

# Final Response Rules

When using this skill:

1. Do not implement code.
2. Do not invoke Codex.
3. Do not claim Codex executed anything.
4. Do not claim the handoff task breakdown is ready until the Final Review Gate passes.
5. Always review the final appended sections as a reviewer.
6. If ambiguity exists, ask the user to confirm.
7. If conflict exists, stop and report it.
8. If a task violates a non-goal, revise the task list before finalizing.
9. If the task breakdown is ready, explicitly say it is ready to hand off.
10. If the task breakdown is not ready, explicitly say it is not ready and list required confirmations.
11. Keep future work separate from current tasks.
12. Make scope boundaries visible.
13. Prefer strictness over enthusiasm.
14. Prefer a smaller, safer task list over a broad, impressive one.
15. End with the current status:

    * Ready to hand off to Codex.
    * Not ready yet; user confirmation required.
