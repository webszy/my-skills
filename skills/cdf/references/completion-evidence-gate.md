# Completion Evidence Gate

Read before any execution completion decision in Execute Now or saved-task resume. This extends CDF's existing verification and final scoped review; it does not add a runtime, task state, approval mechanism, or separate workflow. Saving a task as `READY` is definition persistence, not execution completion, and keeps its existing save/read-back checks.

**Agent can propose completion, but only CDF can declare DONE.** A completion claim, a supplied `PASS`, a Review Result, or a `verified`/`completed` label is input to evaluation, never sufficient evidence or transition authority. CDF must inspect the underlying evidence, not copy the Agent's verdict.

## Evidence Requirements

Use the approved canonical `cdf-scope/v1.acceptance_criteria` in order and verbatim; for Level S Execute Now use the approved `Verify` line. Evaluate the entire approved boundary, including saved-task criteria beyond any single task's mappings. Never change or weaken acceptance or required verification to make the gate pass.

For every completion request, inspect and report:

1. **Acceptance Criteria:** every approved criterion, its observed result, and evidence references. A missing canonical entry is an evidence gap even if all mapped tasks say `verified`.
2. **Validation Results:** actual tests, lint, typecheck, build, and other checks applicable under the approved Verification Strategy. Record the exact command or inspection action, working directory, result, exit code when applicable, and retrievable output. Account for each of tests/lint/typecheck/build as executed, not run, unknown, or not applicable. A category may be `NOT_APPLICABLE` only with a repository/plan-based reason; an unavailable, prohibited, skipped, or failed required check is never not applicable or passed. Do not run a prohibited command just to satisfy the gate. Evidence-backed manual inspection is valid when it is the approved check, but cannot replace a required executable check.
3. **Diff Review:** inspect the complete task-attributable change against the execution baseline, including staged, unstaged, deleted, renamed, and untracked files. A file list or `git diff --stat` alone is insufficient. Inspect actual diff/content and record the review outcome and evidence even for an empty diff. Distinguish preserved pre-existing or concurrent changes from this task's output; never claim them as this task's work or discard them. Unexplained attribution is an evidence gap.
4. **Scope Compliance:** compare the inspected changes with approved scope, exclusions, protected areas, and any phase/partial-approval boundary. Record an explicit scope-compliance conclusion in evidence and disclose every task-attributable out-of-scope change, including unrelated code, configuration, or documentation edits the current Agent later reverted. For each, identify the file, change, reason, authorization evidence if any, and whether it remains or was reverted. Disclosure or reversion is not approval; unauthorized changes follow the existing failure and scope/replanning rules.
5. **Known Issues:** list unresolved defects, incomplete verification, uncertainty, and potential risks with supporting evidence when available. List every required unrun/unknown check in `unverified_items`. Empty issue arrays mean the inspection found none, not that they were omitted. Unrelated known issues may remain disclosed only when evidence shows they do not violate acceptance or required checks; they still go through final review.

Evidence must be actually observed and retrievable: tool/CI execution output, check logs with exit status, inspected file/diff artifacts, or an applicable review record. Agent assertions, planned commands, invented logs/digests, or inaccessible references cannot support a passing conclusion. Identify the inspected source revision and relevant working-tree content with captured artifacts or an actually computed digest; HEAD alone does not bind dirty/untracked content. Prior execution evidence may be reused only after confirming it covers the current relevant source, configuration, dependencies, and approved checks. Missing or stale bindings are evidence gaps.

