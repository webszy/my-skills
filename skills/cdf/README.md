# CDF: Controlled Development Flow

CDF is the single user-facing controlled-development Skill. It understands a development request, inspects repository evidence, classifies risk, locks scope, obtains explicit human approval, then executes the approved work or saves it as a resumable task.

> Small changes should be fast. Risky changes should be controlled.

While CDF is active, every user-facing response starts with `当前流程：cdf v<version>`, using the package version from the skill's `skill.json` (currently `1.2.1`). This also applies to progress, approval, save, and resume messages; it does not add a section to the saved task format.

Each response also briefly states **Current Agent Actions** and **Code Changes Unrelated to This Request**. Report actual work, extra actions and their reasons, and unrelated edits with files, authorization evidence, and retained/reverted status; explicitly state `None` when established or `Unknown` when attribution is unresolved. Final reports cover the request cumulatively and distinguish pre-existing or other Agents' changes. Completion reports reuse activity evidence and `out_of_scope_changes`; disclosure never authorizes extra scope.

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

Planning depth follows the level. Level S uses the fast path below. Level M/L/XL still receive complete analysis, but the default approval message is a concise summary; the eleven-section format belongs to the handoff and saved task.

### Concise Approval Display

Use the user's language and normally one to three short points per section:

- **Requirement Understanding** — outcome, scope, and important exclusions.
- **Technical Approach** — the proposed solution and decisions requiring approval.
- **Implementation Plan** — short steps, observable acceptance, and how to check it.
- **Risks** — material risks, assumptions or conditions, and rollback implications.

End with one choice: approve and execute, or approve and save as task. Keep important conditions and XL phase boundaries visible, but leave evidence inventories, risk tables, canonical YAML, and raw approval/progress records out of chat unless requested. Approval covers only the meaning shown; the internal scope cannot introduce hidden obligations. After approval, confirm in one short sentence.

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

CDF leaves the fast path, reassesses risk, and shows the concise summary if evidence reveals a second target, behavior, shared consumers, or another signal. After approval of **Save as Task**, CDF maps the S fast path into the full document plan and canonical scope without changing meaning; risk stays `Level S`. Formatting alone does not require renewed approval.

### Development Plan Contract

For **Save as Task** at every risk level, CDF organizes already-approved planning material into these eleven canonical document headings before handoff. They are not the default chat approval format:

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

CDF checks the assembled plan against the exact approved summary, freezes it, and hands it to the compiler for verbatim persistence. The saved file also preserves the displayed summary as approval evidence. Formatting adds no authority and does not trigger a second approval; newly discovered scope, decisions, acceptance, or verification obligations require an updated concise summary and renewed approval. **Execute Now** uses the approved planning record directly without rendering eleven sections. `Rollback Plan` may be concise or genuinely `None` for S/M; L/XL retain the detail required by [SKILL.md](SKILL.md).

### Scope Lock and Acceptance Authority

M/L/XL planning prepares one internal canonical `cdf-scope/v1` block before approval. Every saved plan contains one such block, including S tasks mechanically mapped from the approved fast path. Its eight fields are internal and saved-file content, not a mandatory chat display:

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

Every field must exist in the fixed order. `in_scope` and `acceptance_criteria` must each contain at least one non-empty entry; other arrays may be empty. A partial or conditional result with no approved item is `BLOCKED`. After approval, or mechanical mapping of an approved S task, the block is immutable. Execution and compilation may not rewrite it or add scope. Every material obligation must be exposed in the approval summary; internal content alone is not authorization.

The single `cdf-scope/v1` block is the sole canonical scope authority, and its `acceptance_criteria` field is the sole canonical acceptance source. The Development Plan’s `Acceptance Criteria` section is only a readable projection: it repeats every canonical criterion item for item, in the same order and exact wording. It may not add, delete, weaken, broaden, reinterpret, merge, or split a criterion. Task-level criteria may reference only applicable canonical entries verbatim. A newly required or changed criterion is a scope change and requires renewed planning and approval.

### Human Approval

Approval is required at every risk level. It identifies the displayed concise plan (or full plan when requested), phase, or subset and one authorized action:

1. **Execute Now**
2. **Save as Task**

