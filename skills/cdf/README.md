# CDF: Controlled Development Flow

CDF is the single user-facing controlled-development Skill. It understands a development request, inspects repository evidence, classifies risk, locks scope, obtains explicit human approval, then executes the approved work or saves it as a resumable task.

> Small changes should be fast. Risky changes should be controlled.

## When to Use CDF

Invoke CDF explicitly with `$cdf`, `/cdf`, `cdf:`, `controlled-development-flow`, or an explicit request for a controlled development flow.

Use it for:

- a new feature, fix, refactor, configuration change, or other development request;
- a PRD, specification, or requirement that needs repository-backed planning;
- a request to split approved development work into persistent tasks;
- resuming a task previously saved by CDF.

A purely informational request enters no development flow. A request to turn a PRD into tasks still follows the complete analysis and approval path.

CDF is the only user entry point. Task compilation is an internal CDF component with no top-level Skill, separate installation, or independent invocation.

## Workflow

```text
Requirement / PRD / Development Request
    -> Requirement Gate
    -> Requirement Understanding
    -> Evidence Inspection
    -> Risk Classification
    -> Development Plan
    -> cdf-scope/v1 Scope Lock
    -> Human Approval
    -> Execute Now | Save as Task
```

Requirement analysis and planning are internal CDF stages. The internal task compiler is entered only after an approved **Save as Task** decision.

## Control Gates

### Evidence and Repository Traceability

CDF confirms that named targets exist and inspects the smallest sufficient set of relevant code, configuration, tests, documentation, schemas, generated artifacts, and call sites. Material conclusions are separated into facts, inferences, and assumptions. Missing or conflicting evidence is surfaced rather than silently guessed.

When available, CDF records:

```text
Workspace: <absolute path>
Source-Branch: <branch>
Source-Commit: <commit>
Source-Worktree-State: <clean | dirty | Unavailable>
Source-Worktree-Changes: <[] | [Unavailable] | [' M src/foo.ts', '?? src/new-file.ts']>
```

`Source-Worktree-Changes` is one flow-style YAML array limited to tracked or untracked paths relevant to approved, affected, or protected areas. Quote dirty entries so both Git `XY` characters, including a leading space, survive unchanged. No relevant changes uses `[]`; unavailable state uses `[Unavailable]` and records the reason. Dirty state is evidence and a drift signal, not automatic proof of material risk or drift.

### Risk Classification

The S/M/L/XL risk model is unchanged. Risk is determined from impact, blast radius, reversibility, uncertainty, sensitivity, and coordination needs:

| Level | Typical boundary |
|---|---|
| **S** | One local cosmetic or static change with no shared or behavioral impact |
| **M** | Bounded local behavior, a small shared-component change, bounded configuration, or bounded existing-integration usage |
| **L** | Cross-cutting behavior, persistent data, billing, auth, security, privacy, materially meaningful analytics, meaningful external contracts, or non-trivial rollback |
| **XL** | Architecture, a new subsystem/service, migration, major data-flow redesign, phased rollout, or multi-system coordination |

Risk signals provide evidence and may establish a floor; a signal is not automatically the final level. CDF first runs the compact S Reverse Check in `SKILL.md`. A definite Level S candidate does not load the full risk reference; any failed or unknown S row, or any plausible non-S category, loads `risk-classification.md` and its complete signal record. An unresolved `UNKNOWN` forbids a level below the lowest plausible risk. If CDF cannot produce a safely bounded plan, or if conflicting evidence changes meaning, scope, acceptance, or safety, it stops as `BLOCKED`.

Planning depth follows the level. Level S uses the fast path below; Level M, L, and XL use the full Development Plan.

### Level S Fast Path

A confirmed Level S change is approved from four lines, with no canonical Scope Lock and none of the eleven sections:

```markdown
## Fast-Path Plan (Level S)
- Change: <the single target and the exact change>
- Will Not Change: <protected boundary>
- Verify: <observable check>
- Reverse Check: PASS (S-01..S-06)

Approve and execute? Or save as task?
```

The fast path requires every S Reverse Check row to pass with no `UNKNOWN`. The signal record and reverse check are reasoning steps at this level, reported only as the aggregate `Reverse Check` line. Approval is still explicit: the user names both the approved change and the authorized action.

CDF leaves the fast path and produces a full Development Plan as soon as evidence shows a second target, behavioral impact, a shared consumer, or any signal that was assumed `CLEAR`. Choosing **Save as Task** also requires promotion to a full plan, because the task contract carries a canonical Scope Lock; the risk level stays `Level S`.

### Development Plan Contract

Every approval-ready full Development Plan at Level M, L, or XL, plus a Level S plan promoted for **Save as Task**, uses these canonical headings in this order:

