# CDF: Controlled Development Flow

CDF is the single user-facing controlled-development Skill. It understands a development request, inspects repository evidence, classifies risk, locks an implementation plan, obtains explicit human approval, then executes the approved work or saves it as a resumable task.

> Small changes should be fast. Risky changes should be controlled.

## When to Use CDF

Invoke CDF explicitly with `$cdf`, `/cdf`, `cdf:`, `controlled-development-flow`, or an explicit request for a controlled development flow.

Use it for:

- a new feature, fix, refactor, configuration change, or other development request;
- a PRD, specification, or requirement that needs repository-backed planning;
- a request to split approved development work into persistent tasks;
- resuming a task previously saved by CDF.

A purely informational request enters no development flow. A request to turn a PRD into tasks still follows the complete analysis and approval path.

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

Requirement analysis and planning are internal CDF stages, not separate Skill handoffs. `components/cdtask/` is loaded only after an approved **Save as Task** decision.

## Control Gates

### Evidence Before Planning

CDF confirms that named targets exist and inspects the smallest sufficient set of relevant code, configuration, tests, documentation, schemas, generated artifacts, and call sites. Material conclusions are separated into facts, inferences, and assumptions. Missing or conflicting evidence is surfaced rather than silently guessed.

CDF also records available workspace, branch, commit, and relevant tracked or untracked worktree state for later drift checks.

### Risk Classification

Risk is determined from impact, blast radius, reversibility, uncertainty, sensitivity, and coordination needs:

| Level | Typical boundary |
|---|---|
| **S** | One local cosmetic or static change with no shared or behavioral impact |
| **M** | Bounded local behavior, a small shared-component change, bounded configuration, or bounded existing-integration usage |
| **L** | Cross-cutting behavior, persistent data, billing, auth, security, privacy, materially meaningful analytics, meaningful external contracts, or non-trivial rollback |
| **XL** | Architecture, a new subsystem/service, migration, major data-flow redesign, phased rollout, or multi-system coordination |

Risk signals provide evidence and may establish a floor; a signal is not automatically the final level. Level S and M require reverse checks. An unresolved gap uses the lowest plausible safe floor, while a conflict that changes meaning, scope, acceptance, or safety is `BLOCKED`.

### Scope Lock

Every approval-ready plan contains one canonical `cdf-scope/v1` block with eight fields:

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

Every field must exist; genuinely empty fields may use empty arrays. After approval, the canonical block is immutable. Execution and task compilation may not paraphrase, reorder, widen, weaken, normalize, or silently add scope.

### Human Approval

Approval is required at every risk level. It must identify both the approved plan, Scope Lock, phase, or subset and one authorized action:

1. **Execute Now**
2. **Save as Task**

Replies such as `ok`, `continue`, `可以`, or `looks good` are insufficient when the scope or action remains ambiguous. CDF supports full, conditional, and partial approval. Conditions are incorporated into a revised Scope Lock before approval; unapproved partial items remain explicit exclusions.

For phased Level XL work, each phase has its own Development Plan boundary, canonical Scope Lock, Approval Record, and selected action. Approval never carries into a later phase automatically.

## Approved Outcomes

### Execute Now

After explicit approval for **Execute Now**, CDF:

- rechecks repository drift, assumptions, stop conditions, protected areas, and any approved phase boundary;
- implements only the canonical approved scope;
- performs no unrelated cleanup, refactor, dependency addition, or broad reformatting;
- reports only verification actually run, including failures and unverified criteria.

New evidence that changes scope, risk, implementation meaning, acceptance, or rollback stops execution and returns to planning and renewed approval.

### Save as Task

After explicit approval for **Save as Task**, CDF creates the sole internal tasking contract:

```text
Contract-Version: cdf-cdtask/v1
Handoff-Type: approved-tasking
Approval-State: approved
```

The internal task compiler:

- preserves the canonical Scope Lock and Approval Record verbatim;
- compiles stable, dependency-aware tasks without making new product or technical decisions;
- runs a Scope Guard;
- saves to `<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md` by default;
- stores SHA-256 digests for the canonical Scope Lock and Approval Record;
- performs final read-back validation, returns the absolute path, and stops.

If compilation needs new scope, an interface, dependency, architecture decision, changed acceptance criteria, or an inseparable partial remainder, it returns `BLOCKED` to CDF planning for renewed approval.

For a request whose deliverable is a task breakdown, **Save as Task** produces the durable task definition. **Execute Now** means implementing the approved underlying development work; it does not produce an unsaved task list.

CDTask is an internal component. It is not independently installed or invoked.

## Resume a Saved Task

```text
$cdf continue task <path>
```

Before implementation, CDF:

1. validates `cdf-cdtask/v1` and every required section;
2. recomputes the Scope Lock and Approval Record SHA-256 values;
3. compares workspace, branch, commit, relevant committed and uncommitted worktree state, current code, and dependencies;
4. rechecks assumptions, stop conditions, phase boundaries, partial exclusions, acceptance criteria, and verification obligations;
5. determines whether the approved implementation meaning is still valid.

A missing, legacy, or unrecognized contract is rejected without code changes. Material drift or an invalid assumption returns to planning and renewed approval. A demonstrably non-material drift signal may be recorded before continuing.

After validation succeeds, an explicit `continue task <path>` authorizes execution of that saved approved scope for the current turn. A request only to inspect, summarize, or validate the task does not authorize implementation.

## Boundaries

CDF does not:

- modify code or persist a task before valid approval;
- infer approval from acknowledgement or silence;
- expand approved scope or perform adjacent cleanup;
- report a planned verification as completed;
- act as a runtime, scheduler, worker-assignment system, or automatic implementation reviewer.

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

Resume:

```text
$cdf continue task <path>
```

## References

- [Requirement Gate](references/requirement-gate.md)
- [Risk Classification](references/risk-classification.md)
- [Coding Discipline](references/karpathy-guidelines.md)
- [Boundary Cases](references/boundary-cases.md)
- [Internal Task Handoff](references/task-handoff.md)
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
- **Skill package version:** 1.1.0

These are separate version systems. Suite maturity describes the CDF architecture; package version describes the distributable release.

Only `cdf` is a Skill entry point. The internal task compiler uses `COMPONENT.md`, not `SKILL.md`.
