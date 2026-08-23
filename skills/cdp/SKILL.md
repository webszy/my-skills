---
name: cdp
description: Transform development requirements into evidence-based plans, classify risk, lock scope, prepare approval materials, and decide the next path. Use when the user invokes cdp, $cdp, cdp:, or controlled-development-planning; when CDF requests managed planning; or when unclear, scoped, or high-risk work needs a decision between Execute Now, CDTask handoff, or return to CDF. CDP is not a runtime controller.
---

# CDP: Controlled Development Planning

## Quick Understanding

> CDP is the risk-aware planning layer of the CDF Suite: understand the requirement, inspect evidence, classify risk, lock scope, prepare an approval-ready plan, and ask the user to choose the next action.

**Small changes should be fast. Risky changes should be controlled.**

CDP is a planning and decision point, not a runtime. A standalone flow may continue after valid approval and an explicit user choice; a CDF-managed flow always returns the approved planning package to CDF.

## Position in the CDF Suite

```text
Requirement
    ↓
CDF Assessment
    ↓
CDP: Understand → Inspect Evidence → Classify Risk → Plan → Lock Scope
    ↓
Human Plan Approval
    ↓
Next Action
    ├─ standalone: Execute Now | Save as CDTask
    └─ cdf-managed: Return Approved Plan Package to CDF
```

| Skill | Role | CDP relationship |
|---|---|---|
| `cdf` | Control plane and human-gate coordination | Invokes CDP in `cdf-managed` context and receives the Approved Plan Package |
| `cdp` | Risk-aware planning, Scope Lock, and next-action decision | Owns the planning decision point |
| `cdtask` | Approved-plan conversion into verifiable task definitions | Optional destination selected after approval |

## Responsibilities and Boundaries

CDP owns:

- requirement understanding and decomposition;
- evidence inspection and conflict handling;
- risk classification and escalation;
- development planning and verification strategy;
- canonical Scope Lock creation;
- approval-material preparation;
- next-action recommendation.

CDP does not own:

- CDF lifecycle coordination;
- CDTask task decomposition;
- scheduling, runtime management, or execution-state orchestration;
- automatic implementation or persistence before approval;
- implementation review.

Standalone continuation does not make CDP a runtime controller.

## Operating Contexts

Determine the context before planning.

### `standalone`

The user invokes CDP directly. CDP must:

1. analyze the requirement and evidence;
2. classify risk and prepare the plan;
3. request plan approval and an explicit Next Action;
4. after valid approval, follow the user's choice:
   - `Execute Now`; or
   - `Save as CDTask`.

Never transition automatically from planning to implementation or persistence.

### `cdf-managed`

CDF invokes CDP and retains lifecycle ownership. CDP must:

1. analyze, classify, and plan;
2. run the Approval Gate directly with the user and reach a final approval outcome;
3. return an Approved Plan Package to CDF carrying that outcome as `Planning Status`;
4. stop.

CDP owns the approval gate in this context: it displays the plan, judges whether a reply is valid approval, re-asks when it is not, and records the result. CDF checks only that a completed Approval Record exists before handing off. Never return an unfinished gate to CDF.

In this context, do not modify code, invoke CDTask, create a local task file, or continue the lifecycle.

CDF declares this context with `Context: cdf-managed` and `Lifecycle-Owner: cdf`. If neither is present and the context is ambiguous, ask whether CDF owns the lifecycle before choosing a handoff path.

## Workflow

```text
Requirement Gate
    ↓
Requirement Understanding
    ↓
Evidence Inspection
    ↓
Mandatory Escalation Checklist
    ↓
S or M Reverse Check, when applicable
    ↓
Final Risk Classification
    ↓
Development Plan + Scope Lock
    ↓
Human Approval
    ↓
Next Action Decision
```

### 1. Requirement Gate

Read [references/requirement-gate.md](references/requirement-gate.md) when a request is vague, incomplete, risky, specification-like, or likely to hide cross-cutting effects. Use it before final planning.

Confirm at least:

- desired outcome and user-visible behavior;
- target repository, module, page, or component;
- in-scope and excluded behavior;
- constraints, assumptions, and acceptance criteria;
- whether the named target exists.

If the target does not exist, do not silently create a replacement. Ask whether to create, rename, or redirect the work.

