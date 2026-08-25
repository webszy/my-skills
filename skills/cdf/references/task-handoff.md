# Internal Task Handoff

Read this reference only when CDF is about to **Save as Task** or resume a task previously saved by CDF. The component that compiles and persists tasks is internal to CDF; its detailed compilation rules live in [CDTask Component](../components/cdtask/COMPONENT.md).

`cdf-cdtask/v1` is the sole tasking contract. It is an internal handoff format, not a public runtime protocol or a user-facing entry point.

## Entry boundary

CDF may create the handoff only after all of the following are true:

1. requirement meaning is sufficiently clear;
2. relevant repository evidence has been inspected;
3. risk has been classified from impact, blast radius, reversibility, uncertainty, sensitivity, and coordination needs;
4. the Development Plan and canonical `cdf-scope/v1` Scope Lock are complete;
5. a valid Approval Record identifies the approved scope or approved subset;
6. the user explicitly selected **Save as Task**.
7. CDF reran the save drift preflight against the approved planning evidence and either found no drift or recorded why observed drift is non-material.

Raw requirements, PRDs, unapproved plans, ambiguous acknowledgements, and manual task requests are not valid inputs. Route them through the normal CDF requirement, evidence, planning, and approval stages first.

A Level S Fast Path Plan is also not a valid input: it has no canonical Scope Lock. When a fast-path change is to be saved as a task, CDF must first expand it into a full Development Plan with a canonical `cdf-scope/v1` block and obtain approval of that expanded plan. The risk level stays `Level S`.

## Handoff header

Use exactly this contract identity and lifecycle state:

```text
# CDF Task Handoff

Contract-Version: cdf-cdtask/v1
Handoff-Type: approved-tasking
Approval-State: approved
Risk-Level: <Level S | Level M | Level L | Level XL>
Workspace: <absolute path or Unavailable>
Source-Branch: <branch or Unavailable>
Source-Commit: <commit or Unavailable>
Source-Worktree-State: <clean | dirty | Unavailable>
Source-Worktree-Changes: <[] | [Unavailable] | [' M src/foo.ts', '?? src/new-file.ts']>
Save-Drift-Preflight: <matched | non-material-drift>
Save-Drift-Notes: <none | concise evidence-backed conclusion>
```

Use one flow-style YAML array. Use `[]` when no relevant changes exist. When unavailable, use `[Unavailable]` and record the reason; when dirty, quote every entry and preserve both Git `XY` status characters, including leading spaces, for only the approved, affected, or protected repository-relative paths, sorted by path and then status. Do not dump unrelated repository changes. Dirty state is a drift signal, not automatic proof of material drift. Never overwrite or discard a user's uncommitted changes.

`Unavailable` is an explicit evidence state, not a guessed value. Record the reason when missing workspace metadata affects persistence or later drift checks. A material save-preflight difference is not a valid handoff: CDF must first return to planning, refresh evidence and risk, revise the Development Plan or Scope Lock when needed, and obtain renewed approval. The internal compiler receives the latest non-material metadata but does not perform planning.

CDF may also supply naming and destination metadata:

```text
Task-Title: <short approved title>
Requested-Task-Path: <absolute path or Workspace-relative path>
```

Both fields are optional and cannot change approved task meaning. Without `Requested-Task-Path`, use the default `_cdtask` destination. Without `Task-Title`, derive the slug mechanically from the first approved `in_scope` item, falling back to `task` when it has no filesystem-safe characters.

## Required payload

Carry the approved Development Plan directly, with these exact headings in this order:

1. Requirement Understanding;
2. Evidence Summary;
3. Risk Gate Result;
4. Scope Lock;
5. Technical Approach;
6. Implementation Plan;
7. Risks;
8. Rollback Plan;
9. Acceptance Criteria;
10. Verification Strategy;
11. Next Action.

Do not rename, combine, split, or regenerate these sections. Also carry the Approval Record verbatim, the Partial Approval Result when applicable, and the Approved Phase Boundary when approval covers one phase. A Level S or M Rollback Plan may contain a concise reversible action or `None` only when rollback is genuinely not applicable.

The canonical Scope Lock uses this schema:

```yaml
Scope-Lock-Version: cdf-scope/v1
in_scope:
  - <approved outcome or impact>
out_of_scope: []
non_goals: []
assumptions: []
stop_conditions: []
will_change: []
will_not_change: []
acceptance_criteria:
  - <observable result>
```

Every field must exist. `in_scope` and `acceptance_criteria` must each contain at least one non-empty entry before approval or handoff; the other arrays may be empty. Do not manufacture assumptions, non-goals, stop conditions, or exclusions just to populate a field. A partial or conditional result with no approved `in_scope` item is `BLOCKED`.

