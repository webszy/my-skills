---
name: cdf
description: Run a controlled development workflow that understands a development request or PRD, inspects repository evidence, classifies risk, locks scope, obtains explicit human approval, then executes the approved work or saves it as a resumable task. Use when the user explicitly invokes /cdf, $cdf, cdf:, or controlled-development-flow, or explicitly asks for a controlled development flow.
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

## Output First Line

While the CDF workflow is active, begin every user-facing response, including progress updates, clarification or approval requests, blocked results, save confirmations, resume confirmations, and final reports, with this plain-text line:

```text
当前流程：cdf v<version>
```

Read `version` from [skill.json](skill.json) in the same skill directory before the first CDF response. For package version `1.3.0`, the line is `当前流程：cdf v1.3.0`. Use the package version, not Suite maturity or a contract version; do not hardcode the example as the version source. If the metadata cannot be read, use `当前流程：cdf 版本未知` and briefly disclose the missing version instead of guessing. Put the line before any heading or other content, then a blank line. It is a display prefix, not an additional planning section: all response templates below inherit it. Do not inject it into canonical payloads, task-file frontmatter, or progress files; an exact preserved Approval Summary retains it if it was displayed. Merely discussing CDF without entering its workflow does not require this prefix.

## Agent Activity Disclosure

Every user-facing CDF response must also briefly state these two items in the user's language, after its main content and before any approval/action question:

- **当前 Agent 已做 / Current Agent Actions:** work actually performed, including inspections, edits, validation attempts and their results, and any additional work beyond the current request. Distinguish performed actions from planned or unexecuted work. Progress updates cover actions since the previous update; final, blocked, save, and handoff reports cover the current request cumulatively and identify any extra work and why it was done.
- **与当前需求无关的代码改动 / Code Changes Unrelated to This Request:** list every unrelated code/configuration/documentation edit attributable to the current Agent during this request, with file paths, what changed, why, authorization evidence if any, and whether it remains or was reverted. Explicitly write `无` / `None` when evidence establishes there were none, or `无法确认` / `Unknown` with the evidence gap when attribution cannot be established. Preserved pre-existing or other Agents' edits are not this Agent's work; identify them separately when relevant.

Base these disclosures on observed actions and the inspected execution baseline, tool receipts, and diff/content evidence. A clean final diff does not erase an unrelated edit that was reverted. Disclosure never authorizes unrelated work or relaxes the existing scope/approval rules. Keep the two items concise; they do not add canonical planning sections or modify immutable saved-task payloads. Completion reports reuse `completion_gate.evidence` for actual Agent activity and `out_of_scope_changes` for unrelated edits as specified in [Completion Evidence Gate](references/completion-evidence-gate.md).

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
- invent a background runtime, scheduler, worker assignment system, or automatic review system; the saved-task progress sidecar is only an execution journal.

If an explicitly invoked request is purely informational and asks for no development change, answer it normally and state that the controlled development path was not entered. Mentioning the name `cdf`, discussing its files, or explicitly declining CDF is not an invocation.

## Entry Routes

### New Development Request

Run the complete workflow. A request to turn a PRD, requirement document, or idea into tasks does not bypass analysis: it must pass requirement understanding, evidence inspection, risk classification, planning, Scope Lock, and approval before task compilation.

### Read-only Planning Draft