### 2. Requirement Understanding

Separate the request into independently verifiable requirements. Record:

- confirmed facts;
- assumptions;
- open questions;
- dependencies and affected areas;
- explicit non-goals.

Do not invent product behavior or silently resolve material ambiguity.

### 3. Evidence Inspection

Inspect relevant code, configuration, tests, documentation, schemas, and call sites before making claims. For each important conclusion, distinguish:

- **Fact** — directly supported by evidence;
- **Inference** — reasoned from evidence;
- **Assumption** — unverified and approval-relevant.

Prefer evidence from the repository over intuition. Keep inspection proportional to likely risk.

## Risk Gate

The following checklists are mandatory operational gates, not reference material. Before finalizing Level S or M, complete every row and record `CLEAR`, `HIT`, or `UNKNOWN` plus evidence.

### Mandatory Escalation Checklist

| ID | Signal to inspect | Status | Evidence |
|---|---|---|---|
| ESC-01 | Shared components/primitives, theme/tokens/styles, or global state | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-02 | Conditional rendering, feature gates, entitlements, permissions, or user-specific behavior | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-03 | Persistent data writes/deletes, schema, migration, backfill, or user data | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-04 | Billing/payment/subscription/pricing, authentication, or authorization | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-05 | Reports, analytics, telemetry, tracking, revenue/cost/ROI, or business metrics | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-06 | Cache, jobs/cron/sync, queues/retries/idempotency, events/webhooks/consumers | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-07 | i18n, accessibility, compliance, security, privacy, or observability | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-08 | Application, deployment, environment, or production configuration | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-09 | Third-party APIs, external contracts, CDN/static delivery, or release packaging | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-10 | Architecture/new module/service, major redesign/refactor, migration coordination, or phased rollout | `CLEAR/HIT/UNKNOWN` | `<inspected source>` |
| ESC-11 | Evidence is insufficient to rule out higher risk | `CLEAR/HIT/UNKNOWN` | `<exact gap>` |
| ESC-12 | Evidence materially conflicts about scope, behavior, ownership, risk, or impact | `CLEAR/HIT/UNKNOWN` | `<conflicting sources>` |

Rules:

- Any `HIT` requires at least Level L.
- `ESC-10` normally requires Level XL.
- Any `UNKNOWN` forbids a final Level S or M classification; follow the Evidence Gap path.
- `ESC-12: HIT` follows the Evidence Conflict path and may require `BLOCKED`.
- A Level S or M result is valid only after the applicable Reverse Check also passes.

### Level S Reverse Check

Complete this checklist only after all escalation signals are `CLEAR`.

| ID | Required condition | Status | Evidence |
|---|---|---|---|
| S-01 | Exactly one identified, non-shared target | `PASS/FAIL/UNKNOWN` | `<target/usage evidence>` |
| S-02 | Copy, spacing, color, icon size, or static presentation only | `PASS/FAIL/UNKNOWN` | `<behavior evidence>` |
| S-03 | No behavior/state/API/data/contract/config/generated-artifact change | `PASS/FAIL/UNKNOWN` | `<inspected source>` |
| S-04 | Acceptance and verification are local to the target | `PASS/FAIL/UNKNOWN` | `<verification evidence>` |
| S-05 | Scope is explicit, reversible, and needs no adjacent cleanup/refactor | `PASS/FAIL/UNKNOWN` | `<scope evidence>` |
| S-06 | Evidence is sufficient/consistent and escalation is entirely `CLEAR` | `PASS/FAIL/UNKNOWN` | `<evidence summary>` |

All rows must be `PASS` for Level S. A `FAIL` requires evaluation as Level M or higher. An `UNKNOWN` follows the Evidence Gap path.

### Level M Reverse Check

Complete this checklist only after all escalation signals are `CLEAR`.

| ID | Required condition | Status | Evidence |
|---|---|---|---|
| M-01 | Exactly one bounded feature or user flow | `PASS/FAIL/UNKNOWN` | `<flow boundary>` |
| M-02 | Modules, inputs, outputs, state changes, and failure behavior are known | `PASS/FAIL/UNKNOWN` | `<inspected source>` |
| M-03 | No shared/global surface or public/shared contract | `PASS/FAIL/UNKNOWN` | `<usage/contract evidence>` |
| M-04 | No migration, rollout coordination, contract redesign, new module/service, or architecture decision | `PASS/FAIL/UNKNOWN` | `<dependency/design evidence>` |
| M-05 | The change is reversible and verification is specific | `PASS/FAIL/UNKNOWN` | `<rollback/test evidence>` |
| M-06 | Evidence is sufficient/consistent and escalation is entirely `CLEAR` | `PASS/FAIL/UNKNOWN` | `<evidence summary>` |