1. `Requirement Understanding`
2. `Evidence Summary`
3. `Risk Gate Result`
4. `Scope Lock`
5. `Technical Approach`
6. `Implementation Plan`
7. `Risks`
8. `Rollback Plan`
9. `Acceptance Criteria`
10. `Verification Strategy`
11. `Next Action`

The headings are carried directly into a handoff or saved task; they are not renamed, combined, split, or regenerated. Level S uses the fast path instead, and adopts these headings only when promoted for **Save as Task**. `Rollback Plan` may be concise or genuinely `None` for Level S or M, while Level L and XL require the additional detail described in [SKILL.md](SKILL.md).

### Scope Lock and Acceptance Authority

Every approval-ready full plan contains exactly one canonical `cdf-scope/v1` block with eight fields, in this order, including a Level S plan promoted for **Save as Task**:

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

Every field must exist and the order is fixed, because integrity verification derives the payload boundary from the first and last field. `in_scope` and `acceptance_criteria` must each contain at least one non-empty entry before approval; the other arrays may be empty. A partial or conditional result with no approved `in_scope` item is `BLOCKED`. After approval, the canonical block is immutable. Execution and task compilation may not paraphrase, reorder, widen, weaken, normalize, re-indent, or silently add scope.

The single `cdf-scope/v1` block is the sole canonical scope authority, and its `acceptance_criteria` field is the sole canonical acceptance source. The Development Plan’s `Acceptance Criteria` section is only a readable projection: it repeats every canonical criterion item for item, in the same order and exact wording. It may not add, delete, weaken, broaden, reinterpret, merge, or split a criterion. Task-level criteria may reference only applicable canonical entries verbatim. A newly required or changed criterion is a scope change and requires renewed planning and approval.

### Human Approval

Approval is required at every risk level. It must identify both the approved plan, Scope Lock, phase, or subset and one authorized action:

1. **Execute Now**
2. **Save as Task**

Replies such as `ok`, `continue`, `可以`, or `looks good` are insufficient when scope or action remains ambiguous. CDF supports full, conditional, and partial approval. Conditions are incorporated into a revised Scope Lock before approval.

For partial approval, the plan’s one canonical Scope Lock is revised to contain only the safely separable approved subset, while unapproved items remain verbatim and are protected through canonical exclusions. CDF also emits a stable `Partial Approval Result` containing the approval type, verbatim approved items, verbatim unapproved items, and only the canonical version marker. This result is an audit projection: it does not copy the complete Scope Lock and creates no second source of authority.

An Approval Record identifies the approved boundary and selected action. For **Save as Task**, that record authorizes persistence only and explicitly does not authorize code changes in the approval turn or during a future resume. Its content remains unchanged after saving.

For phased Level XL work, each approved phase has its own Development Plan boundary, canonical Scope Lock, Approval Record, and selected action. Approval of one phase never authorizes a later phase. The approved boundary is recorded explicitly:

```markdown
## Approved Phase Boundary
- Phase: <identifier and short name>
- Phase Scope: <what this phase delivers, matching canonical in_scope>
- Ends At: <the observable state that completes this phase>
- Explicitly Deferred: <later-phase work that this approval does not authorize>
```

## Approved Outcomes

### Execute Now

After explicit approval for **Execute Now**, CDF:

- rechecks repository drift, assumptions, stop conditions, protected areas, and any approved phase boundary;
- implements only the canonical approved scope;
- performs no unrelated cleanup, refactor, dependency addition, or broad reformatting;
- reports only verification actually run, including failures and unverified criteria.

New evidence that changes scope, risk, implementation meaning, acceptance, verification, or rollback stops execution and returns to planning and renewed approval.

### Save as Task

Before persistence, CDF performs a drift preflight against the approved planning evidence. It rechecks workspace, branch, commit, worktree state, and relevant `Source-Worktree-Changes`:

- material drift stops the save and returns to refreshed planning, risk assessment, Scope Lock when needed, and renewed approval;
- demonstrably non-material drift is recorded, and the handoff uses the latest traceability metadata.

Only after that preflight does CDF create the internal tasking handoff:

```text
Contract-Version: cdf-cdtask/v1
Handoff-Type: approved-tasking
Approval-State: approved
```

The internal task compiler:

- preserves the canonical Scope Lock and Approval Record verbatim;
- validates the `Acceptance Criteria` projection against `cdf-scope/v1.acceptance_criteria`;
- compiles stable, dependency-aware tasks without making new product or technical decisions;
- preserves a partial-approval audit projection without duplicating the Scope Lock;
- runs a Scope Guard;
- saves to `<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md` by default;
- performs read-back validation comparing both canonical payloads line for line, recomputes their required digests, returns the absolute path, and stops.

If compilation needs new scope, an interface, dependency, architecture decision, changed acceptance criterion, insufficient Scope Lock, or an inseparable partial remainder, it returns `BLOCKED` to CDF planning for renewed approval.

