# cdp

`cdp` is short for `controlled-development-planning`: a risk-based development workflow Skill for AI Coding Agents that clarifies vague requirements before implementation.

Invoke it explicitly with `cdp`, `$cdp`, `cdp:`, or `controlled-development-planning`.

It helps agents avoid two common failure modes:

- Over-planning simple changes.
- Rushing risky changes.
- Implementing the wrong thing from an ambiguous prompt.

Core principle:

> Small changes should be fast. Risky changes should be controlled.

Quick flow: run Requirement Gate, pause for clarification if the request is unclear, treat accepted suggested defaults as explicit assumptions, locate the target, show requirement understanding and decomposition to the user, run the decision tree for initial classification, inspect evidence, run the same tree again for final classification, then use the matching workflow. If examples, the decision tree, and classification conditions disagree, the highest risk level wins.

Decision tree: architecture or phased rollout is Level XL; data, money, reports, auth, jobs, production config, cache invalidation, events/webhooks, third-party integrations, CDN/static delivery, localization/i18n behavior, accessibility/compliance behavior, or similar high-risk runtime areas are Level L unless evidence proves a purely local display/style/copy change; scoped interactions and small API/local state changes are Level M; pure copy/style/static single-component tweaks are Level S only when all low-risk conditions hold.

## Requirement Gate

Before CDP chooses a workflow level, it first checks whether the requirement is clear enough to implement.

If the request is vague, ambiguous, underspecified, or missing acceptance criteria, CDP asks targeted clarification questions instead of rushing into code.

The gate uses a compact definition card, gap list, minimal questions, and suggested defaults to help the user quickly reach executable clarity.

This prevents coding agents from implementing the wrong thing from an ambiguous prompt.

## Compatibility

`cdp` follows the Agent Skills `SKILL.md` format used by Codex and Claude Code:

- Skill folder: `skills/cdp/`
- Skill entrypoint: `skills/cdp/SKILL.md`
- Skill name: `cdp`
- Skill metadata: `skills/cdp/skill.json`
- Codex UI metadata: `skills/cdp/agents/openai.yaml`

The folder name and `SKILL.md` frontmatter `name` match intentionally. This keeps the skill compatible with the Agent Skills specification and makes the short invocation stable.

## Bundled References

`cdp` includes `references/karpathy-guidelines.md` as a bundled MIT-licensed reference for coding-agent guardrails: think before coding, keep changes simple, make surgical edits, and define verifiable success criteria.

For Level M, Level L, and Level XL tasks, the agent must read this reference before producing a plan, design, or implementation. For Level S tasks, reading it is optional so simple changes stay lightweight; use it after a failed attempt or when extra minimal-change guardrails are needed after the reverse check passes. Shared code, multiple affected modules, design tokens/primitives, generated code, common configuration, or high-risk path overlap require reclassification rather than remaining Level S.

The reference is included so users do not need to install `karpathy-guidelines` separately.

If `references/karpathy-guidelines.md` is unavailable in an installed copy, the agent should continue with the cdp rules as the source of truth and mention that the supporting reference was unavailable.

## Target Existence Check

Before editing an existing target, the agent must verify that the requested target exists in the codebase.

For example, if the user asks to modify a button, the agent should first locate that button. If the button does not exist or cannot be uniquely identified, the agent should pause and ask whether the user wants to create a new button, modify a different button, or correct the request.

For new modules, services, top-level workflows, or architecture, the agent should still search first for existing similar modules, routes, packages, or workflows to avoid duplication. Similar existing targets should be treated as extension points unless the user confirms otherwise.

This rule applies to every workflow level, including simple Level S changes. It prevents the agent from guessing or silently creating missing targets.

## Requirement Understanding

After the target existence check, the agent should restate what the user wants before planning, classifying, or editing.

This must be visible to the user, not only internal reasoning. It should identify user intent, current behavior, expected behavior, visible change, and any hidden business change. For simple Level S tasks, this can stay short:

```text
Understanding: Change the submit button color only. No behavior change.
```

## Requirement Decomposition

Before risk classification, the agent should decompose the requirement into possible impact areas:

- UI / style
- Frontend interaction
- State management
- API request/response
- Backend logic
- Database schema
- Permissions/auth
- Scheduled tasks
- Cache invalidation
- Events, webhooks, and message consumers
- Billing/subscription/IAP
- Reporting/metrics
- Third-party API integrations
- CDN/static assets
- Localization/i18n
- Accessibility/compliance
- Production configuration
- Tests