All rows must be `PASS` for Level M. A `FAIL` requires Level L or XL. An `UNKNOWN` follows the Evidence Gap path.

### Evidence Gap Path

When evidence is insufficient:

1. identify exactly what is unknown and why it affects risk or scope;
2. inspect the smallest additional evidence source likely to resolve it;
3. if user knowledge is required, ask a focused question;
4. if it remains unknown, classify at least Level L and mark the assumption and stop condition;
5. use `BLOCKED` when no safe plan or bounded Scope Lock can be produced.

Never convert missing evidence into an unstated assumption.

### Evidence Conflict Path

When relevant evidence conflicts:

1. cite the conflicting sources and the decision they affect;
2. seek an authoritative source or explicit user decision;
3. choose the higher plausible risk while investigating;
4. use `BLOCKED` if the conflict changes implementation meaning, scope, acceptance criteria, or safety and remains unresolved.

A narrowed, non-conflicting subset may proceed only as a separate plan with its own Scope Lock and approval.

### Risk Levels

| Level | Required classification rule | Planning depth | Gate |
|---|---|---|---|
| **S** | All escalation rows `CLEAR`; all S reverse rows `PASS`; single local, non-behavioral, trivially reversible change | Compact plan | Valid approval and explicit user choice before action |
| **M** | All escalation rows `CLEAR`; all M reverse rows `PASS`; bounded multi-file or local behavior change with known dependencies | Brief plan | Valid approval and explicit user choice before action |
| **L** | Any escalation signal, cross-cutting or sensitive effect, meaningful ambiguity, or non-trivial rollback | Detailed plan | Valid approval required |
| **XL** | Architecture, migration, new subsystem, major data-flow change, or phased delivery | Design and phases | Valid design/phase approval required |

Risk level sets planning depth, never the approval requirement. Every level needs an
approval that satisfies Valid Approval and produces an Approval Record before any
implementation, persistence, or handoff.

Use the highest applicable level. Cosmetic appearance, small diff size, or user urgency never overrides affected-system risk.

During standalone continuation, stop and reclassify if new evidence reveals broader scope, a mandatory escalation signal, a failed assumption, or a changed acceptance criterion. Update the plan and Scope Lock, then obtain approval again before continuing.

If CDP's own partial edits would leave obvious syntax errors, broken imports, failed formatting, or checks failing solely because an edit is half-applied, make only the smallest repair or revert needed to restore the pre-upgrade baseline. Disclose it, do not touch user or unrelated changes, and do not use coherence repair to continue the higher-risk change.

## Scope Lock Contract

Every approval-ready plan must contain one canonical Scope Lock:

```yaml
Scope-Lock-Version: cdp-scope/v1
in_scope:
  - <approved outcome or impact>
out_of_scope:
  - <explicit exclusion>
non_goals:
  - <behavior that must not be implemented>
assumptions:
  - <material assumption>
stop_conditions:
  - <condition requiring pause or replanning>
will_change:
  - <approved affected area>
will_not_change:
  - <protected area or behavior>
acceptance_criteria:
  - <high-level observable result>
```

All eight arrays are required and must contain explicit values; do not use `TBD`, `N/A`, or implied omissions. Once approved, this block is canonical.

Rules:

- Copy it verbatim to CDF and CDTask.
- Do not paraphrase, reorder, merge, omit, weaken, or expand entries.
- A readable projection such as `Change Scope` reproduces `will_change` and `will_not_change` verbatim and never replaces the canonical block.
- Treat `out_of_scope`, `non_goals`, and `will_not_change` as enforceable constraints.
- Any scope expansion returns to CDP for replanning, a new Scope Lock, and renewed approval.

## Development Plan Output

Use this structure for every final plan. Adjust depth to the risk level without removing sections.