An explicit request to “generate a task breakdown draft, do not execute or save” permits requirement analysis, repository evidence, risk assessment and an **unapproved draft** in the response. Do not enter CDTask, save a formal task, create Runtime Progress or execution authorization, or label the draft approved. A proposed scope is not a trusted Scope Lock. To implement or persist later, expose the actual plan and complete normal approval. Draft decomposition may use the task template only if useful; it is not an approved-tasking handoff.

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
Source-Worktree-Changes: <[] | [Unavailable] | [' M src/foo.ts', '?? src/new-file.ts']>
```

Represent `Source-Worktree-Changes` as one flow-style YAML array. Limit it to paths relevant to the candidate approved, affected, or protected areas; do not dump an unrelated large-repository status list. Preserve repository-relative paths and both characters of Git's stable `XY` status notation, including a leading space, quote every dirty entry, and sort entries by path and then status. Use `[]` when no relevant changes exist and `[Unavailable]` plus the reason when the state cannot be read. Dirty state is an evidence and drift signal, not automatic proof of material risk or drift. Never overwrite or discard a user's uncommitted changes.

For Level M/L/XL planning and any saved task, identify the sources the plan relies on in the internal evidence record, including read-only APIs, shared contracts, configuration, schemas, and relevant callers outside the write scope or protected areas. Record their paths or source identifiers and a retrievable revision or actually computed content digest; carry this record into the saved plan's Evidence Summary. Include relevant dirty and untracked content: Git status entries identify paths, not content baselines. These dependencies are affected evidence for drift checks; recording them grants no write permission. If a baseline cannot be established, record the gap and apply the Risk Gate's uncertainty rules.

### 4. Risk Gate

First test a Level S candidate against every row below:

| ID | Required condition |
|---|---|
| S-01 | Exactly one identified local presentation target; bounded local usage of an existing shared parameter is allowed |
| S-02 | Copy, spacing, color, icon size, or other static presentation only |
| S-03 | No behavior, state, API, data, contract, configuration, or generated-artifact change |
| S-04 | Acceptance and verification are local to the target |
| S-05 | The change is explicit, trivially reversible, and requires no adjacent cleanup |
| S-06 | Evidence is sufficient and consistent, with no shared definition/API/token edit, other-consumer impact or changed conditional behavior, persistence, money or access, analytics, background work, sensitive concern, configuration, external contract, architecture, evidence gap, or evidence conflict |

Record `PASS`, `FAIL`, or `UNKNOWN` with evidence for every row. All six rows must be `PASS` to use the Level S Fast Path. A definite Level S candidate does not load the full risk reference. Any `FAIL`, `UNKNOWN`, or plausible non-S category requires reading [references/risk-classification.md](references/risk-classification.md), completing its Mandatory Signal Record and applicable M Reverse Check, and then assessing all six dimensions:

- impact;
- blast radius;
- reversibility;
- uncertainty;
- sensitivity;
- coordination requirements.

Bounded Local Usage means an already-supported static parameter at one call site, unchanged shared definition, public interface and global token, unchanged behavior and other consumers, with independent verification and rollback. Inspect the shared contract and affected consumers before marking S-01/S-06 PASS. File count or merely importing a shared component establishes neither S nor a risk floor.

Signals are evidence and may impose a risk floor; a signal is not the final risk by itself. Use the impact-specific floors in the risk reference and the highest level supported by the combined evidence.

| Level | Typical boundary | Planning depth |
|---|---|---|
| **S** | One local cosmetic or static change; no behavioral or shared impact | Fast path: four lines |
| **M** | Bounded local behavior, small shared-component change, bounded configuration, or bounded external-integration usage | Brief, evidence-backed |
| **L** | Cross-cutting behavior, persistent data, billing, auth, security, privacy, materially meaningful analytics, meaningful external contracts, or non-trivial rollback | Detailed with rollback |
| **XL** | Architecture, new subsystem/service, migration, major data-flow redesign, phased rollout, or multi-system coordination | Design and approved phases |

Before Level S, complete the local S Reverse Check above. Before Level M, complete the M Reverse Check in the risk reference. An unresolved `UNKNOWN` forbids a level below the lowest plausible risk; if a safe bounded plan cannot be produced, stop as `BLOCKED`. An unresolved conflict that changes implementation meaning, scope, acceptance, or safety is also `BLOCKED`.

At Level S the S Reverse Check is a reasoning step, not a full deliverable: assess every row, then report only the aggregate `PASS` result on the fast path's `Reverse Check` line. Show a row explicitly only when it is `FAIL` or `UNKNOWN` — which also means the change is not yet eligible for the fast path.

### 5. Development Plan and Scope Lock

Use the lightest plan that safely captures the evidence, risk, scope, implementation direction, and verification.

#### User-Facing Approval Summary

For Level M/L/XL, show a concise summary in the user's language before requesting approval. Prefer these four sections, normally one to three short bullets each; this is a brevity target, not permission to omit a material decision:

```markdown
### Requirement Understanding
<desired outcome, included scope, and meaningful exclusions>

