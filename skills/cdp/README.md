# CDP: Controlled Development Planning

## Quick Understanding

CDP turns unclear development requirements into evidence-based, risk-aware plans with a locked scope and an explicit human decision point.

> Small changes should be fast. Risky changes should be controlled.

CDP plans and recommends the next action. It is not a runtime controller, scheduler, or automatic review system.

## Position in the CDF Suite

```text
CDF — control plane, flow coordination, human approval gates
 ↓
CDP — requirement analysis, evidence, risk, Scope Lock, plan
 ↓
Human Plan Approval
 ↓
Execute Now | CDTask — approved-plan task definition and handoff
```

- **CDF** invokes CDP in managed mode and owns lifecycle continuation.
- **CDP** owns planning, risk decisions, Scope Lock, and approval materials.
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
| **S** | One local static target; every escalation row `CLEAR`; every S Reverse Check row `PASS` | Compact plan and explicit action choice |
| **M** | One bounded flow with known effects; every escalation row `CLEAR`; every M Reverse Check row `PASS` | Brief evidence-backed plan and explicit action choice |
| **L** | Any shared, conditional, persistent, sensitive, production, integration, or evidence-risk signal | Detailed plan and valid scope approval |
| **XL** | Architecture, new subsystem, major data-flow change, migration, or phased rollout | Design, phase boundary, and valid approval |

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
- **Partial Approval** — only named items are approved; all remaining items are shown as `NOT APPROVED — MUST NOT BE IMPLEMENTED`.

A partial approval produces a complete approved-subset Scope Lock and a visible summary of Approved Scope, Unapproved / Remaining, and Authorized Action. Approved and unapproved wording is preserved verbatim.

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
5. Technical Approach
6. Risks
7. Acceptance Criteria
8. Verification Strategy
9. Next Action

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