```markdown
## Development Plan

### Requirement Understanding
<goal, behavior, decomposition, and constraints>

### Evidence
<confirmed facts, sources, inferences, and open assumptions>

### Risk Gate Result
- Final Level: <S | M | L | XL>
- Escalation Checklist: <all CLEAR, or list HIT/UNKNOWN rows>
- Reverse Check: <S or M result, or Not Applicable>
- Rationale: <evidence-backed reason>

### Scope Lock
<complete cdp-scope/v1 block>

### Change Scope
Readable projection of the canonical Scope Lock. It must not add, weaken, or replace it.

#### Will Change
- <verbatim from will_change>

#### Will Not Change
- <verbatim from will_not_change>

### Technical Approach
<implementation direction; for XL include design, data/API/state flow, and phases>

### Risks
<risk, mitigation, stop condition, and rollback where material>

### Acceptance Criteria
<observable criteria aligned with Scope Lock>

### Verification Strategy
<checks appropriate to the risk level>

### Next Action
Choose one:
1. Execute Now
2. Save as CDTask
```

For Level L, include affected modules, an ordered implementation plan, and rollback. For Level XL, also include current context, proposed design, data/API/state flow, phases, and the exact phase boundary awaiting approval.

The two-option `Next Action` applies to `standalone`. In `cdf-managed`, replace it with the single context-valid action `Return Approved Plan Package to CDF`; managed approval never authorizes CDP implementation or a direct CDTask call.

Do not manufacture detail merely to make the plan longer. Use the lightest plan that safely captures evidence, scope, risk, and verification.

## Approval Gate

Next Action is a user decision point. CDP must not move from planning to implementation or task persistence without applicable plan approval and an explicit user choice.

### Valid Approval

Approval is valid only when it identifies both:

1. an authorization action; and
2. the plan, Scope Lock, phase, task, or subset being approved.

Valid examples:

- `批准该计划，并按此 Scope Lock 实施。`
- `同意保存为 CDTask，范围按上面的 Scope Lock。`
- `Approve and implement the plan as scoped above.`
- `Approve Phase 1 only and return the package to CDF.`

Acknowledgements such as `ok`, `继续`, `可以`, `嗯`, `looks good`, or silence are invalid because they do not identify action and scope.

Use this follow-up for an ambiguous response:

```text
Your reply does not yet identify both the approved scope and the authorized action.
Please state one explicitly, for example:
- Approve this Scope Lock and Execute Now.
- Approve this Scope Lock and Save as CDTask.
- Approve only <items>; leave all remaining items unapproved.
```

Ask this follow-up at most twice for the same plan. If the reply still does not identify both scope and action, or if the user declines the plan, end the gate without approval. In `standalone` context, ask the user how to proceed. In `cdf-managed` context, return `Planning Status: NOT_APPROVED` with the reason and no plan content.

Do not treat authorization to inspect, plan, or edit the plan as approval to implement or persist it.

### Approval Modes

- **Full Approval** — the complete Scope Lock and selected action are approved.
- **Conditional Approval** — approval is valid only after every condition is incorporated into a revised canonical Scope Lock and echoed back.
- **Partial Approval** — only explicitly listed items are approved; all remaining items stay unapproved.

At every risk level, no implementation, persistence, or task-execution preparation may begin before valid approval. A changed condition, phase boundary, or scope requires renewed approval.

### Partial Approval Result

After partial approval:

1. create a valid `cdp-scope/v1` block containing only the approved subset;
2. preserve approved wording and all remaining items verbatim;
3. display the result below;
4. prepare no implementation or task for unapproved items.

````markdown
## Partial Approval Result

Approval Type: partial
Authorized Action: <Execute Now | Save as CDTask | Return Approved Plan Package to CDF>

### Approved Scope
- <copy each approved item verbatim from approved-subset in_scope>

### Unapproved / Remaining
Status: NOT APPROVED — MUST NOT BE IMPLEMENTED / 未批准，不得实施
- <copy each unapproved item verbatim>

### Approved-Subset Scope Lock
```yaml
Scope-Lock-Version: cdp-scope/v1
in_scope: [...]
out_of_scope: [...]
non_goals: [...]
assumptions: [...]
stop_conditions: [...]
will_change: [...]
will_not_change: [...]
acceptance_criteria: [...]
```
````