This must be visible to the user before any plan, approval request, or edit. This step is meant to catch hidden risk, not to create a long document. For Level M, it must be included in the compact plan.

## Risk Classification

The agent should perform an initial classification into Level S, Level M, Level L, or Level XL only after Requirement Gate has passed and after requirement understanding and decomposition.

The levels are checkable rules:

- Level S requires a single non-shared target, local static presentation only, no behavior/data/contract/configuration change, sufficient consistent evidence, and a complete low-risk reverse check.
- Level M requires one bounded reversible feature flow, known inputs/outputs/failure behavior, no shared/global surface, no high-risk signal, sufficient consistent evidence, and the same reverse check.
- Level L applies when any shared component/theme/global state, conditional rendering/permission behavior, cache, analytics, i18n, configuration, job/event, persistent-data write, billing, authentication, authorization, production configuration, or similar high-risk signal is present.
- Level XL applies when a new module/service, architecture or major data-flow redesign, coordinated migration, or approval-controlled phased delivery is required.

Before finalizing S or M, the agent must rescan for every mandatory escalation signal. Any positive signal upgrades to at least Level L; any unknown signal prevents S/M finalization.

The initial classification should be visible to the user together with requirement understanding and decomposition.

## Evidence-Based Thinking

After initial classification, the agent should think from concrete code evidence before producing a plan.

For Level M, Level L, and Level XL tasks, the plan or design should be grounded in actual files, symbols, fields, schemas, APIs, configuration keys, call sites, or search results. The agent should explicitly include confirmed evidence and open assumptions before planning.

After evidence inspection, the agent should finalize or upgrade the risk level. If evidence reveals a higher-risk area, it should reclassify immediately and switch to the stricter workflow.

If evidence is insufficient, the agent records the missing evidence, continues safe read-only inspection, or asks the smallest targeted question. It uses provisional Level L controls when higher-risk impact cannot be ruled out and blocks managed planning when the gap changes scope, behavior, risk, or approval meaning.

If evidence conflicts, the agent lists the conflicting claims and sources, uses the highest supported risk, asks for an authoritative decision, and marks the plan blocked until the conflict is resolved. It never chooses the lower-risk interpretation for convenience.

Level S should stay concise, but it still requires enough file or search evidence to locate the exact target and avoid changing the wrong copy, style source, or component.

## Scope Lock Contract

Every approvable or handoff-ready plan contains an internal `Scope-Lock-Version: cdp-scope/v1` block with required arrays for `in_scope`, `out_of_scope`, `non_goals`, `assumptions`, `stop_conditions`, `will_change`, `will_not_change`, and high-level `acceptance_criteria`.

This block is the canonical scope source. CDF and CDTask copy it verbatim; they may not paraphrase, weaken, omit, or expand it. Any required expansion returns to CDP for replanning and renewed approval.

## Workflow Levels

### Level S: Lightweight Plan and Decision

For simple UI, copy, and style changes.

Examples:

- Button color.
- Text wording.
- Spacing.
- Icon size.
- Static UI adjustment.

Agent behavior:

- Produce a compact Development Plan and Scope Lock.
- Recommend `Execute Now`, then wait for the user's explicit Next Action choice.
- Do not create a long plan.
- Provide a brief summary, verification performed, and relevant manual checks after editing.

### Level M: Brief Plan and Decision

For normal scoped feature changes.

Examples:

- Add a filter.
- Change form behavior.
- Add a validation rule.
- Modify a small API call.
- Adjust one page interaction.

Agent behavior:

- Give a compact evidence-backed plan.
- Include the canonical Scope Lock and recommend a Next Action.
- Wait for the user's explicit Next Action choice before implementation or task persistence.
- Provide verification performed and relevant manual checks after editing.

Compact Level M format:

```md
I’ll treat this as Level M.

Understanding:
- ...

Requirement Decomposition:
- ...

Evidence:
- ...

Risk:
- ...

Plan:
1. ...
2. ...

Recommendation: Execute Now because this is scoped and passed the S/M reverse check. Awaiting explicit user choice.
```

### Level L: Approval Required

For high-risk changes.

Examples:

- Database schema.
- Payment, billing, subscription, or IAP logic.
- Reports, revenue, cost, ROI, or business metric logic.
- Authentication or permissions.
- Cron jobs, sync tasks, queues, retries, or idempotency.
- Production or deployment configuration.

