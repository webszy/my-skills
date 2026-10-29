# Saved-Task Execution Progress — v2

Load while validating saved-task history read-only, and before any authorized runtime mutation. Definition/plan/scope/approval remain immutable. Progress is an execution journal, not a scheduler, authorization source or editable task definition.

## Ownership, serialization and binding

CDF owns `<resolved-absolute-task-path>.progress.yaml`. Save never creates it. Create/update it only after [resume validation and current explicit authorization](resume.md). Use a JSON object (valid YAML 1.2) with LF and final LF, so the standard-library validator needs no general YAML dependency. Write atomically through a temporary sibling and rename; preserve prior snapshots for append-only comparison. Never discard old history to resolve a validation error.

Required fields (`validate_cdf.py --describe` lists task/gate/review fields and transitions):

| Field | Meaning |
|---|---|
| progress_contract | `cdf-execution-progress/v2` |
| task_path, task_contract | Resolved absolute definition path, `cdf-cdtask/v2` |
| task_document_sha256 | Actual hash of every final saved-file byte; never substitutes for save-time definition digest |
| definition_sha256, scope_lock_sha256, approval_record_sha256 | Must match the normally validated saved task |
| overall_state | `not_started`, `in_progress`, `blocked`, `completed` |
| created_at, updated_at, completed_at | ISO-8601 with timezone; completed_at null until valid completion |
| source_snapshot | Actual SHA-256 of a retained content manifest/snapshot covering relevant source/configuration/dependencies, including dirty/untracked content |
| authorizations | Append-only runtime records from current explicit requests; never replay an old request as new authority |
| events | Append-only ordered transition journal |
| tasks | Projection of replayed events: every saved ID once, in definition order, with `id`, `state`, `verification_evidence` |
| evidence | Observed evidence registry, retained after invalidation |
| completion_gate, final_review | Current records or null |
| completion_history | Earlier gate/review attempts with invalidation reason; never overwrite history |

An authorization object has `id`, `user_request` (exact), `context` (timestamp/turn), `task_path`, `definition_sha256`, `action: "Execute Saved Approved Scope"`. Scope comes only from the saved canonical block. The validator checks binding/shape, not whether the human actually sent the statement. That must be checked against the conversation.

Evidence objects have `id`, `kind`, retrievable `source`, observed `result`, `snapshot` (actual SHA-256), `check_id` (approved check ID or null for non-check evidence), and boolean `valid`. IDs are unique. Never change historical source/result/snapshot/check identity; invalidate by setting valid false and recording the reason in the reopen/history record. Revalidation creates new evidence IDs, never toggles old ones back to true. A source string or PASS label alone does not prove a real check occurred.

## Task transitions

```text
pending -> in_progress -> verified
                       -> blocked
blocked -> in_progress
verified -> in_progress   (controlled reopen only)
```

Journal every transition as an object with:

- `seq`: consecutive integer starting at 1;
- `task_id`, `from`, `to`, timezone-bearing `at`, `authorization` (record ID);
- `reason`: observed reason, not a generic state label;
- `evidence`: observed check evidence IDs, nonempty for verified;
- `affected_tasks`: all transitive dependent task IDs for reopen, otherwise empty;
- `scope_evidence`: retrievable evidence IDs supporting in-scope/no-new-decision repair, required for reopen;
- `new_decisions`: false; a new product/technical/architecture decision requires replanning, not an event.

Replay begins with all tasks pending. Before first code modification write in_progress, requiring every dependency verified. To mark verified, all of **this task's local task_verification checks** must have actually passed with applicable evidence. Full product AC satisfaction is not a prerequisite for local verified. A block records the concrete cause; recheck it before restarting. On interrupted execution inspect actual output, never blindly repeat effects.

`tasks` is a checked projection, not a parallel mutable authority. The validator replays events, checks dependencies at each start, checks local evidence at verification and compares final projections. Without an earlier trusted snapshot, a self-contained journal cannot prove that history was never replaced; use `--previous-progress` when available and reconcile repository evidence regardless.

## Controlled reopen and downstream invalidation

Reopen verified only for an observed defect/new evidence invalidating previous verification, within original scope and without new decisions. Record reason and scope evidence, retaining every historical verification event and receipt.

On the reopen event, invalidate the task's current evidence and the current verification evidence of **all transitive downstream tasks**. This conservative dependency rule avoids hidden consumers being skipped. Record every downstream ID, including pending tasks. Replaying the event moves already-started downstream tasks to blocked and clears their current verification references; pending descendants remain pending. This derived `verified/in_progress -> blocked` invalidation is not a free-standing user-selectable transition or permission to change scope.

Set overall_state to in_progress or blocked and completed_at to null. Move any current gate/final review into completion_history with the defect/change reason, then clear them. Preserve their original contents. After repair, rerun applicable local checks; blocked descendants restart only when dependencies verify, then revalidate their applicable checks. Recheck product acceptance, the full gate and final review before completion. New evidence can invalidate results even before any source bytes change.

If broader scope or a new decision is needed, stop and use Full Replan, preserving the old definition and history. A reopened task must never be used to launder new requirements through local checks.

## Completion and final review

All tasks verified is necessary, not sufficient. Evaluate every canonical product AC and approved check using [Completion Evidence Gate](completion-evidence-gate.md). Store the report with actual source_snapshot and evaluated_at. Gate PASS allows final review only.

Record final_review with these exact fields:

| Field | Requirement |
|---|---|
| result | PASS, FAIL or PENDING based on actual scoped review |
| evidence | IDs in progress evidence referencing the actual review artifact/receipt, `kind: final_review` |
| source_snapshot | Reviewed source/configuration/dependency content SHA-256 |
| reviewed_at | Actual review time, after gate evaluation |
| outstanding_findings | Unresolved in-scope findings; empty required for PASS |
| required_approval | Whether the existing approved host workflow requires a final human approval; do not invent a new approval requirement |
| approval_evidence | Actual applicable approval references; nonempty if required and PASS |

Only all locally verified tasks, current product/gate PASS, a subsequent current final review PASS without outstanding findings, and all applicable approvals allow overall_state completed and completed_at. A record written by the Agent is not by itself review evidence: CDF must inspect the artifact and relevant full diff. No extra human approval is added where none was required.

Any subsequent relevant source/configuration/dependency change invalidates the affected checks, product/gate result and final review. Archive old gate/review, reopen affected verified tasks as needed, rerun affected checks, retain or rebind unaffected evidence only after checking actual applicability, update the gate and review the new snapshot. HEAD alone cannot bind dirty content. For the mechanical completion record, evidence referenced by the current PASS binds to the current snapshot; reuse requires a new applicability receipt on that snapshot, not silently rewriting old evidence.

Completion history entries are `{completion_gate, final_review, invalidated_reason}`. Preserve failed/insufficient attempts too. Inspect-only requests may report missing/stale evidence but cannot mutate history or reaffirm historical completion as current without reevaluation.