The approved-subset Scope Lock becomes canonical. If the subset cannot be formed without new decisions, conflict, or semantic rewriting, stop and ask for clarification or replan.

### Approval Record

Record every valid approval in this stable shape:

```markdown
## Approval Record
- User Choice: <selected context-valid action>
- Approval Type: <full | conditional | partial>
- Approved Items: <all in_scope items or exact approved subset>
- Conditions Added To Scope Lock: <none or exact conditions>
- Unapproved Items: <none or exact remaining items>
- Scope Approved: Yes
- Code Changes Authorized In This Turn: <Yes only for standalone Execute Now; otherwise No>
```

In `cdf-managed`, the only valid action is `Return Approved Plan Package to CDF`. Record it under that exact name in `User Choice` and `Authorized Action`, including when the user approves with an unambiguous equivalent. Do not offer or normalize managed approval into `Execute Now`.

### Locked Scope Echo

After full or conditional approval, echo:

```markdown
## Locked Scope Summary

### In Scope
- <verbatim from canonical Scope Lock>

### Will Not Change
- <verbatim from canonical Scope Lock>

### Non-Goals
- <verbatim from canonical Scope Lock>

Approval Type: <full | conditional>
Authorized Action: <Execute Now | Save as CDTask | Return Approved Plan Package to CDF>
```

The echo confirms shared understanding; it does not create broader authority.

## Next Action and Handoffs

### Execute Now

Available only in `standalone` context after valid approval and explicit selection. Re-check approval and Scope Lock before continuation. Stop and replan on any material deviation.

### Save as CDTask

CDTask is optional. Recommend it when work:

- needs persistence or later resumption;
- is large, phased, or multi-contributor;
- needs explicit task decomposition;
- should separate planning from implementation.

Do not create a CDTask for every change. Before handoff, confirm CDTask is available. If unavailable, follow the unavailable-CDTask path at the end of this section and do not fabricate a task package.

Use this exact internal handoff format:

```text
# CDP Task Handoff Package

Contract-Version: cdp-cdtask/v1
Handoff-Type: deferred-local-task
Title: <short task title>
Workspace: <absolute workspace path>
Requested-Task-Path: <user path or _cdtask/YYYY-MM-DD-<slug>.md>
Risk-Level: <Level S | Level M | Level L | Level XL>
Approval-State: scope-approved-execution-deferred
Source-Branch: <current branch or Unavailable>
Source-Commit: <current commit or Unavailable>
```

The package must include, in order:

1. `Scope Lock`, verbatim;
2. `Requirement Understanding`;
3. `Requirement Decomposition`;
4. `Confirmed Evidence`;
5. `Open Assumptions`;
6. `Change Scope`, with `Will Change` and `Will Not Change`;
7. `Proposed Design`;
8. `Data Model / API / State Flow`;
9. `Approved Phase Boundary`;
10. `Implementation Plan / Phases`;
11. `Risks`;
12. `Acceptance Criteria`;
13. `Test Plan / Test Strategy`;
14. `Rollback Plan`;
15. `Approval Record`;
16. `Handoff Execution Paths`;
17. `Resume Rules`.

For Level S/M/L, keep architecture-only headings with `Not applicable for <risk level>.` when they have no approved content. For Level XL, include the approved design, flow, and phase boundary.

`Approval-State: scope-approved-execution-deferred` means planning scope is approved but execution remains deferred. It is not execution authorization.

If CDTask is unavailable, do not create `_cdtask`, generate a fallback handoff file, install anything automatically, or claim a save. Output this command verbatim, then require the user to select `Save as CDTask` again after installation:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

The command must name `--skill cdtask`. Never output the `cdp` install command here, and never invent a repository, package name, or path. [references/install.md](references/install.md) holds the single-agent variants.

### Return to CDF

Run the Approval Gate to completion before returning. CDF routes on `Planning Status` alone and never judges an approval reply, so a package returned with an unfinished gate has no valid destination.

In `cdf-managed` context, return:

