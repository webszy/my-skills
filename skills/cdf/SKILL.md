---
name: cdf
description: Run a controlled development workflow that understands a development request or PRD, inspects repository evidence, classifies risk, locks scope, obtains explicit human approval, then executes the approved work or saves it as a resumable task. Use when the user explicitly invokes cdf, /cdf, $cdf, cdf:, or controlled-development-flow, or explicitly asks for a controlled development flow.
---

# CDF: Controlled Development Flow

## Purpose

CDF is the single user-facing controlled-development Skill. It owns the complete path from requirement understanding through an approved outcome:

```text
Requirement / PRD / Development Request
    -> Understand
    -> Inspect Evidence
    -> Assess Risk
    -> Plan
    -> Lock Scope
    -> Human Approval
    -> Execute Now | Save as Task
```

**Small changes should be fast. Risky changes should be controlled.**

Planning is an internal stage of CDF, not a separate handoff. Saving a task uses the internal post-approval component at [components/cdtask/COMPONENT.md](components/cdtask/COMPONENT.md); that component is not independently invoked or installed.

CDF Suite maturity is **v0.1**. This is distinct from the package version recorded in `skill.json`.

## Ownership and Boundaries

CDF owns:

- requirement understanding and decomposition;
- repository evidence inspection and evidence-gap handling;
- risk classification;
- the Development Plan, verification strategy, and rollback plan;
- the canonical Scope Lock;
- full, conditional, and partial human approval;
- the user's `Execute Now` or `Save as Task` decision;
- implementation and actual verification after execution is authorized;
- saved-task validation and controlled resume.

CDF does not:

- modify code or persist a task before valid approval;
- infer approval from acknowledgement or silence;
- expand approved scope, perform adjacent cleanup, or add speculative flexibility;
- treat a planned verification as completed verification;
- invent a runtime, scheduler, worker assignment system, or automatic review system.

If an explicitly invoked request is purely informational and asks for no development change, answer it normally and state that the controlled development path was not entered.

## Entry Routes

### New Development Request

Run the complete workflow. A request to turn a PRD, requirement document, or idea into tasks does not bypass analysis: it must pass requirement understanding, evidence inspection, risk classification, planning, Scope Lock, and approval before task compilation.

### Continue a Saved Task

