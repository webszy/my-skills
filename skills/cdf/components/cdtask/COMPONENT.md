# CDTask: Internal Post-Approval Task Compiler

CDF loads CDTask only after an approved **Save as Task** decision. It has no independent invocation, installation, planning authority, runtime, scheduler or implementation review. The entry contract is `cdf-cdtask/v2`, `handoff_type: approved-tasking`, `approval_state: approved`.

## Authority boundary

CDTask validates the frozen [CDF handoff](../../references/task-handoff.md), decomposes approved work into dependencies and local deliverables, preserves the approved plan and canonical `cdf-scope/v1`, runs Scope Guard, persists/read-backs, returns the path and stops.

It cannot accept raw requirements, classify risk, choose architecture, invent acceptance/verification obligations, broaden write scope, infer approval, execute code, assign workers, or modify progress. Save approval authorizes persistence only. A hash is not proof of human approval provenance.

## Compilation workflow

1. Validate handoff, approved action and exact displayed approval basis. Confirm the plan adds no undisclosed meaning, all eight canonical scope arrays exist, and canonical acceptance is fully projected.
2. Preserve the full Development Plan, Scope Lock, Approval Record, partial projection and phase boundary verbatim. Never normalize approved content to fit a parser or digest.
3. Read [Task Templates](references/task-templates.md); compile stable-ID tasks and acyclic dependencies supported by the approved plan. Local task checks reference the approved Verification Strategy; contribution IDs reference canonical ACs.
4. Check Scope Guard: every positive task mapping is canonical, all write areas/implementation details are entailed, all exclusions and deferred items are protected, no new decision was introduced, every task has local checks, every product criterion has contributing tasks and product checks. Validate both directions, not just existing tasks.
5. Read [Persistence](references/persistence.md); compute the save-time full definition baseline and perform final read-back. A mechanical validator success supplements actual scope/approval review; it never replaces it.
6. Return the verified absolute path and stop. Create no progress sidecar and do not implement the task.

Local `verified` is runtime state, never a compiler label. Immutable definitions use `READY`; planned checks are never claimed as executed.

## Compilation Gate

| Status | Meaning | Next step |
|---|---|---|
| READY | Definitions and scope checks pass; final persisted file read-back and all three digests match | Return path, stop |
| NOT_READY | Deterministic grouping/field/coverage defect repairable from approved content | Repair and recheck without new meaning |
| BLOCKED | Missing authority, semantic ambiguity, scope/verification change, unsafe partial separation, or persistence failure | Return to CDF; no execution |

A grouping-only cycle can be repaired mechanically. A cycle caused by contradictory planning, or missing acceptance coverage that needs new work/decisions, requires replanning rather than weakening checks.

Blocking reason classes: `invalid-handoff`, `approval-invalid`, `scope-lock-invalid`, `ambiguity`, `requires-new-scope`, `acceptance-change`, `verification-change`, `partial-separation`, `persistence-failure`. CDF refreshes evidence/plan and obtains renewed approval for semantic changes. I/O problems need destination/I/O resolution, not invented scope approval.

Return this internal result:

```text
Contract-Version: cdf-cdtask/v2
Compilation-Status: READY | NOT_READY | BLOCKED
Blocked-Reason-Class: <class or Not applicable>
Saved-Task-Path: <absolute path or Unavailable>
Task-Count: <count or Unavailable>
Scope-Lock-Read-Back: verified | not-verified
Approval-Record-Read-Back: verified | not-verified
Scope-Lock-Digest: verified | not-verified
Approval-Record-Digest: verified | not-verified
Definition-Digest: verified | not-verified
Document-Read-Back: verified | not-verified
Reason: <evidence or Not applicable>
```

READY requires all six read-back/digest fields verified and an actual saved path. Do not report an unsaved draft as READY. [Resume](../../references/resume.md) belongs to CDF; CDTask never resumes or edits a previously saved definition.