Agent behavior:

- Do not edit immediately.
- Explain requirement understanding.
- Define change scope with `Will Change` and `Will Not Change`, affected modules, and independent acceptance criteria.
- Propose an implementation plan.
- Explain risks and test plan.
- Wait for explicit approval.

### Level XL: Design Required

For architecture or module-level changes.

Examples:

- New module or backend service.
- Major refactor.
- Full report pipeline.
- Permission system.
- App Store Connect API integration.
- Advertising statistics pipeline.

Agent behavior:

- Create a design first.
- Break implementation into phases with explicit boundaries.
- Preserve the approved design, data/API/state flow, acceptance criteria, and current phase boundary in any deferred local task.
- Prefer per-phase approval for large or risky designs.
- Stop and update the design for approval if implementation invalidates design assumptions or materially changes a phase.
- Avoid large uncontrolled edits.

## Reclassification During Implementation

If implementation reveals a higher-risk area than originally classified, the agent should stop editing immediately, explain the new evidence, and re-enter the stricter workflow from its required approval template. Level S or M upgrades to Level L when high-risk logic is discovered. Level L upgrades to Level XL when architecture, a new service, phased rollout, or major data-flow redesign becomes necessary.

If partial edits have already created syntax errors, broken imports, failed formatting, or build/test failures caused solely by the half-applied edit, the agent may make the smallest repair or revert needed to restore workspace coherence before waiting for stricter approval. That repair must not expand scope.

## Approval and Verification

For Level L and Level XL, approval must identify both the action and the approved Scope Lock, phase, task, or subset. Explicit forms such as `Approve and implement`, `批准并实施`, or `同意按此范围执行` are valid. Standalone acknowledgements such as `ok`, `继续`, `可以`, `嗯`, `Proceed`, or `go ahead` are invalid and trigger a short context-specific confirmation prompt.

CDP supports full approval, conditional approval, and partial approval. Conditions must be normalized into the Scope Lock. Partial approval creates an approved-subset Scope Lock and leaves every other item explicitly unapproved. Scope-expanding conditions require replanning and renewed approval.

After valid approval, CDP echoes a Locked Scope Summary containing `in_scope`, `will_not_change`, and `non_goals`, plus approval type and authorized action. The echo must copy approved items without paraphrasing.

Every Level L and Level XL approval request offers two explicit outcomes:

- `Execute Now` (`Approve and implement` / `同意并修改`): authorize code changes for the displayed Scope Lock or current approved phase.
- `Save as CDTask` (`Approve and save as local task` / `同意并保存为本地 task`): approve the Scope Lock, defer implementation, and hand a `cdp-cdtask/v1` package to `cdtask`.

The deferred outcome does not authorize implementation changes in the current turn. CDTask validates the package and Scope Lock, creates a dependency-aware task breakdown, runs its Task Readiness Gate, and saves it with `status: ready_for_resume`. An explicit path is used when supplied; otherwise the default is `_cdtask/YYYY-MM-DD-<slug>.md` under the current workspace.

CDP checks that CDTask is available before generating the handoff package or creating local files. If CDTask is unavailable, CDP does not create `_cdtask`, does not save a fallback document, and does not install anything automatically. It outputs:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

After installation, the user chooses `Approve and save as local task` again.

The saved task supports two paths:

- Path A: the user requests `Continue local task: <path>`. CDP re-checks the target, evidence, risk, branch, and commit. If nothing material changed, that request authorizes implementation of the saved scope.
- Path B: the user explicitly gives the task to an external coding agent. That agent may implement only the Task Breakdown under the Scope Guard and Handoff Rules. CDP does not automatically treat external execution as completed; bring the result back for CDP verification or closure when needed.

Document readiness alone is not implementation authorization. Material drift requires a revised approval request.

If the user replies to an approval request with a new requirement instead of approval, the previous approval request becomes stale. The agent should incorporate the new requirement, rerun classification and evidence checks, and request approval again for the revised plan.

Verification should match the changed risk area. For example, schema changes need schema or migration validation; billing/report changes need calculation-path checks; auth changes need allowed and denied path checks. If verification fails, fixes may continue only within the approved scope; expanded scope requires renewed approval.

For Level L and Level XL, final responses should include a structured Traceability section. In a git workspace, the agent should actively query current branch and latest commit; if traceability data is unavailable, it should say why.

## Installation

Install for Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -g -y
```

Install for Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a claude-code -g -y
```

Install for both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```
