# CDF Saved-Task Execution Progress

Read this reference during saved-task validation to inspect any existing sidecar read-only and reconcile repository changes before choosing a resume route. Creating or updating progress still requires successful CDF resume validation and the current-turn Resume Authorization Record.

The saved task is immutable definition and approval evidence. Runtime progress lives in a separate mutable sidecar; it never changes scope, acceptance, risk, dependencies, write scope, approval, or execution authorization.

## Ownership and Path

- CDF creates and updates progress; the internal CDTask compiler never creates it during **Save as Task**.
- The deterministic path is `<absolute-saved-task-path>.progress.yaml`.
- The sidecar grants no authority. It is usable only after the saved task passes the normal CDF resume validation and the current user explicitly authorizes continuation.
- The saved task, canonical Scope Lock, Approval Record, and task definitions remain unchanged.
- The expected task document and progress sidecar are control artifacts, not implementation drift. Validate them separately and exclude them from `Source-Worktree-Changes` unless either file is itself an approved implementation target.

## Contract

Create this document only after current-turn resume authorization:

```yaml
progress_contract: cdf-execution-progress/v1
task_path: <resolved absolute saved-task path>
task_contract: cdf-cdtask/v1
task_document_sha256: <64 lowercase hexadecimal characters>
scope_lock_sha256: <digest copied from the validated task>
approval_record_sha256: <digest copied from the validated task>
overall_state: <not_started | in_progress | blocked | completed>
created_at: <ISO-8601 timestamp>
updated_at: <ISO-8601 timestamp>
completed_at: <ISO-8601 timestamp | null>
tasks:
  - id: TASK-001
    state: <pending | in_progress | verified | blocked>
    started_at: <ISO-8601 timestamp | null>
    verified_at: <ISO-8601 timestamp | null>
    blocked_reason: <concise reason | null>
    verification_evidence: []
```

The task list must contain every saved task ID exactly once and no unknown ID. Keep saved dependency order, but do not copy task definitions or canonical payloads into the sidecar.

For each authorized overall completion request, also record the structured `completion_gate` report defined in [Completion Evidence Gate](completion-evidence-gate.md) as an additive top-level field. Gate decisions are evidence, not lifecycle states. Existing `cdf-execution-progress/v1` sidecars without this field remain readable; do not rewrite immutable saved tasks or their approval payloads. Before newly declaring or reaffirming completion, evaluate the gate from current evidence even if an older sidecar already says `completed`. A legacy label alone cannot establish completion; an inspect-only request may report missing evidence but must not mutate progress.

Compute `task_document_sha256` over the complete immutable saved task bytes before creating the sidecar. On every resume, recompute it and require an exact match. Also require the sidecar payload digests to equal the validated digest fields in the saved task. A mismatch is `BLOCKED`; never rewrite either artifact to force a match.

## State Transitions

Use only these transitions:

```text
pending -> in_progress -> verified
                       -> blocked
blocked -> in_progress
```

- Write `in_progress` atomically before the first implementation change for that task.
- Write `verified` only after every mapped canonical acceptance criterion is satisfied and the applicable planned checks were actually run successfully. Record concise observable evidence; never record a planned check as performed.
- Write `blocked` with the concrete reason when work cannot continue inside approved scope.
- Never move `verified` backward merely to rerun work. New evidence that invalidates a verified result follows CDF drift and replanning rules.
- Set `overall_state: completed` and `completed_at` only when every task is `verified`, every canonical acceptance entry has task coverage and current successful verification evidence, the current `completion_gate.status` is `PASS`, and the subsequent final scoped review has no unresolved in-scope finding and all applicable approvals are satisfied. Apply the [Completion Evidence Gate](completion-evidence-gate.md) to the complete canonical array item by item; all tasks being `verified` cannot substitute for this check. Store the criterion-to-check evidence in the applicable tasks' `verification_evidence` and reference it from the report. Any uncovered, failed, or unverified required entry prevents completion. A non-passing gate uses the existing repair/replan or `blocked` handling; do not write `completed_at` for that attempt. Review changes invalidate affected evidence and require gate reevaluation and review before completion.
- Update the sidecar atomically so interruption cannot leave a partially written progress record.

## Resume and Reconciliation

On every resume:

1. validate the saved task, then read any existing sidecar without mutation and validate its contract, paths, task IDs, hashes, timestamps, state values, and dependency consistency;
2. reconcile actual committed and uncommitted changes against the saved plan, evidence dependencies, and recorded progress. Attribute normal approved output only when repository evidence supports it; a state label, timestamp, or overlapping path alone is insufficient. Inspect unexplained changes and stop as `BLOCKED` if attribution remains ambiguous. Attributable approved output is not automatically material drift;
3. finish CDF's assumption and drift checks and select its resume route. Material drift uses the Full-Replan Path; preserve the old task and sidecar binding and never use them to track a newly approved plan;
4. only after the Fast-Resume Path passes and its Resume Authorization Record exists, create or update progress and skip tasks marked `verified` whose evidence still applies to the current repository;
5. inspect repository state before continuing an `in_progress` task, then finish or re-verify it without blindly repeating non-idempotent work;
6. re-check a `blocked` task's reason before moving it to `in_progress`;
7. execute a `pending` task only after all dependencies are `verified`.

If no sidecar exists, reconcile current repository evidence against every task Write Scope before initializing all tasks as `pending`. If overlapping changes make prior execution ambiguous, create no optimistic status and stop as `BLOCKED` for explicit reconciliation. Never infer completion from a changed file alone.

An inspect, review, summarize, or validate request may read the sidecar but must not create or update it.