### Technical Approach
<the proposed solution and any decision the user needs to make>

### Implementation Plan
<short ordered steps, ending with observable acceptance and how it will be checked>

### Risks
<material risks, unresolved conditions, and rollback implications; one short sentence when none are material>

<If action is already explicit: Approve this plan and execute? / Approve this plan and save as task? Otherwise: Approve and execute, or approve and save as task?>
```

Use natural localized labels when helpful, such as 需求理解、技术方案、实施步骤、风险. Keep the approval question to one sentence. Fold important protected boundaries into Requirement Understanding, acceptance and verification into Implementation Plan, and approval-affecting assumptions or stop conditions into Risks. For XL, state the current phase's scope, completion boundary, and deferred phases within these sections. Include the risk level only when it helps the decision. Do not print the eleven-section plan, evidence inventory, signal or reverse-check tables, canonical YAML, hashes, or raw approval/progress records by default. Show full details when the user asks for them. Material uncertainty, sensitive effects, and required decisions must remain visible even when more space is needed.

Complete evidence inspection, risk assessment, implementation and rollback planning before presenting the summary. For M/L/XL, prepare the canonical Scope Lock in working context before approval; do not persist an unapproved task. The summary must faithfully expose every approved outcome, technical decision, acceptance requirement, material assumption, stop condition, and protected boundary. Internal detail can support these statements but cannot add hidden obligations or authority. Check that the summary and planning record agree before asking. If they cannot be expressed concisely without losing meaning, expand only the affected section.

Approval of this summary and a selected action authorizes only the meaning actually presented. Keep the exact approved summary as approval evidence. If the user instead explicitly requests and approves the complete plan, preserve that displayed plan as the approval basis without creating a duplicate summary or Scope Lock. **Execute Now** uses the corresponding planning record and canonical scope directly; it does not require rendering eleven sections. **Save as Task** lets CDF organize that already-approved material into the complete document format in Task Handoff before entering the internal compiler. This is formatting and evidence transcription only: do not add decisions, scope, acceptance criteria, risks requiring consent, or verification obligations. Any such discovery requires an updated concise summary and renewed approval; document formatting alone does not.

#### Level S Fast Path

A confirmed Level S change uses this form instead of the full plan:

```markdown
## Fast-Path Plan (Level S)
- Change: <the single target and the exact change>
- Will Not Change: <protected boundary>
- Verify: <observable check>
- Reverse Check: PASS (S-01..S-06)