An approved Level S fast path has no canonical Scope Lock, so it cannot be handed off directly. CDF first promotes it to a full Development Plan and obtains approval of that plan; the risk level stays `Level S`.

For a request whose deliverable is a task breakdown, **Save as Task** produces the durable task definition. **Execute Now** means implementing the approved underlying development work; it does not produce an unsaved task list.

### Integrity Verification

The canonical Scope Lock and Approval Record must survive persistence and resume unchanged. CDF verifies that by comparing text, not by trusting a remembered value.

Payload boundaries are fixed: the Scope Lock runs from `Scope-Lock-Version: cdf-scope/v1` to the last `acceptance_criteria` entry, the Approval Record runs from `## Approval Record` to its last field, and code-fence delimiters are excluded from both. The eight Scope Lock fields must keep their canonical order, since the boundary depends on it.

Payload bytes use UTF-8, LF line endings, no Markdown fence delimiters, no trailing whitespace on payload lines, and exactly one trailing LF.

Comparison is line for line: same count, same order, same characters including indentation. Any difference is a mismatch, and CDF reports it rather than rewriting approved content to make it pass. Ambiguous boundaries, a duplicated canonical block, or trailing whitespace on a payload line are also rejections.

For a persisted task, CDF computes and stores a SHA-256 digest for each exact canonical payload after the authoritative line-for-line comparison. Those digests are required as the durable resume baseline and are recomputed later. If either digest cannot be computed, the task is not reported as resumable. A legacy `Unavailable` digest requires renewed approval and a verified re-save before execution.

## Resume a Saved Task

```text
$cdf continue task <path>
```

Before implementation, CDF:

1. validates `task_contract: cdf-cdtask/v1` and every required section;
2. extracts both canonical payloads under the fixed boundaries and requires their recomputed digests to match the persisted baselines;
3. compares workspace, branch, commit, `Source-Worktree-State`, relevant `Source-Worktree-Changes`, current code, and dependencies;
4. rechecks assumptions, stop conditions, phase boundaries, partial exclusions, acceptance criteria, and verification obligations;
5. determines whether the approved implementation meaning is still valid.

A missing, legacy, or unrecognized contract is rejected without code changes. Material drift, a failed assumption, new scope, changed risk, or changed acceptance returns to planning and renewed approval.

After validation succeeds, the explicit `$cdf continue task <path>` request creates the following current-turn `Resume Authorization Record`:

```markdown
## Resume Authorization Record
- User Request: <verbatim current continue request>
- Task Path: <resolved absolute path>
- Authorized Action: Execute Saved Approved Scope
- Scope Source: persisted cdf-scope/v1
- Authorization Context: <timestamp when available, otherwise current conversation turn>
- Code Changes Authorized In This Turn: Yes
```

Only then may CDF execute the saved approved scope in dependency order. Before the first code change, CDF creates or validates `<saved-task-path>.progress.yaml` using `cdf-execution-progress/v1`. The sidecar records `pending`, `in_progress`, `verified`, or `blocked`; resume skips only still-applicable `verified` tasks and inspects interrupted work before continuing. The record and sidecar do not modify the saved task or its Approval Record. A request only to inspect, review, summarize, or validate a task creates no Resume Authorization Record and authorizes no implementation or progress mutation.

## Boundaries

CDF does not:

- modify code or persist a task before valid approval;
- infer approval from acknowledgement or silence;
- expand approved scope or perform adjacent cleanup;
- treat a saved persistence approval as future execution authority;
- report a planned verification as completed;
- act as a background runtime, scheduler, worker-assignment system, or automatic implementation reviewer; the progress sidecar is only an execution journal.

The complete source of truth is [SKILL.md](SKILL.md).

## Usage

New development request:

```text
$cdf Analyze this development request, inspect the repository, classify risk,
lock the plan, obtain approval, then execute it or save it as a resumable task.
```

PRD to tasks:

```text
$cdf Inspect this PRD and repository, produce an approval-ready plan, then save
the approved work as dependency-aware tasks.
```

Resume and execute after validation:

```text
$cdf continue task <path>
```

Inspect without execution:

```text
$cdf validate task <path> without executing it
```

## References

- [Requirement Gate](references/requirement-gate.md)
- [Risk Classification](references/risk-classification.md)
- [Coding Discipline](references/karpathy-guidelines.md)
- [Boundary Cases](references/boundary-cases.md)
- [Internal Task Handoff](references/task-handoff.md)
- [Saved-Task Execution Progress](references/execution-progress.md)
- [Internal Task Compiler](components/cdtask/COMPONENT.md)

## Installation

Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

Both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

## Version Semantics

- **CDF Suite maturity:** v0.1
- **Skill package version:** 1.2.0

These are separate version systems. Suite maturity describes the CDF architecture; package version describes the distributable release.

Only `cdf` is a Skill entry point. The internal task compiler uses `COMPONENT.md`, not `SKILL.md`.