Replies such as `ok`, `continue`, `可以`, or `looks good` are insufficient when scope or action remains ambiguous. CDF supports full, conditional, and partial approval. Conditions are incorporated into the working Scope Lock and shown in the revised concise summary before approval.

For partial approval, the canonical scope contains only the safely separable approved subset and protects the remainder. Chat briefly identifies that boundary. The structured `Partial Approval Result` stays internal and is copied into saved tasks; it is audit evidence, not another Scope Lock. Approval and phase records follow the same display rule: show concise meaning in chat and full records in the saved file unless requested.

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
- requires every canonical acceptance entry to have at least one task mapping and a corresponding planned check;
- compiles stable, dependency-aware tasks without making new product or technical decisions;
- preserves a partial-approval audit projection without duplicating the Scope Lock;
- runs a Scope Guard;
- saves to `<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md` by default;
- performs read-back validation comparing both canonical payloads line for line, recomputes their required digests, returns the absolute path, and stops.

If compilation needs new scope, an interface, dependency, architecture decision, changed acceptance criterion, insufficient Scope Lock, or an inseparable partial remainder, it returns `BLOCKED` to CDF planning for renewed approval.

An approved Level S fast path cannot be handed off directly. CDF first maps it into the complete document format and full Approval Record using the original approval statement; risk stays `Level S`. This mechanical expansion does not require renewed approval unless new meaning is discovered.

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
3. validates any existing progress sidecar read-only before selecting a resume route;
4. runs a **Code Evidence Diff** over write scopes, protected areas, and read-only evidence dependencies such as APIs, configuration, schemas, and callers. It compares committed and uncommitted content with source revisions and the Evidence Summary's content baselines; matching Git status entries alone do not prove unchanged content;
5. reconciles actual changes with validated progress, distinguishing pre-existing work, attributable approved output, non-material external drift, and material or unexplained changes;
6. revalidates assumptions, stop conditions, shared contracts, acceptance, verification, rollback, and the phase boundary.

A missing, legacy, or unrecognized contract is rejected without code changes.

**Fast-Resume Path** — after all checks pass, the saved plan must remain valid and evidence must be unchanged or every difference explained as approved execution output or non-material drift. Normal output from an interrupted approved task does not itself require renewed approval. Missing baselines, invalid sidecar bindings, or unresolved attribution cannot be treated as a clean diff; follow CDF's evidence-gap and reconciliation rules.

**Full-Replan Path** — material drift returns to planning. Reinspect changed sources and affected dependencies or assumptions, revise the plan and Scope Lock where needed, and obtain approval of the new plan and action. This ends the old task's resume route even if the Scope Lock wording stays unchanged. **Execute Now** follows 7A using the new plan and Approval Record; **Save as Task** follows 7B to create a new document at a distinct path and stops until a later explicit continue request targets it. Preserve the old task and sidecar binding; do not record new-plan work or copy old runtime statuses into a new sidecar.

Only after the Fast-Resume Path passes does the explicit `$cdf continue task <path>` request create this current-turn `Resume Authorization Record` for the unchanged saved definition:

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

Completion requires every task to be verified, every canonical acceptance entry to have coverage and current successful verification evidence, and the final scoped review to have no unresolved in-scope finding. All tasks being verified is not sufficient on its own.

CDF's [Completion Evidence Gate](references/completion-evidence-gate.md) checks acceptance, actual validation results, diff review, scope compliance, and known or unverified issues for both Execute Now and saved-task completion. Every request produces a structured `completion_gate` report. `FAIL` and `INSUFFICIENT_EVIDENCE` block completion; `PASS` permits the existing final review and does not waive any Human Approval requirement. Agent claims such as `Done` never change task state. Existing task contracts and lifecycle states remain unchanged; older progress sidecars remain readable, but completion must be supported by current gate evidence.

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
- [Completion Evidence Gate](references/completion-evidence-gate.md)
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
- **Skill package version:** 1.2.1

These are separate version systems. Suite maturity describes the CDF architecture; package version describes the distributable release.

Only `cdf` is a Skill entry point. The internal task compiler uses `COMPONENT.md`, not `SKILL.md`.