<Confirm the already-selected action; offer execute/save only if still unspecified.>
```

This is the complete approval-ready artifact for Level S. Do not also produce the eleven canonical sections or a `cdf-scope/v1` block. `Change` is the approved scope, `Will Not Change` is the hard constraint, and `Verify` is the sole acceptance criterion. Approval must unambiguously bind the displayed change and authorized action, using the established conversation context.

The fast path is available only when the S Reverse Check passes on every row with no `UNKNOWN`. Any `FAIL` or `UNKNOWN` means the change is not Level S: classify it at the correct level and use the full plan.

Leave the fast path, reassess risk, and show the concise approval summary whenever evidence during execution shows a second affected target, behavioral impact, a shared definition change or impact on other consumers, or any signal that was assumed `CLEAR`. For an approved `Save as Task`, CDF must assemble the full document plan and canonical Scope Lock before handoff. Map the approved `Change`, `Will Not Change`, and `Verify` without changing their meaning, keep risk at Level S, and preserve the approval statement. Derive only mechanical detail from inspected evidence; use empty optional arrays or genuine `None` where appropriate. Do not seek approval again merely for this expansion. If a material decision or missing acceptance requirement is discovered, revise the concise summary and obtain renewed approval.

#### Full Development Plan

For M/L/XL, read [Coding Discipline](references/karpathy-guidelines.md) before finalizing or implementing the plan. Keep the approval display concise while exposing all material decisions. At M include affected modules, checks and rollback; at L include cross-cutting effects and regression risks; at XL include current/proposed architecture, data/API/state flow and approved phases.

Only for **Save as Task**, load [Task Handoff](references/task-handoff.md) for the eleven-section document plan. CDF organizes already-approved material, checks it against the exact displayed approval basis, then freezes it. CDTask copies that plan verbatim. Formatting alone needs no second approval; any new obligation or decision does.

### Phased Delivery

Treat each approved Level XL phase as a separate controlled round with its own planning boundary, canonical Scope Lock, Approval Record, and selected Next Action. Show the phase boundary in the concise summary. Approval of one phase never authorizes a later phase. After executing or saving the approved phase, stop or return to planning for the next phase; do not carry scope or authorization forward implicitly.

When approval covers one phase, record its identifier, exact approved scope, observable end boundary and explicitly deferred work. In a saved task, serialize the Approved Phase Boundary as specified by [Persistence](components/cdtask/references/persistence.md) before freezing the handoff. Chat needs only the concise boundary unless requested.

### Canonical Scope Lock

Prepare one canonical Scope Lock in the internal planning record for M/L/XL. Every full saved-document Development Plan must contain exactly one such block; an S task maps its approved fast-path content as described above. The YAML is internal control data and saved-file content, not a required user-facing approval display:

```yaml
Scope-Lock-Version: cdf-scope/v1
in_scope: ["<approved outcome or impact>"]
out_of_scope: ["<explicit exclusion>"]
non_goals: []
assumptions: []
stop_conditions: []
will_change: ["<approved affected area>"]
will_not_change: ["<protected area or behavior>"]
acceptance_criteria: ["<observable result>"]
```

All eight fields must exist, in exactly this order, as the canonical payload. For a v2 saved task, use the shown single-line JSON arrays in YAML before approval; the scope schema itself remains v1. A valid block requires at least one non-empty `in_scope` entry and at least one non-empty `acceptance_criteria` entry. The other arrays may be empty when there is no meaningful content; never invent filler merely to populate them. A partial or conditional result with no approved `in_scope` item is `BLOCKED`, not an empty approved plan. Before approval, revise the working block and expose any material change in the summary. After approval (or the purely mechanical mapping of an approved S task), it is canonical immutable data:

- copy it verbatim to an internal task handoff or saved task;
- do not paraphrase, reorder, merge, omit, weaken, expand, re-indent, normalize, or silently add scope;
- treat `out_of_scope`, `non_goals`, and `will_not_change` as hard constraints;
- if execution or task compilation requires any change, return to planning, create a revised block, and obtain renewed approval.

`cdf-scope/v1.acceptance_criteria` is the single canonical acceptance source. The Development Plan's `### Acceptance Criteria` section is only a readable projection: it must contain every canonical criterion item for item, in the same order and exact wording. It cannot add, delete, weaken, broaden, reinterpret, merge, or split a criterion. Task `contributes_to` references identify canonical entries without changing them. Task Verification checks only local deliverables using approved technical direction and Verification Strategy; it is not product acceptance. Full canonical coverage and planned product verification remain mandatory. Any newly required or changed criterion is a scope change: stop as `BLOCKED`, return to CDF planning, refresh the Development Plan and Scope Lock, and obtain renewed approval.

