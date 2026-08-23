# CDP: Controlled Development Planning

## Quick Understanding

CDP turns unclear development requirements into evidence-based, risk-aware plans with a locked scope and an explicit human decision point.

> Small changes should be fast. Risky changes should be controlled.

CDP plans and recommends the next action. It is not a runtime controller, scheduler, or automatic review system.

## Position in the CDF Suite

```text
CDF — control plane, return routing, handoff preconditions
 ↓
CDP — requirement analysis, evidence, risk, Scope Lock, plan
 ↓
Human Plan Approval — run by CDP in both contexts
 ↓
standalone:   Execute Now | Save as CDTask
cdf-managed:  Return Approved Plan Package to CDF
```

- **CDF** invokes CDP in managed mode, routes the return on contract fields, and enforces the handoff preconditions. It does not run the approval gate.
- **CDP** owns planning, risk decisions, Scope Lock, approval materials, and the human approval gate itself — displaying the plan, judging whether a reply is valid approval, and re-asking when it is not.
- **CDTask** optionally converts an approved plan into verifiable task definitions.

The canonical Scope Lock is copied verbatim across every handoff. CDP does not call CDTask or implement code in `cdf-managed` context.

## Responsibilities and Boundaries

CDP is responsible for:

- requirement understanding and decomposition;
- evidence inspection and conflict handling;
- S/M/L/XL risk classification;
- Development Plan and verification strategy;
- canonical `cdp-scope/v1` Scope Lock;
- full, conditional, and partial approval materials;
- Next Action recommendation.

CDP is not responsible for:

- CDF lifecycle orchestration;
- CDTask task decomposition;
- scheduling or runtime management;
- automatic implementation or persistence before approval;
- implementation review.

## Workflow

```text
Requirement Gate
  → Understand and decompose
  → Inspect evidence
  → Run escalation checklist
  → Run S or M Reverse Check when eligible
  → Classify final risk
  → Create Development Plan and Scope Lock
  → Obtain explicit approval
  → Ask for Next Action
```

Use [the Requirement Gate](references/requirement-gate.md) for vague, incomplete, risky, or specification-like requests. Verify that an existing target actually exists before planning a modification.

## Risk Control

CDP uses checkable rules, not visual impression or diff size.

| Level | Eligibility | Planning control |
|---|---|---|
| **S** | One local static target; every escalation row `CLEAR`; every S Reverse Check row `PASS` | Compact plan, valid approval, and explicit action choice |
| **M** | One bounded flow with known effects; every escalation row `CLEAR`; every M Reverse Check row `PASS` | Brief evidence-backed plan, valid approval, and explicit action choice |
| **L** | Any shared, conditional, persistent, sensitive, production, integration, or evidence-risk signal | Detailed plan and valid approval |
| **XL** | Architecture, new subsystem, major data-flow change, migration, or phased rollout | Design, phase boundary, and valid approval |

Risk level sets planning depth, never the approval requirement. Every level needs a valid approval and an Approval Record before implementation, persistence, or handoff.

Before finalizing S or M, inspect every mandatory escalation category:

- shared components, theme systems, design tokens, and global state;
- conditional rendering, feature flags, roles, permissions, and entitlements;
- persistent data, schema, migrations, payments, billing, auth, and access control;
- reports, analytics, telemetry, cache, jobs, queues, timers, and events;
- i18n, accessibility, compliance, security, privacy, and observability;
- configuration, deployment, production settings, third-party contracts, and release delivery;
- architecture, modules, services, migrations, and phased rollout;
- insufficient or conflicting evidence.

Each row records `CLEAR`, `HIT`, or `UNKNOWN` with evidence. Any `HIT` means at least Level L; architecture-class signals normally mean XL. Any `UNKNOWN` forbids S/M. Evidence conflict is `BLOCKED` when it changes plan meaning.

The full operational checklists and output shape are in [SKILL.md](SKILL.md). Complete them in practice; they are not reference-only lists.

## Scope Lock and Approval

Every approval-ready plan contains one canonical `cdp-scope/v1` block with eight required arrays:

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

Once approved, copy the entire block verbatim. Do not paraphrase, reorder, omit, weaken, or expand it. Scope expansion requires CDP replanning and renewed approval.

Approval must identify both an action and the approved plan, Scope Lock, phase, task, or subset. `ok`, `continue`, `可以`, and similar acknowledgements are not approval.

CDP supports:

- **Full Approval** — the complete Scope Lock is approved.
- **Conditional Approval** — exact conditions are first added to a revised canonical Scope Lock.
- **Partial Approval** — only named items are approved; all remaining items are shown as `NOT APPROVED — MUST NOT BE IMPLEMENTED / 未批准，不得实施`.

A partial approval produces a complete approved-subset Scope Lock and a visible Partial Approval Result showing Approved Scope, Unapproved / Remaining, and Authorized Action. Approved and unapproved wording is preserved verbatim, including the bilingual status line above.

## Execution Contexts and Handoffs

### Standalone

After the plan is approved, the user chooses:

1. `Execute Now`
2. `Save as CDTask`

CDP never chooses automatically. `Save as CDTask` is useful for persistent, resumable, large, phased, or separated work and uses `cdp-cdtask/v1` with `Approval-State: scope-approved-execution-deferred`.

### CDF-managed

CDP returns an Approved Plan Package to CDF and stops. It does not implement, invoke CDTask, persist a local task, or continue the lifecycle.

CDF may later pass the approved package to CDTask using `cdf-cdtask/v1`. Both contracts are internal Skill handoff formats, not public runtime protocols.

## Quick Start

Invoke with `cdp`, `$cdp`, `cdp:`, or `controlled-development-planning`:

```text
Use CDP to inspect this requirement, classify risk, produce an approval-ready
Scope Lock and Development Plan, then ask me to choose the next action.
```

Expected plan sections:

1. Requirement Understanding
2. Evidence
3. Risk Gate Result
4. Scope Lock
5. Change Scope — `Will Change` and `Will Not Change`, verbatim from the Scope Lock
6. Technical Approach
7. Risks
8. Acceptance Criteria
9. Verification Strategy
10. Next Action

Every section is required at every risk level; depth varies, presence does not. `Change Scope` is a readable projection of the canonical Scope Lock and never replaces it — CDTask requires it for all risk levels and reports `BLOCKED` when it is absent or contradicts the canonical block.

## References

- [Requirement Gate](references/requirement-gate.md) — requirement clarity and product-risk questions.
- [Karpathy Guidelines](references/karpathy-guidelines.md) — minimal, evidence-based engineering guardrails.
- [Boundary Cases](references/boundary-cases.md) — bilingual examples for escalation, ambiguous approval, evidence conflict, and partial approval.
- [Installation Notes](references/install.md) — installation and CDTask availability guidance.

For Level M/L/XL, read the Karpathy Guidelines before producing the plan or design. For Level S, it is optional after the target check unless a prior attempt failed or extra minimal-change guidance is needed. CDP remains the source of truth if a supporting reference is unavailable.

## Compatibility

CDP uses the Agent Skills layout supported by Codex and Claude Code:

- entrypoint: `skills/cdp/SKILL.md`
- metadata: `skills/cdp/skill.json`
- Codex UI metadata: `skills/cdp/agents/openai.yaml`

## Installation

Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -g -y
```

Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a claude-code -g -y
```

Both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

## Non-Negotiable Rules

- Do not hide missing or conflicting evidence.
- Do not finalize S/M without both mandatory checklists.
- Do not expand or rewrite approved scope.
- Do not accept ambiguous approval.
- Do not auto-transition into implementation or persistence.
- Do not introduce runtime, scheduling, or review behavior.
