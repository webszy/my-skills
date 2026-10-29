# Saved Task Resume and Compatibility

Load for inspect, first Execute Saved Task or continuation. The saved definition is never self-authorizing. Read-only inspection can report defects or produce a draft, but creates no authorization or progress mutation.

## Validation before authorization

1. Read the exact supplied task path. Require `cdf-cdtask/v2` for current execution; apply the legacy route below otherwise.
2. Run [normal integrity validation](../components/cdtask/references/persistence.md) against **all three save-time digests**, including complete definition. Never use `--draft-hashes` to fill a missing resume baseline. Check exact approval provenance/meaning separately.
3. Read [Execution Progress](execution-progress.md); validate any sidecar read-only against the entire saved file, task IDs, event history, evidence and dependencies. Preserve prior snapshots for history comparison where available. A sidecar label is not proof of execution.
4. Run a Code Evidence Diff over all write scopes, protected areas and read-only evidence dependencies from Evidence Summary. Compare commits and actual dirty/untracked content with saved source baselines. HEAD, Git status or matching paths alone do not establish unchanged content.
5. Reconcile actual work against history: distinguish pre-existing work, attributable approved execution output, demonstrably non-material external drift and material/unexplained changes. Do not blindly repeat interrupted or non-idempotent operations. If no sidecar exists, inspect every task write scope before initializing pending states; ambiguous prior execution blocks initialization.
6. Revalidate assumptions, stop conditions, shared contracts, product criteria, local/product checks, rollback and phase/partial boundaries. Missing trustworthy evidence is an explicit uncertainty, never a clean diff.

Invalid binding, digest mismatch or unexplained attribution blocks execution. Preserve files; do not rewrite hashes, approval or states to force a pass. Material drift requires Full Replan. An in-scope defect that invalidates a local verification with no new decision may instead use the controlled reopen path; explain why the original plan still applies.

## Fast Resume and authorization

Use Fast Resume only when the validated saved definition still applies and differences are explained as approved output or demonstrably non-material drift. Record evidence. Normal interrupted approved output alone does not require renewed plan approval.

A current explicit `continue task <path>` or equivalent execute-saved-task request then authorizes the **unchanged saved approved scope**. Create a runtime authorization entry containing an ID, exact user request, timestamp/turn context, resolved task path, validated definition hash and action `Execute Saved Approved Scope`. Only then may CDF create/update progress and execute dependencies. Earlier authorization records are history, never permission for a later turn. A request to inspect/review/summarize/validate is not execute, even if a previous record exists.

Skip only locally verified tasks whose evidence still applies. Inspect in-progress/blocked work, recheck block reasons and dependencies before continuing. Product acceptance is evaluated separately at the full completion boundary.

## Full Replan

When scope, implementation meaning, risk, verification, rollback or a material assumption is invalidated, return to requirement/evidence/risk planning. Use verified prior results as evidence, not approval. Show the revised boundary and obtain approval of the new plan and action, even if Scope Lock wording remains unchanged.

This ends the old resume route. Preserve old task, Approval Record and progress history:

- **Execute Now:** execute the newly approved plan through CDF's normal path; do not bind new work to the old sidecar.
- **Save as Task:** create and verify a distinct new task file, then stop. Later execution requires a new explicit continue request targeting it. Do not blindly copy old states; reconcile/revalidate relevant prior results.

## Legacy and version policy

| Artifact | v1 meaning retained | v1.3.0 output |
|---|---|---|
| cdf-scope/v1 | Eight ordered arrays, canonical immutable product acceptance | Same schema/meaning; v2 task wire profile restricts serialization to JSON arrays for deterministic standard-library parsing |
| cdf-cdtask/v1 | Task verification coupled to mapped canonical criteria; only payload hashes required at save | cdf-cdtask/v2 separates local verification/contribution/product checks and requires complete definition SHA-256 at save |
| cdf-execution-progress/v1 | Original states, full-document binding established at execution, no verified reopen | cdf-execution-progress/v2 adds journaled controlled reopen, invalidation and mandatory final review for completion |
| completion_gate | Original eight report fields retain meaning | v2 progress adds source_snapshot/evaluated_at and explicit evidence validity/check references; existing report semantics are not reinterpreted |

The task/progress changes are incompatible and therefore use v2. Do not mutate v1 definitions, replace their Approval Records, upgrade version strings in place, copy their verified states as v2 truth, or delete old artifacts.

Legacy inspection is read-only: identify the original version; extract original scope/approval under v1 boundaries (LF, no trailing whitespace, no fences, one trailing LF), recompute available payload hashes and any existing v1 sidecar whole-file binding, and check original task mappings/dependencies. Those checks establish only the limited baseline originally saved. Missing hashes, no trustworthy full definition baseline, stale progress or conflicting approval require explicit reconciliation/re-approval; a newly computed hash cannot prove what was originally approved.

For migration, compare the entire old plan and history with trusted original approval evidence and current repository evidence. Present the proposed v2 plan/local checks/product paths and any changed meaning, obtain explicit approval for the new plan and selected action, and preserve the old approval as historical evidence without pretending it approves the new version. Save new v2 definitions at a distinct path when Save is chosen, with a new Approval Record and save-time hashes, then stop. Execute Now may instead use the newly approved live plan. No automatic migration or execution is provided.