Treat the canonical Scope Lock as immutable data. Preserve its canonical block verbatim. The internal compiler must not paraphrase, rewrite, expand, weaken, reorder, normalize away distinctions, or silently add scope. Task-level scope may quote or map to canonical entries, but it cannot replace them.

`cdf-scope/v1.acceptance_criteria` is the sole canonical acceptance source. The Development Plan's `Acceptance Criteria` section is a readable projection only: it must repeat every canonical entry item for item, in the same order and exact wording. Task-level acceptance may reference only applicable canonical entries verbatim. Any addition, deletion, weakening, broadening, reinterpretation, merge, or split is `BLOCKED` and returns to refreshed CDF planning and renewed approval.

For partial approval, carry the audit projection defined in [Human Approval](../SKILL.md#6-human-approval) verbatim.

Do not include the complete Scope Lock in this result. The plan's single `cdf-scope/v1` block remains canonical. Approved Items must exactly match its approved `in_scope` entries; Unapproved Items remain verbatim and must be protected by canonical exclusions. This projection is audit information, not a second authority. Unsafe or ambiguous separation is `BLOCKED` and requires a revised Scope Lock and renewed approval.

## Handoff validation

Before compilation, verify:

- the contract version, handoff type, and approval state are exact;
- the risk level is supported and matches the approved plan;
- the Approval Record identifies the approver statement, approved boundary, timestamp or session context, approval type, and **Save as Task** action;
- the canonical Scope Lock has all eight fields, non-empty `in_scope` and `acceptance_criteria`, and is internally consistent;
- the Development Plan has the exact required headings and carries the approved sections directly;
- the plan's Acceptance Criteria projection exactly matches canonical `acceptance_criteria` item for item, in order and wording;
- plan steps and all task-level acceptance references fit inside the Scope Lock;
- any partial approval contains only the approved subset and keeps the remainder excluded;
- the handoff contains enough repository traceability to perform a later drift check;
- the current worktree state and relevant changes list are valid and the save drift preflight is recorded;
- rollback and phase boundaries are present when applicable.

Task compilation must become `BLOCKED` if safe decomposition would require:

- a new module, interface, behavior, dependency, or affected area;
- broader write scope or changed protected areas;
- changed or newly invented acceptance criteria or verification obligations;
- a new architecture or technical decision not contained in the approved plan;
- resolution of a material planning ambiguity;
- inclusion of an unapproved partial-approval remainder;
- modification of the canonical Scope Lock.

On `BLOCKED`, return the reason and evidence to CDF planning. CDF must reinspect the relevant evidence, produce a refreshed Development Plan and Scope Lock package, and request renewed approval even when re-analysis leaves the Scope Lock text unchanged. The compiler must not resolve the defect by expanding or rewriting scope.

## Integrity verification

Apply [Integrity Verification](../SKILL.md#integrity-verification) unchanged at handoff validation, save, read-back, and resume. Text comparison is authoritative while the approved handoff is available. Persistence additionally requires computed SHA-256 digests for both canonical payloads as the later resume baseline. Ambiguous boundaries, a reordered Scope Lock, an unavailable digest, or a mismatch invalidates persistence; never rewrite approved content to force a match.

## Persistence invariant

The default task path remains:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<slug>.md
```

The persisted document must retain `cdf-cdtask/v1`, source traceability including relevant worktree changes and the save preflight result, the canonical Scope Lock verbatim, immutable Approval Record, required payload digests, Partial Approval Result when applicable, dependency-aware task definitions, Scope Guard, verification and rollback obligations, and resume rules. After writing, read the document back and verify every invariant, including a line-for-line comparison and digest recomputation for both canonical payloads, before reporting success. If save or read-back verification fails, do not report the task as ready.

Task readiness is not execution and does not expand the approved boundary. The saved Approval Record proves approved scope and persistence authorization; it does not authorize future code changes. Never modify the saved record during resume; comparison is validation only.

## Resume and drift authority

Resume only through CDF, for example `$cdf continue task <path>`, or an equivalent explicit natural-language request. There is no separate user-facing task compiler command.

[Resume a Saved Task](../SKILL.md#resume-a-saved-task), [Integrity Verification](../SKILL.md#integrity-verification), and [Repository Drift](../SKILL.md#repository-drift) are the sole authorities for later validation, authorization, and drift decisions. This handoff reference does not redefine them. After current-turn authorization, CDF uses [Execution Progress](execution-progress.md) to create or validate the separate mutable progress sidecar; it never writes runtime status or authorization into the immutable saved task.

Do not bypass validation because the task is recent, the diff is small, or the saved task is marked ready. A request only to inspect, review, summarize, or validate the task authorizes no code change or progress mutation.