For saved tasks, require coverage in both directions: every contribution must reference a canonical criterion, and every canonical entry must have at least one task mapping and a corresponding planned check. Enforce this at compilation, read-back, and resume validation. Completion additionally requires current successful evidence for every canonical entry; checking only the criteria selected by existing tasks is insufficient.

### 6. Human Approval

Approval is required for every risk level. It is valid only when the user identifies both:

1. the displayed concise plan, full plan if explicitly requested, phase, or explicit subset being approved; and
2. the authorized action: `Execute Now` or `Save as Task`.

Valid examples:

- `Approve this plan and execute it.`
- `批准以上 Scope Lock，保存为任务。`
- `Approve Phase 1 only and execute it.`

Replies such as `ok`, `继续`, `可以`, `looks good`, or silence are not sufficient when the authorized action or approved scope is unclear. Ask for an explicit choice without exposing internal contract language. Re-ask at most twice for the unchanged plan; if approval remains ambiguous or is declined, stop without modifying code or saving a task.

Do not ask for an action already explicitly selected in the conversation. “Analyze, then ask me to approve execution” establishes Execute Now as the proposed action, not approval of an unseen plan: ask only “是否批准以上方案并执行？” A clear approval of that displayed plan/action can be used without re-selection. Ambiguous acknowledgements still do not authorize ambiguous scope or action. A concrete user-supplied plan explicitly authorized for implementation is already an approval basis; do not invent a second approval solely to reformat it.

Approval modes:

- **Full** — the displayed plan's complete scope and selected action are approved; its internal Scope Lock must match that meaning.
- **Conditional** — incorporate every condition into the working Scope Lock, show the updated concise summary, and obtain explicit approval of that revision.
- **Partial** — revise the plan's single canonical block for only the approved subset; preserve every unapproved item verbatim in the result below and protect it through canonical exclusions.

If a partial subset cannot be isolated without a new implementation decision, semantic rewrite, or unsafe coupling, return to planning or remain `BLOCKED`.

Record the exact user statement, timestamp/turn context, selected action, approval type, canonical approved items, conditions and unapproved remainder internally. Execute Now uses that record directly; an S fast path needs only its statement, chosen action and Change line. Save as Task uses the [v2 Approval Record serialization](components/cdtask/references/persistence.md) before CDF freezes the handoff. The exact displayed summary or full plan remains approval evidence. Never invent a statement or treat hidden content as authorization.

For partial approval, retain a projection of exact approved/unapproved items without copying a second Scope Lock. Approved Items equal canonical in_scope; the unapproved remainder remains protected by canonical exclusions. Serialize the saved projection under Persistence. Unsafe separation requires a revised plan and renewed approval. Chat briefly identifies the approved subset and deferred remainder; raw records are shown only on request.

After approval, confirm the approved scope and selected action in one short sentence; do not repeat the plan or dump internal records. The confirmation cannot broaden the decision. A valid Approval Record for `Save as Task` records the approved scope and persistence authorization only; its provenance must be checked. It does not authorize future code changes. Preserve that record verbatim after saving and during every resume.

### 7A. Execute Now

After valid approval explicitly authorizes `Execute Now`:

1. compare the current repository branch and commit with the planning evidence when available;
2. re-check assumptions, stop conditions, protected areas, and the approved phase boundary;
3. implement only the canonical approved scope;
4. run only the verification appropriate to the approved change;
5. apply the [Completion Evidence Gate](references/completion-evidence-gate.md), retaining its complete structured report for every completion request;
6. only after `PASS`, perform and record the final scoped review and satisfy all applicable Review and Human Approval requirements before CDF declares completion. Report changed files, observable results, checks actually run, failures, and any unverified criteria even when completion is blocked.

For Level S, retain full evidence internally but default to four user-facing lines: `Changed`, `Verified`, `Scope`, `Remaining Issues`, plus required activity disclosure. Expand failures, risks, unauthorized changes or missing evidence; brevity never hides them.