For `$cdf continue task <path>` or an equivalent natural-language request, follow [Resume a Saved Task](#resume-a-saved-task). Do not treat the saved document as self-authorizing.

## Controlled Development Workflow

### 1. Requirement Gate

Confirm the desired outcome, observable behavior, target repository or area, included and excluded scope, constraints, and acceptance criteria. Confirm that any named target exists before planning a modification.

Read [references/requirement-gate.md](references/requirement-gate.md) when the request is vague, incomplete, risky, specification-like, or likely to hide cross-cutting effects. Ask only questions whose answers can change implementation meaning, risk, scope, interfaces, data, state, or acceptance. Safe defaults must be explicit, narrow, reversible, and accepted by the user; they never bypass sensitive decisions.

If a named target does not exist, do not silently create or redirect it. Ask whether the intended action is creation, rename, or work on a different target.

### 2. Requirement Understanding

Separate the request into independently verifiable requirements. Record:

- confirmed desired behavior;
- constraints and explicit non-goals;
- dependencies and likely affected areas;
- material assumptions;
- open questions that still affect implementation.

Do not silently choose product behavior when multiple material interpretations remain.

### 3. Evidence Inspection

Inspect the smallest sufficient set of relevant code, configuration, tests, documentation, schemas, generated artifacts, and call sites. For each material conclusion, distinguish:

- **Fact** — directly supported by inspected evidence;
- **Inference** — reasoned from facts;
- **Assumption** — not yet verified and relevant to approval.

Prefer repository evidence over intuition. Keep inspection proportional to the plausible risk, but do not classify on visible diff size alone. Capture the absolute workspace path, source branch, source commit, and both of these worktree fields when available:

```text
Source-Worktree-State: <clean | dirty | Unavailable>
Source-Worktree-Changes:
- <stable git status entry for a relevant path>
```

Limit `Source-Worktree-Changes` to paths relevant to the candidate approved, affected, or protected areas; do not dump an unrelated large-repository status list. Preserve repository-relative paths and both characters of Git's stable `XY` status notation, including a leading space, and sort entries by path and then status. Quote entries when needed so YAML retains those bytes. Use an empty list when clean and a single `Unavailable` list entry plus the reason when the state cannot be read. Dirty state is an evidence and drift signal, not automatic proof of material risk or drift. Never overwrite or discard a user's uncommitted changes.

### 4. Risk Gate

Read [references/risk-classification.md](references/risk-classification.md) before final classification. Assess all six dimensions:

- impact;
- blast radius;
- reversibility;
- uncertainty;
- sensitivity;
- coordination requirements.

Complete the Mandatory Signal Record with `CLEAR`, `HIT`, or `UNKNOWN` and evidence for every row:

| ID | Signal |
|---|---|
| ESC-01 | Shared components, primitives, tokens, styles, or global state |
| ESC-02 | Conditional rendering, feature gates, entitlements, permissions, or user-specific behavior |
| ESC-03 | Persistent data writes/deletes, schema, migration, backfill, or user data |
| ESC-04 | Billing, payments, subscriptions, pricing, authentication, or authorization |
| ESC-05 | Reports, analytics, telemetry, revenue/cost/ROI, or business metrics |
| ESC-06 | Cache, jobs, sync, queues, retries, idempotency, events, webhooks, or consumers |
| ESC-07 | Internationalization, accessibility, compliance, security, privacy, or observability |
| ESC-08 | Application, deployment, environment, or production configuration |
| ESC-09 | Third-party APIs, external contracts, static delivery, or release packaging |
| ESC-10 | Architecture, new module/service, major redesign, migration coordination, or phased rollout |
| ESC-11 | Evidence is insufficient to bound a higher plausible risk |
| ESC-12 | Evidence materially conflicts about scope, behavior, ownership, risk, or impact |

Signals are evidence and may impose a risk floor; a signal is not the final risk by itself. In particular, a bounded shared component change, a small analytics event, bounded configuration, or bounded external-integration usage does not automatically require Level L. Use the impact-specific floors in the reference and the highest level supported by the combined evidence.

| Level | Typical boundary | Planning depth |
|---|---|---|
| **S** | One local cosmetic or static change; no behavioral or shared impact | Fast path: four lines |
| **M** | Bounded local behavior, small shared-component change, bounded configuration, or bounded external-integration usage | Brief, evidence-backed |
| **L** | Cross-cutting behavior, persistent data, billing, auth, security, privacy, materially meaningful analytics, meaningful external contracts, or non-trivial rollback | Detailed with rollback |
| **XL** | Architecture, new subsystem/service, migration, major data-flow redesign, phased rollout, or multi-system coordination | Design and approved phases |

Before Level S, complete the S Reverse Check. Before Level M, complete the M Reverse Check. An unresolved `UNKNOWN` forbids a level below the lowest plausible risk; if a safe bounded plan cannot be produced, stop as `BLOCKED`. An unresolved conflict that changes implementation meaning, scope, acceptance, or safety is also `BLOCKED`.

At Level S the signal record and Reverse Check are reasoning steps, not deliverables: assess every row, then report only the `PASS` result on the fast path's `Reverse Check` line. Show a signal row explicitly only when it is `HIT` or `UNKNOWN` — which also means the change is not Level S.

### 5. Development Plan and Scope Lock

Use the lightest plan that safely captures the evidence, risk, scope, implementation direction, and verification.

#### Level S Fast Path

A confirmed Level S change uses this form instead of the full plan:

```markdown
## Fast-Path Plan (Level S)
- Change: <the single target and the exact change>
- Will Not Change: <protected boundary>
- Verify: <observable check>
- Reverse Check: PASS (S-01..S-06)

Approve and execute? Or save as task?
```

This is the complete approval-ready artifact for Level S. Do not also produce the eleven canonical sections or a `cdf-scope/v1` block. `Change` is the approved scope, `Will Not Change` is the hard constraint, and `Verify` is the sole acceptance criterion. Approval still requires the user to name both the approved change and the authorized action.

The fast path is available only when the S Reverse Check passes on every row with no `UNKNOWN`. Any `FAIL` or `UNKNOWN` means the change is not Level S: classify it at the correct level and use the full plan.

Leave the fast path and produce a full Development Plan whenever evidence during execution shows a second target, behavioral impact, a shared consumer, or any signal that was assumed `CLEAR`. Selecting `Save as Task` also requires the full plan and canonical Scope Lock, because the task contract carries them: return to planning, expand the fast-path content into the canonical sections, and obtain approval of that expanded plan.

#### Full Development Plan

Every approval-ready plan at Level M, L, or XL contains:

```markdown
## Development Plan

### Requirement Understanding
<outcome, behavior, decomposition, constraints, and non-goals>

### Evidence Summary
<facts, sources, inferences, assumptions, gaps, and conflicts>

### Risk Gate Result
- Final Level: <M | L | XL>
- Dimensions: <impact, blast radius, reversibility, uncertainty, sensitivity, coordination>
- Mandatory Signals: <record or compact all-clear summary with evidence>
- Reverse Check: <M | Not Applicable>
- Rationale: <evidence-backed reason>

### Scope Lock
<complete canonical cdf-scope/v1 block>

### Technical Approach
<smallest viable implementation direction>

### Implementation Plan
<ordered changes and dependency boundaries>

### Risks
<material risks and mitigations; concise when none are material>

### Rollback Plan
<reversible action, or None only when rollback is genuinely not applicable>

### Acceptance Criteria
<repeat every canonical acceptance_criteria item verbatim, one item per entry, in the same order>

### Verification Strategy
<checks to run if execution is authorized>

### Next Action
1. Execute Now
2. Save as Task
```

These headings and their order are canonical. A handoff or saved task carries the approved sections directly; it does not rename, combine, split, or regenerate them. A Level S change promoted to a full plan for `Save as Task` uses these same headings. For Level M, `Rollback Plan` may be one concise reversible action or `None` only when rollback is genuinely not applicable. For Level L, name affected modules, ordered changes, regression risk, and rollback. For Level XL, also include the current architecture, proposed design, data/API/state flow, delivery phases, and the exact phase boundary awaiting approval.

For Level M, L, and XL, read [references/karpathy-guidelines.md](references/karpathy-guidelines.md) before finalizing the plan or implementing. For Level S, read it only when a prior attempt failed or extra minimal-change guidance is objectively useful.

### Phased Delivery

Treat each approved Level XL phase as a separate controlled round with its own Development Plan boundary, canonical Scope Lock, Approval Record, and selected Next Action. Approval of one phase never authorizes a later phase. After executing or saving the approved phase, stop or return to planning for the next phase; do not carry scope or authorization forward implicitly.

When approval covers one phase, record the boundary alongside the Approval Record:

```markdown
## Approved Phase Boundary
- Phase: <identifier and short name>
- Phase Scope: <what this phase delivers, matching canonical in_scope>
- Ends At: <the observable state that completes this phase>
- Explicitly Deferred: <later-phase work that this approval does not authorize>
```

Every phase-scoped handoff and saved task carries this block verbatim.

### Canonical Scope Lock

Every plan must contain exactly one canonical block:

```yaml
Scope-Lock-Version: cdf-scope/v1
in_scope:
  - <approved outcome or impact>
out_of_scope:
  - <explicit exclusion>
non_goals: []
assumptions: []
stop_conditions: []
will_change:
  - <approved affected area>
will_not_change:
  - <protected area or behavior>
acceptance_criteria:
  - <observable result>
```

All eight fields must exist, in exactly this order, because [Integrity Verification](#integrity-verification) defines the payload boundary by the first and last field. Empty arrays are valid when there is no meaningful content; never invent filler merely to populate them. Before approval the block may be revised visibly. After approval it is canonical immutable data:

- copy it verbatim to an internal task handoff or saved task;
- do not paraphrase, reorder, merge, omit, weaken, expand, re-indent, normalize, or silently add scope;
- treat `out_of_scope`, `non_goals`, and `will_not_change` as hard constraints;
- if execution or task compilation requires any change, return to planning, create a revised block, and obtain renewed approval.

`cdf-scope/v1.acceptance_criteria` is the single canonical acceptance source. The Development Plan's `### Acceptance Criteria` section is only a readable projection: it must contain every canonical criterion item for item, in the same order and exact wording. It cannot add, delete, weaken, broaden, reinterpret, merge, or split a criterion. Task-level criteria may only reference applicable canonical entries verbatim. Any newly required or changed criterion is a scope change: stop as `BLOCKED`, return to CDF planning, refresh the Development Plan and Scope Lock, and obtain renewed approval.

### 6. Human Approval

Approval is required for every risk level. It is valid only when the user identifies both:

1. the plan, Scope Lock, phase, or explicit subset being approved; and
2. the authorized action: `Execute Now` or `Save as Task`.

Valid examples:

- `Approve this plan and execute it.`
- `批准以上 Scope Lock，保存为任务。`
- `Approve Phase 1 only and execute it.`

Replies such as `ok`, `继续`, `可以`, `looks good`, or silence are not sufficient when the authorized action or approved scope is unclear. Ask for an explicit choice without exposing internal contract language. Re-ask at most twice for the unchanged plan; if approval remains ambiguous or is declined, stop without modifying code or saving a task.

Approval modes:

- **Full** — the complete Scope Lock and selected action are approved.
- **Conditional** — incorporate every condition into a revised Scope Lock, show it, and obtain explicit approval of that revision.
- **Partial** — revise the plan's single canonical block for only the approved subset; preserve every unapproved item verbatim in the result below and protect it through canonical exclusions.

If a partial subset cannot be isolated without a new implementation decision, semantic rewrite, or unsafe coupling, return to planning or remain `BLOCKED`.

Record valid approval:

```markdown
## Approval Record
- User Approval: <verbatim approval statement>
- Approval Context: <ISO-8601 timestamp when available, otherwise current conversation turn>
- User Choice: <Execute Now | Save as Task>
- Approval Type: <full | conditional | partial>
- Approved Items: <canonical in_scope items or exact subset>
- Conditions Added To Scope Lock: <none or exact conditions>
- Unapproved Items: <none or exact remainder>
- Scope Approved: Yes
- Code Changes Authorized In This Turn: <Yes for Execute Now; No for Save as Task>
```

An approved Level S fast path records only the approval statement, the user's choice, and the approved `Change` line; it has no canonical Scope Lock to cite. A full Approval Record is required whenever a full Development Plan is.

For partial approval, also emit this stable audit projection:

```markdown
## Partial Approval Result

Approval Type: partial

### Approved Items
- <verbatim approved item>

### Unapproved Items
- <verbatim unapproved item>

### Canonical Approved Scope
Scope-Lock-Version: cdf-scope/v1
```

Do not copy the full Scope Lock into `Partial Approval Result`. Only the Development Plan's `cdf-scope/v1` block is canonical. `Approved Items` must exactly match the approved canonical `in_scope` entries; `Unapproved Items` remains verbatim and is protected by canonical exclusions. The result exists for projection and audit only and creates no second source of authority. If the two sets cannot be separated without changing meaning or safety, stop as `BLOCKED`, return to planning, produce a revised Scope Lock, and obtain renewed approval.

Echo the locked scope and selected action after approval. The echo confirms the decision; it cannot broaden it. An Approval Record for `Save as Task` proves the approved scope and authorizes persistence only. It does not authorize future code changes. Preserve that record verbatim after saving and during every resume.

### 7A. Execute Now

After valid approval explicitly authorizes `Execute Now`:

1. compare the current repository branch and commit with the planning evidence when available;
2. re-check assumptions, stop conditions, protected areas, and the approved phase boundary;
3. implement only the canonical approved scope;
4. run only the verification appropriate to the approved change;
5. report changed files, observable results, checks actually run, failures, and any unverified criteria.

Do not perform unrelated refactors, cleanup, dependency additions, broad reformatting, public-interface changes, or protected-area edits. Remove only artifacts made obsolete by the approved change itself.

For an approved fast path, the approved scope is the `Change` line, the protected boundary is `Will Not Change`, and the acceptance criterion is `Verify`. Every rule below applies to those three lines exactly as it applies to a canonical Scope Lock.

Stop immediately and return to planning when new evidence changes scope, risk, implementation meaning, acceptance criteria, rollback, or a material assumption. Update the Development Plan and Scope Lock and request renewed approval before continuing.

Never describe a planned check as completed. A failed check may be repaired only inside approved scope; otherwise stop and replan.

### 7B. Save as Task

After valid approval explicitly authorizes `Save as Task`:

1. recheck the workspace, branch, commit, `Source-Worktree-State`, and relevant `Source-Worktree-Changes` against the approved planning evidence;
2. if drift is material, stop, return to planning, refresh evidence and risk, revise the Development Plan or Scope Lock when needed, and obtain renewed approval;
3. if drift is demonstrably non-material, record the preflight conclusion and use the latest traceability metadata in the handoff;
4. read [references/task-handoff.md](references/task-handoff.md);
5. create the internal `cdf-cdtask/v1` approved handoff;
6. read and enter [components/cdtask/COMPONENT.md](components/cdtask/COMPONENT.md);
7. validate approval, the canonical Scope Lock, and its acceptance projection;
8. compile dependency-aware tasks and run the Scope Guard;
9. persist the resumable document;
10. read it back and validate its contract, canonical payloads, and traceability;
11. return the saved path and stop.

The default destination is:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md
```

The internal component is already part of CDF. Do not request a separate installation and do not expose it as a Next Action. For a request whose desired deliverable is a task breakdown, `Save as Task` is the action that produces that durable definition; `Execute Now` means implementing the approved underlying development work, not returning an unsaved task list. The save preflight belongs to CDF; the internal compiler receives the latest metadata but does not assess requirements or regain planning authority. If task compilation discovers ambiguity, new scope, a changed acceptance criterion, an insufficient Scope Lock, or an inseparable partial remainder, it returns `BLOCKED`; CDF must re-enter planning, refresh the plan and Scope Lock package, and obtain renewed approval even when re-analysis leaves the Scope Lock text unchanged.

### Integrity Verification

The canonical Scope Lock and the Approval Record must survive persistence and resume unchanged. Verify that by comparing text, not by trusting a remembered value.

Each payload has these boundaries:

- the Scope Lock payload starts at `Scope-Lock-Version: cdf-scope/v1` and ends at the last `acceptance_criteria` entry, or at the `acceptance_criteria: []` line when that array is empty;
- the Approval Record payload starts at `## Approval Record` and ends at its last field;
- Markdown code-fence delimiters are excluded from both.

The eight Scope Lock fields must appear in the order shown in [Canonical Scope Lock](#canonical-scope-lock). A reordered block has no defined payload boundary and is rejected.

Compare payloads line by line: same line count, same order, same characters including indentation. Any difference in wording, indentation, ordering, or line breaks is a mismatch. Reject a mismatch and report it; never rewrite approved content to make a comparison succeed. Ambiguous boundaries, a duplicated canonical block, or trailing whitespace on a payload line are also rejections.

A SHA-256 digest is an optional convenience, never the verification itself. Record one only after actually running a hashing command over the exact payload bytes, for example by writing the payload to a temporary file and running `shasum -a 256`. Never write a digest that was not computed that way. When no digest was computed, record `Unavailable` and rely on text comparison, which is the authoritative check in either case.

## Resume a Saved Task

For an explicit continue request:

1. read the task document from the supplied path;
2. require `task_contract: cdf-cdtask/v1` and validate every required section;
3. apply [Integrity Verification](#integrity-verification) and require the persisted canonical Scope Lock and Approval Record to match their saved payloads line for line;
4. compare the current workspace, branch, commit, `Source-Worktree-State`, relevant `Source-Worktree-Changes`, code, and dependencies with the saved traceability for material drift;
5. re-check assumptions, stop conditions, phase boundaries, partial-approval exclusions, acceptance criteria, and verification obligations;
6. decide whether the approved implementation meaning is still valid.

Reject a missing, legacy, or unrecognized task contract without modifying code.

Material drift, a failed assumption, new scope, changed risk, or changed acceptance returns to planning and renewed approval. Do not execute a stale task.

When validation succeeds, the user's explicit `continue task <path>` request is the new current-turn action authorization. Resolve the path absolutely and create this runtime record without modifying the persisted task or its Approval Record:

```markdown
## Resume Authorization Record
- User Request: <verbatim current continue request>
- Task Path: <resolved absolute path>
- Authorized Action: Execute Saved Approved Scope
- Scope Source: persisted cdf-scope/v1
- Authorization Context: <timestamp when available, otherwise current conversation turn>
- Code Changes Authorized In This Turn: Yes
```

Only after this record exists may CDF execute tasks in dependency order under the same guardrails as `Execute Now`. A request merely to inspect, review, summarize, or validate a task neither creates a Resume Authorization Record nor authorizes implementation.

## Repository Drift

Capture `Workspace`, `Source-Branch`, `Source-Commit`, `Source-Worktree-State`, and `Source-Worktree-Changes` in approved task handoffs when available. The changes list must preserve both Git `XY` status characters for repository-relative paths, including leading spaces, sort by path and then status, and stay limited to approved, affected, or protected paths. Re-check committed and uncommitted state immediately before execution, before persistence, and on resume. A branch, commit, dirty-state, or listed-path difference is a drift signal, not automatically material; inspect whether it changes approved implementation meaning, affected files, assumptions, risk, acceptance, verification, or rollback. Material drift requires refreshed planning and renewed approval. Record demonstrably non-material drift and proceed with current metadata. If traceability is unavailable, disclose the gap and apply the uncertainty rules from the Risk Gate.

## References

- [Requirement Gate](references/requirement-gate.md) — read for ambiguous, risky, PRD-like, or specification-like requests.
- [Risk Classification](references/risk-classification.md) — read before final risk classification.
- [Karpathy Guidelines](references/karpathy-guidelines.md) — read for Level M/L/XL planning and implementation.
- [Boundary Cases](references/boundary-cases.md) — read when a request, approval, evidence conflict, or partial scope is near a control boundary.
- [Task Handoff](references/task-handoff.md) — read only for `Save as Task` or saved-task resume.
- [Internal Task Compiler](components/cdtask/COMPONENT.md) — enter only after approved `Save as Task`.

## Non-Negotiable Rules

- CDF is the only user-facing controlled-development entrypoint.
- Complete requirement analysis, repository evidence inspection, risk classification, planning, Scope Lock, and human approval before any implementation or task compilation.
- Never infer action or scope approval from an ambiguous acknowledgement.
- Never expand or rewrite approved scope.
- Treat `cdf-scope/v1.acceptance_criteria` as the sole canonical acceptance authority.
- Treat saved approval as persistence authority, not future execution authority.
- Never let the internal task compiler make product, architecture, risk, scope, or approval decisions.
- Never continue after material drift or new evidence invalidates the approved plan.
- Never claim verification that was not actually performed.
- Never record a digest that was not actually computed by running a hashing command.
- Keep planning proportional: a Level S change is approved from four lines; risky or architectural work gets the full plan.