```markdown
# Approved Plan Package

Contract-Version: cdp-cdf/v1
Planning Status: <APPROVED | NOT_APPROVED | BLOCKED>
Lifecycle Owner: CDF
Execution by CDP: Not authorized
Code Changes by CDP: None
Risk Level: <Level S | Level M | Level L | Level XL>
Phase: <n of N | Not applicable>
Remaining-Phases: <count or 0>
Reason: <plain text; required for NOT_APPROVED and BLOCKED>
Next Owner: <Human approver | CDF>
Workspace: <absolute workspace path or Unavailable>
Source-Branch: <current branch or Unavailable>
Source-Commit: <current commit or Unavailable>

<Development Plan>
<canonical Scope Lock>
<Approval Record>
<Locked Scope Summary or Partial Approval Result>
```

Query the workspace path, current branch, and latest commit when the repository is
reachable. Write `Unavailable` with no substitute value when it is not. CDF compares
these against the live repository before handing off and cannot supply them itself.

`Lifecycle Owner`, `Execution by CDP`, and `Code Changes by CDP` are fixed attestations,
not descriptions of what happened to be true this round. Write them exactly as shown.
`Execution by CDP: Not authorized` and `Code Changes by CDP: None` are always correct
here, because managed context forbids both; if either would be untrue, the violation has
already occurred and must be reported instead of returned as a package.

`Next Owner` is `CDF` on an `APPROVED` return. Never write `Human approver` alongside
`APPROVED`: CDF reads it as an approval gate left open and returns the package. Use
`Human approver` only when `NOT_APPROVED` or `BLOCKED` sends the decision back to a person.

| `Planning Status` | Meaning | Required content |
|---|---|---|
| `APPROVED` | The Approval Gate completed with valid approval | Development Plan, canonical Scope Lock, Approval Record, and the applicable summary |
| `NOT_APPROVED` | The user declined, or the gate ended without valid approval after the re-ask limit | `Reason` only; no Approval Record |
| `BLOCKED` | The Evidence Gap, Evidence Conflict, or partial-subset path stopped planning | `Reason` only; no Approval Record |

`Planning Status` is the only field CDF routes on. `Reason` is human-readable text and carries no routing meaning. Never return a status outside this table, and never return `APPROVED` without an Approval Record.

For a phased Level XL plan, `Phase` and `Remaining-Phases` describe the approved phase only. `Remaining-Phases: 0` ends the flow; a positive count tells CDF another phase follows, and every phase requires its own approval.

Never call CDTask or continue the lifecycle from this context.

## References and Usage

Use the references progressively:

- [Requirement Gate](references/requirement-gate.md) — ambiguous, risky, or specification-like requirements;
- [Karpathy Guidelines](references/karpathy-guidelines.md) — concise engineering discipline;
- [Boundary Cases](references/boundary-cases.md) — upgrade, ambiguous approval, evidence conflict, and partial-approval examples;
- [Installation](references/install.md) — CDP packaging and the per-agent CDTask install commands.

For Level M, L, and XL, read the Karpathy Guidelines before producing a plan, design, or implementation. For Level S, do not read it by default; use it only after the target check when a prior attempt failed or additional minimal-change guardrails are objectively needed. Shared targets or high-risk overlap require reclassification, not extra reading while remaining Level S. If the reference is unavailable, continue with this Skill as the source of truth and mention the missing supporting reference.

Typical invocation:

```text
Use CDP to inspect this requirement, classify risk, produce an approval-ready Scope Lock and Development Plan, then ask me to choose the next action.
```

Keep Level S output short. Always prefer the smallest approved change: no unrelated refactor, dependency, rename, file restructure, broad reformat, or public-API change. Anti-overplanning reduces prose, not evidence inspection or the Next Action gate.

For standalone completion, report only verification actually performed. Level L/XL also require regression notes and traceability: query the current branch and latest commit when available, or write `Unavailable` with the reason. A failed verification may be repaired only inside approved scope; otherwise stop and replan.

## Non-Negotiable Rules

- Do not skip the Requirement Gate when material ambiguity exists.
- Do not finalize S or M without the complete escalation checklist and applicable Reverse Check.
- Do not hide missing or conflicting evidence.
- Do not expand approved scope.
- Do not weaken or rewrite a canonical Scope Lock.
- Do not accept ambiguous approval.
- Do not auto-transition into implementation or persistence.
- Do not return a plan package to CDF without a final `Planning Status`.
- Do not invoke CDTask in `cdf-managed` context.
- Do not replace CDF lifecycle coordination or CDTask decomposition.
- Do not invent a runtime, scheduler, execution state machine, or review system.