Do not perform unrelated refactors, cleanup, dependency additions, broad reformatting, public-interface changes, or protected-area edits. Remove only artifacts made obsolete by the approved change itself.

For an approved fast path, the approved scope is the `Change` line, the protected boundary is `Will Not Change`, and the acceptance criterion is `Verify`. Every rule below applies to those three lines exactly as it applies to a canonical Scope Lock.

Stop immediately and return to planning when new evidence changes scope, risk, implementation meaning, acceptance criteria, rollback, or a material assumption. Update the Development Plan and Scope Lock and request renewed approval before continuing.

Never describe a planned check as completed. A failed check may be repaired only inside approved scope; otherwise stop and replan.

### Completion Evidence Gate

**Agent can propose completion, but only CDF can declare DONE.** Read [references/completion-evidence-gate.md](references/completion-evidence-gate.md) before evaluating any execution completion request, including a resumed saved task. An Agent's `Done`, `Completed`, report status, or task-state label is a proposal, never transition authority.

The gate sits after verification and before final review in the existing completion path (`VERIFYING → REVIEWING → DONE` conceptually). These are phase labels, not new lifecycle states: saved execution keeps its existing task states and `overall_state: completed`. CDF checks actual acceptance, validation, diff, scope, and issue evidence and outputs `PASS`, `FAIL`, or `INSUFFICIENT_EVIDENCE`. Only `PASS` admits final review; it never completes work automatically or waives existing approval. A finding that invalidates acceptance/evidence or a subsequent relevant change requires reevaluation before completion. Reuse existing in-scope repair, replanning, or `BLOCKED` handling when the gate does not pass.

### 7B. Save as Task

After valid approval explicitly authorizes `Save as Task`:

1. recheck the workspace, branch, commit, `Source-Worktree-State`, and relevant `Source-Worktree-Changes` against the approved planning evidence;
2. if drift is material, stop, return to planning, refresh evidence and risk, revise the Development Plan or Scope Lock when needed, and obtain renewed approval;
3. if drift is demonstrably non-material, record the preflight conclusion and use the latest traceability metadata in the handoff;
4. read [references/task-handoff.md](references/task-handoff.md);
5. assemble the eleven-section document plan from the approved material, preserve the exact displayed approval basis (the summary, or the full plan when explicitly approved), check that the plan and canonical scope add no undisclosed meaning, then freeze the package and create the internal `cdf-cdtask/v2` approved handoff;
6. read and enter [components/cdtask/COMPONENT.md](components/cdtask/COMPONENT.md);
7. validate approval, the canonical Scope Lock, and its acceptance projection;
8. compile dependency-aware tasks and run the Scope Guard;
9. compute both canonical payload digests and the complete definition digest at save, then persist the resumable document;
10. read it back and validate its contract, canonical payloads, digests, and traceability;
11. return the saved path and stop.

