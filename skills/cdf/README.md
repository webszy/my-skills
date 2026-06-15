# cdf

`cdf` is short for `controlled-development-flow`: a risk-based development workflow Skill for AI Coding Agents that clarifies vague requirements before implementation.

Invoke it explicitly with `cdf`, `$cdf`, `cdf:`, or `controlled-development-flow`.

It helps agents avoid two common failure modes:

- Over-planning simple changes.
- Rushing risky changes.
- Implementing the wrong thing from an ambiguous prompt.

Core principle:

> Small changes should be fast. Risky changes should be controlled.

Quick flow: run Requirement Gate, pause for clarification if the request is unclear, treat accepted suggested defaults as explicit assumptions, locate the target, show requirement understanding and decomposition to the user, run the decision tree for initial classification, inspect evidence, run the same tree again for final classification, then use the matching workflow. If examples, the decision tree, and classification conditions disagree, the highest risk level wins.

Decision tree: architecture or phased rollout is Level XL; data, money, reports, auth, jobs, production config, cache invalidation, events/webhooks, third-party integrations, CDN/static delivery, localization/i18n behavior, accessibility/compliance behavior, or similar high-risk runtime areas are Level L unless evidence proves a purely local display/style/copy change; scoped interactions and small API/local state changes are Level M; pure copy/style/static single-component tweaks are Level S only when all low-risk conditions hold.

## Requirement Gate

Before CDF chooses a workflow level, it first checks whether the requirement is clear enough to implement.

If the request is vague, ambiguous, underspecified, or missing acceptance criteria, CDF asks targeted clarification questions instead of rushing into code.

The gate uses a compact definition card, gap list, minimal questions, and suggested defaults to help the user quickly reach executable clarity.

This prevents coding agents from implementing the wrong thing from an ambiguous prompt.

## Compatibility

`cdf` follows the Agent Skills `SKILL.md` format used by Codex and Claude Code:

- Skill folder: `skills/cdf/`
- Skill entrypoint: `skills/cdf/SKILL.md`
- Skill name: `cdf`
- Skill metadata: `skills/cdf/skill.json`
- Codex UI metadata: `skills/cdf/agents/openai.yaml`

The folder name and `SKILL.md` frontmatter `name` match intentionally. This keeps the skill compatible with the Agent Skills specification and makes the short invocation stable.

## Bundled References

`cdf` includes `references/karpathy-guidelines.md` as a bundled MIT-licensed reference for coding-agent guardrails: think before coding, keep changes simple, make surgical edits, and define verifiable success criteria.

For Level M, Level L, and Level XL tasks, the agent must read this reference before producing a plan, design, or implementation. For Level S tasks, reading it is optional so simple changes stay lightweight. Read it for Level S only when target search finds objective signals such as shared code used by multiple modules, more than five references, more than one touched file/module, shared design tokens or primitives, a failed previous attempt, or overlap with high-risk paths.

The reference is included so users do not need to install `karpathy-guidelines` separately.

If `references/karpathy-guidelines.md` is unavailable in an installed copy, the agent should continue with the cdf rules as the source of truth and mention that the supporting reference was unavailable.

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

If decomposition reveals high-risk areas such as data, money, security, permissions, reporting, scheduled tasks, or production configuration, the task should be upgraded to Level L or Level XL even when the visible change looks small.

The initial classification should be visible to the user together with requirement understanding and decomposition.

## Evidence-Based Thinking

After initial classification, the agent should think from concrete code evidence before producing a plan.

For Level M, Level L, and Level XL tasks, the plan or design should be grounded in actual files, symbols, fields, schemas, APIs, configuration keys, call sites, or search results. The agent should explicitly include confirmed evidence and open assumptions before planning.

After evidence inspection, the agent should finalize or upgrade the risk level. If evidence reveals a higher-risk area, it should reclassify immediately and switch to the stricter workflow.

If the evidence is insufficient, the agent should continue inspecting or pause and ask the user instead of outputting a generic plan.

Level S should stay concise, but it still requires enough file or search evidence to locate the exact target and avoid changing the wrong copy, style source, or component.

## Workflow Levels

### Level S: Direct Edit

For simple UI, copy, and style changes.

Examples:

- Button color.
- Text wording.
- Spacing.
- Icon size.
- Static UI adjustment.

Agent behavior:

- Edit directly.
- Do not ask for confirmation.
- Do not create a long plan.
- Provide a brief summary, verification performed, and relevant manual checks after editing.

### Level M: Brief Plan Then Edit

For normal scoped feature changes.

Examples:

- Add a filter.
- Change form behavior.
- Add a validation rule.
- Modify a small API call.
- Adjust one page interaction.

Agent behavior:

- Give a compact evidence-backed plan.
- Proceed if the requirement is clear.
- Ask only if ambiguous.
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

I’ll proceed because this is scoped and does not touch high-risk areas.
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
- Define change scope, affected modules, and a required "Will not change" boundary.
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
- Prefer per-phase approval for large or risky designs.
- Stop and update the design for approval if implementation invalidates design assumptions or materially changes a phase.
- Avoid large uncontrolled edits.

## Reclassification During Implementation

If implementation reveals a higher-risk area than originally classified, the agent should stop editing immediately, explain the new evidence, and re-enter the stricter workflow from its required approval template. Level S or M upgrades to Level L when high-risk logic is discovered. Level L upgrades to Level XL when architecture, a new service, phased rollout, or major data-flow redesign becomes necessary.

If partial edits have already created syntax errors, broken imports, failed formatting, or build/test failures caused solely by the half-applied edit, the agent may make the smallest repair or revert needed to restore workspace coherence before waiting for stricter approval. That repair must not expand scope.

## Approval and Verification

For Level L and Level XL, approval must clearly authorize code changes for the stated scope. Ambiguous acknowledgements such as `OK`, `好的`, `sounds good`, `そうですね`, or `pourquoi pas` are not enough when they could simply mean "I understand"; the agent should ask for explicit approval. Partial approval applies only to the approved subset.

If the user replies to an approval request with a new requirement instead of approval, the previous approval request becomes stale. The agent should incorporate the new requirement, rerun classification and evidence checks, and request approval again for the revised plan.

Verification should match the changed risk area. For example, schema changes need schema or migration validation; billing/report changes need calculation-path checks; auth changes need allowed and denied path checks. If verification fails, fixes may continue only within the approved scope; expanded scope requires renewed approval.

For Level L and Level XL, final responses should include a structured Traceability section. In a git workspace, the agent should actively query current branch and latest commit; if traceability data is unavailable, it should say why.

## Installation

Install for Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Install for Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

Install for both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```