The completion response must also follow [Agent Activity Disclosure](../SKILL.md#agent-activity-disclosure): summarize what the current Agent actually did for this request, identify additional work and why it was done, and explicitly list unrelated edits or state `无` / `None`. Record performed actions with `kind: agent_activity` evidence linked to actual tool receipts or artifacts; use the existing `out_of_scope_changes` array for unrelated edits, even those no longer visible in the final diff. Do not claim pre-existing or other Agents' work as current-Agent output. Unknown attribution is disclosed as an evidence gap, never converted into `None` or an empty array implying confirmed absence. Missing required activity/scope disclosure prevents `PASS` under the existing insufficient-evidence rule.

## Decision and Existing Completion Path

CDF derives the decision after inspecting all requirements above. `FAIL` takes precedence over missing evidence:

| Decision | Condition | Existing flow |
|---|---|---|
| `FAIL` | An actual required validation failed, an acceptance criterion is violated, an unauthorized scope change exists, or an unresolved review finding violates the approved completion boundary | Prevent completion; repair only within approved scope, otherwise stop and replan or use existing `BLOCKED` handling |
| `INSUFFICIENT_EVIDENCE` | No established failure, but a required report field, criterion, check, diff/scope review, usable result, or current evidence binding is missing, unexecuted, or uncertain | Prevent completion; collect permitted evidence or use existing `BLOCKED` handling when unable to continue |
| `PASS` | Every criterion and necessary check has current successful evidence, diff and scope reviews are supported, and all disclosures are complete with no established failure or required evidence gap | Continue into the existing final scoped review only |

`PASS` never directly sets DONE, `overall_state: completed`, or `completed_at`. Preserve the existing final scoped review and its Review Result wherever the host workflow uses one, plus every applicable Human Approval requirement. Pre-execution scope approval does not waive an additional required review/approval; this gate does not introduce a new approval requirement either. Only CDF may declare completion after the gate and those existing requirements pass. Pending review or approval leaves the task incomplete even with a gate `PASS`.

An unresolved in-scope review finding blocks completion. Reevaluate the gate against any finding that invalidates acceptance or evidence. If review or a subsequent edit changes relevant code, tests, configuration, dependencies, scope, or evidence, repeat the affected verification, update the report, and perform final review again. An old `PASS` cannot be carried over to changed output. Record a new report for each completion attempt, including failed or insufficient attempts; never present a prior attempt as current evidence.

## Completion Report

Emit this YAML report on every completion request. All eight fields are required; empty arrays are allowed only when the inspected evidence establishes no applicable entries. The default below represents no evaluated evidence, not a passing report:

```yaml
completion_gate:
  status: INSUFFICIENT_EVIDENCE
  acceptance_criteria: []
  validation_results: []
  changed_files: []
  out_of_scope_changes: []
  known_issues: []
  unverified_items: []
  evidence: []
```

Populate the arrays using these item shapes (result values are check results, not task states):

| Field | Item contents |
|---|---|
| `acceptance_criteria` | `criterion` (verbatim), `result` (`PASS`, `FAIL`, or `UNVERIFIED`), `evidence` (IDs) |
| `validation_results` | `check`, `required`, `result` (`PASS`, `FAIL`, `NOT_RUN`, `UNKNOWN`, or `NOT_APPLICABLE`), `command` (or inspection action), `working_directory`, `exit_code` (null for unrun/non-command checks), `reason`, `evidence` (IDs) |
| `changed_files` | `path`, `change` (including task attribution and pre-existing content preserved), `evidence` (IDs) |
| `out_of_scope_changes` | `path`, `change` (current-Agent attribution, whether retained or reverted, and authorization evidence if any), `reason`, `evidence` (IDs); disclosure never grants authorization |
| `known_issues` | `issue`, `impact`, `evidence` (IDs when available) |
| `unverified_items` | `item`, `reason`, `impact`, `evidence` (IDs when available) |
| `evidence` | unique `id`, `kind`, retrievable `source` (tool receipt, log/artifact path, or file and lines), observed `result`, and `snapshot` identifying the content checked |

Resolve every evidence ID to its actual source and verify it supports the cited conclusion. Include `kind: agent_activity`, `kind: diff_review`, and `kind: scope_compliance` records with observed outcomes even when `changed_files` or `out_of_scope_changes` is empty. A failed exit code contradicts a claimed validation `PASS`; do not trust the label. A zero exit code alone also cannot establish acceptance without the relevant check result.

For Execute Now, include the report inline or link to its retrievable artifact in the completion response; no new persisted artifact is required. For an authorized saved-task execution, also store the current report in the existing progress sidecar as described in [Execution Progress](execution-progress.md). Do not insert it into the immutable task, canonical Scope Lock, or Approval Record. Older task definitions and sidecars remain readable without migrations; their labels do not exempt a new completion decision from this gate. Read-only inspection can evaluate and emit a report but cannot change task state or write progress.

The report is an evidence and decision record. It does not replace the existing final review outcome, grant execution authority, or approve changes. Report an incomplete result honestly when required checks cannot be performed, together with the remaining checks needed for reassessment.

## Behavioral Tests

Use [Completion Evidence Gate Tests](../tests/completion-evidence-gate.md) to exercise decisions and completion boundaries. These are skill behavior tests, not a claim of an executable state-machine implementation.