The default destination is:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md
```

The internal component is already part of CDF. Do not request a separate installation and do not expose it as a Next Action. For a durable task breakdown, `Save as Task` creates the definition; `Execute Now` implements the underlying approved work. An explicitly requested read-only draft uses the draft route without either action. The save path creates no execution-progress sidecar because persistence approval is not execution authorization. The save preflight belongs to CDF; the internal compiler receives the latest metadata but does not assess requirements or regain planning authority. If task compilation discovers ambiguity, new scope, a changed acceptance criterion, an insufficient Scope Lock, or an inseparable partial remainder, it returns `BLOCKED`; CDF must re-enter planning, refresh the plan and Scope Lock package, and obtain renewed approval even when re-analysis leaves the Scope Lock text unchanged.

### Integrity Verification

Only for save or saved-task validation, read [Persistence and Integrity](components/cdtask/references/persistence.md). At save, compare approved payloads verbatim, compute Scope Lock, Approval Record and **complete definition** SHA-256 values, then read back and verify the final file. The definition digest excludes only its own frontmatter line. First execution and every resume use this saved baseline; never establish trust from current contents on first resume. Self-contained hashes detect limited integrity failures; they are not approval signatures.

## Resume a Saved Task

Load [Resume and Compatibility](references/resume.md) for saved-task inspect, first execution or continuation. Validate the task and existing progress read-only, reconcile repository drift and historical work, then require a current explicit execution request before creating authorization or mutating progress. Save and read-only inspect grant no execution authority. Preserve legacy files; never reinterpret v1 as v2 or silently add missing digests.

## Repository Drift

Capture `Workspace`, `Source-Branch`, `Source-Commit`, `Source-Worktree-State`, and flow-style `Source-Worktree-Changes` in approved task handoffs when available. The changes array must preserve both Git `XY` status characters for repository-relative paths, including leading spaces, sort by path and then status, and stay limited to approved, affected, or protected paths, including read-only evidence dependencies. Re-check committed and uncommitted content and the Evidence Summary's source baselines immediately before execution, before persistence, and on resume. A branch, commit, dirty-state, or listed-path difference is a drift signal, not automatically material; inspect whether it changes approved implementation meaning, affected files, assumptions, risk, acceptance, verification, or rollback. The expected progress sidecar is execution metadata, not implementation drift, but its binding and contents must validate. On resume, reconcile approved execution output before classifying drift. Material drift follows the Full-Replan Path and its new-plan action routing. Record demonstrably non-material drift and proceed with current metadata without rewriting approved planning evidence. If traceability is unavailable, disclose the gap and apply the uncertainty rules from the Risk Gate.

## References

- [Requirement Gate](references/requirement-gate.md) — read for ambiguous, risky, PRD-like, or specification-like requests.
- [Risk Classification](references/risk-classification.md) — read when the compact S Reverse Check does not definitively pass.
- [Karpathy Guidelines](references/karpathy-guidelines.md) — read for Level M/L/XL planning and implementation.
- [Boundary Cases](references/boundary-cases.md) — read when a request, approval, evidence conflict, or partial scope is near a control boundary.
- [Task Handoff](references/task-handoff.md) — load only for `Save as Task`; resume loads the dedicated resume reference.
- [Resume and Compatibility](references/resume.md) — read only for saved-task inspect, first execution or continuation.
- [Execution Progress](references/execution-progress.md) — read only before executing or resuming a saved task.
- [Completion Evidence Gate](references/completion-evidence-gate.md) — read before any execution completion decision; includes the report contract and behavioral test cases.
- [Internal Task Compiler](components/cdtask/COMPONENT.md) — enter only after approved `Save as Task`.

## Non-Negotiable Rules

- CDF is the only user-facing controlled-development entrypoint.
- Complete requirement analysis, repository evidence inspection, risk classification, planning, Scope Lock, and human approval before any implementation or task compilation.
- Never infer action or scope approval from an ambiguous acknowledgement.
- Never expand or rewrite approved scope.
- Treat `cdf-scope/v1.acceptance_criteria` as the sole canonical acceptance authority.
- Treat saved approval as persistence authority, not future execution authority.
- Keep saved-task runtime state only in a validated `cdf-execution-progress/v2` sidecar.
- Never let the internal task compiler make product, architecture, risk, scope, or approval decisions.
- Never continue after material drift or new evidence invalidates the approved plan.
- Never claim verification that was not actually performed.
- Never declare execution complete or record `overall_state: completed` without a current Completion Evidence Gate `PASS`, a successful final scoped review, and all applicable approvals.
- Never record a digest that was not actually computed by running a hashing command.
- Keep approval display proportional: Level S uses four lines; M/L/XL use a concise four-section summary. Complete the underlying analysis, but reserve the eleven-section format for the handoff and saved task unless the user requests full details.
