# Internal CDTask v2 Task Templates

Load during compilation only. [Task Handoff](../../../references/task-handoff.md) owns approved planning/acceptance semantics; [Persistence](persistence.md) owns serialization/integrity. The validator's `--describe` output is the mechanical field-name inventory; these templates describe their meaning.

## Task Definitions

Under `## Task Definitions`, use one JSON fenced array of objects with every field below. Empty optional arrays mean genuinely inapplicable; never invent filler.

```json
[
  {
    "id": "TASK-001",
    "name": "Login API",
    "goal": "Deliver the approved login API",
    "depends_on": [],
    "scope_mapping": ["Approved login flow"],
    "write_scope": ["src/login-api.py"],
    "shared_contracts": ["Approved response contract"],
    "implementation_notes": ["Use the approved adapter"],
    "contributes_to": ["AC-001"],
    "task_verification": ["CHECK-API"],
    "must_not_change": ["Authentication mechanism"],
    "assumptions_and_stop_conditions": [],
    "definition_status": "READY"
  }
]
```

This illustrative object is not an approved task. Replace values only with content entailed by the actual approved plan.

- `id`: unique stable `TASK-` plus at least three digits. `name`/`goal`: one approved local deliverable.
- `depends_on`: existing task IDs, no duplicates, self edge or cycles. Start only after dependencies are locally verified.
- `scope_mapping`: verbatim `in_scope`/`will_change` entries, never exclusions. It is a projection, not write authorization.
- `write_scope`: concrete approved paths/areas grounded in inspected evidence; no fabricated paths. Semantic review checks containment and protected boundaries; string membership cannot prove that a path is safe.
- `shared_contracts`/`implementation_notes`: approved contracts and implementation direction only.
- `contributes_to`: nonempty canonical positional AC IDs in canonical order. Does not claim product acceptance passed.
- `task_verification`: nonempty IDs of `kind: task` checks in the approved Verification Strategy. Their descriptions define local verification; no full product AC must pass merely to unblock downstream tasks.
- `must_not_change`: carry all canonical exclusions (`out_of_scope`, `non_goals`, `will_not_change`), plus relevant approved invariants. Unapproved/deferred work can appear only as protection.
- `assumptions_and_stop_conditions`: preserve applicable canonical wording.
- `definition_status`: `READY` only after definition validation; never runtime state.

A compiler cannot add a new promise through verification. If a local check needs new behavior or a technical choice not entailed by the approved plan, return `BLOCKED: verification-change` to CDF planning.

## Dependency Graph

Under `## Dependency Graph`, use one JSON object mapping every task ID to its `depends_on` array exactly. This is a mechanically checked projection, not a second dependency authority. Task order is stable; topological execution comes from dependencies, not file order. No separate Dependency Data table is needed in v2.

```json
{"TASK-001": [], "TASK-002": ["TASK-001"]}
```

## Acceptance Mapping

Under `## Acceptance Mapping`, one JSON object maps **every** canonical positional AC ID to one or more approved `kind: product` check IDs:

```json
{"AC-001": ["CHECK-LOGIN-INTEGRATION"]}
```

Every AC must also occur in at least one task's `contributes_to`. Every approved local/product check must have a verification path. The full canonical array remains authoritative, even when two criteria happen to have identical wording. Never merge entries by text equality.

For login: TASK-001 passes CHECK-API locally; TASK-002 can then build the form and pass its local checks. Only CHECK-LOGIN-INTEGRATION provides the planned end-to-end product evidence for AC-001. Overall completion checks every AC, all required checks and final review.

## Scope Guard and future execution constraints

`## Scope Guard` holds a JSON object `{ "result": "checked", "evidence": "<retrievable compilation/scope review record>" }`. This is a recorded review, not proof that a semantic check actually occurred. Check plan/approval agreement, exact canonical text, positive/protected boundaries, partial/phase separation, full coverage, approved checks, dependency validity and source traceability before recording it.

`## Future CDF Execution Constraints` contains prose stating: resume only through CDF after integrity, history and drift checks plus current explicit authorization; preserve immutable definition/approval/scope/phase boundaries; stop for new decisions or scope; skip only tasks with applicable evidence; perform local verification, then full product acceptance, Completion Evidence Gate and final scoped review. Read-only inspection grants no implementation or progress mutation.

`## Compilation Gate Result` is JSON `{ "status": "READY", "task_count": <integer> }`. It refers only to definition compilation, never implementation completion.
